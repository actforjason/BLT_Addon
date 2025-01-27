import bpy
from bpy.props import EnumProperty, BoolProperty, StringProperty
from bpy.types import AddonPreferences

from .translate import is_enabled_global_translation
from .utils import ADDON_NAME


class Preferences(AddonPreferences):
    bl_idname = ADDON_NAME

    tabs: EnumProperty(items=[("GTRANSLATION", "全局翻译[GT]", "全局翻译"),
                              ("QTRANSLATION", "一键翻译[QT]", "一键翻译"),
                              ("LINKS", "相关链接[LK]", "相关链接")],
                       name="选项卡",
                       description="设置选项卡")

    button_toggle: BoolProperty(
        name="一键翻译",
        description="启动/禁用一键翻译按钮.\n"
                    "PS: 翻译按钮显示在顶栏上",
        default=True
    )

    tooltips_included: BoolProperty(
        name="工具提示",
        description="使用一键翻译进行切换时将影响工具提示的切换.\n"
                    "PS: 默认已影响界面的切换",
        default=True
    )

    use_translate_reports: BoolProperty(
        name="报告",
        default=True
    )

    last_check_update_time: StringProperty(name="上次检查更新时间", default="0")

    def draw_global_translation(self, context):
        from .mo_update import is_updatable
        from .ops.update_translation import UpdateTranslation
        from .ops.check_mo_update import CheckMoUpdate
        from datetime import datetime

        layout = self.layout
        enabled = is_enabled_global_translation()
        if enabled:
            row = layout.row(align=True)
            t = datetime.fromtimestamp(float(self.last_check_update_time)).strftime("%Y-%m-%d %H:%M:%S")
            row.label(text=f"上次检查更新时间: {t}")
            row.operator(CheckMoUpdate.bl_idname)
            if is_updatable:
                row.operator(UpdateTranslation.bl_idname)

        row = layout.row(align=True)
        row.operator("blt.translation_global",
                     text="已启用全局翻译" if enabled else "未启用全局翻译",
                     icon='FILE_REFRESH',
                     depress=enabled)

        message = layout.row()
        message.alignment = 'CENTER'
        message.label(text="启用或禁用全局翻译后, 重启 Blender 后生效!!!")
        column = layout.box().column()

        from .mo_update import mo_info
        if mo_info:
            for item in mo_info:
                if "TextInfo" not in item:
                    if len(item) > 100:
                        for i in item.split(","):
                            column.label(text=i)
                    else:
                        column.label(text=item)
        else:
            column.label(text="无法加载数据")

    def draw_workspace_translation(self, context):
        layout = self.layout
        box = layout.box()
        row = box.row()
        row.label(text="一键翻译:")
        row.prop(self, "button_toggle", text="启用")
        split = box.split()
        split.active = self.button_toggle
        split.prop(self, "tooltips_included")

        view = context.preferences.view
        if hasattr(view, "use_translate_reports"):
            split.prop(self, "use_translate_reports")

    def draw_links(self, context):
        layout = self.layout

        box = layout.box()
        about_title = box.row()
        about_title.alignment = 'CENTER'
        about_title.label(text="关于插件")
        about_msg = box.row()
        about_msg.alignment = 'CENTER'
        about_msg.label(text="☆此插件为免费插件, 禁止用于任何商业用途☆")

        box = layout.box()
        url_title = box.row()
        url_title.alignment = 'CENTER'
        url_title.label(text="文档与反馈")
        urls = box.row()
        urls.operator("wm.url_open", text="帮助文档").url = "https://blt.qa.pjcgart.com/questions/108"
        urls.operator("wm.url_open", text="问答平台").url = "https://blt.qa.pjcgart.com/"

    def draw(self, context):
        layout = self.layout
        tabs = layout.row()
        tabs.prop(self, "tabs", expand=True)
        layout.separator()
        if self.tabs == 'GTRANSLATION':
            self.draw_global_translation(context)
        elif self.tabs == 'QTRANSLATION':
            self.draw_workspace_translation(context)
        elif self.tabs == 'LINKS':
            self.draw_links(context)
        layout.separator()


def register():
    bpy.utils.register_class(Preferences)


def unregister():
    bpy.utils.unregister_class(Preferences)
