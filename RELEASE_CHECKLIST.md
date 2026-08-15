# SafeRx Enterprise release checklist

1. Validate the checked-in Enterprise OpenAPI projection and component mirrors, and
   scan everything this repo actually ships (SDKs, the mcp-server source, and the
   fern docs pages) for forbidden internal patterns and pre-2.0 candidate versions:
   `python scripts/release_preflight.py`. This also enforces release-version
   immutability: if `release/current.yaml`'s `release_version` matches an
   already-tagged `vX.Y.Z` release whose OpenAPI/component/manifest content has since
   changed, preflight fails until `release_version` is bumped — any regeneration or
   contract correction always ships under a new version, never silently overwriting
   a published one.
2. Verify generated SDK artifacts:
   `python scripts/generate_enterprise_sdks.py --check`.
3. Build the signing-aware Python, TypeScript, and C# artifacts. `packages/mcp-server`
   is internal-only and is not built for publication here.
4. Run contract, signing, closed-schema, and package tests.
5. Add a `## [X.Y.Z]` entry to `CHANGELOG.md` describing the release — `sdk-publish.yml`
   fails the publish if the tagged version has no matching entry. Then regenerate the
   Fern changelog docs page: `python scripts/render_fern_changelog.py`.
6. Confirm the backend availability state, evaluator gate, security gate, artifact
   projection gate, documentation bindings, and designated approval.
7. Only after every gate clears, select an immutable release version, tag it `vX.Y.Z`,
   and push the tag — `sdk-publish.yml` publishes all artifacts and creates the
   matching GitHub Release automatically.

The current checked-in release is `2.0.3`, not yet tagged/published (a `git tag v2.0.3`
+ push, or the `sdk-publish.yml` `workflow_dispatch` with `version: 2.0.3`, is what
actually triggers publication — neither has been done). See
`release/current.yaml` for the live release manifest (the filename is stable across
releases; only its contents change).
