from dataclasses import dataclass, field
from miniinit import config


@dataclass
class AppConfig(config.AppConfig):
    uid: str = ''


@dataclass
class Config(config.Config):
    app: AppConfig = field(default_factory=AppConfig)
    ...


def test_config():
    config_data = config.get_config(Config)
    assert config_data.app.uid == '1234567890'
    print(config_data)
