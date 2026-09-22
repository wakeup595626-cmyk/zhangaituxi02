import http.client
import json


HOST = "127.0.0.1"
PORT = 8000
PATH = "/mcp"
PROTOCOL_VERSION = "2025-11-25"


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


def json_response(body):
    if body.lstrip().startswith("event:"):
        payloads = []
        for block in body.replace("\r\n", "\n").split("\n\n"):
            lines = [line[6:] for line in block.split("\n") if line.startswith("data: ")]
            if lines:
                payloads.append(json.loads("\n".join(lines)))
        if not payloads:
            raise RuntimeError("No JSON payload in MCP event stream: {}".format(body))
        return payloads[-1]
    return json.loads(body)


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
        status = response.status
        response_headers = dict(response.getheaders())
        if status != 200:
            body = response.read().decode("utf-8")
            raise RuntimeError("{} failed: {} {}".format(tool_name, status, body))
        body = ""
        while True:
            line = response.readline().decode("utf-8")
            if not line:
                break
            body += line
            if line.startswith("data: "):
                candidate = json.loads(line[6:])
                if candidate.get("id") == request_id:
                    response = candidate
                    break
        else:
            response = None
    finally:
        connection.close()
    if not isinstance(response, dict) or response.get("id") != request_id:
        raise RuntimeError("{} returned no final MCP result: {}".format(tool_name, body))
    content = response.get("result", {}).get("content", [])
    text = "\n".join(item.get("text", "") for item in content if item.get("type") == "text")
    print("CODEX_LIVE_{}_RESULT={}".format(tool_name.upper(), text))
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return text


def main():
    session_id = initialize()
    current_level = nested_call(
        session_id,
        2,
        "editor_toolset.toolsets.scene.SceneTools",
        "get_current_level",
        {},
    )
    print("CODEX_LIVE_LEVEL={}".format(current_level))
    actors = nested_call(
        session_id,
        3,
        "editor_toolset.toolsets.scene.SceneTools",
        "find_actors",
        {"name": "YanLi", "tag": "", "collision_channels": []},
    )
    candidates = actors.get("returnValue", []) if isinstance(actors, dict) else []
    if len(candidates) != 1:
        raise RuntimeError("Expected one YanLi actor, got {}".format(candidates))
    actor = candidates[0]
    print("CODEX_LIVE_YANLI_ACTOR={}".format(json.dumps(actor)))
    components = nested_call(
        session_id,
        4,
        "editor_toolset.toolsets.actor.ActorTools",
        "get_components",
        {"actor": actor},
    )
    component_refs = components.get("returnValue", []) if isinstance(components, dict) else []
    print("CODEX_LIVE_YANLI_COMPONENTS={}".format(json.dumps(component_refs)))
    for index, component in enumerate(component_refs, start=5):
        nested_call(
            session_id,
            index,
            "editor_toolset.toolsets.object.ObjectTools",
            "list_properties",
            {"instance": component},
        )


if __name__ == "__main__":
    main()
