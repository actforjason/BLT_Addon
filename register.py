from . import mo_update
from . import ops
from . import preferences
from . import property
from . import server
from . import src
from . import ui
from .utils import ADDON_NAME
import bpy

module_list = (
    preferences,
    property,
    src,
    ops,
    server,
    ui,
    mo_update
)


def register():
    for module in module_list:
        module.register()


def unregister():
    for module in module_list:
        module.unregister()

