import os
import ssl
import subprocess
import sys
from threading import Thread

import bpy


def sendmsg(msg):
    """发送消息"""
    from .src.modules.websocket import create_connection
    ws = create_connection("ws://127.0.0.1:33333")
    info = '"%s": %s' % (bpy.context.scene.blt_message_objectname, msg)
    ws.send(info)
    ws.close()
    print(info)


def importsendmsg():
    sendmsg("已经导入Blender(Blender Import Finished)!!!")


def new_client(_, server):
    server.send_message_to_all("GetServer")


def message_received(_, server, message):
    message = message.encode('raw_unicode_escape').decode("utf-8")
    print(message)
    if message.find("FilePath:") != -1:
        bpy.context.scene.blt_message = message
        message = bpy.context.scene.blt_message

        GetBlenderFile = message.split(":Filetype:")[0].split("FilePath:")[1]
        GetFileType = message.split(":Filetype:")[1]
        Getobjectname = GetBlenderFile.split("/")[-1].split(".")[0]
        bpy.context.scene.blt_message_objectname = Getobjectname

        for window in bpy.context.window_manager.windows:
            for area in window.screen.areas:
                if area.type == 'VIEW_3D':
                    print(GetFileType)
                    if (GetFileType == "Object"):
                        with bpy.data.libraries.load(GetBlenderFile) as (
                                data_from, data_to):
                            data_to.objects = data_from.objects
                            data_to.collections = data_from.collections
                        a = 0
                        for obj in data_to.objects:
                            if obj.name == Getobjectname:
                                a = 1
                        b = 0
                        for collet in data_to.collections:
                            if collet.name == Getobjectname:
                                b = 1
                        collection = Getobjectname
                        if a == 1 and b == 0:
                            for obj in data_to.objects:
                                if obj.name == collection:
                                    bpy.context.scene.collection.objects.link(obj)
                        if a == 0 and b == 1:
                            for new_coll in data_to.collections:
                                if new_coll.name == collection:
                                    bpy.context.scene.collection.children.link(new_coll)
                        if a == 1 and b == 1:
                            for new_coll in data_to.collections:
                                if new_coll.name == collection:
                                    bpy.context.scene.collection.children.link(new_coll)
                        if a == 0 and b == 0:
                            for new_coll in data_to.collections:
                                bpy.context.scene.collection.children.link(new_coll)
                        a = 0
                        b = 0

                    if (GetFileType == "Collection"):
                        collection = Getobjectname
                        with bpy.data.libraries.load(GetBlenderFile) as (
                                data_from, data_to):
                            data_to.objects = data_from.objects
                            data_to.collections = data_from.collections
                        a = 0
                        for new_coll in data_to.collections:
                            if new_coll.name == collection:
                                a = 1
                            else:
                                a = 0
                        for new_coll in data_to.collections:
                            if a == 1:
                                if new_coll.name == collection:
                                    bpy.context.scene.collection.children.link(new_coll)
                            if a == 0:
                                bpy.context.scene.collection.children.link(new_coll)

                    if (GetFileType == "Material"):
                        with bpy.data.libraries.load(GetBlenderFile) as (
                                data_from, data_to):
                            data_to.materials = data_from.materials

                        for material in data_to.materials:
                            if material.name == Getobjectname:
                                print("import now!!!")

                    if (GetFileType == "HDRI"):
                        hdrworld = bpy.data.worlds['World']
                        hdrworld.use_nodes = True
                        for i in bpy.data.worlds['World'].node_tree.nodes:
                            bpy.data.worlds['World'].node_tree.nodes.remove(i)
                        hdroutput = bpy.data.worlds['World'].node_tree.nodes.new(
                            "ShaderNodeOutputWorld")
                        hdroutput.location = (680, 200)
                        hdrbg = bpy.data.worlds['World'].node_tree.nodes.new(
                            "ShaderNodeBackground")
                        hdrbg.location = (400, 200)
                        hdrnode = bpy.data.worlds['World'].node_tree.nodes.new(
                            "ShaderNodeTexEnvironment")
                        hdrnode.image = bpy.data.images.load(GetBlenderFile)
                        hdrnodes = bpy.data.worlds['World'].node_tree.nodes
                        hdrnode.location = (0, 150)

                        uv_node = hdrnodes.new(type="ShaderNodeTexCoord")
                        uv_node.location = (-300, 150)

                        map_node = hdrnodes.new(type="ShaderNodeMapping")
                        map_node.vector_type = "TEXTURE"
                        map_node.inputs['Rotation'].default_value = (0, 0, 3.141593)
                        uv_node.location = (-150, 150)

                    if GetFileType == "BVH":
                        exepath = sys.argv[0]
                        blendfiles = GetBlenderFile[:-4] + ".blend"
                        mainpath = os.path.abspath(os.path.dirname(
                            os.path.split(os.path.realpath(__file__))[0]))
                        bone_ref_name = GetBlenderFile[:-4].split("/")[-1]
                        resource_high = 2
                        try:
                            resource_high = bpy.context.scene.anim_resource_armature.dimensions[2]
                            filename = mainpath + "\\Anim\\operators\\bvh\\blt_import_bvh.py"
                            getrenderBlendPath = mainpath + "\\Anim\\operators\\bvh\\BLT_BVH.blend"
                            data_b = ""
                            with open(filename, 'w') as f:
                                data_b += "import bpy\n"
                                data_b += "bpy.data.scenes['Scene'].frame_start=0\n"
                                data_b += "bpy.data.scenes['Scene'].frame_end=0\n"
                                data_b += 'bpy.ops.import_anim.bvh(filepath="' + GetBlenderFile.replace("\\",
                                                                                                        "/") + '"' + ",global_scale=0.1)\n"
                                data_b += 'obj=bpy.context.selected_objects[0]\n'
                                data_b += 'dim_y=' + str(resource_high) + '/obj.dimensions[2]\n'
                                data_b += 'bpy.ops.transform.resize(value=(dim_y,dim_y, dim_y), orient_type="GLOBAL", orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type="GLOBAL", mirror=False, use_proportional_edit=False, proportional_edit_falloff="SMOOTH", proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)\n'
                                data_b += 'bpy.ops.wm.save_as_mainfile(filepath="' + blendfiles + '")\n'
                                data_b += "bpy.ops.wm.quit_blender()\n"
                                f.write(data_b)
                                f.close()

                            subprocess.run([exepath, getrenderBlendPath, "--background",
                                            "--python", filename.replace("\\", "/")])

                            with bpy.data.libraries.load(blendfiles) as (data_from, data_to):
                                data_to.objects = [name for name in data_from.objects if name == bone_ref_name]

                            bpy.context.collection.objects.link(
                                bpy.data.objects[bone_ref_name])
                            bpy.context.scene.anim_target_armature = bpy.data.objects[bone_ref_name]

                        except Exception as err:
                            print("infoerr", err)
                            filename = mainpath + "\\Anim\\operators\\bvh\\blt_import_bvh.py"
                            getrenderBlendPath = mainpath + "\\Anim\\operators\\bvh\\BLT_BVH.blend"
                            data_b = ""
                            with open(filename, 'w') as f:
                                data_b += "import bpy\n"
                                data_b += "bpy.data.scenes['Scene'].frame_start=0\n"
                                data_b += "bpy.data.scenes['Scene'].frame_end=0\n"
                                data_b += 'bpy.ops.import_anim.bvh(filepath="' + GetBlenderFile.replace("\\",
                                                                                                        "/") + '"' + ",global_scale=0.1)\n"
                                data_b += 'obj=bpy.context.selected_objects[0]\n'
                                data_b += 'dim_y=' + str(resource_high) + '/obj.dimensions[2]\n'
                                data_b += 'bpy.ops.transform.resize(value=(dim_y,dim_y, dim_y), orient_type="GLOBAL", orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type="GLOBAL", mirror=False, use_proportional_edit=False, proportional_edit_falloff="SMOOTH", proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)\n'
                                data_b += 'bpy.ops.wm.save_as_mainfile(filepath="' + blendfiles + '")\n'
                                data_b += "bpy.ops.wm.quit_blender()\n"
                                f.write(data_b)
                                f.close()

                            subprocess.run([exepath, getrenderBlendPath, "--background",
                                            "--python", filename.replace("\\", "/")])

                            with bpy.data.libraries.load(blendfiles) as (data_from, data_to):
                                data_to.objects = [name for name in data_from.objects if name == bone_ref_name]

                            bpy.context.collection.objects.link(
                                bpy.data.objects[bone_ref_name])

                            bpy.context.scene.anim_target_armature = bpy.data.objects[bone_ref_name]

                    for space in area.spaces:
                        if space.type == 'VIEW_3D' and GetFileType != "BVH":
                            space.shading.type = 'RENDERED'

        t1 = Thread(None, importsendmsg)
        t1.setDaemon(True)
        t1.start()

    if message.find("Blender(Blender Import Finished)") != -1:
        try:
            server.send_message_to_all(message)
        except Exception as e:
            print(e)


def start_server():
    try:
        from .src.modules.websocket_server import WebsocketServer
        server = WebsocketServer(33333, host='127.0.0.1')
        server.set_fn_new_client(new_client)
        server.set_fn_message_received(message_received)
        server.run_forever()
    except Exception as e:
        print(e)


thread = None


def register():
    from .utils import IS_WINDOW
    if IS_WINDOW:
        global thread
        # 不验证 SSL 证书
        ssl._create_default_https_context = ssl._create_unverified_context

        thread = Thread(None, start_server)
        thread.setDaemon(True)
        thread.start()
        print("start blt service")


def unregister():
    global thread
    if thread is not None:
        ...  # kill TODO
