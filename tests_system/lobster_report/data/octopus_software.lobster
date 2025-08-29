{
  "data": [
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
      "refs": [
        "req octopus_example.tentacle_coordination"
      ],
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
      "refs": [
        "req octopus_example.color_camouflage"
      ],
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
      "refs": [
        "req octopus_example.ink_defense"
      ],
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
      "refs": [
        "req octopus_example.prey_detection"
      ],
      "framework": "TRLC",
      "kind": "software_requirement",
      "text": "The software shall process multiple camera feeds for 360-degree underwater vision",
      "status": null
    }
  ],
  "generator": "lobster-trlc",
  "schema": "lobster-req-trace",
  "version": 4
}
