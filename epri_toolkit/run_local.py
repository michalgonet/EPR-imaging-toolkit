import click
from pathlib import Path
from epri_toolkit.classes import Config


@click.command()
@click.option('--config-path', type=str, default="configurations/default_config.json", help='Path to config file')
@click.option('--input-file', type=str, default="data/input", help='Path to input file.')
@click.option('--out-dir', type=str, default="data/output", help='Path to output directory')
def run_local(config_path, input_file, out_dir):
    config = Config(config_path)


if __name__ == '__main__':
    run_local()
