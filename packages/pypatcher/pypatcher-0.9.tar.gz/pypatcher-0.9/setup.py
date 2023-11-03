from setuptools import setup

setup(
    name = 'pypatcher',
    packages = ['pypatcher'],
    version = '0.9',
    license='GPL-3.0',
    description = 'Utility module for handling incremental git patches',
    author = 'David Angulo',
    author_email = 'david.angulo.arias@gmail.com',
    url = 'https://github.com/sgtpepper9907/pypatcher',
    keywords = ['git', 'patches', 'incremental'],
    install_requires=[
        'checksumdir==1.2.0',
        'click==8.1.7',
        'gitdb==4.0.10',
        'GitPython==3.1.40',
        'natsort==8.4.0',
        'smmap==5.0.1',
    ],
)
