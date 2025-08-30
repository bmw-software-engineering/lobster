{
  "schema": "lobster-report",
  "version": 2,
  "generator": "lobster_report",
  "levels": [
    {
      "name": "code",
      "kind": "implementation",
      "items":[
        {
          "tag": "python basic1.trlc_reference",
          "location": {
            "kind": "file",
            "file": "system-test-repo/submodule1/submodule1_file1.py",
            "line": 5,
            "column": null
          },
          "name": "basic1.trlc_reference",
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
          "tag": "python basic2.Example.helper_function",
          "location": {
            "kind": "file",
            "file": "system-test-repo/submodule2/submodule2_file1.py",
            "line": 13,
            "column": null
          },
          "name": "basic2.Example.helper_function",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python basic3.Example.helper_function",
          "location": {
            "kind": "file",
            "file": "system-test-repo/submodule2/folder/submodule2_file2.py",
            "line": 13,
            "column": null
          },
          "name": "basic3.Example.helper_function",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "OK",
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
          "file": "basic.lobster"
        }
      ],
      "needs_tracing_up": false,
      "needs_tracing_down": false,
      "breakdown_requirements": []
    }
  },
  "matrix": []
}