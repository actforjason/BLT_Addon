import threading

import bpy
from bpy.app.handlers import persistent

from .translate.wprkspace import update_workspace_name


@persistent
def __register_workspace_name_timer__(_, __):
    bpy.app.timers.register(update_workspace_name)


def update_blt_is_running():
    from .ops.start_blt_client import blt_is_running, StartBltClient
    blt_is_running.cache_clear()
    StartBltClient.IS_RUNNING = blt_is_running()


def clear_cache():
    """清理缓存
    再判断一次blt是否启动"""
    threading.Thread(target=update_blt_is_running).start()
    return 1


def register():
    __register_workspace_name_timer__(None, None)
    bpy.app.handlers.load_post.append(__register_workspace_name_timer__)


def unregister():
    bpy.app.handlers.load_post.remove(__register_workspace_name_timer__)
