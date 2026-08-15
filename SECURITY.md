# Security

## Reporting a vulnerability

If you find a security issue in this repository (the OpenAPI contract, the
generated SDKs under `packages/`, the Postman collection, or the documentation
source under `fern/`), report it privately rather than opening a public issue.

- Email: security@saferx.online
- Include: a description of the issue, steps to reproduce, and the affected
  file(s)/endpoint(s). Do not include real patient data, prescriptions, or any
  other protected information in a report — use synthetic examples only.
- We aim to acknowledge reports within 3 business days and to provide a
  remediation timeline once the issue is confirmed.

We follow standard safe-harbor practice for good-faith security research
conducted against this repository's contents. This does not authorize testing
against the live production API beyond what your issued Enterprise API key
entitles you to.

## Scope

This repository contains a public API contract and generated client code. It
does not contain the production service implementation, credentials, or
protected health information — those are deliberately excluded from this
projection by our internal release-governance process. Issues with the live
API's behavior (as opposed to this repository's contract/SDK code) should
also be reported through the address above.
