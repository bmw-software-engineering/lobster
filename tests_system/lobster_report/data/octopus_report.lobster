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
            "python test_tentacle_commander.TestTentacleCoordinator"
          ],
          "tracing_status": "OK",
          "framework": "TRLC1",
          "kind": "system_requirement1",
          "text": "The system shall coordinate all eight tentacles simultaneously without getting tangled",
          "status": null
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
            "python test_tentacle_commander.TestColorCamouflage"
          ],
          "tracing_status": "OK",
          "framework": "TRLC2",
          "kind": "system_requirement2",
          "text": "The system shall change colors instantly to blend with coral reefs and escape predators",
          "status": null
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
            "python test_tentacle_commander.TestInkDefense"
          ],
          "tracing_status": "OK",
          "framework": "TRLC3",
          "kind": "system_requirement3",
          "text": "The system shall deploy ink clouds as defensive countermeasure when threatened",
          "status": null
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
            "python test_tentacle_commander.TestPreyDetection"
          ],
          "tracing_status": "OK",
          "framework": "TRLC4",
          "kind": "system_requirement4",
          "text": "The system shall detect and track multiple prey items using advanced underwater vision",
          "status": null
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
            "python test_tentacle_toolkit.TestMotorController"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "software_requirement",
          "text": "The software shall implement motor control algorithms for independent tentacle movement",
          "status": null
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
            "python test_tentacle_toolkit.TestColorProcessor"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "software_requirement",
          "text": "The software shall process color-changing commands to chromatophore cells in real-time",
          "status": null
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
            "python test_tentacle_toolkit.TestInkTrigger"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "software_requirement",
          "text": "The software shall trigger ink sac release with precise timing and volume control",
          "status": null
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
            "python test_tentacle_toolkit.TestVisionProcessor"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "software_requirement",
          "text": "The software shall process multiple camera feeds for 360-degree underwater vision",
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
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Class"
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
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Class"
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
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Class"
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
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Class"
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
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Class"
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
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Class"
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
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Class"
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
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Class"
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
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Class"
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
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Class"
        }
      ],
      "coverage": 80.0
    },
    {
      "name": "test",
      "kind": "activity",
      "items": [
        {
          "tag": "python test_tentacle_commander.TestTentacleCoordinator",
          "location": {
            "kind": "file",
            "file": "test_tentacle_commander.py",
            "line": 14,
            "column": null
          },
          "name": "test_tentacle_commander.TestTentacleCoordinator",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req octopus_example.tentacle_coordination"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Class"
        },
        {
          "tag": "python test_tentacle_commander.TestColorCamouflage",
          "location": {
            "kind": "file",
            "file": "test_tentacle_commander.py",
            "line": 24,
            "column": null
          },
          "name": "test_tentacle_commander.TestColorCamouflage",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req octopus_example.color_camouflage"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Class"
        },
        {
          "tag": "python test_tentacle_commander.TestInkDefense",
          "location": {
            "kind": "file",
            "file": "test_tentacle_commander.py",
            "line": 38,
            "column": null
          },
          "name": "test_tentacle_commander.TestInkDefense",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req octopus_example.ink_defense"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Class"
        },
        {
          "tag": "python test_tentacle_commander.TestPreyDetection",
          "location": {
            "kind": "file",
            "file": "test_tentacle_commander.py",
            "line": 48,
            "column": null
          },
          "name": "test_tentacle_commander.TestPreyDetection",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req octopus_example.prey_detection"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Class"
        },
        {
          "tag": "python test_tentacle_commander.TestDenSecurity",
          "location": {
            "kind": "file",
            "file": "test_tentacle_commander.py",
            "line": 58,
            "column": null
          },
          "name": "test_tentacle_commander.TestDenSecurity",
          "messages": [
            "unknown tracing target req octopus_example.den_security",
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Class"
        },
        {
          "tag": "python test_tentacle_toolkit.TestMotorController",
          "location": {
            "kind": "file",
            "file": "test_tentacle_toolkit.py",
            "line": 14,
            "column": null
          },
          "name": "test_tentacle_toolkit.TestMotorController",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req octopus_example.tentacle_motor_control"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Class"
        },
        {
          "tag": "python test_tentacle_toolkit.TestColorProcessor",
          "location": {
            "kind": "file",
            "file": "test_tentacle_toolkit.py",
            "line": 24,
            "column": null
          },
          "name": "test_tentacle_toolkit.TestColorProcessor",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req octopus_example.chromatophore_processor"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Class"
        },
        {
          "tag": "python test_tentacle_toolkit.TestInkTrigger",
          "location": {
            "kind": "file",
            "file": "test_tentacle_toolkit.py",
            "line": 34,
            "column": null
          },
          "name": "test_tentacle_toolkit.TestInkTrigger",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req octopus_example.ink_sac_trigger"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Class"
        },
        {
          "tag": "python test_tentacle_toolkit.TestVisionProcessor",
          "location": {
            "kind": "file",
            "file": "test_tentacle_toolkit.py",
            "line": 44,
            "column": null
          },
          "name": "test_tentacle_toolkit.TestVisionProcessor",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req octopus_example.vision_processing_unit"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Class"
        },
        {
          "tag": "python test_tentacle_toolkit.TestConstructionPlanner",
          "location": {
            "kind": "file",
            "file": "test_tentacle_toolkit.py",
            "line": 54,
            "column": null
          },
          "name": "test_tentacle_toolkit.TestConstructionPlanner",
          "messages": [
            "unknown tracing target req octopus_example.rock_arrangement_planner",
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Class"
        }
      ],
      "coverage": 80.0
    }
  ],
  "policy": {
    "Requirements": {
      "name": "Requirements",
      "kind": "requirements",
      "traces": [],
      "source": [
        {
          "file": "octopus_system.lobster"
        },
        {
          "file": "octopus_software.lobster"
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
      "kind": "implementation",
      "traces": [
        "Requirements"
      ],
      "source": [
        {
          "file": "tentacle_commander_code.lobster"
        },
        {
          "file": "tentacle_toolkit_code.lobster"
        }
      ],
      "needs_tracing_up": true,
      "needs_tracing_down": false,
      "breakdown_requirements": []
    },
    "test": {
      "name": "test",
      "kind": "activity",
      "traces": [
        "Requirements"
      ],
      "source": [
        {
          "file": "tentacle_commander_test.lobster"
        },
        {
          "file": "tentacle_toolkit_test.lobster"
        }
      ],
      "needs_tracing_up": true,
      "needs_tracing_down": false,
      "breakdown_requirements": []
    }
  },
  "matrix": []
}
