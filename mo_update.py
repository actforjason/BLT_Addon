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
            # 修改为字符串分割方式解析版本号
            local_version_str = file.readline().replace("Version:", "").replace("\n", "")
            mo_version = list(map(int, local_version_str.split('.')))  # 支持 1.5.1 这样的三位版本号
            mo_info = file.readlines()

        response = request.urlopen(mo_info_web_path)
        data = response.read()
        data_str = data.decode("utf-8")
        # 同样修改为字符串分割方式解析云端版本号
        cloud_version_str = data_str.split("\n")[0].replace("Version:", "").replace("\n", "")
        cloud_version = list(map(int, cloud_version_str.split('.')))
        
        # 逐位比较版本号
        is_updatable = False
        # 确保比较时取较小的长度，避免索引越界
        min_len = min(len(cloud_version), len(mo_version))
        for i in range(min_len):
            if cloud_version[i] > mo_version[i]:
                is_updatable = True
                break
            elif cloud_version[i] < mo_version[i]:
                break
        print(f"Blt check mo_info mo_version:{local_version_str} cloud_version:{cloud_version_str} is_updatable:{is_updatable}")

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
