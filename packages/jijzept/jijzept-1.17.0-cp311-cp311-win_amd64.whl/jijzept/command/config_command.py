import os

import click

from jijzept.config.handle_config import CONFIG_PATH, DEFAULT_CONFIG_FILE, create_config


@click.group()
def main():
    pass


@main.command()
def create():
    click.echo("--- Welcome to JijZept ---")
    config_path = click.prompt(
        "Please enter the configuration path", default=CONFIG_PATH
    )
    host_url = click.prompt("Please enter the your API's URL")
    token = click.prompt("Please eneter the your token (subscription key)")
    config_file_name = create_config(
        token=token, host_url=host_url, config_path=os.path.normcase(config_path)
    )
    click.echo(f"Config file path {os.path.normcase(config_file_name)}")
    click.echo("----- Thank you -----")


@main.command()
def show():
    click.echo(
        "JijZept's default configuration path: {}".format(
            os.path.join(CONFIG_PATH, DEFAULT_CONFIG_FILE)
        )
    )

    with open(os.path.join(CONFIG_PATH, DEFAULT_CONFIG_FILE)) as f:
        config_str = f.read()

    click.echo("-------------------")
    click.echo(config_str)
    click.echo("-------------------")


if __name__ == "__main__":
    main()
