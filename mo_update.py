import os
import threading
import time
from urllib import request

import bpy

from .translate import BLT_MO_INFO_PATH
from .utils.public import get_pref

mo_info = None
mo_version = None
is_updatable = False

mo_info_web_path = "http://raw.pjcgart.com/blt_Translation/mo/Mo_UpdateVersion.txt"


def update_mo_info():
    global mo_info, mo_version, is_updatable
    if os.path.exists(BLT_MO_INFO_PATH):
        with open(BLT_MO_INFO_PATH, "r", encoding="utf-8") as file:
            mo_version = float(file.readline().replace("Version:", "").replace("\n", ""))
            mo_info = file.readlines()

        response = request.urlopen(mo_info_web_path)
        data = response.read()
        data_str = data.decode("utf-8")
        cloud_version = float(data_str.split("\n")[0].replace("Version:", "").replace("\n", ""))
        is_updatable = mo_version < cloud_version
        print(f"Blt check mo_info mo_version:{mo_version} cloud_version:{cloud_version} is_updatable:{is_updatable}")

    t = time.time()
    get_pref().last_check_update_time = str(t)
    bpy.ops.wm.save_userpref()
    return is_updatable


def register():
    # 大于30天检测更新
    if os.path.exists(BLT_MO_INFO_PATH):
        pref = get_pref()
        if time.time() > float(pref.last_check_update_time) + 30 * 86400:
            # 时间以秒为单位
            threading.Thread(target=update_mo_info).start()


def unregister():
    ...
