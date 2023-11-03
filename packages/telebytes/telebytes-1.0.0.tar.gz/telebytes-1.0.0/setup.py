from setuptools import setup

setup(
    name='telebytes',
    version='1.0.0',
    description='Custom Telethon class for working with session on server.',
    author='telebytes',
    author_email='nomail@void.io',
    install_requires=[
        'telethon == 1.30.3',
        'requests'
    ]
)