import http.client
import json


HOST = "127.0.0.1"
PORT = 8000
PATH = "/mcp"
PROTOCOL_VERSION = "2025-11-25"
ACTOR_TOOLSET = "editor_toolset.toolsets.actor.ActorTools"
ASSET_TOOLSET = "editor_toolset.toolsets.asset.AssetTools"
OBJECT_TOOLSET = "editor_toolset.toolsets.object.ObjectTools"
SCENE_TOOLSET = "editor_toolset.toolsets.scene.SceneTools"

MESH_REF = {"refPath": "/Game/YanLi/Mesh/SK_YanLi.SK_YanLi"}
ANIMATION_REF = {"refPath": "/Game/YanLi/Animation/YanLi_ChickenDance_Anim.YanLi_ChickenDance_Anim"}
ASSETS_TO_SAVE = [
    "/Game/YanLi/Mesh/SK_YanLi_Skeleton",
    "/Game/YanLi/Mesh/SK_YanLi",
    "/Game/YanLi/Animation/YanLi_ChickenDance_Anim",
    "/Game/YanLi/Mesh/M_YanLi",
    "/Game/YanLi/Mesh/T_YanLi_BaseColor",
    "/Game/MyStuff/MainLevel",
]


def post(payload, session_id=None):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "Mcp-Protocol-Version": PROTOCOL_VERSION,
    }
    if session_id:
        headers["Mcp-Session-Id"] = session_id
    connection = http.client.HTTPConnection(HOST, PORT, timeout=30)
    try:
        connection.request("POST", PATH, body=json.dumps(payload), headers=headers)
        response = connection.getresponse()
        return response.status, dict(response.getheaders()), response.read().decode("utf-8")
    finally:
        connection.close()


def initialize():
    status, headers, body = post({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": {},
            "clientInfo": {"name": "codex-live-unreal", "version": "1.0"},
        },
    })
    if status != 200:
        raise RuntimeError("initialize failed: {} {}".format(status, body))
    session_id = headers.get("Mcp-Session-Id") or headers.get("mcp-session-id")
    if not session_id:
        raise RuntimeError("initialize returned no session id")
    status, _, body = post(
        {"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}},
        session_id,
    )
    if status not in (200, 202):
        raise RuntimeError("initialized notification failed: {} {}".format(status, body))
    return session_id


def nested_call(session_id, request_id, toolset_name, tool_name, arguments):
    payload = {
        "jsonrpc": "2.0",
        "id": request_id,
        "method": "tools/call",
        "params": {
            "name": "call_tool",
            "arguments": {
                "toolset_name": toolset_name,
                "tool_name": tool_name,
                "arguments": arguments,
            },
        },
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "Mcp-Protocol-Version": PROTOCOL_VERSION,
        "Mcp-Session-Id": session_id,
    }
    connection = http.client.HTTPConnection(HOST, PORT, timeout=30)
    try:
        connection.request("POST", PATH, body=json.dumps(payload), headers=headers)
        response = connection.getresponse()
        if response.status != 200:
            raise RuntimeError("{} failed: {} {}".format(
                tool_name, response.status, response.read().decode("utf-8")
            ))
        body = ""
        result = None
        while True:
            line = response.readline().decode("utf-8")
            if not line:
                break
            body += line
            if line.startswith("data: "):
                candidate = json.loads(line[6:])
                if candidate.get("id") == request_id:
                    result = candidate
                    break
    finally:
        connection.close()
    if not result:
        raise RuntimeError("{} returned no final MCP result: {}".format(tool_name, body))
    content = result.get("result", {}).get("content", [])
    text = "\n".join(item.get("text", "") for item in content if item.get("type") == "text")
    print("CODEX_LIVE_CONFIG_{}={}".format(tool_name.upper(), text))
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return text


def main():
    session_id = initialize()
    actors = nested_call(
        session_id,
        2,
        SCENE_TOOLSET,
        "find_actors",
        {"name": "YanLi", "tag": "", "collision_channels": []},
    )
    candidates = actors.get("returnValue", []) if isinstance(actors, dict) else []
    if len(candidates) != 1:
        raise RuntimeError("Expected one YanLi actor, got {}".format(candidates))
    actor = candidates[0]

    components = nested_call(session_id, 3, ACTOR_TOOLSET, "get_components", {"actor": actor})
    component_refs = components.get("returnValue", []) if isinstance(components, dict) else []
    if len(component_refs) != 1:
        raise RuntimeError("Expected one YanLi skeletal component, got {}".format(component_refs))
    component = component_refs[0]

    nested_call(
        session_id,
        4,
        OBJECT_TOOLSET,
        "set_properties",
        {
            "instance": component,
            "values": json.dumps({
                "skeletalMeshAsset": MESH_REF,
                "animationMode": "AnimationSingleNode",
                "animationData": {
                    "animToPlay": ANIMATION_REF,
                    "bSavedLooping": True,
                    "bSavedPlaying": True,
                    "savedPosition": 0.0,
                    "savedPlayRate": 1.0,
                },
                "bUpdateAnimationInEditor": True,
            }),
        },
    )
    nested_call(
        session_id,
        5,
        ACTOR_TOOLSET,
        "set_actor_transform",
        {
            "actor": actor,
            "xform": {
                "location": {"x": 16573.0, "y": 4950.0, "z": 1153.725073},
                "rotation": {"pitch": 0.0, "yaw": 90.0, "roll": 0.0},
                "scale": {"x": 100.0, "y": 100.0, "z": 100.0},
            },
            "worldspace": True,
        },
    )
    nested_call(
        session_id,
        6,
        SCENE_TOOLSET,
        "set_actor_folder",
        {"actor": actor, "folder_path": "NPC/YanLi"},
    )
    nested_call(
        session_id,
        7,
        ASSET_TOOLSET,
        "save_assets",
        {"asset_paths": ASSETS_TO_SAVE},
    )
    nested_call(session_id, 8, SCENE_TOOLSET, "save_actor", {"actor": actor})
    properties = nested_call(
        session_id,
        9,
        OBJECT_TOOLSET,
        "get_properties",
        {
            "instance": component,
            "properties": [
                "skeletalMeshAsset",
                "animationData",
                "animationMode",
                "bUpdateAnimationInEditor",
            ],
        },
    )
    bounds = nested_call(session_id, 10, ACTOR_TOOLSET, "get_actor_bounds", {"actor": actor})
    print("CODEX_LIVE_CONFIG_SUCCESS actor={} properties={} bounds={}".format(
        actor, properties, bounds
    ))


if __name__ == "__main__":
    main()
