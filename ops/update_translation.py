import bpy
from bpy.types import Operator

from ..translate import (
    remove_global_translation,
    enable_global_translation,
)


class UpdateTranslation(Operator):
    bl_idname = "blt.update_translation_global"
    bl_label = "更新全局翻译"

    def execute(self, context):
        try:
            remove_global_translation()
            enable_global_translation(True)
            bpy.ops.blt.quit_blender_dialog('INVOKE_DEFAULT')
        except Exception as e:
            import traceback
            traceback.print_stack()
            traceback.print_exc()
            print(e.args)
            self.report({'ERROR'}, "网络有问题...可以请尝试换个网络, 如手机USB连接或手机WIFI分享!")
        return {"FINISHED"}
