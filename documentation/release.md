# Release Process

## Automated BCR Release Flow

BCR releases are fully automated via GitHub Actions. To trigger a release:

1. Push a tag in the format `lobster-X.Y.Z`.
2. `.github/workflows/release.yml` runs and:
   - Calls `.github/workflows/release_prep.sh` to build a source archive under `archives/` and generate release notes.
   - Creates a GitHub release and uploads the archive as a release asset.
3. `.github/workflows/publish.yml` opens a pull request to the Bazel Central Registry via `publish-to-bcr`.
4. The release workflow also dispatches `.github/workflows/package.yml` to publish
  all packages from the release tag to PyPI. The tagged commit must be on `main`.
  Check the separate PyPI workflow run for the publication result; a successful
  dispatch does not mean that the upload has completed.

Releases published outside the automated release workflow can also trigger the PyPI
workflow directly through the GitHub release event. To publish an existing release
that was missed, manually run the PyPI workflow on `main` with its release tag as
the `tag_name` input. The workflow verifies that the release is published and the
tagged commit is on `main` before building.

### Why a custom archive?

The release uses a custom-built archive (`release_prep.sh`) instead of GitHub's
auto-generated source archive (`/archive/refs/tags/`) for two reasons:

- **`strip_prefix` mismatch**: GitHub names the folder `<repo>-<tag>` (e.g. `lobster-lobster-0.13.2/`),
  but BCR's `source.template.json` expects `<repo>-<version>` (e.g. `lobster-0.13.2/`).
- **Unstable SHA-256**: GitHub can regenerate auto archives at any time, changing the hash
  and breaking BCR's integrity check for existing users. BCR explicitly rejects such URLs as unstable.

### Required secret

`BCR_PUBLISH_TOKEN`: A classic GitHub PAT with `workflow` and `repo` scopes, with write
access to the BCR fork. The default fork is `bmw-software-engineering/bazel-central-registry`
(overrideable via the `registry_fork` input in manual dispatch).
