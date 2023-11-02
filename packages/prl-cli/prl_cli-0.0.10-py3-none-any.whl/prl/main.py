import click
from prl.auth import get_auth_token, login
from .suite import suite
from .run import run


@click.group()
def cli():
    pass


cli.add_command(suite)
cli.add_command(run)
cli.add_command(login)
