import bpy
from bpy.types import Operator

from ..translate.wprkspace import update_workspace_name
from ..utils.public import get_pref


class LanguageSwitch(Operator):
    bl_idname = "blt.language_switch"
    bl_label = "切换中英文"
    bl_description = "一键切换中英文"

    @property
    def language_id(self):
        return "zh_CN" if "zh_CN" in bpy.app.translations.locales else "zh_HANS"
    def execute(self, context):
        view = context.preferences.view
        pref = get_pref()

        # 修复 Blender 4.0 更新语言配置文件导致错误
        if bpy.app.translations.locale not in ['zh_CN', "zh_HANS"]:
            view.language = self.language_id
            view.use_translate_tooltips = False
            view.use_translate_interface = False
            view.use_translate_new_dataname = False

        if pref.tooltips_included:
            view.use_translate_tooltips = not view.use_translate_interface
        if pref.use_translate_reports:
            if hasattr(view, "use_translate_reports"):
                view.use_translate_reports = not view.use_translate_reports

        view.use_translate_interface = not view.use_translate_interface

        if hasattr(view, "use_translate_new_dataname"):
            view.use_translate_new_dataname = False

        # 更新工作空间界面
        update_workspace_name()
        return {"FINISHED"}
