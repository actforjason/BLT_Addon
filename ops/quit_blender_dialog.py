import os
import bpy

from ..translate import is_enabled_global_translation


def start_blender():
    import subprocess
    bpy.ops.wm.save_userpref()
    subprocess.Popen([bpy.app.binary_path])


class QuitBlenderDialog(bpy.types.Operator):
    bl_idname = "blt.quit_blender_dialog"
    bl_label = "退出 Blender"

    def draw(self, context):
        layout = self.layout
        message = "全局翻译已启用" if is_enabled_global_translation() else "全局翻译已禁用"
        layout.label(text=message + ", 重启 Blender 将使之生效.", icon='QUESTION')
        layout.label(text="是否确定立刻关闭 Blender?")

    def execute(self, context):
        start_blender()
        bpy.ops.wm.quit_blender()
        # 使用 os._exit(0) 确保 Blender 安全退出
        os._exit(0)
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
