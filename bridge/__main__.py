import sys
from bridge.core import build_report, mermaid
from bridge.server import serve

def main():
    args = sys.argv[1:]
    cmd = args[0] if args else "status"
    
    if cmd == "status":
        report = build_report()
        print(f"Workspace: {report['workspace']}")
        for pillar in report["pillars"]:
            icon = "[OK]" if pillar["status"] == "ok" else "[N/A]"
            print(f"{icon} {pillar['id']}")
            
    elif cmd == "graph":
        report = build_report()
        print(mermaid(report["pillars"]))
        
    elif cmd == "serve":
        serve()
        
    else:
        print("Usage: python -m bridge [status|graph|serve]")

if __name__ == "__main__":
    main()