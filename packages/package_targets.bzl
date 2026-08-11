"""Starlark helpers for the Lobster packaging targets."""

PACKAGE_ORDER = [
    "package_core",
    "package_trlc",
    "package_codebeamer",
    "package_cpp",
    "package_cpp_test",
    "package_gtest",
    "package_json",
    "package_python",
    "package_metapackage",
    "package_monolithic",
]

TOOL_PACKAGE_MAP = {
    "package_trlc": "trlc",
    "package_codebeamer": "codebeamer",
    "package_cpp": "cpp",
    "package_cpp_test": "cpptest",
    "package_gtest": "gtest",
    "package_json": "json",
    "package_python": "python",
}

PACKAGE_DIR_MAP = {
    "package_core": "lobster-core",
    "package_trlc": "lobster-tool-trlc",
    "package_codebeamer": "lobster-tool-codebeamer",
    "package_cpp": "lobster-tool-cpp",
    "package_cpp_test": "lobster-tool-cpptest",
    "package_gtest": "lobster-tool-gtest",
    "package_json": "lobster-tool-json",
    "package_python": "lobster-tool-python",
    "package_metapackage": "lobster-metapackage",
    "package_monolithic": "lobster-monolithic",
}

SMOKE_TOOLS = [
    "lobster-report",
    "lobster-ci-report",
    "lobster-html-report",
    "lobster-online-report",
    "lobster-online-report-nogit",
    "lobster-cpp",
    "lobster-cpptest",
    "lobster-codebeamer",
    "lobster-gtest",
    "lobster-json",
    "lobster-python",
    "lobster-trlc",
    "lobster-pkg",
    "lobster-rst-report",
]

def _append_block(lines, block):
    for line in block.split("\n"):
        lines.append(line)

def _render_package_case_lines():
    lines = []
    for package_target in PACKAGE_ORDER:
        package_dir = PACKAGE_DIR_MAP[package_target]
        lines.extend([
            "    %s)" % package_target,
            "      package_dir=\"$packages_dir/%s\"" % package_dir,
        ])

        if package_target in TOOL_PACKAGE_MAP:
            lines.extend([
                "      stage_tool_package \"$package_dir\" \"%s\"" % TOOL_PACKAGE_MAP[package_target],
                "      build_wheel \"$package_dir\"",
            ])
        elif package_target == "package_core":
            lines.extend([
                "      stage_core_package \"$package_dir\"",
                "      build_wheel \"$package_dir\"",
            ])
        elif package_target == "package_metapackage":
            lines.extend([
                "      stage_metapackage \"$package_dir\"",
                "      build_wheel \"$package_dir\"",
            ])
        elif package_target == "package_monolithic":
            lines.extend([
                "      stage_monolithic \"$package_dir\"",
                "      build_wheel \"$package_dir\"",
                "      if [[ ! -d \"$package_dir/dist\" ]]; then",
                "        echo \"Wheel build did not produce dist directory\" >&2",
                "        exit 1",
                "      fi",
                "      rm -rf \"$package_dir/meta_dist\"",
                "      mv \"$package_dir/dist\" \"$package_dir/meta_dist\"",
            ])
        else:
            fail("Unsupported package target: %s" % package_target)

        lines.append("      ;;")

    return lines

def _render_pipeline_build_lines():
    lines = []
    for package_target in PACKAGE_ORDER:
        lines.extend([
            "  echo \"Building %s...\"" % package_target,
            "  run_package_build \"%s\"" % package_target,
        ])
    return lines

def _shell_script(mode, fixed_package_target):
    lines = []

    _append_block(lines, """#!/usr/bin/env bash
set -euo pipefail
workspace="${BUILD_WORKSPACE_DIRECTORY:?This target must be run with 'bazel run'.}"
packages_dir="$workspace/packages"

build_wheel() {
  (cd "$1" && python3 -m build --wheel)
}

stage_tool_package() {
  local package_dir="$1"
  local tool_name="$2"
  local staged_lobster="$package_dir/lobster"
  local staged_tools="$staged_lobster/tools"

  rm -rf "$staged_lobster"
  mkdir -p "$staged_tools"
  cp "$workspace/lobster/__init__.py" "$staged_lobster/"
  cp -R "$workspace/lobster/common" "$staged_lobster/"
  cp -R "$workspace/lobster/tools/$tool_name" "$staged_tools/"
}

stage_core_package() {
  local package_dir="$1"
  local staged_lobster="$package_dir/lobster"
  local staged_tools="$staged_lobster/tools"

  rm -rf "$staged_lobster"
  mkdir -p "$staged_tools"
  cp "$workspace/lobster"/*.py "$staged_lobster/"
  cp -R "$workspace/lobster/common" "$staged_lobster/"
  cp -R "$workspace/lobster/htmldoc" "$staged_lobster/"
  cp "$workspace/lobster/tools"/*.py "$staged_tools/"
  cp -R "$workspace/lobster/tools/core" "$staged_tools/"
}

stage_metapackage() {
  local package_dir="$1"
  local staged_lobster="$package_dir/lobster"

  rm -rf "$staged_lobster"
  mkdir -p "$staged_lobster"
  cp "$workspace/lobster/__init__.py" "$staged_lobster/"
  cp -R "$workspace/lobster/common" "$staged_lobster/"
}

stage_monolithic() {
  local package_dir="$1"
  local staged_lobster="$package_dir/lobster"

  rm -rf "$staged_lobster" "$package_dir/dist" "$package_dir/meta_dist"
  cp -R "$workspace/lobster" "$staged_lobster"
}

run_package_build() {
  local package_target="$1"
  local package_dir

  case "$package_target" in
""")

    lines.extend(_render_package_case_lines())

    _append_block(lines, """    *)
      echo "Unknown package target: $package_target" >&2
      exit 1
      ;;
  esac
}

collect_wheels() {
  local pattern="$1"
  local -a wheels

  shopt -s nullglob
  wheels=( $pattern )
  shopt -u nullglob

  if [[ ${#wheels[@]} -eq 0 ]]; then
    echo "No wheels matched: $pattern" >&2
    exit 1
  fi

  printf '%s\\n' "${wheels[@]}"
}

install_wheels() {
  local prefix="$1"
  shift

  rm -rf "$prefix"
  PYTHONPATH= python3 -m pip install --prefix "$prefix" "$@"
}

find_installed_lobster() {
  local prefix="$1"
  local -a candidates
  local candidate

  shopt -s nullglob
  candidates=( "$prefix"/lib/python*/site-packages/lobster "$prefix"/lib/python*/dist-packages/lobster )
  shopt -u nullglob

  for candidate in "${candidates[@]}"; do
    if [[ -d "$candidate" ]]; then
      printf '%s\\n' "$candidate"
      return 0
    fi
  done

  echo "No installed lobster package found under $prefix" >&2
  exit 1
}

find_bin_dir() {
  local prefix="$1"
  local candidate

  for candidate in "$prefix/bin" "$prefix/local/bin"; do
    if [[ -d "$candidate" ]]; then
      printf '%s\\n' "$candidate"
      return 0
    fi
  done

  echo "No bin directory found under $prefix" >&2
  exit 1
}

run_install_diff() {
  local split_prefix="$workspace/test_install"
  local monolithic_prefix="$workspace/test_install_monolithic"
  local -a split_wheels
  local -a monolithic_wheels

  mapfile -t split_wheels < <(collect_wheels "$packages_dir/*/dist/*.whl")
  mapfile -t monolithic_wheels < <(collect_wheels "$packages_dir/lobster-monolithic/meta_dist/*.whl")
  install_wheels "$split_prefix" "${split_wheels[@]}"
  install_wheels "$monolithic_prefix" "${monolithic_wheels[@]}"

  diff -Naur "$(find_installed_lobster "$split_prefix")" "$(find_installed_lobster "$monolithic_prefix")" -x '*.pyc' -x '*pkg*' -x 'pkg/*'
  diff -Naur "$(find_bin_dir "$split_prefix")" "$(find_bin_dir "$monolithic_prefix")" -x '*pkg*' -x 'pkg/*'
}

run_smoke_test() {
  local venv_dir="$workspace/test_install_monolithic_venv"
  local venv_python="$venv_dir/bin/python"
  local venv_bin="$venv_dir/bin"
  local -a monolithic_wheels
  local tool

  rm -rf "$venv_dir"
  python3 -m venv "$venv_dir"
  "$venv_python" -m pip install --upgrade pip
  mapfile -t monolithic_wheels < <(collect_wheels "$packages_dir/lobster-monolithic/meta_dist/*.whl")
  "$venv_python" -m pip install "${monolithic_wheels[@]}"

  for tool in __SMOKE_TOOLS__; do
    "$venv_bin/$tool" --version
  done
}

run_pipeline() {
""".replace("__SMOKE_TOOLS__", " ".join(SMOKE_TOOLS)))

    lines.extend(_render_pipeline_build_lines())

    _append_block(lines, """  echo "Running split-vs-monolithic install equivalence checks..."
  run_install_diff
  echo "Running monolithic wheel smoke test..."
  run_smoke_test
}
""")

    if mode == "build":
        if fixed_package_target:
            _append_block(lines, """if [[ $# -ne 0 ]]; then
  echo "Usage: $0" >&2
  exit 2
fi
run_package_build "%s"
""" % fixed_package_target)
        else:
            _append_block(lines, """if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <package-target>" >&2
  echo "Known targets: %s" >&2
  exit 2
fi
run_package_build "$1"
""" % ", ".join(PACKAGE_ORDER))
    elif mode == "pipeline":
        lines.append("run_pipeline")
    elif mode == "install_diff":
        lines.append("run_install_diff")
    elif mode == "smoke_test":
        lines.append("run_smoke_test")
    else:
        fail("Unsupported mode: %s" % mode)

    lines.append("")
    return "\n".join(lines)

def _lobster_script_impl(ctx):
    script = ctx.actions.declare_file(ctx.label.name)
    ctx.actions.write(
        output = script,
        content = _shell_script(ctx.attr.mode, ctx.attr.package_target),
        is_executable = True,
    )
    return [DefaultInfo(executable = script)]

lobster_script = rule(
    implementation = _lobster_script_impl,
    attrs = {
        "mode": attr.string(values = ["build", "pipeline", "install_diff", "smoke_test"]),
        "package_target": attr.string(default = ""),
    },
    executable = True,
)

def lobster_package_builder(name = "package_builder"):
    lobster_script(
        name = name,
        mode = "build",
    )

def lobster_package_target(name):
    lobster_script(
        name = name,
        mode = "build",
        package_target = name,
    )

def lobster_package_targets(name, names):
    _ = name
    for package_name in names:
        lobster_package_target(name = package_name)

def lobster_package_pipeline(name = "package_pipeline"):
    lobster_script(
        name = name,
        mode = "pipeline",
    )

def lobster_package_install_diff(name = "package_install_diff"):
    lobster_script(
        name = name,
        mode = "install_diff",
    )

def lobster_package_smoke_test(name = "package_smoke_test"):
    lobster_script(
        name = name,
        mode = "smoke_test",
    )
