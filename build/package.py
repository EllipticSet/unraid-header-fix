#!/usr/bin/env python3
"""Build the offline Unraid .plg with an embedded Slackware package; never touch the host OS."""
from pathlib import Path
import argparse, base64, hashlib, shutil, sys, tarfile, tempfile, xml.etree.ElementTree as ET
sys.path.insert(0, str(Path(__file__).resolve().parent))
from package_manifest import NAME, PACKAGE_NAME, VERSION, PKG, AUTHOR, PLUGIN_URL, SUPPORT_URL, ICON, MIN_UNRAID, payload_inputs

ROOT = Path(__file__).resolve().parent.parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output-dir', type=Path, default=ROOT/'dist')
parser.add_argument('--no-publish', action='store_true', help='Leave the committed .plg and checksum untouched')
args = parser.parse_args()
DIST = args.output_dir


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def archive(stage, out):
    """Write a reproducible tar.xz: sorted entries, root ownership, fixed times and modes."""
    with tarfile.open(out, 'w:xz', format=tarfile.USTAR_FORMAT) as tf:
        for path in sorted(stage.rglob('*')):
            info = tf.gettarinfo(str(path), path.relative_to(stage).as_posix())
            info.uid = info.gid = 0
            info.uname = info.gname = 'root'
            info.mtime = 0
            info.mode = 0o755 if path.is_dir() else 0o644
            if path.is_dir():
                tf.addfile(info)
            else:
                with path.open('rb') as f:
                    tf.addfile(info, f)


DIST.mkdir(parents=True, exist_ok=True)
with tempfile.TemporaryDirectory() as temp:
    stage = Path(temp)/'payload'
    for destination, source in payload_inputs(ROOT).items():
        target = stage/destination
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    package = DIST/f'{PKG}.txz'
    archive(stage, package)

install = f'''set -euo pipefail
scratch=$(mktemp -d /tmp/{NAME}-install.XXXXXX)
trap 'rm -rf -- "$scratch"' EXIT
base64 -d > "$scratch/{PKG}.txz" <<'HEADER_FIX_PAYLOAD'
{base64.encodebytes(package.read_bytes()).decode()}HEADER_FIX_PAYLOAD
if ! printf '%s  %s\\n' "{digest(package)}" "$scratch/{PKG}.txz" | sha256sum -c --status -; then
  echo 'Package checksum mismatch; the plugin file is incomplete or modified.' >&2
  exit 1
fi
upgradepkg --install-new --reinstall "$scratch/{PKG}.txz"
# Releases before {VERSION} downloaded the package to the boot device.
rm -f /boot/config/plugins/{NAME}/{PACKAGE_NAME}-*.txz
echo ""
echo "----------------------------------------------------"
echo " WebGUI Header Link Fix has been installed."
echo " Version: {VERSION}"
echo "----------------------------------------------------"
echo ""
'''
remove = f'''removepkg {PACKAGE_NAME} || true
rm -rf /usr/local/emhttp/plugins/{NAME}
rm -rf /boot/config/plugins/{NAME}
echo "WebGUI Header Link Fix has been removed."
'''

plg = ET.Element('PLUGIN', {'name': NAME, 'author': AUTHOR, 'version': VERSION, 'pluginURL': PLUGIN_URL,
                            'support': SUPPORT_URL, 'min': MIN_UNRAID, 'icon': ICON})
ET.SubElement(plg, 'CHANGES').text = '\n' + (ROOT/'build/plugin-changes.md').read_text()
item = ET.SubElement(plg, 'FILE', {'Run': '/bin/bash'})
ET.SubElement(item, 'INLINE').text = install
item = ET.SubElement(plg, 'FILE', {'Run': '/bin/bash', 'Method': 'remove'})
ET.SubElement(item, 'INLINE').text = remove
ET.indent(plg)
out = DIST/f'{NAME}.plg'
ET.ElementTree(plg).write(out, encoding='utf-8', xml_declaration=True)
for path in (package, out):
    (DIST/(path.name + '.sha256')).write_text(f'{digest(path)}  {path.name}\n')
if not args.no_publish:
    shutil.copyfile(out, ROOT/'plugin'/out.name)
    shutil.copyfile(DIST/(out.name + '.sha256'), ROOT/'plugin'/(out.name + '.sha256'))
print(out if args.no_publish else ROOT/'plugin'/out.name)
