from setuptools import setup

setup(name='swgoh_api',
      version='1.0.2',
      description='Library for getting info about Guilds, Players, Units and e.t.c from https://swgoh.gg',
      packages=[
        'swgoh_api',
        'swgoh_api.entities',
        'swgoh_api.utils',
        'swgoh_api.url_requests',
        'swgoh_api.loaders'
      ],
      author_email='da9ert0n@gmail.com',
      install_requires=[
        'ujson',
        'requests'
      ],
      zip_safe=False)