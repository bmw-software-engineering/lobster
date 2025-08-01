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
          "tag": "req example.adas_100_A",
          "location": {
            "kind": "file",
            "file": "./demo.trlc",
            "line": 3,
            "column": 13
          },
          "name": "example.adas_100_A",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [
            "not linked"
          ],
          "tracing_status": "JUSTIFIED",
          "framework": "TRLC",
          "kind": "Requirement",
          "text": "keep the vehicle in lane.",
          "status": null
        }
      ],
      "coverage": 100.0
    },
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
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Function"
        }
      ],
      "coverage": 0.0
    }
  ],
  "policy": {
    "Requirements": {
      "name": "Requirements",
      "kind": "requirements",
      "traces": [],
      "source": [
        {
          "file": "trlc_justified.lobster"
        }
      ],
      "needs_tracing_up": false,
      "needs_tracing_down": true,
      "breakdown_requirements": [
        [
          "Code"
        ]
      ]
    },
    "Code": {
      "name": "Code",
      "kind": "implementation",
      "traces": [
        "Requirements"
      ],
      "source": [
        {
          "file": "python_justified.lobster"
        }
      ],
      "needs_tracing_up": true,
      "needs_tracing_down": false,
      "breakdown_requirements": []
    }
  },
  "matrix": []
}
