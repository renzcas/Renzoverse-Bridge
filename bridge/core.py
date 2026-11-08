import os
import json
from pathlib import Path

# Explicit folder mapping for each pillar to ensure 100% accurate workspace detection
PILLAR_TO_FOLDER = {
    "renzoverse": "Renzoverse",
    "cavesharp-os": "CaveSharp-OS",
    "big-animal": "BIG_ANIMAL",
    "ww3-college": "WW3-College",
    "agentdash": "AgentDash",
    "renzo-hacker-lab": "Renzo-Hacker-Lab",
    "renzo-academy": "Renzo-Academy",
}

def get_workspace_path():
    return Path(os.environ.get("RENZO_WORKSPACE", r"D:\Projects"))

def load_pillars():
    config_path = Path(__file__).parent / "pillars.json"
    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def build_report(workspace_override=None):
    ws = workspace_override or get_workspace_path()
    pillars = load_pillars()
    report_pillars = []
    
    for p in pillars:
        pid = p["id"]
        folder_name = PILLAR_TO_FOLDER.get(pid, pid)
        target_path = ws / folder_name
        
        exists = target_path.exists() and target_path.is_dir()
        
        report_pillars.append({
            "id": pid,
            "folder": folder_name,
            "status": "ok" if exists else "missing",
            "depends_on": p.get("depends_on", [])
        })
        
    return {"workspace": str(ws), "pillars": report_pillars}

def mermaid(pillars):
    lines = ["graph TD"]
    for p in pillars:
        for dep in p.get("depends_on", []):
            lines.append(f"    {dep} --> {p['id']}")
    return "\n".join(lines)

def start_order(pillars):
    visited = set()
    temp = set()
    
    def visit(p_id, deps_map):
        if p_id in temp:
            raise ValueError(f"Circular dependency detected involving {p_id}")
        if p_id not in visited:
            temp.add(p_id)
            for d in deps_map.get(p_id, []):
                visit(d, deps_map)
            temp.remove(p_id)
            visited.add(p_id)

    deps_map = {p["id"]: p.get("depends_on", []) for p in pillars}
    for p in pillars:
        visit(p["id"], deps_map)
    return True