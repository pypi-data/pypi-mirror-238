"""Create a conftest.py
Define the fixture functions in this file to make them accessible across multiple test files.
"""
from pathlib import Path
from tempfile import mkdtemp

import pytest
from beetools.utils import rm_tree

_DESC = __doc__.split('\n')[0]
_PATH = Path(__file__)


class WorkingDir:
    def __init__(self):
        self.dir = Path(mkdtemp(prefix='displayfx_'))


class EnvSetUp:
    def __init__(self):
        self.dir = WorkingDir().dir


@pytest.fixture
def env_setup_self_destruct():
    """Set up the environment base structure"""
    setup_env = EnvSetUp()
    yield setup_env
    rm_tree(setup_env.dir, p_crash=False)


@pytest.fixture
def working_dir_self_destruct():
    """Set up the environment base structure"""
    working_dir = WorkingDir()
    yield working_dir
    rm_tree(working_dir.dir, p_crash=False)
