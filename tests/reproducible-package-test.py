"""Compare committed bytes with a rebuild under a restrictive umask."""
from pathlib import Path
import os, subprocess, sys, tempfile
root = Path(__file__).resolve().parent.parent
with tempfile.TemporaryDirectory() as tmp:
    old_umask = os.umask(0o077)
    try:
        subprocess.run([sys.executable, str(root/'build/package.py'), '--no-publish', '--output-dir', tmp], check=True)
    finally:
        os.umask(old_umask)
    for name in ['header-fix.plg', 'header-fix.plg.sha256']:
        assert (root/'plugin'/name).read_bytes() == (Path(tmp)/name).read_bytes(), name
print('Committed plugin matches a rebuild with a restrictive umask; the build leaves committed files unchanged.')
