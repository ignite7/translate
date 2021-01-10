""" Identify commands. """

# Click
import click

# Utilities
from os import path
import sys
import requests

# Base dir
BASE_DIR = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Modules
from translations.translate.commands import translations
from utils.commons import get_data, get_host

# Host
HOST = get_host()


@translations.command(help='Identify options. [auth required]')
@click.option(
    '--message',
    '-m',
    type=(str),
    required=True,
    help='Message field.'
)
@click.option(
    '--favorite',
    '-f',
    type=(bool),
    is_flag=True,
    default=False,
    help='Save translation to your favorites.'
)
@click.option(
    '--keys-path',
    '-k',
    type=(str),
    help='Custom path to save login keys.'
)
def identify(message: str, favorite: bool, keys_path: str) -> None:
    """ Identify group. """

    data = get_data(keys_path)
    url = f'{HOST}/translations/identify'
    payload = {'message': message, 'favorite': favorite}
    headers = {
        'Authorization': data['authorization']['token']
    }

    return click.echo(
        requests.post(url, data=payload, headers=headers).json()
    )
