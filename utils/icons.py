import os

import bpy.utils.previews

__icons__ = None


class Icons:
    @classmethod
    def register(cls):
        global __icons__
        __icons__ = bpy.utils.previews.new()
        from .public import ADDON_FOLDER
        icon_folder = os.path.join(ADDON_FOLDER, 'src', 'icons')
        for file in os.listdir(icon_folder):
            name, suffix = file.split('.')
            file_path = os.path.abspath(os.path.join(icon_folder, file))
            is_png = file.lower().endswith('.png')
            if is_png and os.path.isfile(file_path):
                __icons__.load(name.lower(), file_path, 'IMAGE', force_reload=True)

    @classmethod
    def get(cls, key):
        global __icons__
        return __icons__[key.lower()]

    @classmethod
    def unregister(cls):
        global __icons__
        bpy.utils.previews.remove(__icons__)
