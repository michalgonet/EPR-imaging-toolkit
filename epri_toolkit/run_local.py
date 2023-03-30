import click

from epri_toolkit.classes import Config, Reconstruction


@click.command()
@click.argument('config-path', type=str, default="configurations/default_config.json")
def run_local(config_path):
    config = Config(config_path)
    reco = Reconstruction()
    reco.get_acq_pars(config)
    reco.get_reco_pars(config)


if __name__ == '__main__':
    run_local()
