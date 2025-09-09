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
          "tag": "req 1@100",
          "location": {
            "kind": "codebeamer",
            "cb_root": "https://localhost:8999",
            "tracker": 10000,
            "item": 1,
            "version": 100,
            "name": "Requirement 1: Dynamic name"
          },
          "name": "Requirement 1: Dynamic name",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python codebeamer_funny_impl.translate_dog_barking"
          ],
          "tracing_status": "OK",
          "framework": "codebeamer",
          "kind": "codebeamer item",
          "text": null,
          "status": "Status 1"
        },
        {
          "tag": "req 2@200",
          "location": {
            "kind": "codebeamer",
            "cb_root": "https://localhost:8999",
            "tracker": 20000,
            "item": 2,
            "version": 200,
            "name": "Requirement 2: Dynamic name"
          },
          "name": "Requirement 2: Dynamic name",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python codebeamer_funny_impl.organize_cloud_shapes"
          ],
          "tracing_status": "OK",
          "framework": "codebeamer",
          "kind": "codebeamer item",
          "text": null,
          "status": "Status 2"
        },
        {
          "tag": "req 3@300",
          "location": {
            "kind": "codebeamer",
            "cb_root": "https://localhost:8999",
            "tracker": 30000,
            "item": 3,
            "version": 300,
            "name": "Requirement 3: Dynamic name"
          },
          "name": "Requirement 3: Dynamic name",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python codebeamer_funny_impl.schedule_cat_meetings"
          ],
          "tracing_status": "OK",
          "framework": "codebeamer",
          "kind": "codebeamer item",
          "text": null,
          "status": "Status 3"
        },
        {
          "tag": "req 4@400",
          "location": {
            "kind": "codebeamer",
            "cb_root": "https://localhost:8999",
            "tracker": 40000,
            "item": 4,
            "version": 400,
            "name": "Requirement 4: Dynamic name"
          },
          "name": "Requirement 4: Dynamic name",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python codebeamer_funny_impl.calibrate_sandwich_perfection"
          ],
          "tracing_status": "OK",
          "framework": "codebeamer",
          "kind": "codebeamer item",
          "text": null,
          "status": "Status 4"
        }
      ],
      "coverage": 100.0
    },
    {
      "name": "Code",
      "kind": "implementation",
      "items": [
        {
          "tag": "python codebeamer_funny_impl.translate_dog_barking",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "abcdef1234567890abcdef1234567890abcdef12",
            "file": "codebeamer_funny_impl.py",
            "line": 6
          },
          "name": "codebeamer_funny_impl.translate_dog_barking",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req 1@100"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Function"
        },
        {
          "tag": "python codebeamer_funny_impl.organize_cloud_shapes",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "abcdef1234567890abcdef1234567890abcdef12",
            "file": "codebeamer_funny_impl.py",
            "line": 11
          },
          "name": "codebeamer_funny_impl.organize_cloud_shapes",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req 2@200"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Function"
        },
        {
          "tag": "python codebeamer_funny_impl.schedule_cat_meetings",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "abcdef1234567890abcdef1234567890abcdef12",
            "file": "codebeamer_funny_impl.py",
            "line": 16
          },
          "name": "codebeamer_funny_impl.schedule_cat_meetings",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req 3@300"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Function"
        },
        {
          "tag": "python codebeamer_funny_impl.calibrate_sandwich_perfection",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "abcdef1234567890abcdef1234567890abcdef12",
            "file": "codebeamer_funny_impl.py",
            "line": 21
          },
          "name": "codebeamer_funny_impl.calibrate_sandwich_perfection",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req 4@400"
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
          "file": "codebeamer_items.lobster"
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
          "file": "codebeamer_funny_impl.lobster"
        }
      ],
      "needs_tracing_up": true,
      "needs_tracing_down": false,
      "breakdown_requirements": []
    }
  },
  "matrix": []
}
