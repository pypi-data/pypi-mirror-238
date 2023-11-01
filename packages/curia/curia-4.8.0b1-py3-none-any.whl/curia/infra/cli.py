import click

from curia.infra.container.cli import container
from curia.infra.databricks.cli import databricks


@click.group()
def cli():
    pass


cli.add_command(container)
cli.add_command(databricks)


if __name__ == "__main__":
    cli()
