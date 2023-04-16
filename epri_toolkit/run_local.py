import click

from epri_toolkit.classes import Config
from epri_toolkit.files_utils import get_raw_data, get_acq_pars
from epri_toolkit.reco_utils import get_reco_pars, reconstruct
from epri_toolkit.processing_utils import sinogram_preprocessing
from epri_toolkit.visualization_utils import disp_2x2, disp_4D


@click.command()
@click.argument('config-path', type=str, default="configurations/default_config.json")
def run_local(config_path):
    config = Config(config_path)
    raw_data = get_raw_data(config)
    acq_pars = get_acq_pars(raw_data.raw_sinogram_pars)
    reco_pars = get_reco_pars(config, acq_pars)
    sinogram = sinogram_preprocessing(raw_data, acq_pars, reco_pars)
    reco = reconstruct(sinogram, acq_pars, reco_pars)

    if acq_pars.img_type == '3D':
        disp_2x2(reco[:, :, int(reco_pars.img_size / 2)],
                 reco[:, int(reco_pars.img_size / 2), :],
                 reco[int(reco_pars.img_size / 2), :, :],
                 sinogram)
    elif acq_pars.img_type == '3D + Spectral':
        disp_4D(reco[:, :, int(reco_pars.img_size / 2), int(reco_pars.img_size / 2)],
                reco[:, int(reco_pars.img_size / 2), :, int(reco_pars.img_size / 2)],
                reco[int(reco_pars.img_size / 2), :, :, int(reco_pars.img_size / 2)],
                reco[20, 30, 40, :])


if __name__ == '__main__':
    run_local()
