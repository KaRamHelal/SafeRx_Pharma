# Contributing

## What's generated vs. hand-maintained

`packages/python/`, `packages/typescript/`, and `packages/csharp/` are
generated from `openapi/enterprise-v1.yaml` (see `scripts/generate_enterprise_sdks.py`
and the Fern config under `fern/apis/`). Do not hand-edit generated client code
directly — changes will be overwritten on the next generation run. If a
generated client has a bug, either the OpenAPI contract or the generator
config needs to change; open an issue describing the symptom rather than a PR
against the generated file.

Contributions that are welcome as direct PRs:

- Fixes to documentation content under `fern/docs/pages/`.
- Fixes to the Postman collection under `postman/`.
- Bug reports against the OpenAPI contract itself (`openapi/enterprise-v1.yaml`,
  `openapi/components.yaml`).

## Release tags

Releases are tagged `vX.Y.Z` (e.g. `v2.0.1`). This has been the convention
since the `v2.0.0` line; a small number of releases before that used bare
`X.Y.Z` tags and were left as historical record rather than retagged.

## Questions

For anything not covered here, see `README.md` and `RELEASE_CHECKLIST.md`, or
reach out through the contact in `SECURITY.md`.
