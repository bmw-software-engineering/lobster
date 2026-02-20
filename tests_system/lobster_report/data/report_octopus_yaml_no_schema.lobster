{
  "schema": "lobster-report",
  "version": 2,
  "generator": "lobster_report",
  "levels": [
    {
      "name": "Requirements",
      "items": [
        {
          "tag": "req octopus_example.tentacle_coordination",
          "location": {
            "kind": "file",
            "file": "octopus_requirements1.trlc",
            "line": 4,
            "column": 28
          },
          "name": "octopus_example.tentacle_coordination",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "req octopus_example.tentacle_motor_control",
            "python tentacle_commander.TentacleCoordinator",
            "pyunit test_tentacle_commander.TestTentacleCoordinator.test_move_tentacles:18"
          ],
          "tracing_status": "OK"
        },
        {
          "tag": "req octopus_example.color_camouflage",
          "location": {
            "kind": "file",
            "file": "octopus_requirements2.trlc",
            "line": 8,
            "column": 29
          },
          "name": "octopus_example.color_camouflage",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "req octopus_example.chromatophore_processor",
            "python tentacle_commander.ColorCamouflage",
            "pyunit test_tentacle_commander.TestColorCamouflage.test_change_color_coral:28",
            "pyunit test_tentacle_commander.TestColorCamouflage.test_change_color_sand:33"
          ],
          "tracing_status": "OK"
        },
        {
          "tag": "req octopus_example.ink_defense",
          "location": {
            "kind": "file",
            "file": "octopus_requirements3.trlc",
            "line": 12,
            "column": 30
          },
          "name": "octopus_example.ink_defense",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "req octopus_example.ink_sac_trigger",
            "python tentacle_commander.InkDefense",
            "pyunit test_tentacle_commander.TestInkDefense.test_deploy_ink:42"
          ],
          "tracing_status": "OK"
        },
        {
          "tag": "req octopus_example.prey_detection",
          "location": {
            "kind": "file",
            "file": "octopus_requirements4.trlc",
            "line": 16,
            "column": 40
          },
          "name": "octopus_example.prey_detection",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "req octopus_example.vision_processing_unit",
            "python tentacle_commander.PreyDetection",
            "pyunit test_tentacle_commander.TestPreyDetection.test_scan_for_prey:52"
          ],
          "tracing_status": "OK"
        },
        {
          "tag": "req octopus_example.tentacle_motor_control",
          "location": {
            "kind": "file",
            "file": "octopus_requirements.trlc",
            "line": 20,
            "column": 30
          },
          "name": "octopus_example.tentacle_motor_control",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req octopus_example.tentacle_coordination"
          ],
          "ref_down": [
            "python tentacle_toolkit.MotorController",
            "pyunit test_tentacle_toolkit.TestMotorController.test_control_motors:18"
          ],
          "tracing_status": "OK"
        },
        {
          "tag": "req octopus_example.chromatophore_processor",
          "location": {
            "kind": "file",
            "file": "octopus_requirements.trlc",
            "line": 25,
            "column": 30
          },
          "name": "octopus_example.chromatophore_processor",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req octopus_example.color_camouflage"
          ],
          "ref_down": [
            "python tentacle_toolkit.ColorProcessor",
            "pyunit test_tentacle_toolkit.TestColorProcessor.test_process_color_change:28"
          ],
          "tracing_status": "OK"
        },
        {
          "tag": "req octopus_example.ink_sac_trigger",
          "location": {
            "kind": "file",
            "file": "octopus_requirements.trlc",
            "line": 30,
            "column": 30
          },
          "name": "octopus_example.ink_sac_trigger",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req octopus_example.ink_defense"
          ],
          "ref_down": [
            "python tentacle_toolkit.InkTrigger",
            "pyunit test_tentacle_toolkit.TestInkTrigger.test_trigger_ink_release:38"
          ],
          "tracing_status": "OK"
        },
        {
          "tag": "req octopus_example.vision_processing_unit",
          "location": {
            "kind": "file",
            "file": "octopus_requirements.trlc",
            "line": 35,
            "column": 30
          },
          "name": "octopus_example.vision_processing_unit",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req octopus_example.prey_detection"
          ],
          "ref_down": [
            "python tentacle_toolkit.VisionProcessor",
            "pyunit test_tentacle_toolkit.TestVisionProcessor.test_process_vision:48"
          ],
          "tracing_status": "OK"
        }
      ],
      "coverage": 100.0
    },
    {
      "name": "Code",
      "items": [
        {
          "tag": "python tentacle_commander.TentacleCoordinator",
          "location": {
            "kind": "file",
            "file": "tentacle_commander.py",
            "line": 7,
            "column": null
          },
          "name": "tentacle_commander.TentacleCoordinator",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req octopus_example.tentacle_coordination"
          ],
          "ref_down": [],
          "tracing_status": "OK"
        },
        {
          "tag": "python tentacle_commander.ColorCamouflage",
          "location": {
            "kind": "file",
            "file": "tentacle_commander.py",
            "line": 14,
            "column": null
          },
          "name": "tentacle_commander.ColorCamouflage",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req octopus_example.color_camouflage"
          ],
          "ref_down": [],
          "tracing_status": "OK"
        },
        {
          "tag": "python tentacle_commander.InkDefense",
          "location": {
            "kind": "file",
            "file": "tentacle_commander.py",
            "line": 22,
            "column": null
          },
          "name": "tentacle_commander.InkDefense",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req octopus_example.ink_defense"
          ],
          "ref_down": [],
          "tracing_status": "OK"
        },
        {
          "tag": "python tentacle_commander.PreyDetection",
          "location": {
            "kind": "file",
            "file": "tentacle_commander.py",
            "line": 29,
            "column": null
          },
          "name": "tentacle_commander.PreyDetection",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req octopus_example.prey_detection"
          ],
          "ref_down": [],
          "tracing_status": "OK"
        },
        {
          "tag": "python tentacle_commander.DenSecurity",
          "location": {
            "kind": "file",
            "file": "tentacle_commander.py",
            "line": 37,
            "column": null
          },
          "name": "tentacle_commander.DenSecurity",
          "messages": [
            "unknown tracing target req octopus_example.den_security",
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING"
        },
        {
          "tag": "python tentacle_toolkit.MotorController",
          "location": {
            "kind": "file",
            "file": "tentacle_toolkit.py",
            "line": 7,
            "column": null
          },
          "name": "tentacle_toolkit.MotorController",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req octopus_example.tentacle_motor_control"
          ],
          "ref_down": [],
          "tracing_status": "OK"
        },
        {
          "tag": "python tentacle_toolkit.ColorProcessor",
          "location": {
            "kind": "file",
            "file": "tentacle_toolkit.py",
            "line": 14,
            "column": null
          },
          "name": "tentacle_toolkit.ColorProcessor",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req octopus_example.chromatophore_processor"
          ],
          "ref_down": [],
          "tracing_status": "OK"
        },
        {
          "tag": "python tentacle_toolkit.InkTrigger",
          "location": {
            "kind": "file",
            "file": "tentacle_toolkit.py",
            "line": 21,
            "column": null
          },
          "name": "tentacle_toolkit.InkTrigger",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req octopus_example.ink_sac_trigger"
          ],
          "ref_down": [],
          "tracing_status": "OK"
        },
        {
          "tag": "python tentacle_toolkit.VisionProcessor",
          "location": {
            "kind": "file",
            "file": "tentacle_toolkit.py",
            "line": 28,
            "column": null
          },
          "name": "tentacle_toolkit.VisionProcessor",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req octopus_example.vision_processing_unit"
          ],
          "ref_down": [],
          "tracing_status": "OK"
        },
        {
          "tag": "python tentacle_toolkit.ConstructionPlanner",
          "location": {
            "kind": "file",
            "file": "tentacle_toolkit.py",
            "line": 36,
            "column": null
          },
          "name": "tentacle_toolkit.ConstructionPlanner",
          "messages": [
            "unknown tracing target req octopus_example.rock_arrangement_planner",
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING"
        }
      ],
      "coverage": 80.0
    },
    {
      "name": "test",
      "items": [
        {
          "tag": "pyunit test_tentacle_commander.TestTentacleCoordinator.test_move_tentacles:18",
          "location": {
            "kind": "file",
            "file": "test_tentacle_commander.py",
            "line": 18,
            "column": null
          },
          "name": "test_tentacle_commander.TestTentacleCoordinator.test_move_tentacles:18",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req octopus_example.tentacle_coordination"
          ],
          "ref_down": [],
          "tracing_status": "OK"
        },
        {
          "tag": "pyunit test_tentacle_commander.TestColorCamouflage.test_change_color_coral:28",
          "location": {
            "kind": "file",
            "file": "test_tentacle_commander.py",
            "line": 28,
            "column": null
          },
          "name": "test_tentacle_commander.TestColorCamouflage.test_change_color_coral:28",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req octopus_example.color_camouflage"
          ],
          "ref_down": [],
          "tracing_status": "OK"
        },
        {
          "tag": "pyunit test_tentacle_commander.TestColorCamouflage.test_change_color_sand:33",
          "location": {
            "kind": "file",
            "file": "test_tentacle_commander.py",
            "line": 33,
            "column": null
          },
          "name": "test_tentacle_commander.TestColorCamouflage.test_change_color_sand:33",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req octopus_example.color_camouflage"
          ],
          "ref_down": [],
          "tracing_status": "OK"
        },
        {
          "tag": "pyunit test_tentacle_commander.TestInkDefense.test_deploy_ink:42",
          "location": {
            "kind": "file",
            "file": "test_tentacle_commander.py",
            "line": 42,
            "column": null
          },
          "name": "test_tentacle_commander.TestInkDefense.test_deploy_ink:42",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req octopus_example.ink_defense"
          ],
          "ref_down": [],
          "tracing_status": "OK"
        },
        {
          "tag": "pyunit test_tentacle_commander.TestPreyDetection.test_scan_for_prey:52",
          "location": {
            "kind": "file",
            "file": "test_tentacle_commander.py",
            "line": 52,
            "column": null
          },
          "name": "test_tentacle_commander.TestPreyDetection.test_scan_for_prey:52",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req octopus_example.prey_detection"
          ],
          "ref_down": [],
          "tracing_status": "OK"
        },
        {
          "tag": "pyunit test_tentacle_commander.TestDenSecurity.test_secure_den:62",
          "location": {
            "kind": "file",
            "file": "test_tentacle_commander.py",
            "line": 62,
            "column": null
          },
          "name": "test_tentacle_commander.TestDenSecurity.test_secure_den:62",
          "messages": [
            "unknown tracing target req octopus_example.den_security",
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING"
        },
        {
          "tag": "pyunit test_tentacle_toolkit.TestMotorController.test_control_motors:18",
          "location": {
            "kind": "file",
            "file": "test_tentacle_toolkit.py",
            "line": 18,
            "column": null
          },
          "name": "test_tentacle_toolkit.TestMotorController.test_control_motors:18",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req octopus_example.tentacle_motor_control"
          ],
          "ref_down": [],
          "tracing_status": "OK"
        },
        {
          "tag": "pyunit test_tentacle_toolkit.TestColorProcessor.test_process_color_change:28",
          "location": {
            "kind": "file",
            "file": "test_tentacle_toolkit.py",
            "line": 28,
            "column": null
          },
          "name": "test_tentacle_toolkit.TestColorProcessor.test_process_color_change:28",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req octopus_example.chromatophore_processor"
          ],
          "ref_down": [],
          "tracing_status": "OK"
        },
        {
          "tag": "pyunit test_tentacle_toolkit.TestInkTrigger.test_trigger_ink_release:38",
          "location": {
            "kind": "file",
            "file": "test_tentacle_toolkit.py",
            "line": 38,
            "column": null
          },
          "name": "test_tentacle_toolkit.TestInkTrigger.test_trigger_ink_release:38",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req octopus_example.ink_sac_trigger"
          ],
          "ref_down": [],
          "tracing_status": "OK"
        },
        {
          "tag": "pyunit test_tentacle_toolkit.TestVisionProcessor.test_process_vision:48",
          "location": {
            "kind": "file",
            "file": "test_tentacle_toolkit.py",
            "line": 48,
            "column": null
          },
          "name": "test_tentacle_toolkit.TestVisionProcessor.test_process_vision:48",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req octopus_example.vision_processing_unit"
          ],
          "ref_down": [],
          "tracing_status": "OK"
        },
        {
          "tag": "pyunit test_tentacle_toolkit.TestConstructionPlanner.test_plan_construction:58",
          "location": {
            "kind": "file",
            "file": "test_tentacle_toolkit.py",
            "line": 58,
            "column": null
          },
          "name": "test_tentacle_toolkit.TestConstructionPlanner.test_plan_construction:58",
          "messages": [
            "unknown tracing target req octopus_example.rock_arrangement_planner",
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING"
        }
      ],
      "coverage": 81.81818181818181
    }
  ],
  "policy": {
    "Requirements": {
      "name": "Requirements",
      "traces": [],
      "source": [
        {
          "file": "octopus_system_no_schema.lobster"
        },
        {
          "file": "octopus_software_no_schema.lobster"
        }
      ],
      "needs_tracing_up": false,
      "needs_tracing_down": true,
      "breakdown_requirements": [
        [
          "Code"
        ],
        [
          "test"
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
          "file": "tentacle_commander_code_no_schema.lobster"
        },
        {
          "file": "tentacle_toolkit_code_no_schema.lobster"
        }
      ],
      "needs_tracing_up": true,
      "needs_tracing_down": false,
      "breakdown_requirements": []
    },
    "test": {
      "name": "test",
      "traces": [
        "Requirements"
      ],
      "source": [
        {
          "file": "tentacle_commander_test_no_schema.lobster"
        },
        {
          "file": "tentacle_toolkit_test_no_schema.lobster"
        }
      ],
      "needs_tracing_up": true,
      "needs_tracing_down": false,
      "breakdown_requirements": []
    }
  },
  "matrix": []
}
