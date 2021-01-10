""" Favorites commands. """

# Click
import click
from click.exceptions import UsageError

# Utilities
from os import path
import sys
import requests

# Base dir
BASE_DIR = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Modules
from utils.commons import get_data, get_host

# Host
HOST = get_host()


@click.group(help='Favorites.')
def favorites() -> None:
    """ Manage favorites group. """

    pass


@favorites.command(help='List favorites. [auth required]')
@click.option(
    '--keys-path',
    '-k',
    type=(str),
    help='Custom path to save login keys.'
)
def list(keys_path: str) -> None:
    """ List favorites group. """

    data = get_data(keys_path)
    url = f'{HOST}/favorites/{data["user"]["username"]}'
    headers = {
        'Authorization': data['authorization']['token']
    }

    return click.echo(requests.get(url, headers=headers).json())


@favorites.command(help='Create favorite. [auth required]')
@click.option(
    '--uuid',
    '-u',
    type=(str),
    required=True,
    help='UUID favorite to delete.'
)
@click.option(
    '--keys-path',
    '-k',
    type=(str),
    help='Custom path to save login keys.'
)
def create(uuid: str, keys_path: str) -> None:
    """ Create group. """

    data = get_data(keys_path)
    url = f'{HOST}/favorites/{data["user"]["username"]}/{uuid}'
    headers = {
        'Authorization': data['authorization']['token']
    }

    return click.echo(requests.post(url, headers=headers).json())


@favorites.command(help='Delete by ID. [auth required]')
@click.option(
    '--uuid',
    '-u',
    type=(str),
    required=True,
    help='UUID favorite to delete.'
)
@click.option(
    '--keys-path',
    '-k',
    type=(str),
    help='Custom path to save login keys.'
)
def delete_by_id(uuid: str, keys_path: str) -> None:
    """ Delete by id group. """

    data = get_data(keys_path)
    url = f'{HOST}/favorites/{data["user"]["username"]}/{uuid}'
    headers = {
        'Authorization': data['authorization']['token']
    }
    response = requests.delete(url, headers=headers)

    if response.status_code != 204:
        raise UsageError('UUID not found.')

    return click.echo(f'<{uuid}> Deleted successfully.')


@favorites.command(help='Delete All. [auth required]')
@click.option(
    '--keys-path',
    '-k',
    type=(str),
    help='Custom path to save login keys.'
)
def delete_all(keys_path: str) -> None:
    """ Delete all group. """

    data = get_data(keys_path)
    url = f'{HOST}/favorites/{data["user"]["username"]}'
    headers = {
        'Authorization': data['authorization']['token']
    }
    response = requests.delete(url, headers=headers)

    if response.status_code != 204:
        raise UsageError('Something was wrong.')

    return click.echo(f'Favorites Deleted successfully.')
