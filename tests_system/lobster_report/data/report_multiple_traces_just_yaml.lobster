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
            "python vehicle_implementation.StupidVehicle.vehicle_exists",
            "python vehicle_implementation.StupidVehicle.run_vehicle_diagnostics",
            "pyunit test_vehicle_implementation.TestStupidVehicle.test_vehicle_exists:25",
            "pyunit test_vehicle_implementation.TestStupidVehicle.test_full_vehicle_diagnostics:150"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "requirement",
          "text": "This is a requirement for vehicle",
          "status": null
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
          "just_up": [
            "Not applicable everywhere"
          ],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python vehicle_implementation.StupidVehicle.run_engine",
            "python vehicle_implementation.StupidVehicle.comprehensive_system_check",
            "python vehicle_implementation.StupidVehicle.run_vehicle_diagnostics",
            "pyunit test_vehicle_implementation.TestStupidVehicle.test_engine_functionality:31",
            "pyunit test_vehicle_implementation.TestStupidVehicle.test_comprehensive_system_check:135",
            "pyunit test_vehicle_implementation.TestStupidVehicle.test_full_vehicle_diagnostics:150",
            "pyunit test_vehicle_implementation.TestVehicleIntegration.test_engine_fuel_integration:172",
            "pyunit test_vehicle_implementation.TestVehicleIntegration.test_mobility_systems_integration:196"
          ],
          "tracing_status": "JUSTIFIED",
          "framework": "TRLC",
          "kind": "requirement",
          "text": "The vehicle shall have an efficient engine system",
          "status": null
        },
        {
          "tag": "req example.safety_system",
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
            "python vehicle_implementation.StupidVehicle.activate_safety_system",
            "python vehicle_implementation.StupidVehicle.comprehensive_system_check",
            "python vehicle_implementation.StupidVehicle.run_vehicle_diagnostics",
            "pyunit test_vehicle_implementation.TestStupidVehicle.test_safety_system_activation:45",
            "pyunit test_vehicle_implementation.TestStupidVehicle.test_comprehensive_system_check:135",
            "pyunit test_vehicle_implementation.TestStupidVehicle.test_full_vehicle_diagnostics:150",
            "pyunit test_vehicle_implementation.TestVehicleIntegration.test_safety_electrical_integration:185"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "requirement",
          "text": "The vehicle shall include comprehensive safety features",
          "status": null
        },
        {
          "tag": "req example.braking_system",
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
            "python vehicle_implementation.StupidVehicle.apply_brakes",
            "pyunit test_vehicle_implementation.TestStupidVehicle.test_braking_system:51",
            "pyunit test_vehicle_implementation.TestStupidVehicle.test_full_vehicle_diagnostics:150",
            "pyunit test_vehicle_implementation.TestVehicleIntegration.test_mobility_systems_integration:196"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "requirement",
          "text": "The vehicle shall have responsive braking capability",
          "status": null
        },
        {
          "tag": "req example.electrical_system",
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
            "python vehicle_implementation.StupidVehicle.check_electrical_system",
            "python vehicle_implementation.StupidVehicle.comprehensive_system_check",
            "pyunit test_vehicle_implementation.TestStupidVehicle.test_electrical_system:65",
            "pyunit test_vehicle_implementation.TestStupidVehicle.test_comprehensive_system_check:135",
            "pyunit test_vehicle_implementation.TestStupidVehicle.test_full_vehicle_diagnostics:150",
            "pyunit test_vehicle_implementation.TestVehicleIntegration.test_safety_electrical_integration:185"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "requirement",
          "text": "The vehicle shall have reliable electrical components",
          "status": null
        },
        {
          "tag": "req example.fuel_system",
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
            "python vehicle_implementation.StupidVehicle.operate_fuel_system",
            "python vehicle_implementation.StupidVehicle.comprehensive_system_check",
            "pyunit test_vehicle_implementation.TestStupidVehicle.test_fuel_system_operation:77",
            "pyunit test_vehicle_implementation.TestStupidVehicle.test_comprehensive_system_check:135",
            "pyunit test_vehicle_implementation.TestStupidVehicle.test_full_vehicle_diagnostics:150",
            "pyunit test_vehicle_implementation.TestVehicleIntegration.test_engine_fuel_integration:172"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "requirement",
          "text": "The vehicle shall have efficient fuel delivery",
          "status": null
        },
        {
          "tag": "req example.transmission_system",
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
            "python vehicle_implementation.StupidVehicle.operate_transmission_system",
            "pyunit test_vehicle_implementation.TestStupidVehicle.test_transmission_system:90",
            "pyunit test_vehicle_implementation.TestStupidVehicle.test_full_vehicle_diagnostics:150",
            "pyunit test_vehicle_implementation.TestVehicleIntegration.test_mobility_systems_integration:196"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "requirement",
          "text": "The vehicle shall have a smooth gear transmission system",
          "status": null
        },
        {
          "tag": "req example.steering_system",
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
            "python vehicle_implementation.StupidVehicle.control_steering_system",
            "pyunit test_vehicle_implementation.TestStupidVehicle.test_steering_system:102",
            "pyunit test_vehicle_implementation.TestStupidVehicle.test_full_vehicle_diagnostics:150",
            "pyunit test_vehicle_implementation.TestVehicleIntegration.test_mobility_systems_integration:196"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "requirement",
          "text": "The vehicle shall have precise steering control",
          "status": null
        },
        {
          "tag": "req example.lighting_system",
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
            "python vehicle_implementation.StupidVehicle.operate_lighting_system",
            "pyunit test_vehicle_implementation.TestStupidVehicle.test_lighting_system:114",
            "pyunit test_vehicle_implementation.TestStupidVehicle.test_full_vehicle_diagnostics:150"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "requirement",
          "text": "The vehicle shall have functional headlights and taillights",
          "status": null
        },
        {
          "tag": "req example.climate_control",
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
            "python vehicle_implementation.StupidVehicle.control_climate_system",
            "pyunit test_vehicle_implementation.TestStupidVehicle.test_climate_control:123",
            "pyunit test_vehicle_implementation.TestStupidVehicle.test_full_vehicle_diagnostics:150"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "requirement",
          "text": "The vehicle shall maintain comfortable cabin temperature",
          "status": null
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
            "req example.vehicle"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python vehicle_implementation.StupidVehicle.run_engine",
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
            "req example.engine"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python vehicle_implementation.StupidVehicle.activate_safety_system",
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
            "req example.safety_system"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python vehicle_implementation.StupidVehicle.apply_brakes",
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
            "req example.braking_system"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python vehicle_implementation.StupidVehicle.check_electrical_system",
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
            "req example.electrical_system"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python vehicle_implementation.StupidVehicle.operate_fuel_system",
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
            "req example.fuel_system"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python vehicle_implementation.StupidVehicle.operate_transmission_system",
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
            "req example.transmission_system"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python vehicle_implementation.StupidVehicle.control_steering_system",
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
            "req example.steering_system"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python vehicle_implementation.StupidVehicle.operate_lighting_system",
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
            "req example.lighting_system"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python vehicle_implementation.StupidVehicle.control_climate_system",
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
            "req example.climate_control"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python vehicle_implementation.StupidVehicle.comprehensive_system_check",
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
            "req example.safety_system",
            "req example.fuel_system",
            "req example.electrical_system",
            "req example.engine"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python vehicle_implementation.StupidVehicle.run_vehicle_diagnostics",
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
            "req example.safety_system",
            "req example.engine",
            "req example.vehicle"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        }
      ],
      "coverage": 100.0
    },
    {
      "name": "Test",
      "items": [
        {
          "tag": "pyunit test_vehicle_implementation.TestStupidVehicle.test_vehicle_exists:25",
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
            "req example.vehicle"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "PyUnit",
          "kind": "Test",
          "status": null
        },
        {
          "tag": "pyunit test_vehicle_implementation.TestStupidVehicle.test_engine_functionality:31",
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
            "req example.engine"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "PyUnit",
          "kind": "Test",
          "status": null
        },
        {
          "tag": "pyunit test_vehicle_implementation.TestStupidVehicle.test_safety_system_activation:45",
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
            "req example.safety_system"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "PyUnit",
          "kind": "Test",
          "status": null
        },
        {
          "tag": "pyunit test_vehicle_implementation.TestStupidVehicle.test_braking_system:51",
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
            "req example.braking_system"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "PyUnit",
          "kind": "Test",
          "status": null
        },
        {
          "tag": "pyunit test_vehicle_implementation.TestStupidVehicle.test_electrical_system:65",
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
            "req example.electrical_system"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "PyUnit",
          "kind": "Test",
          "status": null
        },
        {
          "tag": "pyunit test_vehicle_implementation.TestStupidVehicle.test_fuel_system_operation:77",
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
            "req example.fuel_system"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "PyUnit",
          "kind": "Test",
          "status": null
        },
        {
          "tag": "pyunit test_vehicle_implementation.TestStupidVehicle.test_transmission_system:90",
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
            "req example.transmission_system"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "PyUnit",
          "kind": "Test",
          "status": null
        },
        {
          "tag": "pyunit test_vehicle_implementation.TestStupidVehicle.test_steering_system:102",
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
            "req example.steering_system"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "PyUnit",
          "kind": "Test",
          "status": null
        },
        {
          "tag": "pyunit test_vehicle_implementation.TestStupidVehicle.test_lighting_system:114",
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
            "req example.lighting_system"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "PyUnit",
          "kind": "Test",
          "status": null
        },
        {
          "tag": "pyunit test_vehicle_implementation.TestStupidVehicle.test_climate_control:123",
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
            "req example.climate_control"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "PyUnit",
          "kind": "Test",
          "status": null
        },
        {
          "tag": "pyunit test_vehicle_implementation.TestStupidVehicle.test_comprehensive_system_check:135",
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
            "req example.safety_system",
            "req example.fuel_system",
            "req example.electrical_system",
            "req example.engine"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "PyUnit",
          "kind": "Test",
          "status": null
        },
        {
          "tag": "pyunit test_vehicle_implementation.TestStupidVehicle.test_full_vehicle_diagnostics:150",
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
            "req example.climate_control",
            "req example.lighting_system",
            "req example.steering_system",
            "req example.transmission_system",
            "req example.fuel_system",
            "req example.electrical_system",
            "req example.braking_system",
            "req example.safety_system",
            "req example.engine",
            "req example.vehicle"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "PyUnit",
          "kind": "Test",
          "status": null
        },
        {
          "tag": "pyunit test_vehicle_implementation.TestVehicleIntegration.test_engine_fuel_integration:172",
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
            "req example.fuel_system",
            "req example.engine"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "PyUnit",
          "kind": "Test",
          "status": null
        },
        {
          "tag": "pyunit test_vehicle_implementation.TestVehicleIntegration.test_safety_electrical_integration:185",
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
            "req example.electrical_system",
            "req example.safety_system"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "PyUnit",
          "kind": "Test",
          "status": null
        },
        {
          "tag": "pyunit test_vehicle_implementation.TestVehicleIntegration.test_mobility_systems_integration:196",
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
            "req example.braking_system",
            "req example.steering_system",
            "req example.transmission_system",
            "req example.engine"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "PyUnit",
          "kind": "Test",
          "status": null
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
          "file": "just_requirements.lobster"
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
          "file": "multiple_traces_code.lobster"
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
          "file": "multiple_traces_test.lobster"
        }
      ],
      "needs_tracing_up": true,
      "needs_tracing_down": false,
      "breakdown_requirements": []
    }
  },
  "matrix": []
}
