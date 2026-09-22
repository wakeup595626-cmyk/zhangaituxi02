import bpy
import sys


path = sys.argv[sys.argv.index("--") + 1]
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
bpy.ops.import_scene.fbx(filepath=path, use_anim=True)
armatures = [obj for obj in bpy.context.scene.objects if obj.type == "ARMATURE"]
armature = max(armatures, key=lambda obj: len(obj.data.bones))
print("ACTIONS", [(action.name, action.frame_start, action.frame_end) for action in bpy.data.actions])
print("ACTIVE", armature.animation_data.action.name if armature.animation_data and armature.animation_data.action else "None")
for frame in (1, 30, 120, 210, 270, 300, 360, 420, 510):
    bpy.context.scene.frame_set(frame)
    result = []
    for simple in ("LeftArm", "LeftForeArm", "RightArm", "RightForeArm", "Head"):
        bone = next((bone for bone in armature.pose.bones if bone.name == simple or bone.name.endswith(":" + simple)), None)
        result.append((simple, tuple(round(value, 3) for value in bone.rotation_euler)))
    print("FRAME", frame, result)
