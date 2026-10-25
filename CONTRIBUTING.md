# Contributing

Bug reports, documentation fixes and focused pull requests are welcome.

## Before opening an issue

Read the [README](README.md), search existing issues and use the bug report or feature request form. Include the plugin and Unraid versions and your browser when reporting a bug. Remove credentials and other private information from screenshots and logs.

Report potential vulnerabilities privately as described in [SECURITY.md](SECURITY.md). Follow the [code of conduct](CODE_OF_CONDUCT.md).

## Proposing a change

Start from the latest `main` and keep each pull request focused on one problem. Explain the expected behavior and the checks performed. The page script must keep changing only the unraid.net home link in the header logo, on both the legacy and the unified header.

## Validation

The commands in [.github/workflows/validate.yml](.github/workflows/validate.yml) are the reference for automated validation. They need only Node.js and Python 3:

```bash
node tests/header-fix-test.js
python3 tests/package-test.py
python3 tests/ca-metadata-test.py
python3 tests/reproducible-package-test.py
```

For changes to files under `src/`, regenerate the plugin with `python3 build/package.py` and include the updated `plugin/header-fix.plg` and checksum. See [build/package_manifest.py](build/package_manifest.py) for the plugin identity and package inputs.

Describe automated checks and actual Unraid tests separately. For Unraid tests, record the plugin and Unraid versions and the observed result. Test Unraid release candidates on a system you can recover.

Documentation and issue or pull request templates alone do not require a version change or a package rebuild.

## Releases

1. Create a `release-build/<version>` branch from `main`.
2. Set `VERSION` in [build/package_manifest.py](build/package_manifest.py) to the release date and time, `YYYY.MM.DD.HHMM`, and add a `###<version>` section at the top of [build/plugin-changes.md](build/plugin-changes.md).
3. Push the branch. The release workflow builds the plugin, runs the package checks and commits `plugin/header-fix.plg` and its checksum to the branch. Alternatively, run `python3 build/package.py` locally and commit the result.
4. Open a pull request and merge it after validation passes.
5. On `main`, the release workflow waits for validation of the merge commit, then publishes a GitHub release named after the version, with the changelog section as release notes and the plugin file attached.

## Review

Keep documentation in English and explain behavior in plain language. Contributions are reviewed as time permits; there is no guaranteed response or release schedule.
