from dataclasses import dataclass
import logging

from miniinit import env

logger = logging.getLogger(__name__)


@dataclass
class Env:
    PROJECT_NAME: str = ''


def test_env():
    env_data = env.get_env(Env)
    assert env_data.PROJECT_NAME == 'mini-init'
