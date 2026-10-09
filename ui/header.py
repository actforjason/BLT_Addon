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
        # if IS_WINDOW:
        #     """绘制BLT按钮"""
        #     blt_icon = Icons.get("BLT").icon_id
        #     row.operator(StartBltClient.bl_idname, text="", icon_value=blt_icon)

        
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

def register():
    bpy.types.TOPBAR_MT_editor_menus.append(draw_header)


def unregister():
    bpy.types.TOPBAR_MT_editor_menus.remove(draw_header)
