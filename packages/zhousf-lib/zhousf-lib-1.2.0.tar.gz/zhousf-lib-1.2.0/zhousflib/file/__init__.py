# -*- coding: utf-8 -*-
# @Author  : zhousf
# @Date    : 2023/11/1 
# @Function:
import shutil
from pathlib import Path


def overwrite_folder(from_dir: Path, to_dir: Path):
    """
    覆盖目录，覆盖已有文件
    :param from_dir: 目录
    :param to_dir: 被覆盖目录
    :return:
    """
    for file in from_dir.rglob("*.*"):
        shutil.copy(file, to_dir.joinpath(file.parent.name))
        print(file)
    pass
