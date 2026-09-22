import os
import unreal


MAP_PATH = "/Game/MyStuff/MainLevel"
MESH_DIRECTORY = "/Game/YanLi/Mesh"
ANIMATION_DIRECTORY = "/Game/YanLi/Animation"
MESH_PATH = MESH_DIRECTORY + "/SK_YanLi"
ANIMATION_PATH = ANIMATION_DIRECTORY + "/YanLi_ChickenDance_Anim"
TEXTURE_PATH = MESH_DIRECTORY + "/T_YanLi_BaseColor"
MATERIAL_PATH = MESH_DIRECTORY + "/M_YanLi"

SOURCE_ROOT = r"D:\Users\25653\Desktop\桌面文件夹\UE动画文件夹\艳丽"
MESH_FBX = os.path.join(
    SOURCE_ROOT,
    "Mixamo动作下载（艳丽）",
    "Meshy_AI_Cat_Eared_Daydreamer_0718031617_texture.fbx",
)
ANIMATION_FBX = os.path.join(
    SOURCE_ROOT,
    "Mixamo动作下载（艳丽）",
    "Chicken Dance.fbx",
)
BASE_COLOR_TEXTURE = os.path.join(
    SOURCE_ROOT,
    "艳丽模型",
    "Meshy_AI_Cat_Eared_Daydreamer_0718031617_texture_obj",
    "Meshy_AI_Cat_Eared_Daydreamer_0718031617_texture_obj",
    "Meshy_AI_Cat_Eared_Daydreamer_0718031617_texture.png",
)

PLATFORM_NAME = "StaticMeshActor_19"
PLATFORM_LABEL = "NPC_ArcMid_Platform_04"
ACTOR_LABEL = "YanLi"
ACTOR_FOLDER = "NPC/YanLi"
ACTOR_YAW = 90.0


def log(message):
    unreal.log("CODEX_YANLI {}".format(message))


def load_asset(path, expected_type=None):
    asset = unreal.EditorAssetLibrary.load_asset(path)
    if not asset:
        return None
    if expected_type and not isinstance(asset, expected_type):
        raise RuntimeError(
            "Asset {} has type {}, expected {}".format(
                path, asset.get_class().get_name(), expected_type.__name__
            )
        )
    return asset


def try_load_asset(path, expected_type=None):
    try:
        return load_asset(path, expected_type)
    except Exception as error:
        log("ASSET_LOAD_WARNING path={} error={}".format(path, error))
        return None


def import_task(filename, destination_path, destination_name, options, replace_existing=False):
    task = unreal.AssetImportTask()
    properties = {
        "filename": filename,
        "destination_path": destination_path,
        "destination_name": destination_name,
        "automated": True,
        "async_": False,
        "replace_existing": replace_existing,
        "replace_existing_settings": replace_existing,
    }
    if options:
        properties["options"] = options
    task.set_editor_properties(properties)
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
    imported_paths = list(task.get_editor_property("imported_object_paths"))
    log("IMPORT_RESULT source={} imported={}".format(filename, imported_paths))
    return imported_paths


def import_mesh_if_needed():
    mesh = try_load_asset(MESH_PATH, unreal.SkeletalMesh)
    if mesh and mesh.get_editor_property("skeleton"):
        log("MESH_REUSED path={}".format(mesh.get_path_name()))
        return mesh

    replace_existing = unreal.EditorAssetLibrary.does_asset_exist(MESH_PATH)
    if replace_existing:
        log("MESH_REPAIR_REIMPORT path={}".format(MESH_PATH))

    if not os.path.isfile(MESH_FBX):
        raise RuntimeError("Missing YanLi mesh FBX: {}".format(MESH_FBX))

    options = unreal.FbxImportUI()
    options.set_editor_properties(
        {
            "automated_import_should_detect_type": False,
            "original_import_type": unreal.FBXImportType.FBXIT_SKELETAL_MESH,
            "mesh_type_to_import": unreal.FBXImportType.FBXIT_SKELETAL_MESH,
            "import_mesh": True,
            "import_as_skeletal": True,
            "import_animations": False,
            "import_materials": True,
            "import_textures": True,
            "create_physics_asset": True,
            "override_full_name": True,
        }
    )
    options.skeletal_mesh_import_data.set_editor_properties(
        {
            "import_mesh_lods": False,
            "import_uniform_scale": 1.0,
        }
    )
    import_task(MESH_FBX, MESH_DIRECTORY, "SK_YanLi", options, replace_existing)
    mesh = load_asset(MESH_PATH, unreal.SkeletalMesh)
    if not mesh:
        raise RuntimeError("YanLi skeletal mesh was not created at {}".format(MESH_PATH))
    log("MESH_IMPORTED path={}".format(mesh.get_path_name()))
    return mesh


def save_skeleton(mesh):
    skeleton = mesh.get_editor_property("skeleton")
    if not skeleton:
        raise RuntimeError("YanLi skeletal mesh has no skeleton after import")
    skeleton_path = skeleton.get_path_name()
    if not unreal.EditorAssetLibrary.save_asset(skeleton_path, only_if_is_dirty=False):
        raise RuntimeError("Could not save YanLi skeleton: {}".format(skeleton_path))
    log("SKELETON_SAVED {}".format(skeleton_path))
    return skeleton


def import_animation_if_needed(mesh):
    animation = try_load_asset(ANIMATION_PATH, unreal.AnimSequence)
    skeleton = mesh.get_editor_property("skeleton")
    if animation and animation.get_editor_property("skeleton") == skeleton:
        log("ANIMATION_REUSED path={}".format(animation.get_path_name()))
        return animation

    replace_existing = unreal.EditorAssetLibrary.does_asset_exist(ANIMATION_PATH)
    if replace_existing:
        log("ANIMATION_REPAIR_REIMPORT path={}".format(ANIMATION_PATH))

    if not os.path.isfile(ANIMATION_FBX):
        raise RuntimeError("Missing YanLi animation FBX: {}".format(ANIMATION_FBX))

    if not skeleton:
        raise RuntimeError("YanLi skeletal mesh has no skeleton")

    options = unreal.FbxImportUI()
    options.set_editor_properties(
        {
            "automated_import_should_detect_type": False,
            "original_import_type": unreal.FBXImportType.FBXIT_ANIMATION,
            "mesh_type_to_import": unreal.FBXImportType.FBXIT_ANIMATION,
            "import_mesh": False,
            "import_as_skeletal": True,
            "import_animations": True,
            "import_materials": False,
            "import_textures": False,
            "skeleton": skeleton,
            "override_full_name": True,
        }
    )
    options.anim_sequence_import_data.set_editor_properties(
        {
            "animation_length": unreal.FBXAnimationLengthImportType.FBXALIT_EXPORTED_TIME,
            "import_uniform_scale": 1.0,
        }
    )
    import_task(
        ANIMATION_FBX,
        ANIMATION_DIRECTORY,
        "YanLi_ChickenDance_Anim",
        options,
        replace_existing,
    )
    animation = load_asset(ANIMATION_PATH, unreal.AnimSequence)
    if not animation:
        raise RuntimeError("YanLi animation was not created at {}".format(ANIMATION_PATH))
    log("ANIMATION_IMPORTED path={} length={:.3f}".format(
        animation.get_path_name(), animation.get_editor_property("sequence_length")
    ))
    return animation


def material_paths(mesh):
    materials = list(mesh.get_editor_property("materials"))
    paths = []
    for slot in materials:
        material = slot.get_editor_property("material_interface")
        paths.append(material.get_path_name() if material else "None")
    return materials, paths


def describe_materials(mesh):
    materials, paths = material_paths(mesh)
    log("MESH_MATERIALS slots={} paths={}".format(len(materials), paths))
    return any(path not in ("None", "/Engine/EngineMaterials/WorldGridMaterial.WorldGridMaterial") for path in paths)


def import_base_color_if_needed():
    texture = load_asset(TEXTURE_PATH, unreal.Texture2D)
    if texture:
        log("TEXTURE_REUSED path={}".format(texture.get_path_name()))
        return texture
    if not os.path.isfile(BASE_COLOR_TEXTURE):
        raise RuntimeError("Missing YanLi base-color texture: {}".format(BASE_COLOR_TEXTURE))
    import_task(BASE_COLOR_TEXTURE, MESH_DIRECTORY, "T_YanLi_BaseColor", None)
    texture = load_asset(TEXTURE_PATH, unreal.Texture2D)
    if not texture:
        raise RuntimeError("YanLi base-color texture was not created at {}".format(TEXTURE_PATH))
    log("TEXTURE_IMPORTED path={}".format(texture.get_path_name()))
    return texture


def ensure_yanli_material(mesh):
    existing = load_asset(MATERIAL_PATH, unreal.Material)
    if existing:
        material = existing
        log("MATERIAL_REUSED path={}".format(material.get_path_name()))
    else:
        texture = import_base_color_if_needed()
        material = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
            "M_YanLi",
            MESH_DIRECTORY,
            unreal.Material,
            unreal.MaterialFactoryNew(),
        )
        if not material:
            raise RuntimeError("Could not create YanLi material")
        texture_sample = unreal.MaterialEditingLibrary.create_material_expression(
            material, unreal.MaterialExpressionTextureSample, -320, 0
        )
        texture_sample.set_editor_property("texture", texture)
        roughness = unreal.MaterialEditingLibrary.create_material_expression(
            material, unreal.MaterialExpressionConstant, -320, 180
        )
        roughness.set_editor_property("r", 0.55)
        unreal.MaterialEditingLibrary.connect_material_property(
            texture_sample, "RGB", unreal.MaterialProperty.MP_BASE_COLOR
        )
        unreal.MaterialEditingLibrary.connect_material_property(
            roughness, "", unreal.MaterialProperty.MP_ROUGHNESS
        )
        unreal.MaterialEditingLibrary.recompile_material(material)
        log("MATERIAL_CREATED path={} texture={}".format(
            material.get_path_name(), texture.get_path_name()
        ))

    materials, _ = material_paths(mesh)
    if not materials:
        raise RuntimeError("YanLi mesh has no material slot to assign")
    materials[0].set_editor_property("material_interface", material)
    mesh.set_editor_property("materials", materials)
    mesh.modify()
    return material


def find_platform(actors):
    for actor in actors:
        if actor.get_name() == PLATFORM_NAME:
            return actor
    for actor in actors:
        if actor.get_actor_label() == PLATFORM_LABEL:
            return actor
    raise RuntimeError("YanLi platform not found: {} / {}".format(PLATFORM_NAME, PLATFORM_LABEL))


def find_yanli_actor(actors):
    for actor in actors:
        if actor.get_actor_label() == ACTOR_LABEL:
            if isinstance(actor, unreal.SkeletalMeshActor):
                return actor
            raise RuntimeError("Existing actor labeled YanLi is not a SkeletalMeshActor")
    return None


def configure_actor(mesh, animation):
    world = unreal.EditorLoadingAndSavingUtils.load_map(MAP_PATH)
    if not world:
        raise RuntimeError("Could not load map: {}".format(MAP_PATH))

    actors = unreal.EditorLevelLibrary.get_all_level_actors()
    platform = find_platform(actors)
    platform_location = platform.get_actor_location()
    platform_origin, platform_extent = platform.get_actor_bounds(False)
    platform_top = platform_origin.z + platform_extent.z

    actor = find_yanli_actor(actors)
    created = actor is None
    if created:
        actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
            unreal.SkeletalMeshActor,
            unreal.Vector(platform_location.x, platform_location.y, platform_top + 100.0),
            unreal.Rotator(0.0, 0.0, ACTOR_YAW),
        )
        if not actor:
            raise RuntimeError("Could not spawn YanLi actor")
        actor.set_actor_label(ACTOR_LABEL)
    else:
        actor.set_actor_rotation(unreal.Rotator(0.0, 0.0, ACTOR_YAW), False)
        actor.set_actor_location(
            unreal.Vector(platform_location.x, platform_location.y, platform_top + 100.0),
            False,
            False,
        )

    try:
        actor.set_folder_path(ACTOR_FOLDER)
    except Exception as error:
        log("FOLDER_WARNING {}".format(error))

    components = actor.get_components_by_class(unreal.SkeletalMeshComponent)
    if not components:
        raise RuntimeError("YanLi actor does not have a SkeletalMeshComponent")
    component = components[0]
    component.set_skinned_asset_and_update(mesh)
    component.set_animation_mode(unreal.AnimationMode.ANIMATION_SINGLE_NODE)
    component.set_animation(animation)
    component.set_play_rate(1.0)
    component.play(True)
    component.set_update_animation_in_editor(True)

    # Snap the imported character's visual lower bound to the top of the existing platform.
    actor_origin, actor_extent = actor.get_actor_bounds(False)
    bottom_z = actor_origin.z - actor_extent.z
    actor_location = actor.get_actor_location()
    actor.set_actor_location(
        unreal.Vector(actor_location.x, actor_location.y, actor_location.z + (platform_top - bottom_z)),
        False,
        False,
    )
    actor.modify()

    actor_origin, actor_extent = actor.get_actor_bounds(False)
    bottom_z = actor_origin.z - actor_extent.z
    location = actor.get_actor_location()
    log(
        "ACTOR_CONFIGURED created={} name={} loc=({:.2f},{:.2f},{:.2f}) yaw={:.2f} platform_top={:.2f} bottom={:.2f}".format(
            created,
            actor.get_name(),
            location.x,
            location.y,
            location.z,
            actor.get_actor_rotation().yaw,
            platform_top,
            bottom_z,
        )
    )
    return world, actor


def save_results(world, assets):
    for asset in assets:
        path = asset.get_path_name()
        if not unreal.EditorAssetLibrary.save_asset(path, only_if_is_dirty=False):
            raise RuntimeError("Could not save asset: {}".format(path))
        log("ASSET_SAVED {}".format(path))

    if not unreal.EditorLoadingAndSavingUtils.save_map(world, MAP_PATH):
        raise RuntimeError("Could not save map: {}".format(MAP_PATH))
    log("MAP_SAVED {}".format(MAP_PATH))


def main():
    log("IMPORT_BEGIN")
    mesh = import_mesh_if_needed()
    skeleton = save_skeleton(mesh)
    if not describe_materials(mesh):
        material = ensure_yanli_material(mesh)
        describe_materials(mesh)
    else:
        material = None
    animation = import_animation_if_needed(mesh)
    world, actor = configure_actor(mesh, animation)
    assets_to_save = [skeleton, mesh, animation]
    if material:
        assets_to_save.append(material)
        texture = load_asset(TEXTURE_PATH, unreal.Texture2D)
        if texture:
            assets_to_save.append(texture)
    save_results(world, assets_to_save)
    log("IMPORT_SUCCESS actor={} mesh={} animation={}".format(
        actor.get_name(), mesh.get_path_name(), animation.get_path_name()
    ))


if __name__ == "__main__":
    main()
