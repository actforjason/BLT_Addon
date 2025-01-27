import bpy
from bpy.types import Operator

from ..translate import (
    is_enabled_global_translation,
    remove_global_translation,
    enable_global_translation,
)


class TranslationGlobal(Operator):
    bl_idname = "blt.translation_global"
    bl_label = "全局翻译本地插件"
    bl_description = "全局翻译本地插件(五分钟内重复点击仅下载翻译文件一次)"
    bl_options = {'INTERNAL'}

    @property
    def language(self) -> str:
        return "zh_CN" if "zh_CN" in bpy.app.translations.locales else "zh_HANS"

    def execute(self, context):
        # 根据当前状态切换语言环境
        if is_enabled_global_translation():
            remove_global_translation()
        else:
            view = context.preferences.view

            view.language = self.language
            view.use_translate_interface = True
            view.use_translate_tooltips = True
            try:
                enable_global_translation()
                bpy.ops.blt.quit_blender_dialog('INVOKE_DEFAULT')
            except Exception as e:
                import traceback
                traceback.print_stack()
                traceback.print_exc()
                print(e.args)
                self.report({'ERROR'}, "网络有问题...可以请尝试换个网络, 如手机USB连接或手机WIFI分享!")
        return {'FINISHED'}
