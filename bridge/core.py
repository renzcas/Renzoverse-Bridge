import json
import os
from pathlib import Path

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
    return Path(
        os.environ.get(
            "RENZO_WORKSPACE",
            "/workspaces"
        )
    )


def load_pillars():
    config_file = Path(__file__).parent / "pillars.json"

    with open(config_file, "r", encoding="utf-8") as f:
        return json.load(f)


def build_report():
    workspace = get_workspace_path()
    pillars = load_pillars()

    report = []

    for pillar in pillars:
        pillar_id = pillar["id"]

        folder = PILLAR_TO_FOLDER.get(
            pillar_id,
            pillar_id
        )

        exists = (workspace / folder).exists()

        report.append(
            {
                "id": pillar_id,
                "folder": folder,
                "status": "ok" if exists else "missing",
                "depends_on": pillar.get("depends_on", [])
            }
        )

    return {
        "workspace": str(workspace),
        "pillars": report
    }


def mermaid(pillars):
    lines = ["graph TD"]

    for pillar in pillars:
        for dep in pillar.get("depends_on", []):
            lines.append(
                f"    {dep} --> {pillar['id']}"
            )

    return "\n".join(lines)
