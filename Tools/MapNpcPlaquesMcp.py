import json
import sys

sys.path.insert(0, "Tools")
import ConfigureLiveYanLiMcp as mcp


def main():
    mcp.print = lambda *args, **kwargs: None
    session_id = mcp.initialize()
    actors = mcp.nested_call(
        session_id,
        2,
        "editor_toolset.toolsets.scene.SceneTools",
        "find_actors",
        {"name": "NPC", "tag": "", "collision_channels": []},
    )["returnValue"]

    records = []
    for request_id, actor in enumerate(actors, start=3):
        label = mcp.nested_call(
            session_id,
            request_id,
            "editor_toolset.toolsets.actor.ActorTools",
            "get_label",
            {"actor": actor},
        )["returnValue"]
        transform = mcp.nested_call(
            session_id,
            request_id + 100,
            "editor_toolset.toolsets.actor.ActorTools",
            "get_actor_transform",
            {"actor": actor, "worldspace": True},
        )["returnValue"]
        bounds = mcp.nested_call(
            session_id,
            request_id + 200,
            "editor_toolset.toolsets.actor.ActorTools",
            "get_actor_bounds",
            {"actor": actor},
        )["returnValue"]
        records.append(
            {
                "actor": actor["refPath"],
                "label": label,
                "location": transform["location"],
                "bounds": bounds,
            }
        )
    print(json.dumps(records, ensure_ascii=False))


if __name__ == "__main__":
    main()
