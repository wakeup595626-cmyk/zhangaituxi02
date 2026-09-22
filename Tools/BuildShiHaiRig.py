import bpy
import math
import os
import sys
from mathutils import Vector


def cli_args():
    if "--" not in sys.argv:
        raise RuntimeError("Expected source, donor, and output paths after --")
    args = sys.argv[sys.argv.index("--") + 1:]
    if len(args) != 3:
        raise RuntimeError("Usage: BuildShiHaiRig.py -- <shihai.fbx> <mixamo_tpose.fbx> <output.fbx>")
    return args


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for datablocks in (bpy.data.meshes, bpy.data.armatures, bpy.data.materials, bpy.data.actions):
        for datablock in list(datablocks):
            if datablock.users == 0:
                datablocks.remove(datablock)


def select_only(objects, active=None):
    bpy.ops.object.select_all(action="DESELECT")
    for obj in objects:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = active or objects[-1]


def join_meshes(meshes, name):
    select_only(meshes, meshes[0])
    if len(meshes) > 1:
        bpy.ops.object.join()
    mesh = bpy.context.view_layer.objects.active
    mesh.name = name
    mesh.data.name = f"{name}_Mesh"
    return mesh


def world_bbox(obj):
    points = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
    minimum = [min(point[index] for point in points) for index in range(3)]
    maximum = [max(point[index] for point in points) for index in range(3)]
    return minimum, maximum


def align_mesh_to_donor(mesh, donor_mesh):
    source_min, source_max = world_bbox(mesh)
    target_min, target_max = world_bbox(donor_mesh)
    source_height = max(source_max[2] - source_min[2], 0.001)
    target_height = max(target_max[2] - target_min[2], 0.001)
    uniform_scale = target_height / source_height
    mesh.scale = tuple(value * uniform_scale for value in mesh.scale)
    bpy.context.view_layer.update()

    source_min, source_max = world_bbox(mesh)
    source_center = [(source_min[index] + source_max[index]) * 0.5 for index in range(3)]
    target_center = [(target_min[index] + target_max[index]) * 0.5 for index in range(3)]
    mesh.location = tuple(mesh.location[index] + target_center[index] - source_center[index] for index in range(3))
    bpy.context.view_layer.update()


def find_bone(armature, simple_name):
    for bone in armature.pose.bones:
        if bone.name == simple_name or bone.name.endswith(":" + simple_name):
            return bone
    raise RuntimeError(f"Required bone not found: {simple_name}")


def set_pose(frame, armature, values):
    targets = ["LeftArm", "LeftForeArm", "LeftHand", "RightArm", "RightForeArm", "RightHand", "Head", "Spine", "Spine1"]
    for name in targets:
        bone = find_bone(armature, name)
        bone.rotation_mode = "XYZ"
        bone.rotation_euler = values.get(name, (0.0, 0.0, 0.0))
        bone.keyframe_insert(data_path="rotation_euler", frame=frame, group=bone.name)


def build_animation(armature):
    action = bpy.data.actions.new("ShiHai_ScratchLookSalute")
    if armature.animation_data is None:
        armature.animation_data_create()
    if bpy.app.version >= (5, 0, 0):
        # Blender 5.x actions are layered.  Creating the slot, layer, and
        # keyframe strip explicitly is required before inserting Pose keys.
        slot = action.slots.new("OBJECT", armature.name)
        layer = action.layers.new("Base Layer")
        layer.strips.new(type="KEYFRAME")
        armature.animation_data.action = action
        armature.animation_data.action_slot = slot
    else:
        # Blender 4.x uses legacy actions, which the UE-compatible FBX exporter
        # serializes directly.
        armature.animation_data.action = action

    # 60 fps: left hand scratches the head for three seconds, then the character
    # looks left/right, salutes with the right hand, and settles into attention.
    neutral = {}
    scratch = {
        "LeftArm": (0.25, -0.85, 1.05),
        "LeftForeArm": (0.20, 0.30, 1.30),
        "LeftHand": (0.15, -0.20, 0.40),
    }
    look_left = {"Head": (0.0, 0.0, 0.55)}
    look_right = {"Head": (0.0, 0.0, -0.55)}
    salute = {
        "RightArm": (0.20, 0.65, -1.15),
        "RightForeArm": (0.15, 0.10, -1.45),
        "RightHand": (0.10, 0.15, -0.30),
        "Spine": (0.0, 0.0, 0.04),
    }

    for frame, pose in [
        (1, neutral),
        (30, scratch),
        (210, scratch),
        (240, neutral),
        (270, look_left),
        (300, look_right),
        (330, neutral),
        (360, salute),
        (480, salute),
        (510, neutral),
        (570, neutral),
    ]:
        set_pose(frame, armature, pose)

    action.frame_start = 1
    action.frame_end = 570
    return action


def main():
    shihai_path, donor_path, output_path = cli_args()
    if not os.path.isfile(shihai_path) or not os.path.isfile(donor_path):
        raise RuntimeError("One or more FBX source files do not exist")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    clear_scene()
    bpy.ops.import_scene.fbx(filepath=shihai_path, use_anim=False)
    shi_meshes = [obj for obj in bpy.context.scene.objects if obj.type == "MESH"]
    if not shi_meshes:
        raise RuntimeError("ShiHai FBX did not import a mesh")
    shihai_mesh = join_meshes(shi_meshes, "ShiHai_Rigged")

    bpy.ops.import_scene.fbx(filepath=donor_path, use_anim=False)
    armatures = [obj for obj in bpy.context.scene.objects if obj.type == "ARMATURE"]
    if not armatures:
        raise RuntimeError("Mixamo donor FBX did not import an armature")
    armature = max(armatures, key=lambda obj: len(obj.data.bones))
    armature.name = "ShiHai_Armature"
    armature.data.name = "ShiHai_Skeleton"

    donor_meshes = [obj for obj in bpy.context.scene.objects if obj.type == "MESH" and obj != shihai_mesh]
    if not donor_meshes:
        raise RuntimeError("Mixamo donor FBX did not import a mesh for alignment")
    donor_mesh = join_meshes(donor_meshes, "_DonorAlignment")
    align_mesh_to_donor(shihai_mesh, donor_mesh)

    bpy.data.objects.remove(donor_mesh, do_unlink=True)
    select_only([shihai_mesh, armature], armature)
    try:
        bpy.ops.object.parent_set(type="ARMATURE_AUTO")
    except RuntimeError as error:
        raise RuntimeError(f"Automatic bone weighting failed: {error}")

    if not shihai_mesh.vertex_groups:
        raise RuntimeError("Automatic bone weighting produced no vertex groups")

    action = build_animation(armature)
    use_nla_export = bpy.app.version >= (5, 0, 0)
    if use_nla_export:
        # The Blender 5 exporter only serializes a layered action reliably when
        # it is present in an NLA strip.
        track = armature.animation_data.nla_tracks.new()
        track.name = "ShiHai_ActionTrack"
        strip = track.strips.new("ShiHai_ScratchLookSalute", 1, action)
        strip.action_frame_start = 1
        strip.action_frame_end = 570
        strip.frame_end = 570
        armature.animation_data.action = None
    action_empty = action.is_empty if hasattr(action, "is_empty") else len(action.fcurves) == 0
    curve_range = action.curve_frame_range if hasattr(action, "curve_frame_range") else action.frame_range
    print("ACTION_DEBUG", action_empty, tuple(action.frame_range), tuple(curve_range))
    for frame in (30, 270, 360):
        bpy.context.scene.frame_set(frame)
        left_arm = find_bone(armature, "LeftArm")
        right_arm = find_bone(armature, "RightArm")
        head = find_bone(armature, "Head")
        print("POSE_DEBUG", frame, tuple(left_arm.rotation_euler), tuple(right_arm.rotation_euler), tuple(head.rotation_euler))
    bpy.context.scene.render.fps = 60
    bpy.context.scene.frame_start = 1
    bpy.context.scene.frame_end = 570

    select_only([shihai_mesh, armature], armature)
    bpy.ops.export_scene.fbx(
        filepath=output_path,
        use_selection=True,
        add_leaf_bones=False,
        use_armature_deform_only=True,
        bake_anim=True,
        bake_anim_use_all_actions=not use_nla_export,
        bake_anim_use_nla_strips=use_nla_export,
        bake_anim_use_all_bones=True,
        bake_anim_force_startend_keying=True,
        bake_anim_step=1.0,
        bake_anim_simplify_factor=0.0,
        path_mode="AUTO",
    )
    print(f"EXPORTED: {output_path}")


if __name__ == "__main__":
    main()
