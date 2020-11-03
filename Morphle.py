import bpy
import bmesh
import time

bl_info = {
    "name": "Morphle",
    "description": "Create object with shape keys from selected objects.",
    "author": "Roman Chumak",
    "version": (0, 0, 0, 2),
    "blender": (2, 90, 0),
    "location": "Properties / Object",
    "category": "Object"}


class MORPHLE_create(bpy.types.Operator):
    """Create Morphle"""
    bl_idname = 'morphle.create'
    bl_label = 'Morphle!'
    bl_options = {'INTERNAL', 'UNDO'}

    def execute(self, context):
        objs = []
        for obj in bpy.context.selected_objects:
            if obj.type == 'MESH':
                objs.append([len(obj.data.vertices), obj])

        objs.sort(key=lambda x: x[0], reverse=True)

        morphle_name = "Morphle_" + str(time.time_ns())
        morphle_mesh = bpy.data.meshes.new(morphle_name)
        morphle_obj = bpy.data.objects.new(morphle_name, morphle_mesh)

        morphle_bm = bmesh.new()
        morphle_bm.from_mesh(objs[0][1].data)

        sks = [morphle_obj.shape_key_add(name=obj.name) for _, obj in objs]

        morphle_bm.to_mesh(morphle_mesh)

        for s in range(1, len(objs)):
            print(sks[s])
            target_verts = objs[s][1].data.vertices
            for i in range(len(objs[0][1].data.vertices)):
                k = i % len(target_verts)
                sks[s].data[i].co = target_verts[k].co

        bpy.context.collection.objects.link(morphle_obj)

        return {'FINISHED'}


class MORPHLE_PT_Panel(bpy.types.Panel):
    bl_label = "Morphle"
    bl_idname = "MORPHLE_PT_Panel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    def draw(self, context):
        layout = self.layout
        morphle_ui = layout.column()
        morphle_ui.operator('morphle.create', icon="OUTLINER_OB_VOLUME")


def register():
    bpy.utils.register_class(MORPHLE_create)
    bpy.utils.register_class(MORPHLE_PT_Panel)


def unregister():
    bpy.utils.unregister_class(MORPHLE_create)
    bpy.utils.unregister_class(MORPHLE_PT_Panel)
