""" Translate commands. """

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
from translations.groups import translations
from utils.languages import languages_list
from utils.commons import get_data, get_host

# Host
HOST = get_host()


@translations.command(help='Translate options. [auth required]')
@click.option(
    '--message',
    '-m',
    type=(str),
    required=True,
    help='Message field.'
)
@click.option(
    '--source',
    '-s',
    type=click.Choice(languages_list, case_sensitive=False),
    required=True,
    help='Source language choice.'
)
@click.option(
    '--target',
    '-t',
    type=click.Choice(languages_list, case_sensitive=False),
    required=True,
    help='Target language choice.'
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
def translate(message: str, source: list, target: list,
              favorite: bool, keys_path: str) -> None:
    """ Translate group. """

    data = get_data(keys_path)
    url = f'{HOST}/translations/translate'
    payload = {
        'message': message,
        'source': source,
        'target': target,
        'favorite': favorite
    }
    headers = {
        'Authorization': data['authorization']['token']
    }

    return click.echo(
        requests.post(url, data=payload, headers=headers).json()
    )
