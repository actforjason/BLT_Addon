import bpy
from bpy.types import Operator


class CheckMoUpdate(Operator):
    bl_idname = "blt.check_mo_update"
    bl_label = "检查更新"
    bl_description = "检查mo文件是否有更新"
    bl_options = {"REGISTER", "INTERNAL"}

    def execute(self, context):
        from ..mo_update import update_mo_info
        if update_mo_info():
            self.report({'INFO'}, "BLT:全局翻译可更新!!!! :>")
        else:
            self.report({'INFO'}, "BLT:翻译暂无更新! :>")
        bpy.ops.wm.save_userpref()
        return {"FINISHED"}
