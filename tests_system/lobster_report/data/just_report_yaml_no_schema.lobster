{
  "schema": "lobster-report",
  "version": 2,
  "generator": "lobster_report",
  "levels": [
    {
      "name": "usecases",
      "items": [
        {
          "tag": "req complex_just_example.lost_sock_scenario",
          "location": {
            "kind": "file",
            "file": "just_requirements.trlc",
            "line": 4,
            "column": 22
          },
          "name": "complex_just_example.lost_sock_scenario",
          "messages": [
            "missing reference to System Requirements"
          ],
          "just_up": [
            "Not applicable up reference"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING"
        },
        {
          "tag": "req complex_just_example.monday_motivation_scenario",
          "location": {
            "kind": "file",
            "file": "just_requirements.trlc",
            "line": 9,
            "column": 22
          },
          "name": "complex_just_example.monday_motivation_scenario",
          "messages": [],
          "just_up": [],
          "just_down": [
            "Not applicable down reference"
          ],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "req complex_just_example.monday_mood"
          ],
          "tracing_status": "JUSTIFIED"
        },
        {
          "tag": "req complex_just_example.pizza_waiting_scenario",
          "location": {
            "kind": "file",
            "file": "just_requirements.trlc",
            "line": 14,
            "column": 22
          },
          "name": "complex_just_example.pizza_waiting_scenario",
          "messages": [],
          "just_up": [],
          "just_down": [
            "Not applicable down reference"
          ],
          "just_global": [],
          "tracing_status": "JUSTIFIED"
        },
        {
          "tag": "req complex_just_example.cat_communication_scenario",
          "location": {
            "kind": "file",
            "file": "just_requirements.trlc",
            "line": 19,
            "column": 22
          },
          "name": "complex_just_example.cat_communication_scenario",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [
            "Not applicable up and down reference"
          ],
          "tracing_status": "JUSTIFIED"
        },
        {
          "tag": "req complex_just_example.remote_hunting_scenario",
          "location": {
            "kind": "file",
            "file": "just_requirements.trlc",
            "line": 24,
            "column": 22
          },
          "name": "complex_just_example.remote_hunting_scenario",
          "messages": [],
          "just_up": [
            "Not applicable up reference"
          ],
          "just_down": [
            "Not applicable down reference"
          ],
          "just_global": [],
          "tracing_status": "JUSTIFIED"
        },
        {
          "tag": "req complex_just_example.sadness_relief_scenario",
          "location": {
            "kind": "file",
            "file": "just_requirements.trlc",
            "line": 30,
            "column": 22
          },
          "name": "complex_just_example.sadness_relief_scenario",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "req complex_just_example.joke_generator"
          ],
          "tracing_status": "OK"
        },
        {
          "tag": "req complex_just_example.midnight_snack_temptation_scenario",
          "location": {
            "kind": "file",
            "file": "just_requirements.trlc",
            "line": 34,
            "column": 22
          },
          "name": "complex_just_example.midnight_snack_temptation_scenario",
          "messages": [
            "missing reference to System Requirements"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING"
        }
      ],
      "coverage": 71.42857142857143
    },
    {
      "name": "System Requirements",
      "items": [
        {
          "tag": "req complex_just_example.sock_finder",
          "location": {
            "kind": "file",
            "file": "just_requirements.trlc",
            "line": 38,
            "column": 33
          },
          "name": "complex_just_example.sock_finder",
          "messages": [
            "missing reference to Software Requirements"
          ],
          "just_up": [
            "Not applicable up reference"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "PARTIAL"
        },
        {
          "tag": "req complex_just_example.monday_mood",
          "location": {
            "kind": "file",
            "file": "just_requirements.trlc",
            "line": 43,
            "column": 33
          },
          "name": "complex_just_example.monday_mood",
          "messages": [],
          "just_up": [],
          "just_down": [
            "Not applicable down reference"
          ],
          "just_global": [],
          "ref_up": [
            "req complex_just_example.monday_motivation_scenario"
          ],
          "ref_down": [],
          "tracing_status": "JUSTIFIED"
        },
        {
          "tag": "req complex_just_example.pizza_detector",
          "location": {
            "kind": "file",
            "file": "just_requirements.trlc",
            "line": 49,
            "column": 33
          },
          "name": "complex_just_example.pizza_detector",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [
            "Not applicable down reference"
          ],
          "just_global": [],
          "tracing_status": "PARTIAL"
        },
        {
          "tag": "req complex_just_example.cat_translator",
          "location": {
            "kind": "file",
            "file": "just_requirements.trlc",
            "line": 54,
            "column": 33
          },
          "name": "complex_just_example.cat_translator",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [
            "Not applicable up and down reference"
          ],
          "tracing_status": "JUSTIFIED"
        },
        {
          "tag": "req complex_just_example.remote_locator",
          "location": {
            "kind": "file",
            "file": "just_requirements.trlc",
            "line": 59,
            "column": 33
          },
          "name": "complex_just_example.remote_locator",
          "messages": [],
          "just_up": [
            "Not applicable up reference"
          ],
          "just_down": [
            "Not applicable down reference"
          ],
          "just_global": [],
          "tracing_status": "JUSTIFIED"
        },
        {
          "tag": "req complex_just_example.joke_generator",
          "location": {
            "kind": "file",
            "file": "just_requirements.trlc",
            "line": 65,
            "column": 33
          },
          "name": "complex_just_example.joke_generator",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req complex_just_example.sadness_relief_scenario"
          ],
          "ref_down": [
            "req complex_just_example.pun_database"
          ],
          "tracing_status": "OK"
        },
        {
          "tag": "req complex_just_example.cookie_guard",
          "location": {
            "kind": "file",
            "file": "just_requirements.trlc",
            "line": 70,
            "column": 33
          },
          "name": "complex_just_example.cookie_guard",
          "messages": [
            "missing up reference",
            "missing reference to Software Requirements"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING"
        }
      ],
      "coverage": 57.142857142857146
    },
    {
      "name": "Software Requirements",
      "items": [
        {
          "tag": "req complex_just_example.sock_scanner",
          "location": {
            "kind": "file",
            "file": "just_requirements.trlc",
            "line": 74,
            "column": 35
          },
          "name": "complex_just_example.sock_scanner",
          "messages": [],
          "just_up": [
            "Not applicable up reference"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "JUSTIFIED"
        },
        {
          "tag": "req complex_just_example.mood_analyzer",
          "location": {
            "kind": "file",
            "file": "just_requirements.trlc",
            "line": 79,
            "column": 35
          },
          "name": "complex_just_example.mood_analyzer",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [
            "Not applicable down reference"
          ],
          "just_global": [],
          "tracing_status": "MISSING"
        },
        {
          "tag": "req complex_just_example.pizza_radar",
          "location": {
            "kind": "file",
            "file": "just_requirements.trlc",
            "line": 84,
            "column": 35
          },
          "name": "complex_just_example.pizza_radar",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [
            "Not applicable up and down reference"
          ],
          "tracing_status": "JUSTIFIED"
        },
        {
          "tag": "req complex_just_example.meow_processor",
          "location": {
            "kind": "file",
            "file": "just_requirements.trlc",
            "line": 89,
            "column": 35
          },
          "name": "complex_just_example.meow_processor",
          "messages": [],
          "just_up": [
            "Not applicable up reference"
          ],
          "just_down": [
            "Not applicable down reference"
          ],
          "just_global": [],
          "tracing_status": "JUSTIFIED"
        },
        {
          "tag": "req complex_just_example.pun_database",
          "location": {
            "kind": "file",
            "file": "just_requirements.trlc",
            "line": 95,
            "column": 35
          },
          "name": "complex_just_example.pun_database",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req complex_just_example.joke_generator"
          ],
          "ref_down": [],
          "tracing_status": "OK"
        },
        {
          "tag": "req complex_just_example.cushion_explorer",
          "location": {
            "kind": "file",
            "file": "just_requirements.trlc",
            "line": 100,
            "column": 35
          },
          "name": "complex_just_example.cushion_explorer",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING"
        }
      ],
      "coverage": 66.66666666666667
    }
  ],
  "policy": {
    "usecases": {
      "name": "usecases",
      "traces": [],
      "source": [
        {
          "file": "just_usecases_no_schema.lobster"
        }
      ],
      "needs_tracing_up": false,
      "needs_tracing_down": true,
      "breakdown_requirements": [
        [
          "System Requirements"
        ]
      ]
    },
    "System Requirements": {
      "name": "System Requirements",
      "traces": [
        "usecases"
      ],
      "source": [
        {
          "file": "just_system_requirements_no_schema.lobster"
        }
      ],
      "needs_tracing_up": true,
      "needs_tracing_down": true,
      "breakdown_requirements": [
        [
          "Software Requirements"
        ]
      ]
    },
    "Software Requirements": {
      "name": "Software Requirements",
      "traces": [
        "System Requirements"
      ],
      "source": [
        {
          "file": "just_software_requirements_no_schema.lobster"
        }
      ],
      "needs_tracing_up": true,
      "needs_tracing_down": false,
      "breakdown_requirements": []
    }
  },
  "matrix": []
}
