import bpy 

class NODE_PT_Panel(bpy.types.Panel):
    bl_label = "Arsa Hair"
    bl_category = "Arsa Hair"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout

        row = layout.row(align=True)
        row.operator('view3d.generate_hair_from_mesh', text='Generate hair from mesh')
        
        layout.separator()
        row = layout.row(align=True)
        row.operator('view3d.test', text='test')

        # scene = context.scene

        # # Create a simple row.
        # layout.label(text=" Simple Row:")

        # row = layout.row()
        # row.prop(scene, "frame_start")
        # row.prop(scene, "frame_end")

        # # Create an row where the buttons are aligned to each other.
        # layout.label(text=" Aligned Row:")

        # row = layout.row(align=True)
        # row.prop(scene, "frame_start")
        # row.prop(scene, "frame_end")

        # # Create two columns, by using a split layout.
        # split = layout.split()

        # # First column
        # col = split.column()
        # col.label(text="Column One:")
        # col.prop(scene, "frame_end")
        # col.prop(scene, "frame_start")

        # # Second column, aligned
        # col = split.column(align=True)
        # col.label(text="Column Two:")
        # col.prop(scene, "frame_start")
        # col.prop(scene, "frame_end")

        # # Big render button
        # layout.label(text="Big Button:")
        # row = layout.row()
        # row.scale_y = 3.0
        # row.operator("render.render")

        # # Different sizes in a row
        # layout.label(text="Different button sizes:")
        # row = layout.row(align=True)
        # row.operator("render.render")

        # sub = row.row()
        # sub.scale_x = 2.0
        # sub.operator("render.render")

        # row.operator("render.render")

class AH_Texture_PT_Panel(bpy.types.Panel):
    bl_label = "Hair Texture Setting"
    bl_category = "Arsa Hair"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    def draw(self, context):
        activeMat = bpy.context.object.active_material
        layout = self.layout
        cr = layout.template_color_ramp
        if activeMat.name.startswith('ah_'):
            layout.row(align=False).label(text="Random Color :")
            random_color = activeMat.node_tree.nodes[activeMat.name+'_node'].node_tree.nodes['random_color']
            cr(random_color, "color_ramp", expand=True)
            layout.row(align=False).label(text="Shadow Color :")
            shadow_color = activeMat.node_tree.nodes[activeMat.name+'_node'].node_tree.nodes['shadow_color']
            cr(shadow_color, "color_ramp", expand=True)
        else:layout.row(align=False).label(text="Not Arsa Hair Material")

class AH_Curve_PT_Panel(bpy.types.Panel):
    bl_label = "Curve Tool"
    bl_category = "Arsa Hair"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        row = layout.row(align=True)
        row.label(text="Select curve point :")
        row = layout.row(align=True)
        row.operator('view3d.curve_select_first', text="first")
        row.operator('view3d.curve_select_last', text="last")
        layout.separator()
        row = layout.row(align=True)
        row.operator('view3d.curve_switch_direction', text="switch directon")