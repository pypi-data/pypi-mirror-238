import subprocess
import sys
from pathlib import Path


def execute(text: str, folder: Path) -> str:
    p = subprocess.run([sys.executable, '-'],
                       input=text.encode(),
                       stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT)
    print(p)
    return p.stdout.decode()


def execute_python_code(doc):
    r, _ = doc.view.pos
    text = execute('\n'.join(doc.lines[:r]), doc.path)
    if text:
        doc.change(r, 0, r, 0, text.splitlines() + [''])
        doc.view.mark = (r, 0)
