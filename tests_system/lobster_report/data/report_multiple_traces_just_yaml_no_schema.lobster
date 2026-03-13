{
  "schema": "lobster-report",
  "version": 2,
  "generator": "lobster_report",
  "levels": [
    {
      "name": "Requirements",
      "items": [
        {
          "tag": "itm example.vehicle",
          "location": {
            "kind": "file",
            "file": "demo.trlc",
            "line": 3,
            "column": 13
          },
          "name": "example.vehicle",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "itm vehicle_implementation.StupidVehicle.vehicle_exists",
            "itm vehicle_implementation.StupidVehicle.run_vehicle_diagnostics",
            "itm test_vehicle_implementation.TestStupidVehicle.test_vehicle_exists:25",
            "itm test_vehicle_implementation.TestStupidVehicle.test_full_vehicle_diagnostics:150"
          ],
          "tracing_status": "OK"
        },
        {
          "tag": "itm example.engine",
          "location": {
            "kind": "file",
            "file": "demo.trlc",
            "line": 7,
            "column": 13
          },
          "name": "example.engine",
          "messages": [],
          "just_up": [
            "Not applicable everywhere"
          ],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "itm vehicle_implementation.StupidVehicle.run_engine",
            "itm vehicle_implementation.StupidVehicle.comprehensive_system_check",
            "itm vehicle_implementation.StupidVehicle.run_vehicle_diagnostics",
            "itm test_vehicle_implementation.TestStupidVehicle.test_engine_functionality:31",
            "itm test_vehicle_implementation.TestStupidVehicle.test_comprehensive_system_check:135",
            "itm test_vehicle_implementation.TestStupidVehicle.test_full_vehicle_diagnostics:150",
            "itm test_vehicle_implementation.TestVehicleIntegration.test_engine_fuel_integration:172",
            "itm test_vehicle_implementation.TestVehicleIntegration.test_mobility_systems_integration:196"
          ],
          "tracing_status": "JUSTIFIED"
        },
        {
          "tag": "itm example.safety_system",
          "location": {
            "kind": "file",
            "file": "demo.trlc",
            "line": 12,
            "column": 13
          },
          "name": "example.safety_system",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "itm vehicle_implementation.StupidVehicle.activate_safety_system",
            "itm vehicle_implementation.StupidVehicle.comprehensive_system_check",
            "itm vehicle_implementation.StupidVehicle.run_vehicle_diagnostics",
            "itm test_vehicle_implementation.TestStupidVehicle.test_safety_system_activation:45",
            "itm test_vehicle_implementation.TestStupidVehicle.test_comprehensive_system_check:135",
            "itm test_vehicle_implementation.TestStupidVehicle.test_full_vehicle_diagnostics:150",
            "itm test_vehicle_implementation.TestVehicleIntegration.test_safety_electrical_integration:185"
          ],
          "tracing_status": "OK"
        },
        {
          "tag": "itm example.braking_system",
          "location": {
            "kind": "file",
            "file": "demo.trlc",
            "line": 16,
            "column": 13
          },
          "name": "example.braking_system",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "itm vehicle_implementation.StupidVehicle.apply_brakes",
            "itm test_vehicle_implementation.TestStupidVehicle.test_braking_system:51",
            "itm test_vehicle_implementation.TestStupidVehicle.test_full_vehicle_diagnostics:150",
            "itm test_vehicle_implementation.TestVehicleIntegration.test_mobility_systems_integration:196"
          ],
          "tracing_status": "OK"
        },
        {
          "tag": "itm example.electrical_system",
          "location": {
            "kind": "file",
            "file": "demo.trlc",
            "line": 20,
            "column": 13
          },
          "name": "example.electrical_system",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "itm vehicle_implementation.StupidVehicle.check_electrical_system",
            "itm vehicle_implementation.StupidVehicle.comprehensive_system_check",
            "itm test_vehicle_implementation.TestStupidVehicle.test_electrical_system:65",
            "itm test_vehicle_implementation.TestStupidVehicle.test_comprehensive_system_check:135",
            "itm test_vehicle_implementation.TestStupidVehicle.test_full_vehicle_diagnostics:150",
            "itm test_vehicle_implementation.TestVehicleIntegration.test_safety_electrical_integration:185"
          ],
          "tracing_status": "OK"
        },
        {
          "tag": "itm example.fuel_system",
          "location": {
            "kind": "file",
            "file": "demo.trlc",
            "line": 24,
            "column": 13
          },
          "name": "example.fuel_system",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "itm vehicle_implementation.StupidVehicle.operate_fuel_system",
            "itm vehicle_implementation.StupidVehicle.comprehensive_system_check",
            "itm test_vehicle_implementation.TestStupidVehicle.test_fuel_system_operation:77",
            "itm test_vehicle_implementation.TestStupidVehicle.test_comprehensive_system_check:135",
            "itm test_vehicle_implementation.TestStupidVehicle.test_full_vehicle_diagnostics:150",
            "itm test_vehicle_implementation.TestVehicleIntegration.test_engine_fuel_integration:172"
          ],
          "tracing_status": "OK"
        },
        {
          "tag": "itm example.transmission_system",
          "location": {
            "kind": "file",
            "file": "demo.trlc",
            "line": 28,
            "column": 13
          },
          "name": "example.transmission_system",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "itm vehicle_implementation.StupidVehicle.operate_transmission_system",
            "itm test_vehicle_implementation.TestStupidVehicle.test_transmission_system:90",
            "itm test_vehicle_implementation.TestStupidVehicle.test_full_vehicle_diagnostics:150",
            "itm test_vehicle_implementation.TestVehicleIntegration.test_mobility_systems_integration:196"
          ],
          "tracing_status": "OK"
        },
        {
          "tag": "itm example.steering_system",
          "location": {
            "kind": "file",
            "file": "demo.trlc",
            "line": 32,
            "column": 13
          },
          "name": "example.steering_system",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "itm vehicle_implementation.StupidVehicle.control_steering_system",
            "itm test_vehicle_implementation.TestStupidVehicle.test_steering_system:102",
            "itm test_vehicle_implementation.TestStupidVehicle.test_full_vehicle_diagnostics:150",
            "itm test_vehicle_implementation.TestVehicleIntegration.test_mobility_systems_integration:196"
          ],
          "tracing_status": "OK"
        },
        {
          "tag": "itm example.lighting_system",
          "location": {
            "kind": "file",
            "file": "demo.trlc",
            "line": 36,
            "column": 13
          },
          "name": "example.lighting_system",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "itm vehicle_implementation.StupidVehicle.operate_lighting_system",
            "itm test_vehicle_implementation.TestStupidVehicle.test_lighting_system:114",
            "itm test_vehicle_implementation.TestStupidVehicle.test_full_vehicle_diagnostics:150"
          ],
          "tracing_status": "OK"
        },
        {
          "tag": "itm example.climate_control",
          "location": {
            "kind": "file",
            "file": "demo.trlc",
            "line": 40,
            "column": 13
          },
          "name": "example.climate_control",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "itm vehicle_implementation.StupidVehicle.control_climate_system",
            "itm test_vehicle_implementation.TestStupidVehicle.test_climate_control:123",
            "itm test_vehicle_implementation.TestStupidVehicle.test_full_vehicle_diagnostics:150"
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
          "tag": "itm vehicle_implementation.StupidVehicle.vehicle_exists",
          "location": {
            "kind": "file",
            "file": "vehicle_implementation.py",
            "line": 24,
            "column": null
          },
          "name": "vehicle_implementation.StupidVehicle.vehicle_exists",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "itm example.vehicle"
          ],
          "ref_down": [],
          "tracing_status": "OK"
        },
        {
          "tag": "itm vehicle_implementation.StupidVehicle.run_engine",
          "location": {
            "kind": "file",
            "file": "vehicle_implementation.py",
            "line": 30,
            "column": null
          },
          "name": "vehicle_implementation.StupidVehicle.run_engine",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "itm example.engine"
          ],
          "ref_down": [],
          "tracing_status": "OK"
        },
        {
          "tag": "itm vehicle_implementation.StupidVehicle.activate_safety_system",
          "location": {
            "kind": "file",
            "file": "vehicle_implementation.py",
            "line": 43,
            "column": null
          },
          "name": "vehicle_implementation.StupidVehicle.activate_safety_system",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "itm example.safety_system"
          ],
          "ref_down": [],
          "tracing_status": "OK"
        },
        {
          "tag": "itm vehicle_implementation.StupidVehicle.apply_brakes",
          "location": {
            "kind": "file",
            "file": "vehicle_implementation.py",
            "line": 63,
            "column": null
          },
          "name": "vehicle_implementation.StupidVehicle.apply_brakes",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "itm example.braking_system"
          ],
          "ref_down": [],
          "tracing_status": "OK"
        },
        {
          "tag": "itm vehicle_implementation.StupidVehicle.check_electrical_system",
          "location": {
            "kind": "file",
            "file": "vehicle_implementation.py",
            "line": 84,
            "column": null
          },
          "name": "vehicle_implementation.StupidVehicle.check_electrical_system",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "itm example.electrical_system"
          ],
          "ref_down": [],
          "tracing_status": "OK"
        },
        {
          "tag": "itm vehicle_implementation.StupidVehicle.operate_fuel_system",
          "location": {
            "kind": "file",
            "file": "vehicle_implementation.py",
            "line": 101,
            "column": null
          },
          "name": "vehicle_implementation.StupidVehicle.operate_fuel_system",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "itm example.fuel_system"
          ],
          "ref_down": [],
          "tracing_status": "OK"
        },
        {
          "tag": "itm vehicle_implementation.StupidVehicle.operate_transmission_system",
          "location": {
            "kind": "file",
            "file": "vehicle_implementation.py",
            "line": 115,
            "column": null
          },
          "name": "vehicle_implementation.StupidVehicle.operate_transmission_system",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "itm example.transmission_system"
          ],
          "ref_down": [],
          "tracing_status": "OK"
        },
        {
          "tag": "itm vehicle_implementation.StupidVehicle.control_steering_system",
          "location": {
            "kind": "file",
            "file": "vehicle_implementation.py",
            "line": 131,
            "column": null
          },
          "name": "vehicle_implementation.StupidVehicle.control_steering_system",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "itm example.steering_system"
          ],
          "ref_down": [],
          "tracing_status": "OK"
        },
        {
          "tag": "itm vehicle_implementation.StupidVehicle.operate_lighting_system",
          "location": {
            "kind": "file",
            "file": "vehicle_implementation.py",
            "line": 150,
            "column": null
          },
          "name": "vehicle_implementation.StupidVehicle.operate_lighting_system",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "itm example.lighting_system"
          ],
          "ref_down": [],
          "tracing_status": "OK"
        },
        {
          "tag": "itm vehicle_implementation.StupidVehicle.control_climate_system",
          "location": {
            "kind": "file",
            "file": "vehicle_implementation.py",
            "line": 176,
            "column": null
          },
          "name": "vehicle_implementation.StupidVehicle.control_climate_system",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "itm example.climate_control"
          ],
          "ref_down": [],
          "tracing_status": "OK"
        },
        {
          "tag": "itm vehicle_implementation.StupidVehicle.comprehensive_system_check",
          "location": {
            "kind": "file",
            "file": "vehicle_implementation.py",
            "line": 203,
            "column": null
          },
          "name": "vehicle_implementation.StupidVehicle.comprehensive_system_check",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "itm example.safety_system",
            "itm example.fuel_system",
            "itm example.electrical_system",
            "itm example.engine"
          ],
          "ref_down": [],
          "tracing_status": "OK"
        },
        {
          "tag": "itm vehicle_implementation.StupidVehicle.run_vehicle_diagnostics",
          "location": {
            "kind": "file",
            "file": "vehicle_implementation.py",
            "line": 225,
            "column": null
          },
          "name": "vehicle_implementation.StupidVehicle.run_vehicle_diagnostics",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "itm example.safety_system",
            "itm example.engine",
            "itm example.vehicle"
          ],
          "ref_down": [],
          "tracing_status": "OK"
        }
      ],
      "coverage": 100.0
    },
    {
      "name": "Test",
      "items": [
        {
          "tag": "itm test_vehicle_implementation.TestStupidVehicle.test_vehicle_exists:25",
          "location": {
            "kind": "file",
            "file": "test_vehicle_implementation.py",
            "line": 25,
            "column": null
          },
          "name": "test_vehicle_implementation.TestStupidVehicle.test_vehicle_exists:25",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "itm example.vehicle"
          ],
          "ref_down": [],
          "tracing_status": "OK"
        },
        {
          "tag": "itm test_vehicle_implementation.TestStupidVehicle.test_engine_functionality:31",
          "location": {
            "kind": "file",
            "file": "test_vehicle_implementation.py",
            "line": 31,
            "column": null
          },
          "name": "test_vehicle_implementation.TestStupidVehicle.test_engine_functionality:31",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "itm example.engine"
          ],
          "ref_down": [],
          "tracing_status": "OK"
        },
        {
          "tag": "itm test_vehicle_implementation.TestStupidVehicle.test_safety_system_activation:45",
          "location": {
            "kind": "file",
            "file": "test_vehicle_implementation.py",
            "line": 45,
            "column": null
          },
          "name": "test_vehicle_implementation.TestStupidVehicle.test_safety_system_activation:45",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "itm example.safety_system"
          ],
          "ref_down": [],
          "tracing_status": "OK"
        },
        {
          "tag": "itm test_vehicle_implementation.TestStupidVehicle.test_braking_system:51",
          "location": {
            "kind": "file",
            "file": "test_vehicle_implementation.py",
            "line": 51,
            "column": null
          },
          "name": "test_vehicle_implementation.TestStupidVehicle.test_braking_system:51",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "itm example.braking_system"
          ],
          "ref_down": [],
          "tracing_status": "OK"
        },
        {
          "tag": "itm test_vehicle_implementation.TestStupidVehicle.test_electrical_system:65",
          "location": {
            "kind": "file",
            "file": "test_vehicle_implementation.py",
            "line": 65,
            "column": null
          },
          "name": "test_vehicle_implementation.TestStupidVehicle.test_electrical_system:65",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "itm example.electrical_system"
          ],
          "ref_down": [],
          "tracing_status": "OK"
        },
        {
          "tag": "itm test_vehicle_implementation.TestStupidVehicle.test_fuel_system_operation:77",
          "location": {
            "kind": "file",
            "file": "test_vehicle_implementation.py",
            "line": 77,
            "column": null
          },
          "name": "test_vehicle_implementation.TestStupidVehicle.test_fuel_system_operation:77",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "itm example.fuel_system"
          ],
          "ref_down": [],
          "tracing_status": "OK"
        },
        {
          "tag": "itm test_vehicle_implementation.TestStupidVehicle.test_transmission_system:90",
          "location": {
            "kind": "file",
            "file": "test_vehicle_implementation.py",
            "line": 90,
            "column": null
          },
          "name": "test_vehicle_implementation.TestStupidVehicle.test_transmission_system:90",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "itm example.transmission_system"
          ],
          "ref_down": [],
          "tracing_status": "OK"
        },
        {
          "tag": "itm test_vehicle_implementation.TestStupidVehicle.test_steering_system:102",
          "location": {
            "kind": "file",
            "file": "test_vehicle_implementation.py",
            "line": 102,
            "column": null
          },
          "name": "test_vehicle_implementation.TestStupidVehicle.test_steering_system:102",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "itm example.steering_system"
          ],
          "ref_down": [],
          "tracing_status": "OK"
        },
        {
          "tag": "itm test_vehicle_implementation.TestStupidVehicle.test_lighting_system:114",
          "location": {
            "kind": "file",
            "file": "test_vehicle_implementation.py",
            "line": 114,
            "column": null
          },
          "name": "test_vehicle_implementation.TestStupidVehicle.test_lighting_system:114",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "itm example.lighting_system"
          ],
          "ref_down": [],
          "tracing_status": "OK"
        },
        {
          "tag": "itm test_vehicle_implementation.TestStupidVehicle.test_climate_control:123",
          "location": {
            "kind": "file",
            "file": "test_vehicle_implementation.py",
            "line": 123,
            "column": null
          },
          "name": "test_vehicle_implementation.TestStupidVehicle.test_climate_control:123",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "itm example.climate_control"
          ],
          "ref_down": [],
          "tracing_status": "OK"
        },
        {
          "tag": "itm test_vehicle_implementation.TestStupidVehicle.test_comprehensive_system_check:135",
          "location": {
            "kind": "file",
            "file": "test_vehicle_implementation.py",
            "line": 135,
            "column": null
          },
          "name": "test_vehicle_implementation.TestStupidVehicle.test_comprehensive_system_check:135",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "itm example.safety_system",
            "itm example.fuel_system",
            "itm example.electrical_system",
            "itm example.engine"
          ],
          "ref_down": [],
          "tracing_status": "OK"
        },
        {
          "tag": "itm test_vehicle_implementation.TestStupidVehicle.test_full_vehicle_diagnostics:150",
          "location": {
            "kind": "file",
            "file": "test_vehicle_implementation.py",
            "line": 150,
            "column": null
          },
          "name": "test_vehicle_implementation.TestStupidVehicle.test_full_vehicle_diagnostics:150",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "itm example.climate_control",
            "itm example.lighting_system",
            "itm example.steering_system",
            "itm example.transmission_system",
            "itm example.fuel_system",
            "itm example.electrical_system",
            "itm example.braking_system",
            "itm example.safety_system",
            "itm example.engine",
            "itm example.vehicle"
          ],
          "ref_down": [],
          "tracing_status": "OK"
        },
        {
          "tag": "itm test_vehicle_implementation.TestVehicleIntegration.test_engine_fuel_integration:172",
          "location": {
            "kind": "file",
            "file": "test_vehicle_implementation.py",
            "line": 172,
            "column": null
          },
          "name": "test_vehicle_implementation.TestVehicleIntegration.test_engine_fuel_integration:172",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "itm example.fuel_system",
            "itm example.engine"
          ],
          "ref_down": [],
          "tracing_status": "OK"
        },
        {
          "tag": "itm test_vehicle_implementation.TestVehicleIntegration.test_safety_electrical_integration:185",
          "location": {
            "kind": "file",
            "file": "test_vehicle_implementation.py",
            "line": 185,
            "column": null
          },
          "name": "test_vehicle_implementation.TestVehicleIntegration.test_safety_electrical_integration:185",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "itm example.electrical_system",
            "itm example.safety_system"
          ],
          "ref_down": [],
          "tracing_status": "OK"
        },
        {
          "tag": "itm test_vehicle_implementation.TestVehicleIntegration.test_mobility_systems_integration:196",
          "location": {
            "kind": "file",
            "file": "test_vehicle_implementation.py",
            "line": 196,
            "column": null
          },
          "name": "test_vehicle_implementation.TestVehicleIntegration.test_mobility_systems_integration:196",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "itm example.braking_system",
            "itm example.steering_system",
            "itm example.transmission_system",
            "itm example.engine"
          ],
          "ref_down": [],
          "tracing_status": "OK"
        }
      ],
      "coverage": 100.0
    }
  ],
  "policy": {
    "Requirements": {
      "name": "Requirements",
      "traces": [],
      "source": [
        {
          "file": "just_requirements_no_schema.lobster"
        }
      ],
      "needs_tracing_up": false,
      "needs_tracing_down": true,
      "breakdown_requirements": [
        [
          "Code"
        ],
        [
          "Test"
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
          "file": "multiple_traces_code_no_schema.lobster"
        }
      ],
      "needs_tracing_up": true,
      "needs_tracing_down": false,
      "breakdown_requirements": []
    },
    "Test": {
      "name": "Test",
      "traces": [
        "Requirements"
      ],
      "source": [
        {
          "file": "multiple_traces_test_no_schema.lobster"
        }
      ],
      "needs_tracing_up": true,
      "needs_tracing_down": false,
      "breakdown_requirements": []
    }
  },
  "matrix": []
}
