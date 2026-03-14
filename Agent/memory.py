import json
import os
from langgraph.checkpoint.memory import MemorySaver

MEMORY_FILE = "conversation_history.json"
THREAD_ID = "research_agent_thread"

def get_memory():
    return MemorySaver()

def save_session(messages: list):
    existing = load_session()
    existing.extend(messages)
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(existing, f, indent=2)

def load_session() -> list:
    if not os.path.exists(MEMORY_FILE):
        return []
    
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def format_history_for_agent(history: list) -> list:
    formatted = []
    for entry in history:
        if "role" in entry and "content" in entry:
            formatted.append({
                "role": entry["role"],
                "content": entry["content"]
            })
    return formatted