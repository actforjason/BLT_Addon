from .translate import BLT_PATH, BLT_INFO_PATH
from .utils import __mkdir__
import bpy
from bpy.props import StringProperty

def register():
    # 初始化相关目录
    __mkdir__(BLT_PATH)
    __mkdir__(BLT_INFO_PATH)

    # 增加插件变量
    bpy.types.Scene.blt_message = StringProperty(name="")
    bpy.types.Scene.blt_message_objectname = StringProperty(name="")
    bpy.types.Scene.blt_message_directoryname = StringProperty(name="")


def unregister():
    # 删除插件变量
    del bpy.types.Scene.blt_message
    del bpy.types.Scene.blt_message_objectname
    del bpy.types.Scene.blt_message_directoryname
