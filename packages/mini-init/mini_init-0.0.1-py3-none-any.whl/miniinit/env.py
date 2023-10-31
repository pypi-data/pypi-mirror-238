from typing import Type, TypeVar

from dacite import from_dict
from dotenv import dotenv_values

T = TypeVar('T')


def get_env(env_class: Type[T], env_path: str = '.env') -> T:
    """
    获取环境变量.env

    :param env_class: 环境变量类
    :param env_path: 环境变量路径
    :return: 环境变量
    """
    return from_dict(
        data_class=env_class,
        data=dotenv_values(env_path, encoding='utf8')
    )
