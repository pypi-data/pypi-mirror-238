from setuptools import setup

setup(
    name='requim',
    version='1.0.4',
    description='Additional cryptological package for Telethon.',
    author='requim',
    author_email='nomail@void.io',
    install_requires=[
        'telethon == 1.30.3',
        'requests'
    ]
)