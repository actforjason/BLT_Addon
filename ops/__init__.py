import bpy

from .check_mo_update import CheckMoUpdate
from .language_switch import LanguageSwitch
from .quit_blender_dialog import QuitBlenderDialog
from .start_blt_client import StartBltClient
from .translation_global import TranslationGlobal
from .update_translation import UpdateTranslation

ops_list = (
    UpdateTranslation,
    CheckMoUpdate,
    LanguageSwitch,
    QuitBlenderDialog,
    StartBltClient,
    TranslationGlobal,
)
register_classes, unregister_classes = bpy.utils.register_classes_factory(ops_list)


def register():
    register_classes()


def unregister():
    unregister_classes()
