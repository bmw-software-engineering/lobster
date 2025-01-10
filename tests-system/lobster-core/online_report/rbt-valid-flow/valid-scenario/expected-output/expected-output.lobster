{
  "schema": "lobster-report",
  "version": 2,
  "generator": "lobster_report",
  "levels": [
    {
      "name": "code",
      "kind": "implementation",
      "items": [
        {
          "tag": "python basic.trlc_reference",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "main",
            "file": "tests-system/lobster-core/online_report/rbt-valid-flow/valid-scenario/input/basic.py",
            "line": 5,
            "exec_commit_id": "fa1c6e7818ccbe0ec5b87ea6a7667c34f4f750ca"
          },
          "name": "basic.trlc_reference",
          "messages": [],
          "just_up": [
            "helper function"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "language": "Python",
          "kind": "Function"
        },
        {
          "tag": "python basic.Example.helper_function",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "main",
            "file": "tests-system/lobster-core/online_report/rbt-valid-flow/valid-scenario/input/basic.py",
            "line": 13,
            "exec_commit_id": "fa1c6e7818ccbe0ec5b87ea6a7667c34f4f750ca"
          },
          "name": "basic.Example.helper_function",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python basic.Example.nor",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "main",
            "file": "tests-system/lobster-core/online_report/rbt-valid-flow/valid-scenario/input/basic.py",
            "line": 17,
            "exec_commit_id": "fa1c6e7818ccbe0ec5b87ea6a7667c34f4f750ca"
          },
          "name": "basic.Example.nor",
          "messages": [
            "unknown tracing target req example.req_nor"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        }
      ],
      "coverage": 66.66666666666667
    }
  ],
  "policy": {
    "code": {
      "name": "code",
      "kind": "implementation",
      "traces": [],
      "source": [
        {
          "file": "basic.lobster",
          "filters": []
        }
      ],
      "needs_tracing_up": false,
      "needs_tracing_down": false,
      "breakdown_requirements": []
    }
  },
  "matrix": []
}
