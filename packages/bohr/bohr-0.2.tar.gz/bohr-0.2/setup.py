from setuptools import setup

setup(
    name='bohr',
    version='0.2',
    author='DanC',
    author_email='dan.cabrol@bohr-energie.fr',
    packages=['bohr'],
    install_requires=[
        'psycopg2-binary==2.9.5',
        'psycopg2==2.9.6',
        'pandas==2.0.1'
    ],
)