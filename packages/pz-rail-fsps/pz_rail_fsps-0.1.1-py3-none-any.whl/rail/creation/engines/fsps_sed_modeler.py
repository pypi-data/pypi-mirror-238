from rail.creation.engine import Modeler
from rail.core.stage import RailStage
from rail.core.data import ModelHandle, Hdf5Handle
from ceci.config import StageParameter as Param
try:
    import fsps
except RuntimeError: # pragma: no cover
    print('Install FSPS with the following commands:\n'
          'pip uninstall fsps\n'
          'git clone --recursive https://github.com/dfm/python-fsps.git\n'
          'cd python-fsps\n'
          'python -m pip install .\n'
          'export SPS_HOME=$(pwd)/src/fsps/libfsps\n')
import numpy as np
import gc


class FSPSSedModeler(Modeler):
    r"""
    Derived class of Modeler for creating a single galaxy rest-frame SED model using FSPS (Conroy08).

    Notes
    -----
    Only the most important parameters are provided via config_options. The remaining ones from FSPS can be
    provided when creating the rest-frame SED model.

    Install FSPS with the following commands:
    pip uninstall fsps
    git clone --recursive https://github.com/dfm/python-fsps.git
    cd python-fsps
    python -m pip install .
    export SPS_HOME=$(pwd)/src/fsps/libfsps
    """

    name = "FSPS_sed_model"
    config_options = RailStage.config_options.copy()

    config_options.update(chunk_size=10000, hdf5_groupname=str,
                          compute_vega_mags=Param(bool, False, msg='True uses Vega magnitudes versus AB magnitudes'),
                          vactoair_flag=Param(bool, False, msg='If True, output wavelengths in air (rather than vac)'),
                          zcontinuous=Param(int, 1, msg='Flag for interpolation in metallicity of SSP before CSP'),
                          add_agb_dust_model=Param(bool, True,
                                                   msg='Turn on/off adding AGB circumstellar dust contribution to SED'),
                          add_dust_emission=Param(bool, True,
                                                  msg='Turn on/off adding dust emission contribution to SED'),
                          add_igm_absorption=Param(bool, False,
                                                   msg='Turn on/off adding IGM absorption contribution to SED'),
                          add_neb_emission=Param(bool, False, msg='Turn on/off nebular emission model based on Cloudy'),
                          add_neb_continuum=Param(bool, False, msg='Turn on/off nebular continuum component'),
                          add_stellar_remnants=Param(bool, True, msg='Turn on/off adding stellar remnants contribution '
                                                                     'to stellar mass'),
                          compute_light_ages=Param(bool, False, msg=' If True then the returned spectra are actually '
                                                                    'light-weighted ages (in Gyr)'),
                          nebemlineinspec=Param(bool, False, msg='True to include emission line fluxes in spectrum'),
                          smooth_velocity=Param(bool, True, msg='True/False for smoothing in '
                                                                'velocity/wavelength space'),
                          smooth_lsf=Param(bool, False, msg='True/False for smoothing SSPs by a wavelength dependent '
                                                            'line spread function'),
                          cloudy_dust=Param(bool, False, msg='Switch to include dust in the Cloudy tables'),
                          agb_dust=Param(float, 1.0, msg='Scales the circumstellar AGB dust emission'),
                          tpagb_norm_type=Param(int, 2, msg='Flag for TP-AGB normalization scheme, '
                                                            'default Villaume, Conroy, Johnson 2015 normalization'),
                          dell=Param(float, 0.0, msg='Shift in log(L_bol) of the TP-AGB isochrones'),
                          delt=Param(float, 0.0, msg='Shift in log(T_eff) of the TP-AGB isochrones'),
                          redgb=Param(float, 1.0, msg='Modify weight given to RGB. Only available with BaSTI '
                                                      'isochrone set'),
                          agb=Param(float, 1.0, msg='Modify weight given to TP-AGB'),
                          fcstar=Param(float, 1.0, msg='Fraction of stars that the Padova isochrones identify '
                                                       'as Carbon stars'),
                          sbss=Param(float, 0.0, msg='Specific frequency of blue straggler stars'),
                          fbhb=Param(float, 0.0, msg='Fraction of horizontal branch stars that are blue'),
                          pagb=Param(float, 1.0, msg='Weight given to the post–AGB phase'),
                          redshifts_key=Param(str, 'redshifts', msg='galaxy redshift, dataset keyword name'),
                          zmet_key=Param(str, 'zmet', msg=' The metallicity is specified as an integer ranging '
                                                          'between 1 and nz. If zcontinuous > 0 then this parameter '
                                                          'is ignored, dataset keyword name'),
                          stellar_metallicities_key=Param(str, 'stellar_metallicity',
                                                          msg='galaxy stellar metallicities (log10(Z / Zsun)) '
                                                              'dataset keyword name, to be used with zcontinuous > 0,'
                                                              'dataset keyword name'),
                          pmetals_key=Param(str, 'pmetals', msg='The power for the metallicty distribution function,'
                                                                'only used if zcontinous=2, dataset keyword name'),
                          imf_type=Param(int, 1, msg='IMF type, see FSPS manual, default Chabrier IMF'),
                          imf_upper_limit=Param(float, 120., msg='The upper limit of the IMF in solar masses'),
                          imf_lower_limit=Param(float, 0.08, msg='The lower limit of the IMF in solar masses'),
                          imf1=Param(float, 1.3, msg='log slope of IMF in 0.08<M/Msun<0.5, if imf_type=2'),
                          imf2=Param(float, 2.3, msg='log slope of IMF in 0.5<M/Msun<1, if imf_type=2'),
                          imf3=Param(float, 2.3, msg='log slope of IMF in M/Msun>1, if imf_type=2'),
                          vdmc=Param(float, 0.08, msg='IMF parameter defined in van Dokkum (2008). '
                                                      'Only used if imf_type=3'),
                          mdave=Param(float, 0.5, msg='IMF parameter defined in Dave (2008). Only used if imf_type=4.'),
                          evtype=Param(int, -1, msg='Compute SSPs for only the given evolutionary type. '
                                                    'All phases used when set to -1.'),
                          use_wr_spectra=Param(int, 1, msg='Turn on/off the WR spectral library'),
                          logt_wmb_hot=Param(float, 0.0, msg='Use the Eldridge (2017) WMBasic hot star library above '
                                                             'this value of log(T_eff) or 25,000K,whichever is larger'),
                          masscut=Param(float, 150.0, msg='Truncate the IMF above this value'),
                          velocity_dispersions_key=Param(str, 'stellar_velocity_dispersion',
                                                         msg='stellar velocity dispersions (km/s), '
                                                             'dataset keyword name'),
                          min_wavelength=Param(float, 3000, msg='minimum rest-frame wavelength'),
                          max_wavelength=Param(float, 10000, msg='maximum rest-frame wavelength'),
                          gas_ionizations_key=Param(str, 'gas_ionization',
                                                    msg='gas ionization values dataset keyword name'),
                          gas_metallicities_key=Param(str, 'gas_metallicity',
                                                      msg='gas metallicities (log10(Zgas / Zsun)) dataset '
                                                          'keyword name'),
                          igm_factor=Param(float, 1.0, msg='Factor used to scale the IGM optical depth'),
                          sfh_type=Param(int, 0, msg='star-formation history type, see FSPS manual, default SSP'),
                          tau_key=Param(str, 'tau', msg='Defines e-folding time for the SFH, in Gyr. Only used if '
                                                        'sfh=1 or sfh=4, dataset keyword name'),
                          const_key=Param(str, 'const', msg='Defines the constant component of the SFH, Only used if'
                                                            ' sfh=1 or sfh=4, dataset keyword name'),
                          sf_start_key=Param(str, 'sf_start', msg='Start time of the SFH, in Gyr. Only used if sfh=1 or '
                                                                  'sfh=4 or sfh=5, dataset keyword name'),
                          sf_trunc_key=Param(str, 'sf_trunc', msg='Truncation time of the SFH, in Gyr. Only used if '
                                                                  'sfh=1 or sfh=4 or sfh=5, dataset keyword name'),
                          stellar_ages_key=Param(str, 'stellar_age', msg='galaxy stellar ages (Gyr),'
                                                                         'dataset keyword name'),
                          fburst_key=Param(str, 'fburst', msg='Deﬁnes the fraction of mass formed in an instantaneous '
                                                              'burst of star formation. Only used if sfh=1 or sfh=4,'
                                                              'dataset keyword name'),
                          tburst_key=Param(str, 'tburst', msg='Defines the age of the Universe when the burst occurs.'
                                                              ' If tburst > tage then there is no burst. Only used if'
                                                              ' sfh=1 or sfh=4, dataset keyword name'),
                          sf_slope_key=Param(str, 'sf_slope', msg='For sfh=5, this is the slope of the SFR after time '
                                                                  'sf_trunc, dataset keyword name'),
                          dust_type=Param(int, 2, msg='attenuation curve for dust type, see FSPS manual, '
                                                      'default Calzetti'),
                          dust_tesc=Param(float, 7.0, msg='Stars younger than dust_tesc are attenuated by both dust1 and'
                                                          ' dust2, while stars older are attenuated by dust2 only. '
                                                          'Units are log(yrs)'),
                          dust_birth_cloud_key=Param(str, 'dust1_birth_cloud',
                                                     msg='dust parameter describing young stellar light attenuation '
                                                         '(dust1 in FSPS), dataset keyword name'),
                          dust_diffuse_key=Param(str, 'dust2_diffuse', msg='dust parameters describing old stellar '
                                                                           'light attenuation (dust2 in FSPS) '
                                                                           'dataset keyword name'),
                          dust_clumps=Param(int, -99, msg='Dust parameter describing the dispersion of a Gaussian PDF'
                                                          ' density distribution for the old dust. Setting this value to'
                                                          ' -99.0 sets the distribution to a uniform screen, '
                                                          'values other than -99 are no longer supported'),
                          frac_nodust=Param(float, 0.0, msg='Fraction of starlight that is not attenuated by the diffuse'
                                                            ' dust component'),
                          frac_obrun=Param(float, 0.0, msg='Fraction of the young stars (age < dust_tesc) that are not '
                                                           'attenuated by dust1 and that do not contribute to any '
                                                           'nebular emission, representing runaway OB stars or escaping '
                                                           'ionizing radiation. These stars are still attenuated by '
                                                           'dust2.'),
                          dust_index_key=Param(str, 'dust_index', msg='Power law index of the attenuation curve. '
                                                                      'Only used when dust_type=0, dataset keyword '
                                                                      'name'),
                          dust_powerlaw_modifier_key=Param(str, 'dust_calzetti_modifier',
                                                           msg='power-law modifiers to the shape of the '
                                                               'Calzetti et al. (2000) attenuation curve (dust1_index),'
                                                               'dataset keyword name'),
                          mwr_key=Param(str, 'mwr', msg='The ratio of total to selective absorption which characterizes '
                                                        'the MW extinction curve: RV=AV/E(B-V), used when dust_type=1,'
                                                        'dataset keyword name'),
                          uvb_key=Param(str, 'uvb', msg='Parameter characterizing the strength of the 2175A extinction '
                                                        'feature with respect to the standard Cardelli et al. '
                                                        'determination for the MW. Only used when dust_type=1,'
                                                        'dataset keyword name'),
                          wgp1_key=Param(str, 'wgp1', msg='Integer specifying the optical depth in the Witt & Gordon '
                                                          '(2000) models. Values range from 1 − 18, used only when'
                                                          'dust_type=3, dataset keyword name'),
                          wgp2=Param(int, 1, msg=' Integer specifying the type of large-scale geometry and '
                                                 'extinction curve. Values range from 1-6, used only when dust_type=3'),
                          wgp3=Param(int, 1, msg='Integer specifying the local geometry for the Witt & Gordon (2000) '
                                                 'dust models, used only when dust_type=3'),
                          dust_emission_gamma_key=Param(str, 'dust_gamma',
                                                        msg='Relative contributions of dust heated at Umin, '
                                                            'parameter of Draine and Li (2007) dust emission model'
                                                            'dataset keyword name'),
                          dust_emission_umin_key=Param(str, 'dust_umin',
                                                       msg='Minimum radiation field strengths, parameter of '
                                                           'Draine and Li (2007) dust emission model, '
                                                           'dataset keyword name'),
                          dust_emission_qpah_key=Param(str, 'dust_qpah',
                                                       msg='Grain size distributions in mass in PAHs, '
                                                           'parameter of Draine and Li (2007) dust emission model,'
                                                           'dataset keyword name'),
                          fraction_agn_bol_lum_key=Param(str, 'f_agn',
                                                         msg='Fractional contributions of AGN wrt stellar bolometric'
                                                             ' luminosity, dataset keyword name'),
                          agn_torus_opt_depth_key=Param(str, 'tau_agn', msg='Optical depths of the AGN dust torii'
                                                                            ' dataset keyword name'),
                          tabulated_sfh_key = Param(str, 'tabulated_sfh', msg='tabulated SFH dataset keyword name'),
                          tabulated_lsf_key = Param(str, 'tabulated_lsf', msg='tabulated LSF dataset keyword name'),
                          physical_units=Param(bool, False), msg='False (True) for rest-frame spectra in units of'
                                                                 'Lsun/Hz (erg/s/Hz)',
                          restframe_wave_key=Param(str, 'restframe_wavelengths',
                                                   msg='Rest-frame wavelength keyword name of the output hdf5 dataset'),
                          restframe_sed_key=Param(str, 'restframe_seds', msg='Rest-frame SED keyword name of the '
                                                                             'output hdf5 dataset'))

    inputs = [("input", Hdf5Handle)]
    # outputs = [("model", ModelHandle)]
    outputs = [("model", Hdf5Handle)]

    def __init__(self, args, comm=None):
        """
        This function initializes the FSPSSedModeler class and checks that the provided parameters are within the
        allowed ranges.

        Parameters
        ----------
        args:
        comm:

        """
        RailStage.__init__(self, args, comm=comm)
        self._output_handle = None

        if self.config.min_wavelength < 0: # pragma: no cover
            raise ValueError("min_wavelength must be positive, not {self.config.min_wavelength}")
        if (self.config.max_wavelength < 0) | (self.config.max_wavelength <= self.config.min_wavelength): # pragma: no cover
            raise ValueError("max_wavelength must be positive and greater than min_wavelength,"
                             " not {self.config.max_wavelength}")

        if self.config.zcontinuous not in [0, 1, 2, 3]: # pragma: no cover
            raise ValueError("zcontinous={} is not valid, allowed values are 0,1,2,3".format(self.config.zcontinuous))

        if self.config.imf_type not in [0, 1, 2, 3, 4, 5]: # pragma: no cover
            raise ValueError("imf_type={} is not valid, allowed values are 0,1,2,3,4,5".format(self.config.imf_type))

        if self.config.sfh_type not in [0, 1, 3, 4, 5]: # pragma: no cover
            raise ValueError("sfh_type={} is not valid, allowed values are 0,1,2,3,4,5".format(self.config.sfh_type))

        if self.config.dust_type not in [0, 1, 2, 3, 4, 5, 6]: # pragma: no cover
            raise ValueError("dust_type={} is not valid, allowed values are 0,1,2,3,4,5,6"
                             .format(self.config.dust_type))

    def _get_rest_frame_seds(self, zred, zmet, logzsol, pmetals, sigma_smooth, gas_logu, gas_logz, tau, const,
                             sf_start, sf_trunc, tage, fburst, tburst, sf_slope, dust1, dust2, dust_index, dust1_index,
                             mwr, uvb, wgp1, duste_gamma, duste_umin, duste_qpah, fagn, agn_tau, tabulated_sfhs,
                             tabulated_lsfs):
        """
        This function loops through the galaxy physical parameters provided by the user and generates rest-frame SEDs
        with FSPS for each of those. If the keyword self.config.physical_units is set to True, then the returned SED
        is in units of erg/s/Hz otherwise units are Lsun/Hz.

        Parameters
        ----------
        zred: numpy.array
            Redshift. If this value is non-zero and if redshift_colors=1, the magnitudes will be computed for the
            spectrum placed at redshift zred.
        zmet: numpy.array
            The metallicity is specified as an integer ranging between 1 and nz. If zcontinuous > 0 then this
            parameter is ignored.
        logzsol: numpy.array
            Parameter describing the metallicity, given in units of  log10(Z/Zsun). Only used if zcontinuous > 0.
        pmetals: numpy.array
            The power for the metallicty distribution function. The MDF is given by (Ze^-Z)^pmetals where
            Z=z/(zsun*10^logzsol) and z is the metallicity in linear units (i.e., zsun=0.019). Using a negative value
            will result in smoothing of the SSPs by a three-point triangular kernel before linear interpolation
            (in logZ) to the requested metallicity. Only used if zcontinuous = 2.
        sigma_smooth: numpy.array
            If smooth_velocity is True, this gives the velocity dispersion in km/s. Otherwise, it gives the width of
            the gaussian wavelength smoothing in Angstroms. These widths are in terms of sigma, not FWHM.
        gas_logu: numpy.array
             Log of the gas ionization parameter; relevant only for the nebular emission model.
        gas_logz: numpy.array
            Log of the gas-phase metallicity; relevant only for the nebular emission model. In units of log10(Z/Zsun).
        tau: numpy.array
            Defines e-folding time for the SFH, in Gyr. Only used if sfh=1 or sfh=4.
        const: numpy.array
            Defines the constant component of the SFH. This quantity is defined as the fraction of mass formed in a
            constant mode of SF; the range is therefore 0<=C<=1. Only used if sfh=1 or sfh=4.
        sf_start: numpy.array
            Start time of the SFH, in Gyr. Only used if sfh=1 or sfh=4 or sfh=5.
        sf_trunc: numpy.array
            Truncation time of the SFH, in Gyr. If set to 0.0, there is no trunction. Only used if sfh=1 or sfh=4 or
             sfh=5.
        tage: numpy.array
            If set to a non-zero value, the fsps.StellarPopulation.compute_csp() method will compute the spectra and
             magnitudes only at this age, and will therefore only output one age result. The units are Gyr.
             (The default is to compute and return results from t=0 to the maximum age in the isochrones).
        fburst: numpy.array
            Defines the fraction of mass formed in an instantaneous burst of star formation. Only used if sfh=1 or sfh=4.
        tburst: numpy.array
            Defines the age of the Universe when the burst occurs. If tburst > tage then there is no burst. Only used
            if sfh=1 or sfh=4.
        sf_slope: numpy.array
            For sfh=5, this is the slope of the SFR after time sf_trunc.
        dust1: numpy.array
            Dust parameter describing the attenuation of young stellar light, i.e. where t <= dust_tesc
            (for details, see Conroy et al. 2009a).
        dust2: numpy.array
            Dust parameter describing the attenuation of old stellar light, i.e. where t > dust_tesc
            (for details, see Conroy et al. 2009a).
        dust_index: numpy.array
            Power law index of the attenuation curve. Only used when dust_type=0.
        dust1_index: numpy.array
            Power law index of the attenuation curve affecting stars younger than dust_tesc corresponding to dust1.
            Used for all dust types.
        mwr: numpy.array
            The ratio of total to selective absorption which characterizes the MW extinction curve: RV=AV/E(B-V).
            Only used when dust_type=1.
        uvb: numpy.array
            Parameter characterizing the strength of the 2175A extinction feature with respect to the standard
            Cardelli et al. determination for the MW. Only used when dust_type=1.
        wgp1: numpy.array
            Integer specifying the optical depth in the Witt & Gordon (2000) models. Values range from 1 − 18,
            corresponding to optical depths of 0.25, 0.50, 0.75, 1.00, 1.50, 2.00, 2.50, 3.00, 3.50, 4.00, 4.50, 5.00,
            5.50, 6.00, 7.00, 8.00, 9.00, 10.0. Note that these optical depths are defined differently from the optical
            depths defined by the parameters dust1 and dust2. See Witt & Gordon (2000) for details.
        duste_gamma: numpy.array
            Parameter of the Draine & Li (2007) dust emission model. Specifies the relative contribution of dust heated
             at a radiation field strength of Umin and dust heated at Umin<U<Umax. Allowable range is 0.0 - 1.0.
        duste_umin: numpy.array
            Parameter of the Draine & Li (2007) dust emission model. Specifies the minimum radiation field strength in
             units of the MW value. Valid range is 0.1 - 25.0.
        duste_qpah: numpy.array
            Parameter of the Draine & Li (2007) dust emission model. Specifies the grain size distribution through the
             fraction of grain mass in PAHs. This parameter has units of % and a valid range of 0.0 - 10.0.
        fagn: numpy.array
            The total luminosity of the AGN, expressed as a fraction of the bolometric stellar luminosity
            (so it can be greater than 1). The shape of the AGN SED is from the Nenkova et al. 2008 templates.
        agn_tau: numpy.array
            Optical depth of the AGN dust torus, which affects the shape of the AGN SED. Outside the range (5, 150) the
             AGN SED is an extrapolation.
        tabulated_sfhs: numpy.array
            Numpy array storing the tabulated galaxy star-formation histories.
        tabulated_lsfs: numpy.array
            Numpy array storing the values for the line-spread function smoothing.

        Returns
        -------
        restframe_wavelengths: numpy.array
            Numpy array of the rest-frame wavelengths generated from FSPS. Wavelengths are in units of Ångstrom.
        restframe_seds: numpy.array
            Numpy array of the rest-frame SEDs generated from FSPS. If self.config.physical_units is True, then
            the output units are erg/s/Hz, otherwise it's Lsun/Hz.
        """

        restframe_wavelengths = {}
        restframe_seds = {}

        for i in range(len(tage)):
            sp = fsps.StellarPopulation(compute_vega_mags=self.config.compute_vega_mags,
                                        vactoair_flag=self.config.vactoair_flag,
                                        zcontinuous=self.config.zcontinuous,
                                        add_agb_dust_model=self.config.add_agb_dust_model,
                                        add_dust_emission=self.config.add_dust_emission,
                                        add_igm_absorption=self.config.add_igm_absorption,
                                        add_neb_emission=self.config.add_neb_emission,
                                        add_neb_continuum=self.config.add_neb_continuum,
                                        add_stellar_remnants=self.config.add_stellar_remnants,
                                        compute_light_ages=self.config.compute_light_ages,
                                        nebemlineinspec=self.config.nebemlineinspec,
                                        smooth_velocity=self.config.smooth_velocity,
                                        smooth_lsf=self.config.smooth_lsf,
                                        cloudy_dust=self.config.cloudy_dust, agb_dust=self.config.agb_dust,
                                        tpagb_norm_type=self.config.tpagb_norm_type, dell=self.config.dell,
                                        delt=self.config.delt, redgb=self.config.redgb, agb=self.config.agb,
                                        fcstar=self.config.fcstar, sbss=self.config.sbss, fbhb=self.config.fbhb,
                                        pagb=self.config.pagb, zred=zred[i],
                                        zmet=zmet[i], logzsol=logzsol[i],
                                        pmetals=pmetals[i], imf_type=self.config.imf_type,
                                        imf_upper_limit=self.config.imf_upper_limit,
                                        imf_lower_limit=self.config.imf_lower_limit, imf1=self.config.imf1,
                                        imf2=self.config.imf2, imf3=self.config.imf3, vdmc=self.config.vdmc,
                                        mdave=self.config.mdave, evtype=self.config.evtype,
                                        use_wr_spectra=self.config.use_wr_spectra,
                                        logt_wmb_hot=self.config.logt_wmb_hot,
                                        masscut=self.config.masscut, sigma_smooth=sigma_smooth[i],
                                        min_wave_smooth=self.config.min_wavelength,
                                        max_wave_smooth=self.config.max_wavelength,
                                        gas_logu=gas_logu[i], gas_logz=gas_logz[i],
                                        igm_factor=self.config.igm_factor, sfh=self.config.sfh_type,
                                        tau=tau[i], const=const[i], sf_start=sf_start[i],
                                        sf_trunc=sf_trunc[i], tage=tage[i],
                                        fburst=fburst[i], tburst=tburst[i],
                                        sf_slope=sf_slope[i], dust_type=self.config.dust_type,
                                        dust_tesc=self.config.dust_tesc, dust1=dust1[i], dust2=dust2[i],
                                        dust_clumps=self.config.dust_clumps,
                                        frac_nodust=self.config.frac_nodust, frac_obrun=self.config.frac_obrun,
                                        dust_index=dust_index[i], dust1_index=dust1_index[i],
                                        mwr=mwr[i], uvb=uvb[i], wgp1=wgp1[i], wgp2=self.config.wgp2,
                                        wgp3=self.config.wgp3,
                                        duste_gamma=duste_gamma[i], duste_umin=duste_umin[i],
                                        duste_qpah=duste_qpah[i],
                                        fagn=fagn[i], agn_tau=agn_tau[i])

            if self.config.sfh_type == 3:
                assert tabulated_sfhs is not None
                if self.config.zcontinuous == 3:  # pragma: no cover
                    # age_array, sfr_array, metal_array = np.loadtxt(tabulated_sfh_files[i], usecols=(0, 1, 2),
                    #                                                unpack=True)
                    age_array, sfr_array, metal_array = tabulated_sfhs[i]
                    sp.set_tabular_sfh(age_array, sfr_array, Z=metal_array)
                elif self.config.zcontinuous == 1:
                    # age_array, sfr_array = np.loadtxt(tabulated_sfh_file[i], usecols=(0, 1), unpack=True)
                    age_array, sfr_array = tabulated_sfhs[i]
                    sp.set_tabular_sfh(age_array, sfr_array, Z=None)
                else:  # pragma: no cover
                    raise ValueError

            if self.config.smooth_lsf:
                assert self.config.smooth_velocity is True, 'lsf smoothing only works if smooth_velocity is True'
                assert tabulated_lsfs is not None
                # lsf_values = np.loadtxt(tabulated_lsf_file, usecols=(0, 1))
                # wave = lsf_values[:, 0]  # pragma: no cover
                # sigma = lsf_values[:, 1]  # pragma: no cover
                wave, sigma = tabulated_lsfs[i]
                sp.set_lsf(wave, sigma, wmin=self.config.min_wavelength,
                           wmax=self.config.max_wavelength)  # pragma: no cover

            restframe_wavelength, restframe_sed_Lsun_Hz = sp.get_spectrum(tage=tage[i], peraa=False)

            selected_wave_range = np.where((restframe_wavelength >= self.config.min_wavelength) &
                                           (restframe_wavelength <= self.config.max_wavelength))
            restframe_wavelength = restframe_wavelength[selected_wave_range]
            restframe_wavelengths[i] = restframe_wavelength

            if self.config.physical_units:
                solar_luminosity_erg_s = 3.8275 * 10 ** 33  # Prša et al. 2016
                restframe_sed_erg_s_Hz = restframe_sed_Lsun_Hz[selected_wave_range] * solar_luminosity_erg_s
                restframe_seds[i] = restframe_sed_erg_s_Hz.astype('float64')
            else:
                restframe_sed_Lsun_Hz = restframe_sed_Lsun_Hz[selected_wave_range]
                restframe_seds[i] = restframe_sed_Lsun_Hz.astype('float64')

        restframe_wavelengths = np.array([restframe_wavelengths[0]])
        restframe_seds = np.array([restframe_seds[i] for i in range(len(tage))])

        return restframe_wavelengths, restframe_seds

    def fit_model(self, input_data=None):
        """
        This function creates rest-frame SED models from an input galaxy population catalog.

        Parameters
        ----------
        input_data: Hdf5Handle
            This is the input catalog in the form of an Hdf5Handle.

        Returns
        -------
        model: ModelHandle
            ModelHandle storing the rest-frame SED models
        """
        self.set_data('input', input_data)
        self.run()
        self.finalize()

        model = self.get_handle("model")
        return model

    def run(self):
        """
        Run method. It Calls `StellarPopulation` from FSPS to create a galaxy rest-frame SED.
        Thanks to Josue de Santiago, this function is able to run in parallel via mpi by splitting the full sample in
        chunks of user-defined size.

        Parameters
        ----------

        """
        iterator = self.input_iterator('input')
        first = True
        self._initialize_run()
        self._output_handle = None
        for s, e, test_data in iterator:
            print(f"Process {self.rank} running creator on chunk {s} - {e}")
            self._process_chunk(s, e, test_data, first)
            first = False
            # Running garbage collection manually seems to be needed
            # to avoid memory growth for some estimators
            gc.collect()
        self._finalize_run()

    def _process_chunk(self, start, end, data, first):
        """
        Calculate the restframe SEDs for a chunk of galaxies using the input parameters.

        Parameters
        ----------
        start
        end
        data
        first

        Returns
        -------

        """
        redshifts = data[self.config.redshifts_key][()]
        stellar_ages = data[self.config.stellar_ages_key][()]
        stellar_metallicities = data[self.config.stellar_metallicities_key][()]
        velocity_dispersions = data[self.config.velocity_dispersions_key][()]
        gas_ionizations = data[self.config.gas_ionizations_key][()]
        gas_metallicities = data[self.config.gas_metallicities_key][()]
        zmet = data[self.config.zmet_key][()]
        pmetals = data[self.config.pmetals_key][()]
        tau = data[self.config.tau_key][()]
        const = data[self.config.const_key][()]
        sf_start = data[self.config.sf_start_key][()]
        sf_trunc = data[self.config.sf_trunc_key][()]
        fburst = data[self.config.fburst_key][()]
        tburst = data[self.config.tburst_key][()]
        sf_slope = data[self.config.sf_slope_key][()]
        dust_birth_cloud = data[self.config.dust_birth_cloud_key][()]
        dust_diffuse = data[self.config.dust_diffuse_key][()]
        dust_index = data[self.config.dust_index_key][()]
        dust_powerlaw_modifier = data[self.config.dust_powerlaw_modifier_key][()]
        mwr = data[self.config.mwr_key][()]
        uvb = data[self.config.uvb_key][()]
        wgp1 = data[self.config.wgp1_key][()]
        dust_emission_gamma = data[self.config.dust_emission_gamma_key][()]
        dust_emission_umin = data[self.config.dust_emission_umin_key][()]
        dust_emission_qpah = data[self.config.dust_emission_qpah_key][()]
        frac_bol_lum_agn = data[self.config.fraction_agn_bol_lum_key][()]
        agn_torus_opt_depths = data[self.config.agn_torus_opt_depth_key][()]
        tabulated_sfhs = data[self.config.tabulated_sfh_key][()]
        tabulated_lsfs = data[self.config.tabulated_lsf_key][()]

        wavelengths, restframe_seds = self._get_rest_frame_seds(zred=redshifts,
                                                                zmet=zmet, logzsol=stellar_metallicities,
                                                                pmetals=pmetals,
                                                                sigma_smooth=velocity_dispersions,
                                                                gas_logu=gas_ionizations, gas_logz=gas_metallicities,
                                                                tau=tau,
                                                                const=const, sf_start=sf_start,
                                                                sf_trunc=sf_trunc, tage=stellar_ages,
                                                                fburst=fburst, tburst=tburst, sf_slope=sf_slope,
                                                                dust1=dust_birth_cloud, dust2=dust_diffuse,
                                                                dust_index=dust_index,
                                                                dust1_index=dust_powerlaw_modifier,
                                                                mwr=mwr, uvb=uvb, wgp1=wgp1,
                                                                duste_gamma=dust_emission_gamma,
                                                                duste_umin=dust_emission_umin,
                                                                duste_qpah=dust_emission_qpah,
                                                                fagn=frac_bol_lum_agn, agn_tau=agn_torus_opt_depths,
                                                                tabulated_sfhs=tabulated_sfhs,
                                                                tabulated_lsfs=tabulated_lsfs)
        output_chunk = {self.config.restframe_wave_key: wavelengths, self.config.restframe_sed_key: restframe_seds,
                        self.config.redshifts_key: redshifts}
        self._do_chunk_output(output_chunk, start, end, first)

    def _initialize_run(self):
        """

        Returns
        -------

        """
        self._output_handle = None

    def _finalize_run(self):
        """

        Returns
        -------

        """
        self._output_handle.finalize_write()

    def _do_chunk_output(self, output_chunk, start, end, first):
        """

        Parameters
        ----------
        output_chunk
        start
        end
        first

        Returns
        -------

        """
        if first:
            self._output_handle = self.add_handle('model', data = output_chunk)
            self._output_handle.initialize_write(self._input_length, communicator = self.comm)
        self._output_handle.set_data(output_chunk, partial=True)
        self._output_handle.write_chunk(start, end)
