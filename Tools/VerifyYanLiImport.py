import unreal


MAP_PATH = "/Game/MyStuff/MainLevel"
MESH_PATH = "/Game/YanLi/Mesh/SK_YanLi"
ANIMATION_PATH = "/Game/YanLi/Animation/YanLi_ChickenDance_Anim"
MATERIAL_PATH = "/Game/YanLi/Mesh/M_YanLi"
TEXTURE_PATH = "/Game/YanLi/Mesh/T_YanLi_BaseColor"
PLATFORM_NAME = "StaticMeshActor_19"
ACTOR_LABEL = "YanLi"


def log(message):
    unreal.log("CODEX_YANLI_VERIFY {}".format(message))


def require_asset(path, expected_type):
    asset = unreal.EditorAssetLibrary.load_asset(path)
    if not asset or not isinstance(asset, expected_type):
        raise RuntimeError("Missing or invalid asset: {}".format(path))
    return asset


def main():
    log("BEGIN")
    mesh = require_asset(MESH_PATH, unreal.SkeletalMesh)
    animation = require_asset(ANIMATION_PATH, unreal.AnimSequence)
    material = require_asset(MATERIAL_PATH, unreal.Material)
    texture = require_asset(TEXTURE_PATH, unreal.Texture2D)

    materials = list(mesh.get_editor_property("materials"))
    assigned = [
        slot.get_editor_property("material_interface").get_path_name()
        if slot.get_editor_property("material_interface")
        else "None"
        for slot in materials
    ]
    if material.get_path_name() not in assigned:
        raise RuntimeError("YanLi mesh does not use M_YanLi: {}".format(assigned))

    base_color_node = unreal.MaterialEditingLibrary.get_material_property_input_node(
        material, unreal.MaterialProperty.MP_BASE_COLOR
    )
    if not base_color_node or not isinstance(base_color_node, unreal.MaterialExpressionTextureSample):
        raise RuntimeError("YanLi material base color is not driven by a texture sample")
    if base_color_node.get_editor_property("texture") != texture:
        raise RuntimeError("YanLi material does not use its base-color texture")

    if mesh.get_editor_property("skeleton") != animation.get_editor_property("skeleton"):
        raise RuntimeError("YanLi animation skeleton differs from mesh skeleton")
    sequence_length = animation.get_editor_property("sequence_length")
    if sequence_length <= 0.0:
        raise RuntimeError("YanLi animation has no playable duration")

    world = unreal.EditorLoadingAndSavingUtils.load_map(MAP_PATH)
    if not world:
        raise RuntimeError("Could not load map")
    actors = unreal.EditorLevelLibrary.get_all_level_actors()
    platform = next((actor for actor in actors if actor.get_name() == PLATFORM_NAME), None)
    actor = next((actor for actor in actors if actor.get_actor_label() == ACTOR_LABEL), None)
    if not platform or not actor:
        raise RuntimeError("YanLi actor or its platform is missing")

    components = actor.get_components_by_class(unreal.SkeletalMeshComponent)
    if not components:
        raise RuntimeError("YanLi actor has no SkeletalMeshComponent")
    component = components[0]
    actor_mesh = component.get_skeletal_mesh_asset()
    animation_data = component.get_editor_property("animation_data")
    actor_animation = animation_data.get_editor_property("anim_to_play")
    data_members = [name for name in dir(animation_data) if not name.startswith("_")]
    log("ANIMATION_DATA_MEMBERS={}".format(",".join(data_members)))
    loop = None
    loop_property = None
    for candidate in ("looping", "b_looping", "saved_looping", "b_saved_looping"):
        try:
            loop = animation_data.get_editor_property(candidate)
            loop_property = candidate
            break
        except Exception:
            pass
    playing = None
    playing_property = None
    for candidate in ("playing", "b_playing", "saved_playing", "b_saved_playing"):
        try:
            playing = animation_data.get_editor_property(candidate)
            playing_property = candidate
            break
        except Exception:
            pass
    log("ACTOR_BINDINGS mesh={} animation={} expected_mesh={} expected_animation={}".format(
        actor_mesh.get_path_name() if actor_mesh else "None",
        actor_animation.get_path_name() if actor_animation else "None",
        mesh.get_path_name(),
        animation.get_path_name(),
    ))
    if actor_mesh != mesh:
        raise RuntimeError("YanLi actor is not using SK_YanLi")
    if actor_animation != animation:
        raise RuntimeError("YanLi actor is not using YanLi_ChickenDance_Anim")
    if component.get_editor_property("animation_mode") != unreal.AnimationMode.ANIMATION_SINGLE_NODE:
        raise RuntimeError("YanLi actor animation mode is not single-node")
    if loop is not True:
        raise RuntimeError("YanLi animation loop property is unavailable or false: {}".format(data_members))

    platform_origin, platform_extent = platform.get_actor_bounds(False)
    actor_origin, actor_extent = actor.get_actor_bounds(False)
    platform_top = platform_origin.z + platform_extent.z
    actor_bottom = actor_origin.z - actor_extent.z
    actor_height = actor_extent.z * 2.0
    if abs(platform_top - actor_bottom) > 2.0:
        raise RuntimeError("YanLi is not resting on the platform: top={}, bottom={}".format(platform_top, actor_bottom))
    if not 180.0 <= actor_height <= 210.0:
        raise RuntimeError("YanLi height is not proportional to the other NPCs: {}".format(actor_height))

    location = actor.get_actor_location()
    log(
        "SUCCESS actor={} loc=({:.2f},{:.2f},{:.2f}) yaw={:.2f} height={:.2f} sequence={:.3f}s loop={} playing={} material={} texture={} platform_top={:.2f} bottom={:.2f}".format(
            actor.get_name(),
            location.x,
            location.y,
            location.z,
            actor.get_actor_rotation().yaw,
            actor_height,
            sequence_length,
            "{}={}".format(loop_property, loop),
            "{}={}".format(playing_property, playing),
            material.get_path_name(),
            texture.get_path_name(),
            platform_top,
            actor_bottom,
        )
    )


if __name__ == "__main__":
    main()
