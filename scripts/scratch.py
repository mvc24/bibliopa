import json
from pathlib import Path
from pprint import pp

log = Path("data/processing_log.json")

batched = Path("data/batched")

def tree(directory):
    print(f"- {directory}")
    for path in sorted(directory.rglob("*")):
        depth = len(path.relative_to(directory).parts)
        spacer = "   " * depth
        print(f"{spacer}+ {path.name}")

tree(Path.cwd())
