<div align="center">

<img src="icon.svg" alt="WebGUI Header Link Fix icon" width="120">

<h1>WebGUI Header Link Fix</h1>

<p><strong>Makes the Unraid logo in the <a href="https://unraid.net/">Unraid</a> WebGUI header open the WebGUI start page.</strong></p>

<p>
  <a href="https://github.com/EllipticSet/unraid-header-fix/actions/workflows/validate.yml"><img src="https://github.com/EllipticSet/unraid-header-fix/actions/workflows/validate.yml/badge.svg" alt="Validate plugin"></a>
  <a href="https://github.com/EllipticSet/unraid-header-fix/releases/latest"><img src="https://img.shields.io/github/v/release/EllipticSet/unraid-header-fix?label=release&amp;color=blue" alt="Latest GitHub release"></a>
  <img src="https://img.shields.io/badge/Unraid-7.1%2B-e8543f" alt="Unraid requirement: 7.1+">
  <a href="LICENSE"><img src="https://img.shields.io/github/license/EllipticSet/unraid-header-fix?color=green" alt="License: GPL-3.0"></a>
</p>

</div>

In the Unraid WebGUI, the logo in the header opens unraid.net in a new tab. This plugin changes it to open the WebGUI start page in the same tab, the page selected in **Settings → Display Settings**.

The plugin has no settings, runs no background service and makes no network requests. It adds a small script to the WebGUI page that changes only the logo link.

> This project continues the [original plugin by Derek Kaser](https://github.com/dkaser/unraid-header-fix), which reached end of support in October 2026. It is maintained by EllipticSet and is not an official Unraid project.

## Compatibility

| Unraid | Header |
| --- | --- |
| 7.1 to 7.3 | Legacy header (`unraid-header-os-version`) |
| 7.4 | Unified header (`unraid-header`), including the placeholder shown while it loads |

Only links that point exactly to the unraid.net home page are changed. Other unraid.net links in the header, such as documentation or account links, keep working as before.

## Installation

Once the plugin is available in Community Applications, open **Apps** in Unraid, search for **WebGUI Header Link Fix** and select **Install**.

### Direct installation

Alternatively, open **Plugins → Install Plugin** and paste:

```text
https://raw.githubusercontent.com/EllipticSet/unraid-header-fix/main/plugin/header-fix.plg
```

The plugin file contains the package, so installation and updates do not download anything else.

### Moving from the original plugin

The plugin keeps the original name (`header-fix`) and version scheme, so it replaces the original plugin directly. Once the original plugin redirects its updates here, existing installations update from **Plugins** without reinstalling.

## Removal

Remove the plugin from **Plugins**. The logo link returns to unraid.net after the page is reloaded.

## Versioning

Versions use the date and time of the release, `YYYY.MM.DD.HHMM`, as in the original plugin. This keeps every release newer than the original plugin's last version. The changelog is shown in **Plugins** and in [build/plugin-changes.md](build/plugin-changes.md).

## Support

Report problems in [Issues](https://github.com/EllipticSet/unraid-header-fix/issues). Include the plugin and Unraid versions and the browser you use. Report vulnerabilities as described in [SECURITY.md](SECURITY.md).

## Development

The plugin is built by [build/package.py](build/package.py), which uses only the Python standard library. It packages `src/` into a reproducible Slackware package and embeds it in `plugin/header-fix.plg`. See [CONTRIBUTING.md](CONTRIBUTING.md) for checks and the release process, and [docs/community-apps.md](docs/community-apps.md) for the Community Applications listing.

## License

GPL-3.0, like the original project by Derek Kaser. See [LICENSE](LICENSE).
