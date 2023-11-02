from distutils.core import setup

with open('requirements.txt') as f:
    install_requires = f.read().strip().split('\n')

setup(
    name = 'pypatcher',
    packages = ['pypatcher'],
    version = '0.8',
    license='GPL-3.0',
    description = 'Utility module for handling incremental git patches',
    author = 'David Angulo',
    author_email = 'david.angulo.arias@gmail.com',
    url = 'https://github.com/sgtpepper9907/pypatcher',
    download_url = 'https://github.com/sgtpepper9907/pypatcher/archive/refs/tags/v0.1.tar.gz',
    keywords = ['git', 'patches', 'incremental'],
    install_requires=install_requires
)
