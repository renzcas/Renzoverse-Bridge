import sys

from bridge.core import build_report
from bridge.core import mermaid


def main():

    cmd = (
        sys.argv[1]
        if len(sys.argv) > 1
        else "status"
    )

    if cmd == "status":

        report = build_report()

        print(
            f"Workspace: {report['workspace']}"
        )

        for pillar in report["pillars"]:

            icon = (
                "[OK]"
                if pillar["status"] == "ok"
                else "[N/A]"
            )

            print(
                f"{icon} {pillar['id']}"
            )

    elif cmd == "graph":

        report = build_report()

        print(
            mermaid(report["pillars"])
        )

    else:

        print(
            "Usage: python -m bridge [status|graph]"
        )


if __name__ == "__main__":
    main()