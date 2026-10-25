# Community Applications

The plugin is submitted to Community Applications as **WebGUI Header Link Fix**, to replace the original listing by Derek Kaser. Once this listing is approved, he agreed to redirect updates from the original plugin to this repository and to remove the original listing.

Direct installation remains available through **Plugins → Install Plugin** using:

```text
https://raw.githubusercontent.com/EllipticSet/unraid-header-fix/main/plugin/header-fix.plg
```

## Repository metadata

- [`ca_profile.xml`](../ca_profile.xml): repository profile.
- [`plugins/header-fix.xml`](../plugins/header-fix.xml): plugin listing, installation URL, compatibility and icon.
- [`icon.svg`](../icon.svg): repository icon used by the profile. The plugin listing uses the Font Awesome `wrench` icon, as on the Plugins page.
- Support: [GitHub Issues](https://github.com/EllipticSet/unraid-header-fix/issues).

When updating the listing, keep it aligned with the plugin: the `PluginURL` must match the `pluginURL` attribute of `plugin/header-fix.plg` exactly, and the minimum Unraid version must match its `min` attribute. Run `python3 tests/ca-metadata-test.py` after each change. This checks the repository files; availability in the catalogue must be checked in Community Applications.

## Submission

1. Sign in at [ca.unraid.net/submit](https://ca.unraid.net/submit/new) with an Unraid account.
2. Enter `https://github.com/EllipticSet/unraid-header-fix`.
3. Run **Validate** and **Scan**, fix any reported issues and submit. Plugin submissions are reviewed manually.

Reference layout: [official Community Apps starter](https://github.com/unraid/unraid-community-apps-starter). Maintainer help: [Community Applications submission help](https://ca.unraid.net/submit/help).
