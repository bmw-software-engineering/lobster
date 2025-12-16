{
  "schema": "lobster-report",
  "version": 2,
  "generator": "lobster_report",
  "levels": [
    {
      "name": "Code",
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
            "unknown tracing target req example.adas_100"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING"
        }
      ],
      "coverage": 0.0
    }
  ],
  "policy": {
    "Code": {
      "name": "Code",
      "traces": [],
      "source": [
        {
          "file": "python_unknown_tracing_target_no_schema.lobster"
        }
      ],
      "needs_tracing_up": false,
      "needs_tracing_down": false,
      "breakdown_requirements": []
    }
  },
  "matrix": []
}
