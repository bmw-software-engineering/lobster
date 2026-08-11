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

def _shell_script(mode, fixed_package_target):
    lines = [
        "#!/usr/bin/env bash",
        "set -euo pipefail",
        "workspace=\"${BUILD_WORKSPACE_DIRECTORY:?This target must be run with 'bazel run'.}\"",
        "packages_dir=\"$workspace/packages\"",
        "",
        "# Old Makefile equivalents for the generated Bazel targets:",
        "#   package_builder / package_core / package_trlc / package_codebeamer /",
        "#   package_cpp / package_cpp_test / package_gtest / package_json /",
        "#   package_python / package_metapackage / package_monolithic",
        "#   -> make -C packages/<package-dir> package",
        "#",
        "#   package_install_diff",
        "#   -> install split wheels into test_install, install monolithic wheel",
        "#      into test_install_monolithic, then diff site-packages/lobster and bin",
        "#",
        "#   package_smoke_test",
        "#   -> create test_install_monolithic_venv, install the monolithic wheel,",
        "#      and run each console script with --version",
        "#",
        "#   package_pipeline",
        "#   -> run the package targets in order, then run install_diff and smoke_test",
        "",
        "build_wheel() {",
        "  # Makefile equivalent: python3 -m build --wheel",
        "  (cd \"$1\" && python3 -m build --wheel)",
        "}",
        "",
        "stage_tool_package() {",
        "  # Makefile equivalent for tool packages like lobster-tool-trlc:",
        "  #   rm -rf lobster && mkdir -p lobster/tools &&",
        "  #   cp $(LOBSTER_ROOT)/lobster/__init__.py lobster &&",
        "  #   cp -Rv $(LOBSTER_ROOT)/lobster/common lobster &&",
        "  #   cp -Rv $(LOBSTER_ROOT)/lobster/tools/<tool_name> lobster/tools",
        "  local package_dir=\"$1\"",
        "  local tool_name=\"$2\"",
        "  local staged_lobster=\"$package_dir/lobster\"",
        "  local staged_tools=\"$staged_lobster/tools\"",
        "",
        "  rm -rf \"$staged_lobster\"",
        "  mkdir -p \"$staged_tools\"",
        "  cp \"$workspace/lobster/__init__.py\" \"$staged_lobster/\"",
        "  cp -R \"$workspace/lobster/common\" \"$staged_lobster/\"",
        "  cp -R \"$workspace/lobster/tools/$tool_name\" \"$staged_tools/\"",
        "}",
        "",
        "stage_core_package() {",
        "  # Makefile equivalent for lobster-core:",
        "  #   rm -rf lobster && mkdir -p lobster/tools &&",
        "  #   cp $(LOBSTER_ROOT)/lobster/*.py lobster &&",
        "  #   cp -Rv $(LOBSTER_ROOT)/lobster/common lobster &&",
        "  #   cp -Rv $(LOBSTER_ROOT)/lobster/htmldoc lobster &&",
        "  #   cp $(LOBSTER_ROOT)/lobster/tools/*.py lobster/tools &&",
        "  #   cp -Rv $(LOBSTER_ROOT)/lobster/tools/core lobster/tools",
        "  local package_dir=\"$1\"",
        "  local staged_lobster=\"$package_dir/lobster\"",
        "  local staged_tools=\"$staged_lobster/tools\"",
        "",
        "  rm -rf \"$staged_lobster\"",
        "  mkdir -p \"$staged_tools\"",
        "  cp \"$workspace/lobster\"/*.py \"$staged_lobster/\"",
        "  cp -R \"$workspace/lobster/common\" \"$staged_lobster/\"",
        "  cp -R \"$workspace/lobster/htmldoc\" \"$staged_lobster/\"",
        "  cp \"$workspace/lobster/tools\"/*.py \"$staged_tools/\"",
        "  cp -R \"$workspace/lobster/tools/core\" \"$staged_tools/\"",
        "}",
        "",
        "stage_metapackage() {",
        "  # Makefile equivalent for lobster-metapackage:",
        "  #   rm -rf lobster && mkdir -p lobster &&",
        "  #   cp $(LOBSTER_ROOT)/lobster/__init__.py lobster &&",
        "  #   cp -Rv $(LOBSTER_ROOT)/lobster/common lobster",
        "  local package_dir=\"$1\"",
        "  local staged_lobster=\"$package_dir/lobster\"",
        "",
        "  rm -rf \"$staged_lobster\"",
        "  mkdir -p \"$staged_lobster\"",
        "  cp \"$workspace/lobster/__init__.py\" \"$staged_lobster/\"",
        "  cp -R \"$workspace/lobster/common\" \"$staged_lobster/\"",
        "}",
        "",
        "stage_monolithic() {",
        "  # Makefile equivalent for lobster-monolithic pre-build stage:",
        "  #   rm -rf lobster dist meta_dist && cp -Rv $(LOBSTER_ROOT)/lobster lobster",
        "  local package_dir=\"$1\"",
        "  local staged_lobster=\"$package_dir/lobster\"",
        "",
        "  rm -rf \"$staged_lobster\" \"$package_dir/dist\" \"$package_dir/meta_dist\"",
        "  cp -R \"$workspace/lobster\" \"$staged_lobster\"",
        "}",
        "",
        "run_package_build() {",
        "  local package_target=\"$1\"",
        "  local package_dir",
        "",
        "  case \"$package_target\" in",
    ]

    for package_target in PACKAGE_ORDER:
        package_dir = PACKAGE_DIR_MAP[package_target]
        if package_target in TOOL_PACKAGE_MAP:
            lines.extend([
                "    # Makefile equivalent: make -C packages/%s package" % package_dir,
                "    %s)" % package_target,
                "      package_dir=\"$packages_dir/%s\"" % package_dir,
                "      stage_tool_package \"$package_dir\" \"%s\"" % TOOL_PACKAGE_MAP[package_target],
                "      build_wheel \"$package_dir\"",
                "      ;;",
            ])
        elif package_target == "package_core":
            lines.extend([
                "    # Makefile equivalent: make -C packages/%s package" % package_dir,
                "    %s)" % package_target,
                "      package_dir=\"$packages_dir/%s\"" % package_dir,
                "      stage_core_package \"$package_dir\"",
                "      build_wheel \"$package_dir\"",
                "      ;;",
            ])
        elif package_target == "package_metapackage":
            lines.extend([
                "    # Makefile equivalent: make -C packages/%s package" % package_dir,
                "    %s)" % package_target,
                "      package_dir=\"$packages_dir/%s\"" % package_dir,
                "      stage_metapackage \"$package_dir\"",
                "      build_wheel \"$package_dir\"",
                "      ;;",
            ])
        elif package_target == "package_monolithic":
            lines.extend([
                "    # Makefile equivalent: make -C packages/%s package" % package_dir,
                "    %s)" % package_target,
                "      package_dir=\"$packages_dir/%s\"" % package_dir,
                "      stage_monolithic \"$package_dir\"",
                "      build_wheel \"$package_dir\"",
                "      if [[ ! -d \"$package_dir/dist\" ]]; then",
                "        echo \"Wheel build did not produce dist directory\" >&2",
                "        exit 1",
                "      fi",
                "      rm -rf \"$package_dir/meta_dist\"",
                "      mv \"$package_dir/dist\" \"$package_dir/meta_dist\"",
                "      ;;",
            ])

    lines.extend([
        "    *)",
        "      echo \"Unknown package target: $package_target\" >&2",
        "      exit 1",
        "      ;;",
        "  esac",
        "}",
        "",
        "collect_wheels() {",
        "  local pattern=\"$1\"",
        "  local -a wheels",
        "",
        "  shopt -s nullglob",
        "  wheels=( $pattern )",
        "  shopt -u nullglob",
        "",
        "  if [[ ${#wheels[@]} -eq 0 ]]; then",
        "    echo \"No wheels matched: $pattern\" >&2",
        "    exit 1",
        "  fi",
        "",
        "  printf '%s\n' \"${wheels[@]}\"",
        "}",
        "",
        "install_wheels() {",
        "  local prefix=\"$1\"",
        "  shift",
        "",
        "  rm -rf \"$prefix\"",
        "  PYTHONPATH= python3 -m pip install --prefix \"$prefix\" \"$@\"",
        "}",
        "",
        "find_installed_lobster() {",
        "  local prefix=\"$1\"",
        "  local -a candidates",
        "  local candidate",
        "",
        "  shopt -s nullglob",
        "  candidates=( \"$prefix\"/lib/python*/site-packages/lobster \"$prefix\"/lib/python*/dist-packages/lobster )",
        "  shopt -u nullglob",
        "",
        "  for candidate in \"${candidates[@]}\"; do",
        "    if [[ -d \"$candidate\" ]]; then",
        "      printf '%s\n' \"$candidate\"",
        "      return 0",
        "    fi",
        "  done",
        "",
        "  echo \"No installed lobster package found under $prefix\" >&2",
        "  exit 1",
        "}",
        "",
        "find_bin_dir() {",
        "  local prefix=\"$1\"",
        "  local candidate",
        "",
        "  for candidate in \"$prefix/bin\" \"$prefix/local/bin\"; do",
        "    if [[ -d \"$candidate\" ]]; then",
        "      printf '%s\n' \"$candidate\"",
        "      return 0",
        "    fi",
        "  done",
        "",
        "  echo \"No bin directory found under $prefix\" >&2",
        "  exit 1",
        "}",
        "",
        "run_install_diff() {",
        "  # Makefile equivalent:",
        "  #   PYTHONPATH= pip3 install --prefix test_install packages/*/dist/*.whl &&",
        "  #   PYTHONPATH= pip3 install --prefix test_install_monolithic \\",
        "  #       packages/lobster-monolithic/meta_dist/*.whl &&",
        "  #   diff -Naur test_install/lib/python*/site-packages/lobster \\",
        "  #       test_install_monolithic/lib/python*/site-packages/lobster \\",
        "  #       -x \"*.pyc\" -x \"*pkg*\" -x \"pkg/*\" &&",
        "  #   diff -Naur test_install/bin test_install_monolithic/bin -x \"*pkg*\" -x \"pkg/*\"",
        "  local split_prefix=\"$workspace/test_install\"",
        "  local monolithic_prefix=\"$workspace/test_install_monolithic\"",
        "  local -a split_wheels",
        "  local -a monolithic_wheels",
        "",
        "  mapfile -t split_wheels < <(collect_wheels \"$packages_dir/*/dist/*.whl\")",
        "  mapfile -t monolithic_wheels < <(collect_wheels \"$packages_dir/lobster-monolithic/meta_dist/*.whl\")",
        "  install_wheels \"$split_prefix\" \"${split_wheels[@]}\"",
        "  install_wheels \"$monolithic_prefix\" \"${monolithic_wheels[@]}\"",
        "",
        "  diff -Naur \"$(find_installed_lobster \"$split_prefix\")\" \"$(find_installed_lobster \"$monolithic_prefix\")\" -x '*.pyc' -x '*pkg*' -x 'pkg/*'",
        "  diff -Naur \"$(find_bin_dir \"$split_prefix\")\" \"$(find_bin_dir \"$monolithic_prefix\")\" -x '*pkg*' -x 'pkg/*'",
        "}",
        "",
        "run_smoke_test() {",
        "  # Makefile equivalent:",
        "  #   python3 -m venv test_install_monolithic_venv &&",
        "  #   . test_install_monolithic_venv/bin/activate && pip install --upgrade pip &&",
        "  #   pip install packages/lobster-monolithic/meta_dist/*.whl &&",
        "  #   lobster-report --version && ... && lobster-rst-report --version",
        "  local venv_dir=\"$workspace/test_install_monolithic_venv\"",
        "  local venv_python=\"$venv_dir/bin/python\"",
        "  local venv_bin=\"$venv_dir/bin\"",
        "  local -a monolithic_wheels",
        "  local tool",
        "",
        "  rm -rf \"$venv_dir\"",
        "  python3 -m venv \"$venv_dir\"",
        "  \"$venv_python\" -m pip install --upgrade pip",
        "  mapfile -t monolithic_wheels < <(collect_wheels \"$packages_dir/lobster-monolithic/meta_dist/*.whl\")",
        "  \"$venv_python\" -m pip install \"${monolithic_wheels[@]}\"",
        "",
        "  for tool in lobster-report lobster-ci-report lobster-html-report lobster-online-report lobster-online-report-nogit lobster-cpp lobster-cpptest lobster-codebeamer lobster-gtest lobster-json lobster-python lobster-trlc lobster-pkg lobster-rst-report; do",
        "    \"$venv_bin/$tool\" --version",
        "  done",
        "}",
        "",
        "run_pipeline() {",
        "  # Makefile equivalent top-level flow:",
        "  #   $(BAZEL) run //packages:package_core",
        "  #   $(BAZEL) run //packages:package_trlc",
        "  #   $(BAZEL) run //packages:package_codebeamer",
        "  #   $(BAZEL) run //packages:package_cpp",
        "  #   $(BAZEL) run //packages:package_cpp_test",
        "  #   $(BAZEL) run //packages:package_gtest",
        "  #   $(BAZEL) run //packages:package_json",
        "  #   $(BAZEL) run //packages:package_python",
        "  #   $(BAZEL) run //packages:package_metapackage",
        "  #   $(BAZEL) run //packages:package_monolithic",
        "  #   PYTHONPATH= pip3 install ... && diff ... && smoke test...",
        "  local package_target",
    ])

    for package_target in PACKAGE_ORDER:
        lines.extend([
            "  echo \"Building %s...\"" % package_target,
            "  run_package_build \"%s\"" % package_target,
        ])

    lines.extend([
        "  echo \"Running split-vs-monolithic install equivalence checks...\"",
        "  run_install_diff",
        "  echo \"Running monolithic wheel smoke test...\"",
        "  run_smoke_test",
        "}",
        "",
    ])

    if mode == "build":
        if fixed_package_target:
            lines.extend([
                "if [[ $# -ne 0 ]]; then",
                "  echo \"Usage: $0\" >&2",
                "  exit 2",
                "fi",
                "run_package_build \"%s\"" % fixed_package_target,
            ])
        else:
            lines.extend([
                "if [[ $# -ne 1 ]]; then",
                "  echo \"Usage: $0 <package-target>\" >&2",
                "  echo \"Known targets: %s\" >&2" % ", ".join(PACKAGE_ORDER),
                "  exit 2",
                "fi",
                "run_package_build \"$1\"",
            ])
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
