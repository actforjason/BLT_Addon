"""
Copyright (C) 2020 PJ PENG
pjwaixingren@me.com
Created by pjpeng
"""
from . import register as reg

bl_info = {
    "name": "BLT",
    "description": "This addon use to BLT Software",
    "author": "Keshi, pjwaixingren, 小萌新",
    "version": (2025, 7, 18),
    "blender": (3, 0, 0),
    "location": "Menu BlT",
    "wiki_url": "https://www.pjcgart.com",
    "tracker_url": "https://blt.qa.pjcgart.com",
    "category": "UI"
}


def register():
    reg.register()


def unregister():
    reg.unregister()
