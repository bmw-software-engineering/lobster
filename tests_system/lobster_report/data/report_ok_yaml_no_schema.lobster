{
  "schema": "lobster-report",
  "version": 2,
  "generator": "lobster_report",
  "levels": [
    {
      "name": "Requirements",
      "items": [
        {
          "tag": "req example.vehicle",
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
            "python vehicle_implementation.StupidVehicle.vehicle_exists"
          ],
          "tracing_status": "OK"
        },
        {
          "tag": "req example.engine",
          "location": {
            "kind": "file",
            "file": "demo.trlc",
            "line": 7,
            "column": 13
          },
          "name": "example.engine",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python vehicle_implementation.StupidVehicle.run_engine"
          ],
          "tracing_status": "OK"
        },
        {
          "tag": "req example.safety_system",
          "location": {
            "kind": "file",
            "file": "demo.trlc",
            "line": 11,
            "column": 13
          },
          "name": "example.safety_system",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python vehicle_implementation.StupidVehicle.activate_safety_system"
          ],
          "tracing_status": "OK"
        },
        {
          "tag": "req example.braking_system",
          "location": {
            "kind": "file",
            "file": "demo.trlc",
            "line": 15,
            "column": 13
          },
          "name": "example.braking_system",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python vehicle_implementation.StupidVehicle.apply_brakes"
          ],
          "tracing_status": "OK"
        },
        {
          "tag": "req example.electrical_system",
          "location": {
            "kind": "file",
            "file": "demo.trlc",
            "line": 19,
            "column": 13
          },
          "name": "example.electrical_system",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python vehicle_implementation.StupidVehicle.check_electrical_system"
          ],
          "tracing_status": "OK"
        },
        {
          "tag": "req example.fuel_system",
          "location": {
            "kind": "file",
            "file": "demo.trlc",
            "line": 23,
            "column": 13
          },
          "name": "example.fuel_system",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python vehicle_implementation.StupidVehicle.operate_fuel_system"
          ],
          "tracing_status": "OK"
        },
        {
          "tag": "req example.transmission_system",
          "location": {
            "kind": "file",
            "file": "demo.trlc",
            "line": 27,
            "column": 13
          },
          "name": "example.transmission_system",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python vehicle_implementation.StupidVehicle.operate_transmission_system"
          ],
          "tracing_status": "OK"
        },
        {
          "tag": "req example.steering_system",
          "location": {
            "kind": "file",
            "file": "demo.trlc",
            "line": 31,
            "column": 13
          },
          "name": "example.steering_system",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python vehicle_implementation.StupidVehicle.control_steering_system"
          ],
          "tracing_status": "OK"
        },
        {
          "tag": "req example.lighting_system",
          "location": {
            "kind": "file",
            "file": "demo.trlc",
            "line": 35,
            "column": 13
          },
          "name": "example.lighting_system",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python vehicle_implementation.StupidVehicle.operate_lighting_system"
          ],
          "tracing_status": "OK"
        },
        {
          "tag": "req example.climate_control",
          "location": {
            "kind": "file",
            "file": "demo.trlc",
            "line": 39,
            "column": 13
          },
          "name": "example.climate_control",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python vehicle_implementation.StupidVehicle.control_climate_system"
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
          "tag": "python vehicle_implementation.StupidVehicle.vehicle_exists",
          "location": {
            "kind": "file",
            "file": "./vehicle_implementation.py",
            "line": 24,
            "column": null
          },
          "name": "vehicle_implementation.StupidVehicle.vehicle_exists",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req example.vehicle"
          ],
          "ref_down": [],
          "tracing_status": "OK"
        },
        {
          "tag": "python vehicle_implementation.StupidVehicle.run_engine",
          "location": {
            "kind": "file",
            "file": "./vehicle_implementation.py",
            "line": 30,
            "column": null
          },
          "name": "vehicle_implementation.StupidVehicle.run_engine",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req example.engine"
          ],
          "ref_down": [],
          "tracing_status": "OK"
        },
        {
          "tag": "python vehicle_implementation.StupidVehicle.activate_safety_system",
          "location": {
            "kind": "file",
            "file": "./vehicle_implementation.py",
            "line": 43,
            "column": null
          },
          "name": "vehicle_implementation.StupidVehicle.activate_safety_system",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req example.safety_system"
          ],
          "ref_down": [],
          "tracing_status": "OK"
        },
        {
          "tag": "python vehicle_implementation.StupidVehicle.apply_brakes",
          "location": {
            "kind": "file",
            "file": "./vehicle_implementation.py",
            "line": 63,
            "column": null
          },
          "name": "vehicle_implementation.StupidVehicle.apply_brakes",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req example.braking_system"
          ],
          "ref_down": [],
          "tracing_status": "OK"
        },
        {
          "tag": "python vehicle_implementation.StupidVehicle.check_electrical_system",
          "location": {
            "kind": "file",
            "file": "./vehicle_implementation.py",
            "line": 84,
            "column": null
          },
          "name": "vehicle_implementation.StupidVehicle.check_electrical_system",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req example.electrical_system"
          ],
          "ref_down": [],
          "tracing_status": "OK"
        },
        {
          "tag": "python vehicle_implementation.StupidVehicle.operate_fuel_system",
          "location": {
            "kind": "file",
            "file": "./vehicle_implementation.py",
            "line": 101,
            "column": null
          },
          "name": "vehicle_implementation.StupidVehicle.operate_fuel_system",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req example.fuel_system"
          ],
          "ref_down": [],
          "tracing_status": "OK"
        },
        {
          "tag": "python vehicle_implementation.StupidVehicle.operate_transmission_system",
          "location": {
            "kind": "file",
            "file": "./vehicle_implementation.py",
            "line": 115,
            "column": null
          },
          "name": "vehicle_implementation.StupidVehicle.operate_transmission_system",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req example.transmission_system"
          ],
          "ref_down": [],
          "tracing_status": "OK"
        },
        {
          "tag": "python vehicle_implementation.StupidVehicle.control_steering_system",
          "location": {
            "kind": "file",
            "file": "./vehicle_implementation.py",
            "line": 131,
            "column": null
          },
          "name": "vehicle_implementation.StupidVehicle.control_steering_system",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req example.steering_system"
          ],
          "ref_down": [],
          "tracing_status": "OK"
        },
        {
          "tag": "python vehicle_implementation.StupidVehicle.operate_lighting_system",
          "location": {
            "kind": "file",
            "file": "./vehicle_implementation.py",
            "line": 150,
            "column": null
          },
          "name": "vehicle_implementation.StupidVehicle.operate_lighting_system",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req example.lighting_system"
          ],
          "ref_down": [],
          "tracing_status": "OK"
        },
        {
          "tag": "python vehicle_implementation.StupidVehicle.control_climate_system",
          "location": {
            "kind": "file",
            "file": "./vehicle_implementation.py",
            "line": 176,
            "column": null
          },
          "name": "vehicle_implementation.StupidVehicle.control_climate_system",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req example.climate_control"
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
          "file": "trlc_ok_no_schema.lobster"
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
      "traces": [
        "Requirements"
      ],
      "source": [
        {
          "file": "python_ok_no_schema.lobster"
        }
      ],
      "needs_tracing_up": true,
      "needs_tracing_down": false,
      "breakdown_requirements": []
    }
  },
  "matrix": []
}
