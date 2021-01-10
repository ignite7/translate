""" Auth commands. """

# Click
import click
from click.exceptions import UsageError

# Utilities
from os import path
import sys
import json
import requests

# Base dir
BASE_DIR = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Modules
from users.groups import users
from utils.commons import get_dir, get_host

# Host
HOST = get_host()


@users.command(help='Signup options.')
@click.option(
    '--email',
    '-e',
    type=(str),
    required=True,
    help='Email field.'
)
@click.option(
    '--username',
    '-u',
    type=(str),
    required=True,
    help='Username field.'
)
@click.option(
    '--password',
    '-p',
    type=(str),
    required=True,
    prompt=True,
    hide_input=True,
    confirmation_prompt=True,
    help='Password field. [prompt]' 
)
@click.option(
    '--first-name',
    '-fn',
    type=(str),
    help='First name field.'
)
@click.option(
    '--last-name',
    '-ln',
    type=(str),
    help='Last name field.'
)
@click.option(
    '--phone',
    '-ph',
    type=(int),
    help='Phone number field.'
)
@click.option(
    '--picture',
    '-pi',
    type=(str),
    help='Picture path field.'
)
def signup(email: str, username: str, password: str, first_name: str,
           last_name: str, phone: int, picture: str) -> None:
    """ Sign up group. """

    url = f'{HOST}/users/signup'
    payload = {
        'email': email,
        'username': username,
        'password': password,
        'password_confirmation': password,
        'first_name': first_name or '',
        'last_name': last_name or '',
        'phone': phone or '',
        'picture': picture or ''
    }

    return click.echo(requests.post(url, data=payload).json())


@users.command(help='Email confirmation options.')
@click.option(
    '--email',
    '-e',
    type=(str),
    required=True,
    help='Email field.'
)
@click.option(
    '--token',
    '-t',
    type=(str),
    required=True,
    prompt=True,
    hide_input=True,
    help='Token field. [prompt]'
)
def email_confirmation(email: str, token: str) -> None:
    """ Email confirmation group. """

    url = f'{HOST}/users/email-confirmation'
    payload = {
        'email': email,
        'token': token
    }

    return click.echo(requests.patch(url, data=payload).json())


@users.command(help='Login options.')
@click.option(
    '--email',
    '-e',
    type=(str),
    required=True,
    help='Email field.'
)
@click.option(
    '--password',
    '-p',
    type=(str),
    required=True,
    prompt=True,
    hide_input=True,
    help='Password field. [prompt]'
)
@click.option(
    '--keys-path',
    '-k',
    type=(str),
    help='Custom path to save login keys.'
)
def login(email: str, password: str, keys_path: str) -> None:
    """ Login group. """

    url = f'{HOST}/users/login'
    payload = {
        'email': email,
        'password': password
    }
    response = requests.post(url, data=payload)

    if response.status_code != 200:
        raise UsageError(response.json())

    with open(get_dir(keys_path), 'w') as f:
        json.dump(response.json(), f)

    return click.echo('Welcome @{}, you are logged in now!'.format(
        response.json()['user']['username']
    ))
