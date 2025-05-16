# context.py - place for get_env_vars() and related logic
# hub/context.py

_context = {}

def _init(context):
    global _context
    _context = context

def get_env_vars():
    return _context.get("env_vars", {})

def get_user_vars():
    return _context.get("user_vars", {})

def get_chat_history():
    return _context.get("chat_history", [])

def send_message(message):
    print({"type": "message", "content": message})

def call_agent(agent_id, input_data):
    print({
        "type": "call_agent",
        "agent_id": agent_id,
        "input": input_data
    })
