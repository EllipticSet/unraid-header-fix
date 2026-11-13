# Community Applications

The plugin is listed in Community Applications as **WebGUI Header Link Fix**, in the **Tools / Utilities** and **Plugins** categories. The repository was approved on 2 November 2026 and the plugin appeared in the catalogue on 13 November 2026. It replaces the original listing by Derek Kaser, which is no longer in the catalogue. He agreed to redirect updates from the original plugin to this repository.

To install it, open **Apps** in Unraid, search for **WebGUI Header Link Fix** and select **Install**. The listing can also be found in the [Community Applications web catalogue](https://unraid.net/community/apps?q=WebGUI+Header+Link+Fix).

Direct installation remains available through **Plugins → Install Plugin** using:

```text
https://raw.githubusercontent.com/EllipticSet/unraid-header-fix/main/plugin/header-fix.plg
```

## Repository metadata

- [`ca_profile.xml`](../ca_profile.xml): repository profile.
- [`plugins/header-fix.xml`](../plugins/header-fix.xml): plugin listing, installation URL, compatibility and icon.
- [`icon.svg`](../icon.svg): icon used by the profile and the plugin listing. The Plugins page in Unraid shows only PNG images, so the package installs `images/header-fix.png`, rendered from `icon.svg` at 96 × 96 pixels; regenerate it when the icon changes.
- Support: [GitHub Issues](https://github.com/EllipticSet/unraid-header-fix/issues).

When updating the listing, keep it aligned with the plugin: the `PluginURL` must match the `pluginURL` attribute of `plugin/header-fix.plg` exactly, and the minimum Unraid version must match its `min` attribute. Run `python3 tests/ca-metadata-test.py` after each change. This checks the repository files; availability in the catalogue must be checked in Community Applications.
