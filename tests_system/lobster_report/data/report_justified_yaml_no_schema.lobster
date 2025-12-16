{
  "schema": "lobster-report",
  "version": 2,
  "generator": "lobster_report",
  "levels": [
    {
      "name": "Requirements",
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
          "tracing_status": "JUSTIFIED"
        }
      ],
      "coverage": 100.0
    },
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
            "missing up reference"
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
    "Requirements": {
      "name": "Requirements",
      "traces": [],
      "source": [
        {
          "file": "trlc_justified_no_schema.lobster"
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
      "traces": [
        "Requirements"
      ],
      "source": [
        {
          "file": "python_justified_no_schema.lobster"
        }
      ],
      "needs_tracing_up": true,
      "needs_tracing_down": false,
      "breakdown_requirements": []
    }
  },
  "matrix": []
}
