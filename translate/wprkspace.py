import bpy
from bpy.app.handlers import persistent

WORKSPACE_NAME_TRANSLATION = {
    "Animation": '动画',
    "Compositing": '合成',
    "Geometry Nodes": '几何节点',
    "Layout": '布局',
    "Modeling": '建模',
    "Rendering": '渲染',
    "Scripting": '脚本',
    "Sculpting": '雕刻',
    "Shading": '着色',
    "Texture Paint": '纹理绘制',
    "UV Editing": 'UV 编辑',
    "2D Animation": '2D 动画',
    "2D Full Canvas": '2D 全画布',
    "Motion Tracking": '动作跟踪',
    "Masking": '遮罩',
    "Video Editing": '视频编辑'
}

WORKSPACE_NAME_TRANSLATION_REVERSAL = {v: k for k, v in WORKSPACE_NAME_TRANSLATION.items()}


def update_workspace_name():
    is_cn = bpy.context.preferences.view.use_translate_interface
    workspace_name_dict = WORKSPACE_NAME_TRANSLATION if is_cn else WORKSPACE_NAME_TRANSLATION_REVERSAL
    for workspace in bpy.data.workspaces:
        if workspace.name in workspace_name_dict:
            workspace.name = workspace_name_dict[workspace.name]



