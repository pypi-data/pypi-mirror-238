from pathlib import Path
from typing import Any

from ruamel.yaml import YAML, YAMLError


def path_exists(file_path: str) -> bool:
    """
    判断路径是否存在

    :param file_path: 文件路径
    :return: 是否存在
    """
    return Path(file_path).exists()


def read_file(file_path: str, encoding: str = 'utf8') -> str:
    """
    读取文件内容

    :param file_path: 文件路径
    :param encoding: 编码格式默认utf8
    :return: 文件内容
    """
    with open(file_path, encoding=encoding) as f:
        return f.read()


def read_yaml_file(file_path: str, encoding: str = 'utf8', default={}) -> Any:
    """
    读取yaml文件

    :param file_path: 文件路径
    :param encoding: 编码格式默认utf8
    :param default: 默认值
    :return: yaml文件内容
    """
    if not path_exists(file_path):
        return default
    try:
        res = YAML(typ='safe').load(read_file(file_path, encoding))
        return default if res is None else res
    except YAMLError as _:
        return default
