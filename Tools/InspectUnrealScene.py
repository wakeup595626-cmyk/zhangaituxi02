import unreal


MAP_PATH = "/Game/MyStuff/MainLevel"
TARGET_NAMES = {
    "StaticMeshActor_16",
    "StaticMeshActor_19",
    "ShiHai",
    "YanLi",
    "SkeletalMeshActor_2",
}


def asset_path(asset):
    return asset.get_path_name() if asset else "None"


def main():
    unreal.log("CODEX_SCENE_INSPECT_BEGIN")
    world = unreal.EditorLoadingAndSavingUtils.load_map(MAP_PATH)
    if not world:
        raise RuntimeError("Could not load map: {}".format(MAP_PATH))

    actors = unreal.EditorLevelLibrary.get_all_level_actors()
    unreal.log("CODEX_SCENE_ACTOR_COUNT={}".format(len(actors)))
    for actor in actors:
        label = actor.get_actor_label()
        if actor.get_name() not in TARGET_NAMES and label not in TARGET_NAMES:
            continue

        location = actor.get_actor_location()
        rotation = actor.get_actor_rotation()
        try:
            folder = str(actor.get_folder_path())
        except Exception:
            folder = "<unavailable>"
        unreal.log(
            "CODEX_ACTOR name={} label={} class={} folder={} loc=({:.2f},{:.2f},{:.2f}) rot=({:.2f},{:.2f},{:.2f})".format(
                actor.get_name(),
                label,
                actor.get_class().get_name(),
                folder,
                location.x,
                location.y,
                location.z,
                rotation.roll,
                rotation.pitch,
                rotation.yaw,
            )
        )

        for component in actor.get_components_by_class(unreal.SkeletalMeshComponent):
            mesh = component.get_editor_property("skeletal_mesh")
            try:
                anim_data = component.get_editor_property("animation_data")
                animation = anim_data.get_editor_property("anim_to_play") if anim_data else None
            except Exception:
                animation = None
            unreal.log(
                "CODEX_SKEL_COMPONENT actor={} component={} mesh={} animation={} mode={}".format(
                    actor.get_name(),
                    component.get_name(),
                    asset_path(mesh),
                    asset_path(animation),
                    str(component.get_editor_property("animation_mode")),
                )
            )

    unreal.log("CODEX_SCENE_INSPECT_END")


if __name__ == "__main__":
    main()
