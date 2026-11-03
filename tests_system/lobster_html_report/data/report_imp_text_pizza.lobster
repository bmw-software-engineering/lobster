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
          "tag": "req pizza.example",
          "location": {
            "kind": "file",
            "file": "pizza_requirements.trlc",
            "line": 1,
            "column": 1
          },
          "name": "pizza.example",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python pizza_implementation.OvenController.start_cooking"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "system_requirement",
          "text": "The oven shall cook pizza until it is ready.",
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
          "tag": "python pizza_implementation.OvenController.start_cooking",
          "location": {
            "kind": "file",
            "file": "pizza_implementation.py",
            "line": 10,
            "column": 5
          },
          "name": "pizza_implementation.OvenController.start_cooking",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req pizza.example"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Function",
          "text": "Starts the oven and cooks the pizza until it is ready."
        }
      ],
      "coverage": 100.0
    }
  ],
  "policy": {
    "Requirements": {
      "name": "Requirements",
      "kind": "requirements",
      "traces": [
        "Code"
      ],
      "source": [
        {
          "file": "pizza_requirements.trlc"
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
      "traces": [],
      "source": [
        {
          "file": "pizza_implementation.py"
        }
      ],
      "needs_tracing_up": true,
      "needs_tracing_down": false,
      "breakdown_requirements": []
    }
  },
  "matrix": []
}
