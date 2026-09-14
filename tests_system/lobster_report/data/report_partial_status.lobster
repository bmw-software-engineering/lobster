{
  "schema": "lobster-report",
  "version": 2,
  "generator": "lobster_report",
  "levels": [
    {
      "name": "Requirements",
      "kind": "requirements",
      "items": [],
      "coverage": 0.0
    },
    {
      "name": "MidReqs",
      "kind": "requirements",
      "items": [
        {
          "tag": "req example.mid_level_only_justified_up",
          "location": {
            "kind": "file",
            "file": "mid.trlc",
            "line": 3,
            "column": 13
          },
          "name": "example.mid_level_only_justified_up",
          "messages": [
            "missing reference to Code"
          ],
          "just_up": [
            "not derived from a top-level requirement yet"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "PARTIAL",
          "framework": "TRLC",
          "kind": "requirement",
          "text": "This mid-level item only justifies its up reference.",
          "status": null
        }
      ],
      "coverage": 0.0
    },
    {
      "name": "Code",
      "kind": "implementation",
      "items": [],
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
          "file": "partial_status_requirements.lobster"
        }
      ],
      "needs_tracing_up": false,
      "needs_tracing_down": true,
      "breakdown_requirements": [
        [
          "MidReqs"
        ]
      ]
    },
    "MidReqs": {
      "name": "MidReqs",
      "kind": "requirements",
      "traces": [
        "Requirements"
      ],
      "source": [
        {
          "file": "partial_status_midreqs.lobster"
        }
      ],
      "needs_tracing_up": true,
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
        "MidReqs"
      ],
      "source": [
        {
          "file": "partial_status_code.lobster"
        }
      ],
      "needs_tracing_up": true,
      "needs_tracing_down": false,
      "breakdown_requirements": []
    }
  },
  "matrix": []
}
