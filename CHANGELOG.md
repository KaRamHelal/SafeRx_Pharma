# Changelog

All notable changes to the SafeRx Enterprise API, SDKs, and MCP adapter are
documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/);
releases are tagged `vX.Y.Z`.

Release history before this file existed (2026-08) predates consistent GitHub
Releases tracking. For the complete published version history, see
[PyPI (saferx-pharma)](https://pypi.org/project/saferx-pharma/#history),
[npm (saferx-pharma-sdk)](https://www.npmjs.com/package/saferx-pharma-sdk?activeTab=versions),
and [NuGet (SafeRx)](https://www.nuget.org/packages/SafeRx#versions-body-tab).
Entries below are not a backfilled reconstruction of that history.

## [Unreleased]

### Changed
- Repository reorganized: SDKs and the MCP adapter moved under `packages/`;
  the OpenAPI spec is now a single source of truth (`openapi/enterprise-v1.yaml`)
  mirrored into Fern via symlinks instead of hand-duplicated copies; release
  manifest renamed from a version-stamped filename to `release/current.yaml`.
- Public documentation pages corrected to reflect that the SDKs are actually
  published (they previously, incorrectly, described themselves as
  unpublished/internal-only).
