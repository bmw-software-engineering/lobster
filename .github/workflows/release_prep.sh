#!/usr/bin/env bash

set -o errexit -o nounset -o pipefail

TAG="$1"

if [[ "$TAG" == lobster-* ]]; then
  VERSION="${TAG#lobster-}"
else
  echo "ERROR: tag '${TAG}' does not match expected format 'lobster-X.Y.Z'" >&2
  exit 1
fi

mkdir -p archives

PREFIX="lobster-${VERSION}"
ARCHIVE="archives/${TAG}.tar.gz"

git archive --format=tar --prefix="${PREFIX}/" "$TAG" | gzip > "$ARCHIVE"

SHA=$(sha256sum "$ARCHIVE" | awk '{print $1}')

cat <<EOF
## Bzlmod

Add this to your MODULE.bazel:

~~~starlark
bazel_dep(name = "lobster", version = "${VERSION}")
~~~

## WORKSPACE

~~~starlark
load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

http_archive(
    name = "lobster",
    sha256 = "${SHA}",
    strip_prefix = "${PREFIX}",
    urls = ["https://github.com/bmw-software-engineering/lobster/releases/download/${TAG}/${TAG}.tar.gz"],
)
~~~
EOF
