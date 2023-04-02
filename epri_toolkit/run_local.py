import click

from epri_toolkit.classes import Config, Reconstruction
from epri_toolkit.files_utils import load_bruker_files
from epri_toolkit import reco_utils
from epri_toolkit.processing_utils import sinogram_interpolation, sinogram_integration


@click.command()
@click.argument('config-path', type=str, default="configurations/default_config.json")
def run_local(config_path):
    config = Config(path=config_path)
    sinogram, acq_pars = load_bruker_files(config)
    reco_pars = reco_utils.get_reco_pars(config, acq_pars)
    sinogram_interpolated = sinogram_interpolation(sinogram, reco_pars)
    sinogram_integrated = sinogram_integration(sinogram_interpolated)
    reco = Reconstruction(sinogram=sinogram_integrated, acq_pars=acq_pars, reco_pars=reco_pars)
    reco.reco_array = reco_utils.fbp3d(sinogram_integrated, reco_pars)

    import matplotlib.pyplot as plt
    plt.subplot(2, 2, 1)
    plt.imshow(reco.reco_array[:, :, 32], cmap=plt.cm.jet)
    plt.subplot(2, 2, 2)
    plt.imshow(reco.reco_array[:, 32, :], cmap=plt.cm.jet)
    plt.subplot(2, 2, 3)
    plt.imshow(reco.reco_array[32, :, :], cmap=plt.cm.jet)
    plt.subplot(2, 2, 4)
    plt.plot(reco.sinogram[:, 200])
    plt.show()


if __name__ == '__main__':
    run_local()
