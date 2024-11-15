# pylint: disable=C0103
""" Test library for the boot generator. """
import logging
import os
import tempfile

from typing import Optional, Tuple

# pylint: disable=E0401
from Fakeroot import Fakeroot


class Boot:
    """ Test library for the boot generator. """

    ROBOT_LIBRARY_SCOPE = 'SUITE'

    # directory for initrd build output
    target: str
    # helper
    fake = Fakeroot()

    def __init__(self):
        """ Init Python logging. """
        logging.basicConfig(level=logging.DEBUG)

    def build_boot(
        self,
        config: Optional[str] = None,
        generator: Optional[str] = None
    ):
        """ Build the boot archive. """
        if config is None:
            config = os.path.abspath(os.path.join(
                os.path.dirname(__file__), '..', 'data', 'boot.yaml'))
        if generator is None:
            generator = "boot_generator"

        self.target = tempfile.mkdtemp()
        logging.info('Target directory: %s', self.target)

        cmd = f'bash -c "source /build/venv/bin/activate; {generator} {config} {self.target}"'
        self.fake.run(cmd)

    def _unpack(self):
        """ Unpack the boot tar. """
        archive = os.path.join(self.target, 'boot.tar')

        assert os.path.isfile(archive)

        self._run(f'tar xf {archive}')

    def _run(self, cmd: str, check=True) -> Tuple[str, str]:
        """ Run command using fakeroot. """

        return self.fake.run_fake(
            cmd=cmd,
            cwd=self.target,
            check=check
        )

    def load(self):
        """ Unpack the initrd and read the init script. """
        self._unpack()

    def cleanup(self):
        """ Remove generated artefacts. """
        self._run(f'rm -rf {self.target}')

    def file_should_exist(self, path: str, file_type: str = 'regular file'):
        """ Check that a file exists. """
        assert self.target is not None
        if path.startswith('/'):
            path = path[1:]
        file = os.path.join(self.target, path)

        self.fake.abs_file_should_exist(file, file_type)

    def directory_should_exist(self, path: str):
        """ Check that a folder exists. """
        assert self.target is not None
        if path.startswith('/'):
            path = path[1:]
        d = os.path.join(self.target, path)

        self.fake.abs_directory_should_exist(d)

    def should_have_mode(self, path: str, mode: str):
        """ Check that a file exists. """
        assert self.target is not None
        if path.startswith('/'):
            path = path[1:]
        path = os.path.join(self.target, path)

        self.fake.abs_should_have_mode(
            path=path,
            mode=int(mode))

    def should_be_owned_by(self, path: str, uid: str, gid: str):
        """ Check that a file exists. """
        assert self.target is not None
        if path.startswith('/'):
            path = path[1:]
        path = os.path.join(self.target, path)

        self.fake.abs_should_be_owned_by(
            path=path,
            uid=int(uid),
            gid=int(gid))
