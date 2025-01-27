from os.path import dirname, realpath

import bpy

ADDON_FOLDER = dirname(dirname(realpath(__file__)))


def get_pref():
    from .. import __package__ as __addon_name__
    return bpy.context.preferences.addons[__addon_name__].preferences
