import bpy
import sys

output = sys.argv[sys.argv.index("--") + 1]
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
bpy.ops.object.armature_add(enter_editmode=False)
armature = bpy.context.object
armature.name = "TestArmature"
bone = armature.pose.bones[0]
bone.rotation_mode = "XYZ"
action = bpy.data.actions.new("TestAction")
armature.animation_data_create()
armature.animation_data.action = action
for frame, angle in ((1, 0.0), (30, 1.0), (60, 0.0)):
    bone.rotation_euler = (angle, 0.0, 0.0)
    bone.keyframe_insert(data_path="rotation_euler", frame=frame)
print("TEST", len(action.fcurves), action.frame_range)
bpy.ops.object.select_all(action="DESELECT")
armature.select_set(True)
bpy.context.view_layer.objects.active = armature
bpy.ops.export_scene.fbx(filepath=output, use_selection=True, bake_anim=True, bake_anim_use_all_actions=True, bake_anim_use_nla_strips=False, bake_anim_use_all_bones=True, bake_anim_force_startend_keying=True, bake_anim_step=1.0, bake_anim_simplify_factor=0.0, add_leaf_bones=False)
