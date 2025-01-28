import os
import shutil
import time
import zipfile
from urllib import request

import bpy

from .. import __file__ as __root_file__
from ..utils import __get_blender_global_path__, __mkdir__, copytree, IS_MAC, IS_PORTABLE

ADDON_ROOT_PATH = os.path.dirname(os.path.realpath(__root_file__))  # 插件根目录
ADDON_LOCALE_PATH = os.path.join(ADDON_ROOT_PATH, "src", "locale")  # 插件 locale 目录
BLENDER_GLOBAL_PATH = __get_blender_global_path__()  # Blender 全局目录

# TODO 将全局与需要移动翻译的文件夹分开
BV = bpy.app.version
BLENDER_BASE_VERSION = f"{BV[0]}.{BV[1]}"  # Blender 版本号
BLENDER_GLOBAL_VERSION_PATH = f"{BLENDER_GLOBAL_PATH}" if IS_PORTABLE else f"{BLENDER_GLOBAL_PATH}/{BLENDER_BASE_VERSION}"  # Blender 全局版本路径
BLENDER_GLOBAL_DATAFILE_PATH = os.path.join(BLENDER_GLOBAL_VERSION_PATH, "datafiles")  # Blender 全局 datafiles 路径
BLENDER_GLOBAL_LOCALE_PATH = os.path.join(BLENDER_GLOBAL_DATAFILE_PATH, "locale")  # Blender 全局 locale 路径
blender_local = os.path.join(os.path.dirname(bpy.app.binary_path), BLENDER_BASE_VERSION, "datafiles", "locale")# 当前blender程序中local路径

BLT_PATH = os.path.join(BLENDER_GLOBAL_PATH, "BLT_translation_Dicts")  # BLTDicts 路径
BLT_INFO_PATH = os.path.join(BLT_PATH, "info")  # BLTDicts info 路径
BLT_MO_INFO_PATH = os.path.join(BLT_PATH, "Mo_UpdateVersion.txt")
BLT_DATAFILES_PATH = os.path.join(BLT_PATH, "datafiles")  # BLTDicts datafiles 路径
BLT_LOCALE_PATH = os.path.join(BLT_DATAFILES_PATH, "locale")  # BLTDicts locale 路径

def is_enabled_global_translation() -> bool:
    """是否已启用全局翻译
    :return: bool
    """
    return os.path.exists(BLENDER_GLOBAL_LOCALE_PATH)


def remove_global_translation() -> None:
    """ 移除全局翻译
    :return:
    """
    shutil.rmtree(BLENDER_GLOBAL_LOCALE_PATH)


def enable_global_translation(forced: bool = False):
    """获取全局翻译"""
    # 移除旧版翻译
    if os.path.exists(BLT_DATAFILES_PATH):
        shutil.rmtree(BLT_DATAFILES_PATH)
    # 检查并创建 blt_path
    __mkdir__(BLT_PATH)
    datafiles_zip_path = os.path.join(BLT_PATH, "datafiles.zip")
    # 判断翻译文件是否存在且过期
    zip_file_not_find = not os.path.exists(datafiles_zip_path)
    mo_info_file_not_find = not os.path.exists(BLT_MO_INFO_PATH)

    time_out = os.path.isfile(datafiles_zip_path) and time.time() - os.path.getmtime(datafiles_zip_path) > 5000  # 秒
    if zip_file_not_find or mo_info_file_not_find or time_out or forced:
        # 存在过期文件时删除
        if os.path.exists(datafiles_zip_path):
            os.remove(datafiles_zip_path)
        if os.path.exists(BLT_MO_INFO_PATH):
            os.remove(BLT_MO_INFO_PATH)
        # 下载翻译文件
        zip_web_path = "http://raw.pjcgart.com/blt_Translation/mo/datafiles.zip"
        mo_info_web_path = "http://raw.pjcgart.com/blt_Translation/mo/Mo_UpdateVersion.txt"
        request.urlretrieve(zip_web_path, datafiles_zip_path)
        request.urlretrieve(mo_info_web_path, BLT_MO_INFO_PATH)
    # 解压翻译文件d
    zip_file = zipfile.ZipFile(datafiles_zip_path)
    zip_list = zip_file.namelist()
    for f in zip_list:
        zip_file.extract(f, BLT_PATH)
    zip_file.close()
    # 复制翻译文件
    __mkdir__(BLENDER_GLOBAL_DATAFILE_PATH)

    __copy_blender_mo_to_global__()
    copytree(BLT_LOCALE_PATH, BLENDER_GLOBAL_LOCALE_PATH)
    zh_hans_path = os.path.join(BLENDER_GLOBAL_LOCALE_PATH, "zh_HANS")
    zh_cn_path = os.path.join(BLENDER_GLOBAL_LOCALE_PATH, "zh_CN")
    if os.path.exists(zh_hans_path):
        copytree(zh_hans_path, zh_cn_path)
    __copy_languages_file__()

    from ..mo_update import update_mo_info
    update_mo_info()


def __copy_blender_mo_to_global__():
    """复制当前Blender的所有Mo到全局文件夹"""
    
    if IS_MAC:
        print("Mac !! TODO Move Mo")
        print(blender_local)
        print(BLENDER_GLOBAL_LOCALE_PATH)
    else:
        copytree(blender_local, BLENDER_GLOBAL_LOCALE_PATH)


def __copy_languages_file__():
    """复制BLT的languages文件到全局文件夹"""
    source = os.path.join(ADDON_LOCALE_PATH, 'languages')
    target = os.path.join(BLENDER_GLOBAL_LOCALE_PATH, "languages")
    shutil.copyfile(source, target)
