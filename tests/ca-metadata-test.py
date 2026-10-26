"""Check that the Community Applications metadata matches the plugin."""
from pathlib import Path
import re, xml.etree.ElementTree as ET
r = Path(__file__).resolve().parent.parent
manifest = ET.parse(r/'plugin/header-fix.plg').getroot()
entry = ET.parse(r/'plugins/header-fix.xml').getroot()
profile = ET.parse(r/'ca_profile.xml').getroot()
assert profile.tag == 'CommunityApplications' and (profile.findtext('Profile') or '').strip()
assert entry.tag == 'Plugin' and entry.findtext('PluginURL') == manifest.get('pluginURL')
assert manifest.get('author') == entry.findtext('PluginAuthor') == 'EllipticSet'
assert entry.findtext('Support') == manifest.get('support')
assert entry.findtext('Name') == 'WebGUI Header Link Fix'
assert entry.findtext('MinVer') == manifest.get('min') == '7.1.0' and entry.find('MaxVer') is None
assert entry.findtext('Beta') == 'false' and entry.find('Deprecated') is None
assert entry.find('IconFA') is None and entry.findtext('Icon') == profile.findtext('Icon')
assert manifest.get('icon') == 'header-fix.png'
assert entry.findtext('License') == 'GPL-3.0' and 'GNU GENERAL PUBLIC LICENSE' in (r/'LICENSE').read_text()
assert (r/'icon.svg').is_file() and (r/'src/usr/local/emhttp/plugins/header-fix/images/header-fix.png').is_file() and profile.findtext('Icon').endswith('/main/icon.svg')
for p in [r/'ca_profile.xml', r/'plugins/header-fix.xml']:
    text = p.read_text()
    assert 'YOUR_' not in text and '/master/' not in text, p.name
changes = manifest.findtext('CHANGES').strip()
headings = re.findall(r'^###(.+)$', changes, re.M)
assert headings and headings[0] == manifest.get('version'), headings[:1]
assert all(re.fullmatch(r'\d{4}\.\d\d\.\d\d\.\d+', h) for h in headings), 'Changelog headings must use date-based versions'
assert headings == sorted(headings, key=lambda h: [int(x) for x in h.split('.')], reverse=True), 'Changelog must be newest first'
print('CA profile, plugin wrapper, exact plugin URL, author/support, compatibility and changelog passed.')
