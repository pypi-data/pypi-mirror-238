import logging.config

from .config import d_config
from .util import path_exists, read_file, read_yaml_file
from . import config, env, util

# 显示banner
if d_config.banner.is_show and path_exists(d_config.banner.file_path):
    print(read_file(d_config.banner.file_path))
    print(d_config.banner.welcome, end='\n\n')

# 更改日志配置
if d_config.log.is_use and path_exists(d_config.log.yaml_path):
    logging.config.dictConfig(
        config=read_yaml_file(d_config.log.yaml_path)
    )

__all__ = [
    'config',
    'env',
    'util'
]
