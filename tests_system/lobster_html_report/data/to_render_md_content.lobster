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
            "file": ".\\demo.trlc",
            "line": 3,
            "column": 13
          },
          "name": "example.adas_100_A",
          "messages": [
            "status is status1, expected abc or def",
            "missing reference to Code"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Requirement",
          "text": "# Test\n\n## List\n\n- first\n- second\n- third\n\n### Table\n\n|H1|H2|\n|-|-|\n|B1|B2|\n\n*italic*  \n**bold**",
          "status": "status1"
        }
      ],
      "coverage": 0.0
    },
    {
      "name": "Code",
      "kind": "implementation",
      "items": [
        {
          "tag": "python software.Example",
          "location": {
            "kind": "file",
            "file": ".\\software.py",
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
          "file": "requirements.lobster"
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
          "file": "code.lobster"
        }
      ],
      "needs_tracing_up": true,
      "needs_tracing_down": false,
      "breakdown_requirements": []
    }
  },
  "matrix": []
}
