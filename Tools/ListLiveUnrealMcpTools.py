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
    connection = http.client.HTTPConnection(HOST, PORT, timeout=15)
    try:
        connection.request("POST", PATH, body=json.dumps(payload), headers=headers)
        response = connection.getresponse()
        body = response.read().decode("utf-8")
        return response.status, dict(response.getheaders()), body
    finally:
        connection.close()


def parse_json(body):
    return json.loads(body) if body else None


def main():
    status, headers, body = post({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": {},
            "clientInfo": {"name": "codex-local-recovery", "version": "1.0"},
        },
    })
    if status != 200:
        raise RuntimeError("MCP initialize failed: {} {}".format(status, body))
    session_id = headers.get("Mcp-Session-Id") or headers.get("mcp-session-id")
    if not session_id:
        raise RuntimeError("MCP initialize returned no session id")
    initialize_result = parse_json(body)
    print("CODEX_MCP_INIT={}".format(json.dumps(initialize_result, ensure_ascii=False)))
    print("CODEX_MCP_SESSION={}".format(session_id))

    status, _, body = post(
        {
            "jsonrpc": "2.0",
            "method": "notifications/initialized",
            "params": {},
        },
        session_id,
    )
    if status not in (200, 202):
        raise RuntimeError("MCP initialized notification failed: {} {}".format(status, body))

    status, _, body = post(
        {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
        session_id,
    )
    if status != 200:
        raise RuntimeError("MCP tools/list failed: {} {}".format(status, body))
    tools = parse_json(body)["result"]["tools"]
    print("CODEX_MCP_TOOL_COUNT={}".format(len(tools)))
    for tool in tools:
        print("CODEX_MCP_TOOL name={} description={} schema={}".format(
            tool.get("name"),
            tool.get("description", "").replace("\n", " "),
            json.dumps(tool.get("inputSchema", {}), ensure_ascii=False),
        ))


if __name__ == "__main__":
    main()
