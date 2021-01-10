""" Account commands. """

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
from users.auth.commands import users
from utils.commons import get_data, get_host

# Host
HOST = get_host()


@users.command(help='Account info options. [auth required]')
@click.option(
    '--keys-path',
    '-k',
    type=(str),
    help='Custom path to save login keys.'
)
def account_info(keys_path) -> None:
    """ Get info account. """

    data = get_data(keys_path)
    url = f'{HOST}/users/{data["user"]["username"]}'
    headers = {
        'Authorization': data['authorization']['token']
    }

    return click.echo(requests.get(url, headers=headers).json())


@users.command(help='Update account options. [auth required]')
@click.option(
    '--email',
    '-e',
    type=(str),
    help='Email field.'
)
@click.option(
    '--username',
    '-u',
    type=(str),
    help='Username field.'
)
@click.option(
    '--password',
    '-p',
    type=(str),
    help='Password field.'
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
@click.option(
    '--keys-path',
    '-k',
    type=(str),
    help='Custom path to save login keys.'
)
def update_account(email: str, username: str,
                   password: str, first_name: str,
                   last_name: str, phone: int,
                   picture: str, keys_path: str) -> None:
    """ Update account group. """

    data = get_data(keys_path)
    url = f'{HOST}/users/{data["user"]["username"]}'
    payload = {
        'email': email,
        'username': username,
        'password': password,
        'password_confirmation': password,
        'first_name': first_name,
        'last_name': last_name,
        'phone': phone,
        'picture': picture
    }
    headers = {
        'Authorization': data['authorization']['token']
    }

    return click.echo(
        requests.put(url, data=payload, headers=headers).json()
    )


@users.command(help='Request reset password options.')
@click.option(
    '--email',
    '-e',
    type=(str),
    required=True,
    help='Email field'
)
def request_reset_password(email: str) -> None:
    """ Request reset password group. """

    url = f'{HOST}/users/reset-password'
    payload = {'email': email}

    return click.echo(requests.post(url, data=payload).json())


@users.command(help='Reset password options.')
@click.option(
    '--token',
    '-t',
    type=(str),
    required=True,
    prompt=True,
    hide_input=True,
    help='Token field. [prompt]'
)
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
    confirmation_prompt=True,
    help='Password field. [prompt]'
)
def reset_password(token: str, email: str, password: str) -> None:
    """ Reset password group. """

    url = f'{HOST}/users/reset-password'
    payload = {
        'token': token,
        'email': email,
        'password': password,
        'password_confirmation': password
    }

    return click.echo(requests.patch(url, data=payload).json())
