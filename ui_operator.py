import bpy, os
import bmesh

from bpy.props import BoolProperty, StringProperty, EnumProperty

class Ah_Generate_from_mesh_OT_Operator(bpy.types.Operator):
    bl_idname = "view3d.generate_hair_from_mesh"
    bl_label = "Generate hair form mesh"
    bl_description = "Generate hair from mesh"

    useExistingMat = BoolProperty()
    useExistingBevel = BoolProperty()
    material = StringProperty()
    bevel = StringProperty()

    def execute(self, context):
        mirror = None
        data = bpy.data
        ops = bpy.ops
        ctx = bpy.context
        # duplicate selected object and remove unused wireframe
        baseObject = bpy.context.active_object.name
        bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'})
        generatedObject = "ah_"+baseObject
        bpy.context.active_object.name = generatedObject

        append_lib("ah_bevel", "Object")
        bpy.ops.object.select_all(action="DESELECT")
        bpy.context.view_layer.objects.active = bpy.data.objects[generatedObject]
        bpy.data.objects[generatedObject].select_set(True)

        if data.objects[generatedObject].modifiers.get('Mirror'):
            mirror = True
            data.objects[generatedObject].modifiers['Mirror'].show_viewport = False
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='DESELECT')
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
        if mirror:
            ops.object.modifier_add(type='MIRROR')
        
        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.curve.spline_type_set(type='NURBS')
        index = 0
        for spline in bpy.context.object.data.splines:
            bpy.context.object.data.splines[index].use_endpoint_u=True
            index+=1
        ctx.object.data.resolution_u = 2
        bpy.context.object.data.bevel_object = bpy.data.objects["ah_bevel"]
        bpy.ops.object.mode_set(mode="OBJECT")
        bpy.context.object.data.bevel_mode = 'OBJECT'


        bpy.context.view_layer.objects.active = bpy.data.objects[baseObject]

        bpy.context.object.hide_viewport = True

        bpy.ops.object.select_all(action="DESELECT")
        # create_collection()

        bpy.ops.object.select_all(action="DESELECT")
        bpy.context.view_layer.objects.active = bpy.data.objects[generatedObject]
        bpy.data.objects[generatedObject].select_set(True)
        bpy.ops.object.shade_smooth()
        bpy.ops.object.material_slot_add()

        append_lib("ah_node", "NodeTree")
        materialName = generatedObject
        if self.useExistingMat:
            materialName = self.material
        create_material(materialName)

        return {'FINISHED'}

class Test_OT_Operator(bpy.types.Operator):

    bl_idname = "view3d.test"
    bl_label = "test"
    bl_description = "test"

    def execute(self, context):
        nodes = bpy.data.materials['ah_Sphere'].node_tree.nodes
        links = bpy.data.materials['ah_Sphere'].node_tree.links

        node1 = nodes.get('ah_Sphereah_node')
        node2 = nodes.get('Principled BSDF')

        links.new(node1.outputs['Color'], node2.inputs['Base Color'])
        links.new(node1.outputs['Alpha'], node2.inputs['Alpha'])
        links.new(node1.outputs['Normal'], node2.inputs['Normal'])

        return{"FINISHED"}

class Curve_Select_First_OT_Operator(bpy.types.Operator):
    bl_idname = "view3d.curve_select_first"
    bl_label = "Select First"
    bl_description = "Select first vertext in curve"
    
    def execute(self, context):
        bpy.ops.curve.de_select_first()
        return{"FINISHED"}

class Curve_Select_Last_OT_Operator(bpy.types.Operator):
    bl_idname = "view3d.curve_select_last"
    bl_label = "Select last"
    bl_description = "Select last vertext in curve"
    
    def execute(self, context):
        bpy.ops.curve.de_select_last()
        return{"FINISHED"}

class Curve_Switch_Direction_OT_Operator(bpy.types.Operator):
    bl_idname = "view3d.curve_switch_direction"
    bl_label = "Swithc curve direction"
    bl_description = "Swithc curve direction"
    
    def execute(self, context):
        bpy.ops.curve.switch_direction()
        return{"FINISHED"}
# def create_collection(materialName):

def append_lib(objName, directory):
    sep = os.sep
    found = None
    if directory == "Object":
        found = bpy.context.scene.objects.get(objName)
    elif directory == "NodeTree":
        found = bpy.data.node_groups.get(objName)
    if not found:
        filepath = get_addon_path()+"lib.blend"
        bpy.ops.wm.append(
            filepath = filepath,
            directory = filepath+sep+directory,
            filename = objName)

def create_material(name):
    groupName = name+"_node"
    foundMaterial = bpy.data.materials.get(name)
    if not foundMaterial:
        bpy.data.materials.new(name)
        bpy.context.object.data.materials[0] = bpy.data.materials[name]
        bpy.context.object.active_material.use_nodes = True
        bpy.context.object.active_material.blend_method = 'HASHED'
        bpy.context.object.active_material.shadow_method = 'HASHED'
        node_group = bpy.data.node_groups['ah_node']
        new_group_node = bpy.data.materials[name].node_tree.nodes.new(type='ShaderNodeGroup')
        new_group_node.node_tree = node_group
        new_group_node.name = groupName
        new_group_node.node_tree.name = groupName
    else:
        bpy.context.object.data.materials[0] = bpy.data.materials[name]

    #connect the node 
    nodes = bpy.data.materials[name].node_tree.nodes
    links = bpy.data.materials[name].node_tree.links
    node1 = nodes.get(groupName)
    node2 = nodes.get('Principled BSDF')
    links.new(node1.outputs['Color'], node2.inputs['Base Color'])
    links.new(node1.outputs['Alpha'], node2.inputs['Alpha'])
    links.new(node1.outputs['Normal'], node2.inputs['Normal'])


def create_collection():
    foundCollection = bpy.data.collections.get("agni_hair_lib")
    if not foundCollection:
        bpy.ops.collection.create(name="agni_hair_lib")
        bpy.context.scene.collection.children.link(bpy.data.collections["agni_hair_lib"])

def get_addon_path():
    sep = os.sep

    # Search for addon dirs
    roots = bpy.utils.script_paths()
    possible_dir_names = ["agni_hair", "agni_hair" + '-master']
    for root in roots:
        if os.path.basename(root) != 'scripts': continue
        filepath = root + sep + 'addons'
        dirs = next(os.walk(filepath))[1]
        folders = [x for x in dirs if x in possible_dir_names]
        if folders:
            return filepath + sep + folders[0] + sep
    return 'ERROR: No path found for ' + "agni_hair" + '!'

# template popup menu

def get_material_list(scene, context):
    items = []
    for mat in bpy.data.materials:
        if mat.name.startswith('ah_'):
            items.append((mat.name, mat.name, mat.name))
    return items
def get_bevel_list(scene, context):
    items = []
    for bev in bpy.data.objects:
        if bev.name.startswith('ah_bevel'):
            items.append((bev.name, bev.name, bev.name))
    return items

class WM_OT_myOp(bpy.types.Operator):
    bl_label = "test"
    bl_idname = "wm.test"
    
    useExistingMat = BoolProperty(name='Use exist material')
    mat = EnumProperty(name="ArsaHair material", items = get_material_list)
    useExistingBevel = BoolProperty(name="Use exist bevel curve")
    bevel = EnumProperty(name="ArsaHair Bevel", items = get_bevel_list)
    # text = bpy.props.StringProperty(name="hello", default="")

    def draw(self, context):
        layout = self.layout

        layout.prop(self, "useExistingMat")
        if self.useExistingMat:
            layout.prop(self, "mat")
        layout.prop(self, "useExistingBevel")
        if self.useExistingBevel:
            layout.prop(self, "bevel")
        
        # layout.prop(self, "text")

    def execute(self, context):
        bpy.ops.view3d.generate_hair_from_mesh(useExistingMat= self.useExistingMat, useExistingBevel=self.useExistingBevel, material=self.mat, bevel=self.bevel)
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)