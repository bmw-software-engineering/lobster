{
  "schema": "lobster-report",
  "version": 2,
  "generator": "lobster_report",
  "levels": [
    {
      "name": "Code",
      "kind": "implementation",
      "items": [
        {
          "tag": "python software.Example",
          "location": {
            "kind": "file",
            "file": "./software.py",
            "line": 1,
            "column": null
          },
          "name": "software.Example",
          "messages": [
            "tracing destination python software.Example is unversioned"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "python software.Example@1.0"
          ],
          "ref_down": [
            "python software.Example"
          ],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Function"
        }
      ],
      "coverage": 0.0
    }
  ],
  "policy": {
    "Code": {
      "name": "Code",
      "kind": "implementation",
      "traces": [],
      "source": [
        {
          "file": "python_unversioned_trace_dest.lobster"
        }
      ],
      "needs_tracing_up": false,
      "needs_tracing_down": false,
      "breakdown_requirements": []
    }
  },
  "matrix": []
}
