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
            "commit": "e8af194598c88c4b15f3a39c125f00ea62dc7a2e",
            "file": "test-lobster-online-report-m66px5k8/basic.py",
            "line": 5
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
            "commit": "e8af194598c88c4b15f3a39c125f00ea62dc7a2e",
            "file": "test-lobster-online-report-m66px5k8/basic.py",
            "line": 13
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
            "commit": "e8af194598c88c4b15f3a39c125f00ea62dc7a2e",
            "file": "test-lobster-online-report-m66px5k8/basic.py",
            "line": 17
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
