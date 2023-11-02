import os
import subprocess

if "SPS_HOME" not in os.environ:
    os.environ["SPS_HOME"] = "/opt/hostedtoolcache/Python/fsps"
    subprocess.run(["git", "clone", "https://github.com/cconroy20/fsps.git",
                    "/opt/hostedtoolcache/Python/fsps"], capture_output=True)

import pytest
import rail.fsps
from rail.core.data import TableHandle
from rail.core.stage import RailStage
from rail.creation.engines import fsps_photometry_creator, fsps_sed_modeler

RAIL_FSPS_DIR = os.path.abspath(os.path.join(os.path.dirname(rail.fsps.__file__), '..', '..'))
default_rail_fsps_files_folder = os.path.join(RAIL_FSPS_DIR, 'rail', 'examples_data', 'creation_data', 'data',
                                              'fsps_default_data')


@pytest.mark.parametrize(
    "settings,error",
    [
        ({"min_wavelength": -1000}, ValueError),
    ],
)
def test_FSPSSedModeler_bad_min_wavelength(settings, error):
    """Test bad wavelength range that should raise Value and Type errors."""
    with pytest.raises(error):
        fsps_sed_modeler.FSPSSedModeler.make_stage(name='FSPSSedModeler', **settings)


@pytest.mark.parametrize(
    "settings,error",
    [
        ({"min_wavelength": 3000}, ValueError),
        ({"max_wavelength": 1000}, ValueError),
    ],
)
def test_FSPSSedModeler_bad_max_wavelength(settings, error):
    """Test bad wavelength range that should raise Value and Type errors."""
    with pytest.raises(error):
        fsps_sed_modeler.FSPSSedModeler.make_stage(name='FSPSSedModeler', **settings)


@pytest.mark.parametrize(
    "settings,error",
    [
        ({"zcontinuous": 4}, ValueError),
    ],
)
def test_FSPSSedModeler_bad_zcontinous(settings, error):
    """Test bad wavelength range that should raise Value and Type errors."""
    with pytest.raises(error):
        fsps_sed_modeler.FSPSSedModeler.make_stage(name='FSPSSedModeler', **settings)


@pytest.mark.parametrize(
    "settings,error",
    [
        ({"imf_type": 6}, ValueError),
    ],
)
def test_FSPSSedModeler_bad_imf_type(settings, error):
    """Test bad wavelength range that should raise Value and Type errors."""
    with pytest.raises(error):
        fsps_sed_modeler.FSPSSedModeler.make_stage(name='FSPSSedModeler', **settings)


@pytest.mark.parametrize(
    "settings,error",
    [
        ({"sfh_type": 6}, ValueError),
    ],
)
def test_FSPSSedModeler_bad_sfh_type(settings, error):
    """Test bad wavelength range that should raise Value and Type errors."""
    with pytest.raises(error):
        fsps_sed_modeler.FSPSSedModeler.make_stage(name='FSPSSedModeler', **settings)


@pytest.mark.parametrize(
    "settings,error",
    [
        ({"dust_type": 7}, ValueError),
    ],
)
def test_FSPSSedModeler_bad_dust_type(settings, error):
    """Test bad wavelength range that should raise Value and Type errors."""
    with pytest.raises(error):
        fsps_sed_modeler.FSPSSedModeler.make_stage(name='FSPSSedModeler', **settings)


@pytest.mark.parametrize(
    "settings,error",
    [
        ({"filter_folder": os.path.join(default_rail_fsps_files_folder, 'test_fsps_sed.fits')}, OSError),
    ],
)
def test_FSPSPhotometryCreator_bad_filter_folder(settings, error):
    """Test bad filter folder that should raise OS errors."""
    with pytest.raises(error):
        fsps_photometry_creator.FSPSPhotometryCreator.make_stage(name='FSPSPhotometryCreator', **settings)


@pytest.mark.parametrize(
    "settings,error",
    [
        ({"Om0": 2}, ValueError),
    ],
)
def test_FSPSPhotometryCreator_bad_Om0(settings, error):
    """Test bad filter folder that should raise Value errors."""
    with pytest.raises(error):
        fsps_photometry_creator.FSPSPhotometryCreator.make_stage(name='FSPSPhotometryCreator',
                                         filter_folder=os.path.join(default_rail_fsps_files_folder, 'filters'),
                                         **settings)


@pytest.mark.parametrize(
    "settings,error",
    [
        ({"Ode0": 2}, ValueError),
    ],
)
def test_FSPSPhotometryCreator_bad_Ode0(settings, error):
    """Test bad filter folder that should raise Value errors."""
    with pytest.raises(error):
        fsps_photometry_creator.FSPSPhotometryCreator.make_stage(name='FSPSPhotometryCreator',
                                         filter_folder=os.path.join(default_rail_fsps_files_folder, 'filters'),
                                         **settings)


@pytest.mark.parametrize(
    "settings,error",
    [
        ({"h": 2}, ValueError),
    ],
)
def test_FSPSPhotometryCreator_bad_h(settings, error):
    """Test bad filter folder that should raise Value errors."""
    with pytest.raises(error):
        fsps_photometry_creator.FSPSPhotometryCreator.make_stage(name='FSPSPhotometryCreator',
                                         filter_folder=os.path.join(default_rail_fsps_files_folder, 'filters'),
                                         **settings)


def test_FSPSPhotometryCreator():
    DS = RailStage.data_store
    DS.__class__.allow_overwrite = True
    trainFile = os.path.join(default_rail_fsps_files_folder, 'model_FSPSSedModeler.hdf5')
    training_data = DS.read_file("training_data", TableHandle, trainFile)
    fspsphotometrycreator = fsps_photometry_creator.FSPSPhotometryCreator.make_stage(redshifts_key='redshifts',
                                                             restframe_sed_key='restframe_seds',
                                                             restframe_wave_key='restframe_wavelengths',
                                                             apparent_mags_key='apparent_mags',
                                                             filter_folder=os.path.join(default_rail_fsps_files_folder,
                                                                                        'filters'),
                                                             instrument_name='lsst', wavebands='u,g,r,i,z,y',
                                                             filter_wave_key='wave', filter_transm_key='transmission',
                                                             Om0=0.3, Ode0=0.7, w0=-1, wa=0.0, h=0.7,
                                                             use_planck_cosmology=True, physical_units=False)
    fspsphotometry = fspsphotometrycreator.sample(input_data=training_data)
    assert len(fspsphotometry.data['apparent_mags']) == 10


def test_FSPSPhotometryCreator_noPlanck():
    DS = RailStage.data_store
    DS.__class__.allow_overwrite = True
    trainFile = os.path.join(default_rail_fsps_files_folder, 'model_FSPSSedModeler.hdf5')
    training_data = DS.read_file("training_data", TableHandle, trainFile)
    fspsphotometrycreator = fsps_photometry_creator.FSPSPhotometryCreator.make_stage(redshifts_key='redshifts',
                                                             restframe_sed_key='restframe_seds',
                                                             restframe_wave_key='restframe_wavelengths',
                                                             apparent_mags_key='apparent_mags',
                                                             filter_folder=os.path.join(default_rail_fsps_files_folder,
                                                                                        'filters'),
                                                             instrument_name='lsst', wavebands='u,g,r,i,z,y',
                                                             filter_wave_key='wave', filter_transm_key='transmission',
                                                             Om0=0.3, Ode0=0.7, w0=-1, wa=0.0, h=0.7,
                                                             use_planck_cosmology=False, physical_units=True)
    fspsphotometry = fspsphotometrycreator.sample(input_data=training_data)
    assert len(fspsphotometry.data['apparent_mags']) == 10


def test_FSPSSedModeler():
    DS = RailStage.data_store
    DS.__class__.allow_overwrite = True
    trainFile = os.path.join(default_rail_fsps_files_folder, 'input_galaxy_properties_fsps.hdf5')
    training_data = DS.read_file("training_data", TableHandle, trainFile)
    fspssedmodeler = fsps_sed_modeler.FSPSSedModeler.make_stage(chunk_size=10, hdf5_groupname='model', name='FSPSSedModeler',
                                               compute_vega_mags=False, vactoair_flag=False,
                                               zcontinuous=1, add_agb_dust_model=True,
                                               add_dust_emission=True, add_igm_absorption=True,
                                               add_neb_emission=True, add_neb_continuum=True,
                                               add_stellar_remnants=True, compute_light_ages=False,
                                               nebemlineinspec=True, smooth_velocity=True,
                                               smooth_lsf=False, cloudy_dust=False,
                                               agb_dust=1.0, tpagb_norm_type=2, dell=0.0,
                                               delt=0.0, redgb=1.0, agb=1.0, fcstar=1.0, sbss=0.0,
                                               fbhb=0.0, pagb=1.0, redshifts_key='redshifts',
                                               zmet_key='zmet', stellar_metallicities_key='stellar_metallicity',
                                               pmetals_key='pmetals', imf_type=1, imf_upper_limit=120.,
                                               imf_lower_limit=0.08, imf1=1.3, imf2=2.3, imf3=2.3, vdmc=0.08,
                                               mdave=0.5, evtype=-1, use_wr_spectra=1, logt_wmb_hot=0.0, masscut=150.0,
                                               velocity_dispersions_key='stellar_velocity_dispersion',
                                               min_wavelength=3000,
                                               max_wavelength=10000, gas_ionizations_key='gas_ionization',
                                               gas_metallicities_key='gas_metallicity', igm_factor=1.0, sfh_type=3,
                                               tau_key='tau', const_key='const', sf_start_key='sf_start',
                                               sf_trunc_key='sf_trunc', stellar_ages_key='stellar_age',
                                               fburst_key='fburst', tburst_key='tburst', sf_slope_key='sf_slope',
                                               dust_type=2, dust_tesc=7.0, dust_birth_cloud_key='dust1_birth_cloud',
                                               dust_diffuse_key='dust2_diffuse', dust_clumps=-99, frac_nodust=0.0,
                                               frac_obrun=0.0, dust_index_key='dust_index',
                                               dust_powerlaw_modifier_key='dust_calzetti_modifier', mwr_key='mwr',
                                               uvb_key='uvb', wgp1_key='wgp1', wgp2=1, wgp3=1,
                                               dust_emission_gamma_key='dust_gamma', dust_emission_umin_key='dust_umin',
                                               dust_emission_qpah_key='dust_qpah', fraction_agn_bol_lum_key='f_agn',
                                               agn_torus_opt_depth_key='tau_agn', tabulated_sfh_key='tabulated_sfh',
                                               tabulated_lsf_key='tabulated_lsf', physical_units=False,
                                               restframe_wave_key='restframe_wavelengths',
                                               restframe_sed_key='restframe_seds')
    fspssedmodel = fspssedmodeler.fit_model(training_data)
    assert len(fspssedmodel.data['restframe_seds']) == 10


def test_FSPSSedModeler_smooth_lsf():
    DS = RailStage.data_store
    DS.__class__.allow_overwrite = True
    trainFile = os.path.join(default_rail_fsps_files_folder, 'input_galaxy_properties_fsps.hdf5')
    training_data = DS.read_file("training_data", TableHandle, trainFile)
    fspssedmodeler = fsps_sed_modeler.FSPSSedModeler.make_stage(chunk_size=10, hdf5_groupname='model', name='FSPSSedModeler',
                                               compute_vega_mags=False, vactoair_flag=False,
                                               zcontinuous=1, add_agb_dust_model=True,
                                               add_dust_emission=True, add_igm_absorption=True,
                                               add_neb_emission=True, add_neb_continuum=True,
                                               add_stellar_remnants=True, compute_light_ages=False,
                                               nebemlineinspec=True, smooth_velocity=True,
                                               smooth_lsf=True, cloudy_dust=False,
                                               agb_dust=1.0, tpagb_norm_type=2, dell=0.0,
                                               delt=0.0, redgb=1.0, agb=1.0, fcstar=1.0, sbss=0.0,
                                               fbhb=0.0, pagb=1.0, redshifts_key='redshifts',
                                               zmet_key='zmet', stellar_metallicities_key='stellar_metallicity',
                                               pmetals_key='pmetals', imf_type=1, imf_upper_limit=120.,
                                               imf_lower_limit=0.08, imf1=1.3, imf2=2.3, imf3=2.3, vdmc=0.08,
                                               mdave=0.5, evtype=-1, use_wr_spectra=1, logt_wmb_hot=0.0, masscut=150.0,
                                               velocity_dispersions_key='stellar_velocity_dispersion',
                                               min_wavelength=3000,
                                               max_wavelength=10000, gas_ionizations_key='gas_ionization',
                                               gas_metallicities_key='gas_metallicity', igm_factor=1.0, sfh_type=3,
                                               tau_key='tau', const_key='const', sf_start_key='sf_start',
                                               sf_trunc_key='sf_trunc', stellar_ages_key='stellar_age',
                                               fburst_key='fburst', tburst_key='tburst', sf_slope_key='sf_slope',
                                               dust_type=2, dust_tesc=7.0, dust_birth_cloud_key='dust1_birth_cloud',
                                               dust_diffuse_key='dust2_diffuse', dust_clumps=-99, frac_nodust=0.0,
                                               frac_obrun=0.0, dust_index_key='dust_index',
                                               dust_powerlaw_modifier_key='dust_calzetti_modifier', mwr_key='mwr',
                                               uvb_key='uvb', wgp1_key='wgp1', wgp2=1, wgp3=1,
                                               dust_emission_gamma_key='dust_gamma', dust_emission_umin_key='dust_umin',
                                               dust_emission_qpah_key='dust_qpah', fraction_agn_bol_lum_key='f_agn',
                                               agn_torus_opt_depth_key='tau_agn', tabulated_sfh_key='tabulated_sfh',
                                               tabulated_lsf_key='tabulated_lsf', physical_units=True,
                                               restframe_wave_key='restframe_wavelengths',
                                               restframe_sed_key='restframe_seds')
    fspssedmodel = fspssedmodeler.fit_model(training_data)
    assert len(fspssedmodel.data['restframe_seds']) == 10