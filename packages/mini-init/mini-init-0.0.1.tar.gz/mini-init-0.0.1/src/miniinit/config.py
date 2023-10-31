from dataclasses import dataclass, field
from typing import Type, TypeVar

from dacite import from_dict

from .util import read_yaml_file

T = TypeVar('T')


@dataclass
class LogConfig:
    # 是否使用
    is_use: bool = True
    # 配置文件路径
    yaml_path: str = 'config/log.yaml'


@dataclass
class BannerConfig:
    # 是否显示
    is_show: bool = True
    # banner文件路径
    file_path: str = 'banner.txt'
    # 欢迎词
    welcome: str = ''


@dataclass
class AppConfig:
    # 项目名称
    name: str = ''
    # 项目版本
    version: str = ''


@dataclass
class Config:
    log: LogConfig = field(default_factory=LogConfig)
    banner: BannerConfig = field(default_factory=BannerConfig)
    app: AppConfig = field(default_factory=AppConfig)

    # 其他参数自行继承扩展
    ...


# 配置文件默认路径, 不可修改
d_config_path: str = 'config/application.yaml'


def get_config(config_class: Type[T]) -> T:
    """
    获取配置信息

    :param config_class: 配置类
    :param file_path: 配置文件路径
    :return: 配置信息
    """
    return from_dict(
        data_class=config_class,
        data=read_yaml_file(file_path=d_config_path)
    )


# 默认参数
d_config = get_config(Config)
