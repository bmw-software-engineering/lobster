{
  "schema": "lobster-report",
  "version": 2,
  "generator": "lobster_report",
  "levels": [
    {
      "name": "Requirements",
      "kind": "requirements",
      "items": [
        {
          "tag": "req demo.covered",
          "location": {
            "kind": "file",
            "file": "demo.trlc",
            "line": 3,
            "column": 5
          },
          "name": "demo.covered",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "requirement",
          "text": "A fully covered requirement",
          "status": null
        },
        {
          "tag": "req demo.not_covered",
          "location": {
            "kind": "file",
            "file": "demo.trlc",
            "line": 8,
            "column": 5
          },
          "name": "demo.not_covered",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "requirement",
          "text": "A requirement without a test",
          "status": null
        }
      ],
      "coverage": 50.0
    }
  ],
  "policy": {
    "Requirements": {
      "name": "Requirements",
      "kind": "requirements",
      "traces": [],
      "source": [
        {
          "file": "demo.lobster"
        }
      ],
      "needs_tracing_up": false,
      "needs_tracing_down": false,
      "breakdown_requirements": []
    }
  },
  "matrix": []
}
