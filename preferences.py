import bpy
from bpy.props import EnumProperty, BoolProperty, StringProperty, PointerProperty
from bpy.types import AddonPreferences

from .translate import is_enabled_global_translation
from .utils import ADDON_NAME

# 添加全局变量存储快捷键
addon_keymaps = []


class Preferences(AddonPreferences):
    bl_idname = ADDON_NAME

    tabs: EnumProperty(items=[("GTRANSLATION", "全局翻译[GT]", "全局翻译"),
                              ("QTRANSLATION", "双语切换[QT]", "语言切换按钮"),
                              ("LINKS", "相关链接[LK]", "相关链接")],
                       name="选项卡",
                       description="设置选项卡")

    button_toggle: BoolProperty(
        name="双语切换",
        description="启动/禁用语言切换按钮.\n"
                    "PS: 切换按钮显示在顶栏上",
        default=True
    )

    tooltips_included: BoolProperty(
        name="工具提示",
        description="切换时将影响工具提示的切换.\n"
                    "PS: 默认已影响界面的切换",
        default=True
    )

    use_translate_reports: BoolProperty(
        name="报告",
        description="切换时将影响报告的切换.\n"
                    "PS: 默认已影响报告的切换",
        default=True
    ) 

    # 添加快捷键设置属性
    language_switch_key: StringProperty(
        name="快捷键",
        description="语言切换快捷键",
        default="NONE"
    )
    
    language_switch_ctrl: BoolProperty(
        name="Ctrl",
        description="是否需要Ctrl键",
        default=False
    )
    
    language_switch_shift: BoolProperty(
        name="Shift",
        description="是否需要Shift键",
        default=False
    )
    
    language_switch_alt: BoolProperty(
        name="Alt",
        description="是否需要Alt键",
        default=False
    )

    last_check_update_time: StringProperty(name="上次检查更新时间", default="0")
    
    # 存储上一次的快捷键设置
    _last_keymap_settings = None
    
    def update_keymap(self):
        """更新快捷键设置"""
        wm = bpy.context.window_manager
        kc = wm.keyconfigs.addon
        if not kc:
            return
            
        # 只更新已存在的快捷键项
        if addon_keymaps:
            km, kmi = addon_keymaps[0]  # 获取第一个快捷键项（语言切换）
            # 更新修饰键
            kmi.ctrl = self.language_switch_ctrl
            kmi.shift = self.language_switch_shift
            kmi.alt = self.language_switch_alt
            
            # 更新按键
            if self.language_switch_key != "NONE":
                kmi.type = self.language_switch_key
            else:
                kmi.type = 'NONE'

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
                     text="翻译已启用" if enabled else "点击启用翻译",
                     icon='FILE_REFRESH',
                     depress=enabled)

        message = layout.row()
        message.alignment = 'CENTER'
        message.label(text="启用或禁用全局翻译后, 需要重启Blender!!!")
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
            column.label(text="更新日志未能加载")

    def draw_workspace_translation(self, context):
        layout = self.layout
        # 检查是否需要更新快捷键
        self.check_keymap_update()
        
        box = layout.box()
        row = box.row()
        row.label(text="语言切换按钮:")
        row.prop(self, "button_toggle", text="启用")
        split = box.split()
        split.active = self.button_toggle
        split.prop(self, "tooltips_included")

        view = context.preferences.view
        if hasattr(view, "use_translate_reports"):
            split.prop(self, "use_translate_reports")
            
        # 添加快捷键设置
        box = layout.box()
        col = box.column()
        col.label(text="快捷键设置:")
        row = col.row()
        row.prop(self, "language_switch_ctrl", text="Ctrl")
        row.prop(self, "language_switch_shift", text="Shift")
        row.prop(self, "language_switch_alt", text="Alt")
        row = col.row()
        row.prop(self, "language_switch_key", text="按键")
        row = col.row()
        row.label(text="提示: 修改设置后点击其他区域自动应用", icon='INFO')
    def draw_links(self, context):
        layout = self.layout
        # 检查是否需要更新快捷键
        self.check_keymap_update()

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
        
    def check_keymap_update(self):
        """检查快捷键设置是否需要更新"""
        current_settings = (
            self.language_switch_key,
            self.language_switch_ctrl,
            self.language_switch_shift,
            self.language_switch_alt
        )
        
        # 如果设置发生变化，则更新快捷键
        if self._last_keymap_settings != current_settings:
            self._last_keymap_settings = current_settings
            self.update_keymap()

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

def register_keymaps():
    """注册快捷键"""
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='Window', space_type='EMPTY', region_type='WINDOW')
        kmi = km.keymap_items.new("blt.language_switch", 
                                  type='NONE',  # 不设置默认按键
                                  value='PRESS')
        
        addon_keymaps.append((km, kmi))
        
        # 从偏好设置中读取默认快捷键设置
        try:
            pref = bpy.context.preferences.addons[ADDON_NAME].preferences
            if pref:
                kmi.ctrl = pref.language_switch_ctrl
                kmi.shift = pref.language_switch_shift
                kmi.alt = pref.language_switch_alt
                if pref.language_switch_key != "NONE":
                    kmi.type = pref.language_switch_key
        except:
            pass


def unregister_keymaps():
    """注销快捷键"""
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        for km, kmi in addon_keymaps:
            km.keymap_items.remove(kmi)
    addon_keymaps.clear()





def register():
    bpy.utils.register_class(Preferences)
    # 注册快捷键
    register_keymaps()


def unregister():
    bpy.utils.unregister_class(Preferences)
    # 注销快捷键
    unregister_keymaps()