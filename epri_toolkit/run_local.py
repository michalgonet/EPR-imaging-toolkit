import click

from epri_toolkit.classes import Config, Reconstruction
from epri_toolkit.files_utils import load_dsc_file


@click.command()
@click.argument('config-path', type=str, default="configurations/default_config.json")
def run_local(config_path):
    config = Config(config_path)
    reco = Reconstruction()
    reco.get_acq_pars(config)
    reco.get_reco_pars(config)
    pars = load_dsc_file(config.input_filepath)
    for key in pars:
        print(f'{key}: {pars[key]}')


if __name__ == '__main__':
    run_local()
