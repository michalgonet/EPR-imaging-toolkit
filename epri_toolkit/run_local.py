import click

from epri_toolkit.classes import Config, Reconstruction
from epri_toolkit.files_utils import get_raw_data, get_acq_pars
from epri_toolkit import reco_utils
from epri_toolkit import processing_utils
from epri_toolkit.visualization_utils import disp_2x2


@click.command()
@click.argument('config-path', type=str, default="configurations/default_config.json")
def run_local(config_path):
    config = Config(config_path)
    raw_data = get_raw_data(config)
    acq_pars = get_acq_pars(raw_data.raw_sinogram_pars)
    reco_pars = reco_utils.get_reco_pars(config, acq_pars)
    sinogram = processing_utils.sinogram_preprocessing(raw_data, acq_pars, reco_pars)
    reco = Reconstruction(sinogram=sinogram, acq_pars=acq_pars, reco_pars=reco_pars)

    reco.reco_array = reco_utils.fbp3d(sinogram, reco_pars)

    disp_2x2(reco.reco_array[:, :, int(reco_pars.img_size / 2)],
             reco.reco_array[:, int(reco_pars.img_size / 2), :],
             reco.reco_array[int(reco_pars.img_size / 2), :, :],
             sinogram)


if __name__ == '__main__':
    run_local()
