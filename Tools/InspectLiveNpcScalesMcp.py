import http.client
import json


HOST = "127.0.0.1"
PORT = 8000
PATH = "/mcp"
PROTOCOL_VERSION = "2025-11-25"
SCENE_TOOLSET = "editor_toolset.toolsets.scene.SceneTools"
ACTOR_TOOLSET = "editor_toolset.toolsets.actor.ActorTools"


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
        result = None
        body = ""
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
        raise RuntimeError("{} returned no final result: {}".format(tool_name, body))
    text = "\n".join(
        item.get("text", "")
        for item in result.get("result", {}).get("content", [])
        if item.get("type") == "text"
    )
    return json.loads(text)


def find_by_label(session_id, request_id, label):
    result = nested_call(
        session_id,
        request_id,
        SCENE_TOOLSET,
        "find_actors",
        {"name": label, "tag": "", "collision_channels": []},
    )
    return result.get("returnValue", [])


def main():
    session_id = initialize()
    labels = ["ShiHai", "JiangJun", "将军", "YanLi"]
    request_id = 2
    for label in labels:
        actors = find_by_label(session_id, request_id, label)
        request_id += 1
        for actor in actors:
            bounds = nested_call(session_id, request_id, ACTOR_TOOLSET, "get_actor_bounds", {"actor": actor})
            request_id += 1
            transform = nested_call(session_id, request_id, ACTOR_TOOLSET, "get_actor_transform", {"actor": actor})
            request_id += 1
            box = bounds["returnValue"]
            height = box["max"]["z"] - box["min"]["z"]
            print("CODEX_NPC_SCALE label={} ref={} height={:.6f} bounds={} transform={}".format(
                label, actor["refPath"], height, json.dumps(box), json.dumps(transform["returnValue"])
            ))


if __name__ == "__main__":
    main()
