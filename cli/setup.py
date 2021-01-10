""" CLI Setup. """

# Utilities
from setuptools import setup, find_packages

# Specifications of the setup
setup(
    name='translate_cli',
    version='0.1',
    description='Translate CLI',
    url='https://www.sergiovanberkel.com/',
    author='Sergio van Berkel Acosta',
    author_mail='sergio.vanberkel@gmail.com',
    python_requires='>=3.6.*',
    install_requires=['click>=7.1.2', 'requests>=2.25.1'],
    packages=find_packages(),
    py_modules=['main'],
    entry_points='''
        [console_scripts]
        translate-cli=main:cli
    '''
)
