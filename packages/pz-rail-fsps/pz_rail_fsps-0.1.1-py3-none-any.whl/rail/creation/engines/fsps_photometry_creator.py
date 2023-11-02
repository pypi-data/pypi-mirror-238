from rail.creation.engine import Creator
from rail.core.stage import RailStage
from rail.core.data import Hdf5Handle
from ceci.config import StageParameter as Param
import numpy as np
from rail.core.utils import find_rail_file
from astropy.cosmology import Planck15, w0waCDM
from scipy import interpolate
import os
import h5py


class FSPSPhotometryCreator(Creator):
    """
    Derived class of Creator that generate synthetic photometric fsps_default_data from the rest-frame SED model
    generated with the FSPSSedModeler class.
    The user is required to provide galaxy redshifts and filter information in an .npy format for the code to run.
    The restframe SEDs are stored in a pickle file or passed as ModelHandle.
    Details of what each file should contain are explicited in config_options.
    The output is a Fits table containing magnitudes.
    """

    name = "FSPS_Photometry_Creator"
    default_files_folder = find_rail_file(os.path.join('examples_data', 'creation_data', 'data', 'fsps_default_data'))
    config_options = RailStage.config_options.copy()
    config_options.update(redshift_key=Param(str, 'redshifts', msg='Redshift keyword name of the hdf5 dataset '
                                                                   'containing rest-frame SEDs'),
                          restframe_sed_key=Param(str, 'restframe_seds', msg='Rest-frame SED keyword name of the '
                                                                             'hdf5 dataset containing rest-frame SEDs'),
                          restframe_wave_key=Param(str, 'wavelength', msg='Rest-frame wavelengths keyword name of the'
                                                                          'hdf5 dataset containing rest-frame SEDs'),
                          apparent_mags_key=Param(str, 'apparent_mags', msg='Apparent magnitudes keyword name of the '
                                                                            'output hdf5 dataset'),
                          filter_folder=Param(str, os.path.join(default_files_folder, 'filters'),
                                              msg='Folder containing filter transmissions'),
                          instrument_name=Param(str, 'lsst', msg='Instrument name as prefix to filter transmission'
                                                                 ' files'),
                          wavebands=Param(str, 'u,g,r,i,z,y', msg='Comma-separated list of wavebands'),
                          filter_wave_key=Param(str, 'wave', msg=''),
                          filter_transm_key=Param(str, 'transmission', msg=''),
                          Om0=Param(float, 0.3, msg='Omega matter at current time'),
                          Ode0=Param(float, 0.7, msg='Omega dark energy at current time'),
                          w0=Param(float, -1, msg='Dark energy equation-of-state parameter at current time'),
                          wa=Param(float, 0., msg='Slope dark energy equation-of-state evolution with scale factor'),
                          h=Param(float, 0.7, msg='Dimensionless hubble constant'),
                          use_planck_cosmology=Param(bool, False, msg='True to overwrite the cosmological parameters'
                                                                      'to their Planck2015 values'),
                          physical_units=Param(bool, False), msg='False (True) for rest-frame spectra in units of'
                                                                 'Lsun/Hz (erg/s/Hz)')

    inputs = [("model", Hdf5Handle)]
    outputs = [("output", Hdf5Handle)]

    def __init__(self, args, comm=None):
        """
        Initialize class.
        The _b and _c tuples for jax are composed of None or 0, depending on whether you don't or do want the
        array axis to map over for all arguments.
        Parameters
        ----------
        args:
        comm:
        """
        RailStage.__init__(self, args, comm=comm)

        if not os.path.isdir(self.config.filter_folder):
            raise OSError("File {self.config.filter_folder} not found")
        self.wavebands = self.config.wavebands.split(',')
        filter_wavelengths, filter_transmissions = [], []
        for waveband in self.wavebands:
            with h5py.File(os.path.join(self.config.filter_folder,
                                        '{}_{}_transmission.h5'.format(self.config.instrument_name, waveband)),
                           'r') as h5table:
                filter_transmissions.append(h5table[self.config.filter_transm_key][()])
                filter_wavelengths.append(h5table[self.config.filter_wave_key][()])
        self.filter_transmissions = np.array(filter_transmissions, dtype=object)
        self.filter_wavelengths = np.array(filter_wavelengths, dtype=object)

        if (self.config.Om0 < 0.) | (self.config.Om0 > 1.):
            raise ValueError("The mass density at the current time {self.config.Om0} is outside of allowed"
                             " range 0. < Om0 < 1.")
        if (self.config.Ode0 < 0.) | (self.config.Ode0 > 1.):
            raise ValueError("The dark energy density at the current time {self.config.Ode0} is outside of allowed"
                             " range 0. < Ode0 < 1.")
        if (self.config.h < 0.) | (self.config.h > 1.):
            raise ValueError("The dimensionless Hubble constant {self.config.h} is outside of allowed"
                             " range 0 < h < 1")

        if self.config.use_planck_cosmology:
            self.cosmology = Planck15
        else:
            self.cosmology = w0waCDM(self.config.h * 100, self.config.Om0, self.config.Ode0,
                                     w0=self.config.w0, wa=self.config.wa)

    def _compute_apparent_magnitudes(self, rest_frame_wavelengths, rest_frame_seds, redshifts):
        """

        Parameters
        ----------
        rest_frame_wavelengths: numpy.array
        rest_frame_seds: numpy.array
        redshifts: numpy.array

        Returns
        -------
        apparent_magnitudes: numpy.array
            Array of shape (n_galaxies, n_bands) containing the computed apparent AB magnitudes

        """

        apparent_magnitudes = {}

        for i in self.split_tasks_by_rank(range(len(redshifts))):

            if self.config.physical_units:
                restframe_sed = rest_frame_seds[i]
            else:
                solar_luminosity_erg_s = 3.8275 * 10 ** 33  # Prša et al. 2016
                restframe_sed = rest_frame_seds[i] * solar_luminosity_erg_s

            Mpc_in_cm = 3.08567758128 * 10 ** 24
            speed_of_light_cm_s = 2.9979245800 * 10 ** 18
            lum_dist_cm = self.cosmology.luminosity_distance(redshifts[i]).value * Mpc_in_cm

            observedframe_sed_erg_s_cm2_Hz = (1 + redshifts[i]) ** 2 * restframe_sed / \
                (4 * np.pi * (1 + redshifts[i]) * lum_dist_cm ** 2)

            observedframe_wavelength = rest_frame_wavelengths * (1 + redshifts[i])
            observedframe_wavelength_in_Hz = speed_of_light_cm_s / observedframe_wavelength

            magnitudes = []

            for j in range(len(self.filter_transmissions)):
                filter_wavelength_in_hz = speed_of_light_cm_s / self.filter_wavelengths[j]
                interp_function = interpolate.interp1d(filter_wavelength_in_hz, self.filter_transmissions[j],
                                                       bounds_error=False, fill_value=0)
                filt_interp = interp_function(observedframe_wavelength_in_Hz)
                numerator = np.trapz(observedframe_sed_erg_s_cm2_Hz * filt_interp / observedframe_wavelength,
                                     x=observedframe_wavelength)
                denominator = np.trapz(filt_interp / observedframe_wavelength,
                                       x=observedframe_wavelength)
                mag_ab = -2.5 * np.log10(numerator / denominator) - 48.6
                magnitudes.append(mag_ab)

            apparent_magnitudes[i] = magnitudes

        if self.comm is not None:  # pragma: no cover
            apparent_magnitudes = self.comm.gather(apparent_magnitudes)

            if self.rank != 0:  # pragma: no cover
                return None, None

            apparent_magnitudes = {k: v for a in apparent_magnitudes for k, v in a.items()}

        apparent_magnitudes = np.array([apparent_magnitudes[i]
                                        for i in range(len(redshifts))])

        return apparent_magnitudes

    def sample(self, seed: int = None, input_data=None, **kwargs):
        r"""
        Creates observed magnitudes for the population of galaxies and stores them into an Hdf5Handle.

        Parameters
        ----------
        seed: int
            The random seed to control sampling
        input_data: Hdf5Handle
            Hdf5Handle containing the rest-frame SED models.

        Returns
        -------
        output: Hdf5Handle
            Hdf5Handle storing the apparent magnitudes and redshifts of galaxies.

        Notes
        -----
        This method puts  `seed` into the stage configuration data, which makes them available to other methods.
        It then calls the `run` method. Finally, the `Hdf5Handle` associated to the `output` tag is returned.

        """
        self.config["seed"] = seed
        self.config.update(**kwargs)
        self.set_data('model', input_data)
        self.run()
        self.finalize()
        output = self.get_handle("output")
        return output

    def run(self):
        """
        This function computes apparent AB magnitudes in the provided wavebands for all the galaxies
        in the population having rest-frame SEDs computed by FSPS.
        It then stores apparent magnitudes, redshifts and running indices into an Hdf5Handle.

        Returns
        -------

        """
        self.model = self.get_data('model')
        redshifts = self.model[self.config.redshift_key][()]
        rest_frame_seds = self.model[self.config.restframe_sed_key][()]
        rest_frame_wave = self.model[self.config.restframe_wave_key][()]

        apparent_magnitudes = self._compute_apparent_magnitudes(rest_frame_wave, rest_frame_seds, redshifts)

        idxs = np.arange(1, len(redshifts) + 1, 1, dtype=int)

        if self.rank == 0:
            output_mags = {'id': idxs, self.config.redshifts_key: redshifts,
                           self.config.apparent_mags_key: apparent_magnitudes}
            self.add_data('output', output_mags)
