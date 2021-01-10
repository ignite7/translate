""" CLI. """

# Click
import click

# Utilities
from os import path
import sys

# Base dir
BASE_DIR = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Commands
from users.accounts.commands import users
from translations.identify.commands import translations
from histories.commands import histories
from favorites.commands import favorites


@click.group(help='Language Translation CLI.')
def cli():
    """Manage the main cli."""

    pass


# Add commands.
cli.add_command(users)
cli.add_command(translations)
cli.add_command(histories)
cli.add_command(favorites)


if __name__ == '__main__':
    cli()
