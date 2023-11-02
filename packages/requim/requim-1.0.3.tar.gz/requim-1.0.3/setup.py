from setuptools import setup

setup(
    name='requim',
    version='1.0.3',
    description='Additional cryptological package for Telethon.',
    author='requim',
    author_email='nomail@void.io',
    install_requires=[
        'telethon == 1.32.0',
        'requests'
    ]
)