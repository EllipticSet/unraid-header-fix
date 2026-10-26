"""Check the committed .plg: checksum, attributes, embedded package and installer scripts."""
from pathlib import Path
import base64, hashlib, io, sys, tarfile, xml.etree.ElementTree as ET
root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root/'build'))
from package_manifest import NAME, PACKAGE_NAME, VERSION, PKG, AUTHOR, PLUGIN_URL, SUPPORT_URL, MIN_UNRAID, payload_inputs
plg = Path(sys.argv[1]) if len(sys.argv) > 1 else root/'plugin'/f'{NAME}.plg'
checksum = Path(str(plg) + '.sha256').read_text().split()
assert checksum == [hashlib.sha256(plg.read_bytes()).hexdigest(), plg.name], 'Committed checksum mismatch'
el = ET.parse(plg).getroot()
assert el.tag == 'PLUGIN' and el.get('name') == NAME
assert el.get('version') == VERSION
assert el.get('author') == AUTHOR and el.get('pluginURL') == PLUGIN_URL and el.get('support') == SUPPORT_URL
assert el.get('min') == MIN_UNRAID and el.get('max') is None
assert not el.findall('FILE/URL'), 'The plugin must not download files'
install, remove = el.findall('FILE')
assert install.get('Run') == '/bin/bash' and install.get('Method') is None
assert remove.get('Run') == '/bin/bash' and remove.get('Method') == 'remove'
script = install.findtext('INLINE')
assert script.startswith('set -euo pipefail\n')
encoded = script.split("<<'HEADER_FIX_PAYLOAD'\n", 1)[1].split('\nHEADER_FIX_PAYLOAD', 1)[0]
blob = base64.b64decode(encoded)
assert f'"{hashlib.sha256(blob).hexdigest()}"' in script, 'Embedded checksum mismatch'
assert f'upgradepkg --install-new --reinstall "$scratch/{PKG}.txz"' in script
assert f'rm -f /boot/config/plugins/{NAME}/{PACKAGE_NAME}-*.txz' in script
assert f'removepkg {PACKAGE_NAME}' in remove.findtext('INLINE')
expected = payload_inputs(root)
assert 'install/slack-desc' in expected and f'usr/local/emhttp/plugins/{NAME}/HeaderFix.page' in expected
assert f'usr/local/emhttp/plugins/{NAME}/images/{el.get("icon")}' in expected, 'Plugin icon is not packaged'
with tarfile.open(fileobj=io.BytesIO(blob), mode='r:xz') as tf:
    files = [m.name for m in tf.getmembers() if m.isfile()]
    assert len(files) == len(set(files)), 'Duplicate payload entries'
    assert set(files) == set(expected), 'Payload manifest mismatch'
    for m in tf.getmembers():
        assert m.isdir() or m.isfile(), 'Unsupported archive entry type'
        assert not m.name.startswith('/') and '..' not in Path(m.name).parts
        assert m.uid == m.gid == 0 and m.uname == m.gname == 'root' and m.mtime == 0
        assert m.mode == (0o755 if m.isdir() else 0o644)
    for name, source in expected.items():
        assert tf.extractfile(name).read() == source.read_bytes(), 'Stale packaged source: ' + name
slack = (root/'src/install/slack-desc').read_text().splitlines()
assert sum(line.startswith(f'{PACKAGE_NAME}:') for line in slack) == 11, 'slack-desc needs eleven description lines'
print('Plugin attributes, checksums, embedded package contents and installer scripts passed.')
