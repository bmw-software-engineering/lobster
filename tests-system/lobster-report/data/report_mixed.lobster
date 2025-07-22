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
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python software.Example"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Requirement",
          "text": "keep the vehicle in lane for A.",
          "status": null
        },
        {
          "tag": "req example.adas_100_B",
          "location": {
            "kind": "file",
            "file": "./demo.trlc",
            "line": 8,
            "column": 13
          },
          "name": "example.adas_100_B",
          "messages": [
            "missing reference to Code"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Requirement",
          "text": "keep the vehicle in lane for B.",
          "status": null
        }
      ],
      "coverage": 50.0
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
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req example.adas_100_A"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Function"
        }
      ],
      "coverage": 100.0
    }
  ],
  "policy": {
    "Requirements": {
      "name": "Requirements",
      "kind": "requirements",
      "traces": [],
      "source": [
        {
          "file": "trlc_mixed.lobster"
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
          "file": "python_mixed.lobster"
        }
      ],
      "needs_tracing_up": true,
      "needs_tracing_down": false,
      "breakdown_requirements": []
    }
  },
  "matrix": []
}
