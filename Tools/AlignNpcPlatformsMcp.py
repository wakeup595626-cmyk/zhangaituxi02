import json
import sys

sys.path.insert(0, "Tools")
import ConfigureLiveYanLiMcp as mcp


SCENE = "editor_toolset.toolsets.scene.SceneTools"
ACTOR = "editor_toolset.toolsets.actor.ActorTools"
OBJECT = "editor_toolset.toolsets.object.ObjectTools"
ASSET = "editor_toolset.toolsets.asset.AssetTools"


def call(session_id, request_id, toolset, tool, arguments):
    return mcp.nested_call(session_id, request_id, toolset, tool, arguments)


def bounds(session_id, request_id, actor):
    return call(session_id, request_id, ACTOR, "get_actor_bounds", {"actor": actor})[
        "returnValue"
    ]


def transform(session_id, request_id, actor):
    return call(
        session_id,
        request_id,
        ACTOR,
        "get_actor_transform",
        {"actor": actor, "worldspace": True},
    )["returnValue"]


def align_actor_to_platform(session_id, request_id, actor, platform):
    platform_bounds = bounds(session_id, request_id, platform)
    platform_x = (platform_bounds["min"]["x"] + platform_bounds["max"]["x"]) / 2
    platform_y = (platform_bounds["min"]["y"] + platform_bounds["max"]["y"]) / 2
    platform_top = platform_bounds["max"]["z"]
    xform = transform(session_id, request_id + 1, actor)
    xform["location"] = {"x": platform_x, "y": platform_y, "z": platform_top + 100.0}
    call(
        session_id,
        request_id + 2,
        ACTOR,
        "set_actor_transform",
        {"actor": actor, "xform": xform, "worldspace": True},
    )
    actor_bounds = bounds(session_id, request_id + 3, actor)
    xform["location"]["z"] += platform_top - actor_bounds["min"]["z"]
    call(
        session_id,
        request_id + 4,
        ACTOR,
        "set_actor_transform",
        {"actor": actor, "xform": xform, "worldspace": True},
    )
    return bounds(session_id, request_id + 5, actor)


def main():
    mcp.print = lambda *args, **kwargs: None
    session_id = mcp.initialize()
    request_id = 2

    plaque = {
        "refPath": "/Game/MyStuff/MainLevel.MainLevel:PersistentLevel.StaticMeshActor_28"
    }
    plaque_xform = transform(session_id, request_id, plaque)
    request_id += 1
    new_platform_xform = {
        "location": {
            "x": plaque_xform["location"]["x"] + 2.0,
            "y": plaque_xform["location"]["y"],
            "z": plaque_xform["location"]["z"],
        },
        "rotation": {"pitch": 0.0, "yaw": 0.0, "roll": 0.0},
        "scale": {"x": 2.0, "y": 2.0, "z": 2.0},
    }
    existing = call(
        session_id,
        request_id,
        SCENE,
        "find_actors",
        {"name": "NPC_ArcMid_Platform_GuoShu", "tag": "", "collision_channels": []},
    )["returnValue"]
    request_id += 1
    if existing:
        fruit_platform = existing[0]
    else:
        fruit_platform = call(
            session_id,
            request_id,
            SCENE,
            "add_to_scene_from_asset",
            {
                "asset_path": "/Engine/BasicShapes/Cube",
                "name": "NPC_ArcMid_Platform_05",
                "xform": new_platform_xform,
                "snap_to_ground": False,
            },
        )["returnValue"]
        request_id += 1
        call(
            session_id,
            request_id,
            ACTOR,
            "set_label",
            {"actor": fruit_platform, "label": "NPC_ArcMid_Platform_GuoShu"},
        )
        request_id += 1
        call(
            session_id,
            request_id,
            SCENE,
            "set_actor_folder",
            {"actor": fruit_platform, "folder_path": "NPC/Platforms"},
        )
        request_id += 1
        component = call(
            session_id,
            request_id,
            ACTOR,
            "get_components",
            {"actor": fruit_platform},
        )["returnValue"][0]
        request_id += 1
        call(
            session_id,
            request_id,
            OBJECT,
            "set_properties",
            {
                "instance": component,
                "values": json.dumps(
                    {
                        "overrideMaterials": [
                            {
                                "refPath": "/Engine/EngineMaterials/WorldGridMaterial.WorldGridMaterial"
                            }
                        ]
                    }
                ),
            },
        )
        request_id += 1

    assignments = [
        (
            "GuoShu",
            {"refPath": "/Game/MyStuff/MainLevel.MainLevel:PersistentLevel.StaticMeshActor_1"},
            fruit_platform,
        ),
        (
            "OldLi",
            {"refPath": "/Game/MyStuff/MainLevel.MainLevel:PersistentLevel.SkeletalMeshActor_4"},
            {"refPath": "/Game/MyStuff/MainLevel.MainLevel:PersistentLevel.StaticMeshActor_20"},
        ),
        (
            "XuBuZhang",
            {"refPath": "/Game/MyStuff/MainLevel.MainLevel:PersistentLevel.SkeletalMeshActor_5"},
            {"refPath": "/Game/MyStuff/MainLevel.MainLevel:PersistentLevel.StaticMeshActor_21"},
        ),
        (
            "FengLaoBan",
            {"refPath": "/Game/MyStuff/MainLevel.MainLevel:PersistentLevel.SkeletalMeshActor_6"},
            {"refPath": "/Game/MyStuff/MainLevel.MainLevel:PersistentLevel.StaticMeshActor_22"},
        ),
    ]
    result = {}
    for name, actor, platform in assignments:
        result[name] = align_actor_to_platform(session_id, request_id, actor, platform)
        request_id += 10

    call(
        session_id,
        request_id,
        ASSET,
        "save_assets",
        {"asset_paths": ["/Game/MyStuff/MainLevel"]},
    )
    result["GuoShuPlatform"] = bounds(session_id, request_id + 1, fruit_platform)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
