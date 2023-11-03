from pathlib import Path
from git import Repo
from checksumdir import dirhash
from natsort import natsorted
from pypatcher.errors import (AlreadyPatchedError, OriginBranchDetectionError, InvalidPatchesDirectory, NothingToPatchError)
import re
import datetime

class Patcher():

    def __init__(self, repo_path: Path) -> None:
        self.__repo = Repo(repo_path)

    def new_patch(self, message: str, patches_dir: Path, only_staging_area: bool = True) -> None:
        self.__validate_patches_dir(patches_dir)
        timestamp = datetime.datetime.utcnow().strftime('%Y_%m_%dT%H%M%S')

        diff = self.__repo.git.diff('--staged' if only_staging_area else '', '--ignore-all-space')

        if not diff:
            raise NothingToPatchError()

        file_name = timestamp + '__' + re.sub(r'\s+', '_', message).lower() + '.patch'
        patches_dir.joinpath(file_name).write_text(diff + "\n")

        # Save unstaged WIP
        self.__repo.git.stash('push', '--keep-index')

        # Restore changes to apply patch
        self.__repo.git.restore('--staged', '.')
        self.__repo.git.restore('.')

        # Detach head
        self.__repo.git.checkout('--detach')

        self.apply_patches(patches_dir)

        # Unstash WIP changes
        self.__repo.git.stash('pop')

    def apply_patches(self, patches_dir: Path, is_prod: bool = False):
        self.__validate_patches_dir(patches_dir)
        patches_commit_message = self.__get_commit_message_for_patches(patches_dir)

        if self.__repo.head.is_detached and not is_prod:
            current_commit = self.__repo.head.commit

            if current_commit.message.strip() == patches_commit_message:
                raise AlreadyPatchedError()

            # delete origin HEAD
            remote_name = re.match(r'^.+$', self.__repo.git.remote(), flags=re.MULTILINE)

            if not remote_name:
                raise OriginBranchDetectionError()

            remote_name = remote_name[0].strip()
            self.__repo.git.remote('set-head', remote_name, '-d')
            origin_branch_match = re.match(r'^[^\/]*\/([^\ ]+)', self.__repo.git.branch('--remote', '--no-abbrev'))
            origin_branch = origin_branch_match.groups()[0] if origin_branch_match else None

            if not origin_branch:
                raise OriginBranchDetectionError()

            self.__repo.git.checkout(origin_branch)

        self.__repo.git.checkout('--detach')

        patches = natsorted([p.absolute().as_posix() for p in patches_dir.glob('*.patch')])
        for patch in patches:
            self.__repo.git.apply(patch, '--ignore-space-change', '--ignore-whitespace')

        if not is_prod:
            self.__repo.git.add('.')
            self.__repo.git.commit('-m', patches_commit_message, author='pypatcher <pypatcher@pypatcher.com>')

    def __validate_patches_dir(self, patches_dir: Path) -> None:
        if not patches_dir.exists() or not patches_dir.is_dir():
            raise InvalidPatchesDirectory()

    def __get_commit_message_for_patches(self, patches_dir: Path) -> str:
        return 'pypatcher/' + dirhash(patches_dir, hashfunc='sha256')
