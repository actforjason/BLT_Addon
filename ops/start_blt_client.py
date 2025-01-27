"""BLT 客户端"""
import os
import subprocess
from functools import cache

from bpy.types import Operator

from ..translate import BLT_INFO_PATH


def get_blt_client_exe_path_from_info() -> str:
    """ 获取 info 中 BLT 可执行文件位置
    :return:
    """
    info_path = os.path.join(BLT_INFO_PATH, "BLT_Version.info")
    blt_exe_path = ""
    if os.path.exists(info_path):
        with open(info_path, "r", encoding="utf-8", errors="ignore") as info:
            # 根据 BLT_Version 文件格式设置字符串切片 [8:-1]
            blt_exe_path = info.readline()[8:-1]
    return blt_exe_path


@cache
def blt_is_running():
    """检查BLT是否在运行"""
    res = os.popen("tasklist")
    tasklist = res._stream.buffer.read().decode(encoding="utf-8", errors="ignore")
    return tasklist.find("BLT_") != -1


class StartBltClient(Operator):
    bl_idname = "blt.start_blt_client"
    bl_label = "启动 BLT 客户端"
    bl_description = "一键启动 BLT 客户端"

    # IS_RUNNING = False
    #
    # @classmethod
    # def poll(cls, context) -> bool:
    #     return not cls.IS_RUNNING

    def execute(self, context):
        # 检查是否正在运行中
        blt_is_running.cache_clear()
        if blt_is_running():
            self.report({'INFO'}, "BLT已经被启动.")
            return {'FINISHED'}
        # 获取客户端位置并运行
        client = get_blt_client_exe_path_from_info()
        if not client:
            self.report({'ERROR'}, "你还没有安装或使用过BLT, 请先下载并运行BLT !!")
        else:
            subprocess.Popen(client)
            self.report({'INFO'}, "BLT已经被启动, 请耐心等待.")
        return {'FINISHED'}
