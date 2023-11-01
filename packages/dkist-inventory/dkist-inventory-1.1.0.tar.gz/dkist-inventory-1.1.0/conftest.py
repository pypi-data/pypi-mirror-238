from filelock import FileLock
from pathlib import Path

import pytest


def rm_tree(pth):
    for child in pth.glob('*'):
        if child.is_file():
            child.unlink()
        else:
            rm_tree(child)
    pth.rmdir()


def pytest_addoption(parser):
    parser.addoption("--cached-tmpdir", action="store", default=None)


@pytest.fixture(scope="session")
def cached_tmpdir(tmp_path_factory, pytestconfig):
    """
    This fixture provides a way to override a temp directory from the cli so
    that it can be reused between test runs.
    """
    cached_dir = pytestconfig.getoption("--cached-tmpdir")
    if not cached_dir:
        # Setup a temp dir which is shared between all workers
        root_tmp_dir = tmp_path_factory.getbasetemp().parent
        tempdir = root_tmp_dir / "dkist-inventory"
        tempdir.mkdir(exist_ok=True)

        yield tempdir

    else:
        cached_dir = Path(cached_dir).expanduser().absolute()
        if not cached_dir.exists():
            cached_dir.mkdir()

        yield cached_dir
