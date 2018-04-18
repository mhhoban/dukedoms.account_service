from setuptools import setup, find_packages

setup(
  name='dukedomsaccountservice',
  version='0.0.0',
  description='microservice for managinng player accountns for Dukedoms of Daleria',
  packages=find_packages(exclude=['swagger_codegen','*.tests']),
  include_package_data=True,
  install_requires=[
    'addict',
    'bravado',
    'connexion',
    'flask',
    'flask_api',
    'psycopg2',
    'retrying',
    'sqlalchemy'
  ]
)
