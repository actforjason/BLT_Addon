import time

import bpy
import bpy.utils.previews

from ..ops.language_switch import LanguageSwitch
from ..ops.start_blt_client import StartBltClient
from ..utils import IS_WINDOW
from ..utils.icons import Icons
from ..utils.public import get_pref

show = 5
start = time.time()


def draw_header(self, context):
    # 仅在 WINDOWS 系统绘制此按钮
    from ..mo_update import is_updatable
    if context.region.alignment != 'RIGHT':
        row = self.layout.row(align=True)
        if IS_WINDOW:
            """绘制BLT按钮"""
            blt_icon = Icons.get("BLT").icon_id
            row.operator(StartBltClient.bl_idname, text="", icon_value=blt_icon)


        
        if get_pref().button_toggle:
            """中英按钮"""
            interface = context.preferences.view.use_translate_interface
            key = "CN" if interface else "EN"
            icon = Icons.get(key).icon_id
            row.operator(LanguageSwitch.bl_idname, text="", icon_value=icon)
        if is_updatable and time.time() - start < show:
            r = row.row()
            r.alert = True
            r.label(text=f"BLT全局翻译可更新!!!! :>")

        # 文本区块
        box = row.box()  # 添加外框
        box.label(text="Status")  # 将 label 放在 box 中
def register():
    bpy.types.TOPBAR_HT_upper_bar.append(draw_header)


def unregister():
    bpy.types.TOPBAR_HT_upper_bar.remove(draw_header)
