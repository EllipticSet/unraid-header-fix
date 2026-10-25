"""Single source for the plugin identity, version and payload inputs."""
NAME = 'header-fix'
PACKAGE_NAME = 'unraid-header-fix'
# Date-based versions (YYYY.MM.DD.HHMM) continue the original plugin's scheme,
# so installations of earlier releases always see a newer version.
VERSION = '2026.10.25.1800'
PKG = f'{PACKAGE_NAME}-{VERSION}-noarch-1'
AUTHOR = 'EllipticSet'
REPOSITORY = 'https://github.com/EllipticSet/unraid-header-fix'
# Kept at plugin/header-fix.plg so installations from earlier releases keep updating.
PLUGIN_URL = 'https://raw.githubusercontent.com/EllipticSet/unraid-header-fix/main/plugin/header-fix.plg'
SUPPORT_URL = 'https://github.com/EllipticSet/unraid-header-fix/issues'
ICON = 'fa-wrench'
MIN_UNRAID = '7.1.0'


def payload_inputs(root):
    """Return destination -> source for every file installed by the package."""
    src = root/'src'
    return {path.relative_to(src).as_posix(): path for path in sorted(src.rglob('*')) if path.is_file()}
