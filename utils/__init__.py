import os
import sys
from shutil import copy2, Error, copystat

import bpy

from .. import __package__ as __addon_name__

ADDON_NAME = __addon_name__
IS_WINDOW = sys.platform == 'win32'
IS_MAC = sys.platform == 'darwin'
IS_LINUX = sys.platform == 'linux'
IS_PORTABLE = "portable" in __file__


def __mkdir__(path) -> None:
    """文件夹不存在递归创建文件夹"""
    if not os.path.exists(path):
        os.makedirs(path)


def __get_blender_global_path__() -> str:
    if IS_PORTABLE:  # 便携目录
        return __get_portable_path__()

    # Blender 全局目录赋值
    if IS_WINDOW:
        return os.path.join(
            os.getenv("APPDATA"), "Blender Foundation", "Blender")
    elif IS_MAC:
        return os.path.join(os.getenv("HOME"), "Library", "Application Support", "Blender")
    elif IS_LINUX:
        # as /home/<user>/.config/blender/
        return os.path.join(os.getenv("HOME"), ".config", "blender")
    else:
        raise Exception("不支持的系统平台: " + sys.platform)


def __get_portable_path__() -> str:
    if IS_WINDOW:
        return os.path.join(os.path.dirname(bpy.app.binary_path), "portable")
    print("__file__", __file__)
    raise Exception("不支持的系统平台: " + sys.platform)


def copytree(src, dst, symlinks=False, ignore=None):
    """"https://stackoverflow.com/questions/12683834/how-to-copy-directory-recursively-in-python-and-overwrite-all/12687372#12687372"""
    names = os.listdir(src)
    if ignore is not None:
        ignored_names = ignore(src, names)
    else:
        ignored_names = set()

    if not os.path.isdir(dst):  # This one line does the trick
        os.makedirs(dst)
    errors = []
    for name in names:
        if name in ignored_names:
            continue
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        try:
            if symlinks and os.path.islink(srcname):
                linkto = os.readlink(srcname)
                os.symlink(linkto, dstname)
            elif os.path.isdir(srcname):
                copytree(srcname, dstname, symlinks, ignore)
            else:
                # Will raise a SpecialFileError for unsupported file types
                copy2(srcname, dstname)
        # catch the Error from the recursive copytree so that we can
        # continue with other files
        except Error as err:
            errors.extend(err.args[0])
        except EnvironmentError as why:
            errors.append((srcname, dstname, str(why)))
        try:
            copystat(src, dst)
        except OSError as why:
            if WindowsError is not None and isinstance(why, WindowsError):
                # Copying file access times may fail on Windows
                pass
            else:
                errors.extend((src, dst, str(why)))

        if errors:
            raise Error(errors)
