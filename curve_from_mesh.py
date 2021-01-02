import bpy
import bmesh
bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((0, 0, 0), (0, 0, 0), (0, 0, 0)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})

bpy.ops.object.editmode_toggle()
bpy.ops.mesh.select_mode(type="EDGE")
obj = bpy.context.edit_object
me = obj.data

bm = bmesh.from_edit_mesh(me)
for e in bm.edges:
    if not e.smooth:
        e.select=True

bmesh.update_edit_mesh(me, False)
bpy.ops.mesh.loop_multi_select(ring=True)
bpy.ops.mesh.delete(type='EDGE_FACE')
bpy.ops.object.editmode_toggle()
bpy.ops.object.convert(target='CURVE')

bpy.context.object.data.bevel_mode = 'OBJECT'
bpy.context.object.data.bevel_object = bpy.data.objects["NurbsPath"]

