import http.client
import json
import time


HOST = "127.0.0.1"
PORT = 8000
PATH = "/mcp"
PROTOCOL_VERSION = "2025-11-25"
TOOLSET = "EditorToolset.EditorAppToolset"


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


def call(session_id, request_id, tool_name, arguments):
    payload = {
        "jsonrpc": "2.0",
        "id": request_id,
        "method": "tools/call",
        "params": {
            "name": "call_tool",
            "arguments": {
                "toolset_name": TOOLSET,
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
    connection = http.client.HTTPConnection(HOST, PORT, timeout=60)
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
    print("CODEX_PIE_{}={}".format(tool_name.upper(), text))
    return json.loads(text)


def main():
    session_id = initialize()
    state = call(session_id, 2, "IsPIERunning", {})
    if not state.get("returnValue"):
        call(
            session_id,
            3,
            "StartPIE",
            {
                "options": {
                    "bSimulate": False,
                    "playMode": "PlayMode_InViewPort",
                    "warmupSeconds": 1.0,
                }
            },
        )
        time.sleep(2.0)
    state = call(session_id, 4, "IsPIERunning", {})
    if not state.get("returnValue"):
        raise RuntimeError("PIE did not start")
    print("CODEX_PIE_SUCCESS")


if __name__ == "__main__":
    main()
