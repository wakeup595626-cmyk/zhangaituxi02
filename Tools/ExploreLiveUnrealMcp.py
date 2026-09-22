import http.client
import json
import sys


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


def call_tool(session_id, request_id, name, arguments):
    status, _, body = post(
        {
            "jsonrpc": "2.0",
            "id": request_id,
            "method": "tools/call",
            "params": {"name": name, "arguments": arguments},
        },
        session_id,
    )
    if status != 200:
        raise RuntimeError("{} failed: {} {}".format(name, status, body))
    print("CODEX_MCP_{}_RAW={}".format(name.upper(), body))
    return body


def main():
    session_id = initialize()
    toolsets = sys.argv[1:]
    if not toolsets:
        call_tool(session_id, 2, "list_toolsets", {})
        return
    for index, toolset_name in enumerate(toolsets, start=2):
        call_tool(
            session_id,
            index,
            "describe_toolset",
            {"toolset_name": toolset_name},
        )


if __name__ == "__main__":
    main()
