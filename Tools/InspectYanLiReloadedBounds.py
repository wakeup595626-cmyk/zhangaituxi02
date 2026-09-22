import unreal


MAP_PATH = "/Game/MyStuff/MainLevel"


def main():
    world = unreal.EditorLoadingAndSavingUtils.load_map(MAP_PATH)
    if not world:
        raise RuntimeError("Could not load map")
    actors = unreal.EditorLevelLibrary.get_all_level_actors()
    yanli = next(actor for actor in actors if actor.get_actor_label() == "YanLi")
    platform = next(actor for actor in actors if actor.get_name() == "StaticMeshActor_19")
    component = yanli.get_components_by_class(unreal.SkeletalMeshComponent)[0]
    actor_origin, actor_extent = yanli.get_actor_bounds(False)
    platform_origin, platform_extent = platform.get_actor_bounds(False)
    location = yanli.get_actor_location()
    scale = yanli.get_actor_scale3d()
    relative_scale = component.get_editor_property("relative_scale3d")
    unreal.log(
        "CODEX_YANLI_RELOAD actor_loc=({:.6f},{:.6f},{:.6f}) actor_scale=({:.6f},{:.6f},{:.6f}) component_scale=({:.6f},{:.6f},{:.6f}) bounds_min=({:.6f},{:.6f},{:.6f}) bounds_max=({:.6f},{:.6f},{:.6f}) platform_top={:.6f}".format(
            location.x,
            location.y,
            location.z,
            scale.x,
            scale.y,
            scale.z,
            relative_scale.x,
            relative_scale.y,
            relative_scale.z,
            actor_origin.x - actor_extent.x,
            actor_origin.y - actor_extent.y,
            actor_origin.z - actor_extent.z,
            actor_origin.x + actor_extent.x,
            actor_origin.y + actor_extent.y,
            actor_origin.z + actor_extent.z,
            platform_origin.z + platform_extent.z,
        )
    )


if __name__ == "__main__":
    main()
