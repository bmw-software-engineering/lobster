# Release Process

## Automated BCR Release Flow

BCR releases are fully automated via GitHub Actions. To trigger a release:

1. Push a tag in the format `lobster-X.Y.Z`.
2. `.github/workflows/release.yml` runs and:
   - Calls `.github/workflows/release_prep.sh` to build a source archive under `archives/` and generate release notes.
   - Creates a **draft** GitHub release and uploads the archive as a release asset.
3. `.github/workflows/publish.yml` opens a pull request to the Bazel Central Registry via `publish-to-bcr`.
4. After the BCR PR is merged, the draft GitHub release is finalized.
5. `.github/workflows/package.yml` publishes all packages to PyPI.

### Why a custom archive?

The release uses a custom-built archive (`release_prep.sh`) instead of GitHub's
auto-generated source archive (`/archive/refs/tags/`) for two reasons:

- **`strip_prefix` mismatch**: GitHub names the folder `<repo>-<tag>` (e.g. `lobster-lobster-0.13.2/`),
  but BCR's `source.template.json` expects `<repo>-<version>` (e.g. `lobster-0.13.2/`).
- **Unstable SHA-256**: GitHub can regenerate auto archives at any time, changing the hash
  and breaking BCR's integrity check for existing users. BCR explicitly rejects such URLs as unstable.

### Required secret

`BCR_PUBLISH_TOKEN`: A classic GitHub PAT with `workflow` and `repo` scopes, with write
access to your BCR fork. The default fork is `Rahul-Sutariya/bazel-central-registry`
(overrideable via the `registry_fork` input in manual dispatch).
