import click
from pypatcher.patcher import Patcher
from pathlib import Path

@click.group()
def cli():
    pass

@click.command()
@click.argument('patch_repo_src', type=click.Path(exists=True))
@click.argument('patch_destination', type=click.Path(exists=True))
@click.argument('message')
def new_patch(patch_repo_src, patch_destination, message):
    patch_repo_src = Path(patch_repo_src)
    patch_destination = Path(patch_destination)

    patcher = Patcher(patch_repo_src)
    patcher.new_patch(message, patches_dir=patch_destination)

@click.command()
@click.argument('target_repo_path', type=click.Path(exists=True))
@click.argument('patches_directory', type=click.Path(exists=True))
@click.option('--production', is_flag=True)
def apply_patches(target_repo_path, patches_directory, production):
    target_repo_path = Path(target_repo_path)
    patches_directory = Path(patches_directory)

    patcher = Patcher(target_repo_path)
    patcher.apply_patches(patches_directory, is_prod=production)


cli.add_command(new_patch)
cli.add_command(apply_patches)
