"""An MCP-style tool server (Lesson 35 demo).

One tool registry, schema validation before execution, read/write/
destructive classes, and one audit log — callable from a graph, a crew
or a chat. Stdlib only.
"""
REGISTRY = {
    "lookup_order": {"class": "read", "required": ["order_id"]},
    "draft_reply": {"class": "write", "required": ["order_id", "text"]},
    "refund_order": {"class": "destructive", "required": ["order_id", "amount"]},
}
AUDIT = []
def call_tool(name, args, approved=False):
    spec = REGISTRY.get(name)
    if spec is None:
        return {"ok": False, "error": f"unknown tool: {name}"}
    missing = [k for k in spec["required"] if k not in args]
    if missing:
        return {"ok": False, "error": f"missing arguments: {','.join(missing)}"}
    if spec["class"] == "destructive" and not approved:
        AUDIT.append(f"GATED {name} (destructive, no approval)")
        return {"ok": False, "error": "destructive tool requires human approval"}
    AUDIT.append(f"CALLED {name} class={spec['class']}")
    return {"ok": True, "result": f"{name} executed for order {args['order_id']}"}
def main():
    print("tool server: one registry, three orchestration callers")
    print(" ", call_tool("lookup_order", {"order_id": "1042"}))
    print(" ", call_tool("draft_reply", {"order_id": "1042", "text": "refund approved"}))
    print(" ", call_tool("refund_order", {"order_id": "1042", "amount": 49.0}))
    print(" ", call_tool("refund_order", {"order_id": "1042", "amount": 49.0}, approved=True))
    print(" ", call_tool("lookup_order", {}))
    for line in AUDIT: print(f"  audit: {line}")
    print("tool server demo complete")
if __name__ == "__main__":
    main()
