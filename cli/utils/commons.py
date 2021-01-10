""" Commons utils. """

# Click
from click.exceptions import UsageError

# Utilities
from os import path
from pathlib import Path
import json


def get_json(route: str) -> dict:
    """ Get json data or raise error. """

    if not path.isfile(route):
        raise UsageError('The path is not a valid json file.')

    with open(route, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            raise UsageError('Invalid json file.')

    if not data.get('authorization', False) and not data.get('user', False):
        raise UsageError('Invalid credentials.')

    return data


def get_data(keys_path: str = '') -> str:
    """ Get data of the json file. """

    save_path = path.join(str(Path.home()), '.translate_cli.json')

    if keys_path and path.exists(keys_path):
        save_path = keys_path

    return get_json(save_path)


def get_dir(keys_path: str = '') -> str:
    """ Get home dir or custom path. """

    save_path = path.join(str(Path.home()), '.translate_cli.json')

    if keys_path and path.exists(keys_path) and path.isdir(keys_path):
        save_path = path.join(keys_path, '.translate_cli.json')

    return save_path


def get_host(dev: bool = False, prod: bool = True) -> str:
    """ Get DNS of the API. """

    if dev:
        host = 'http://0.0.0.0:8000'
    else:
        host = 'http://ec2-18-134-181-101.eu-west-2.compute.amazonaws.com:8000'

    return host
