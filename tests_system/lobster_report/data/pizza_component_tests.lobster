{
  "data": [
    {
      "tag": "pyunit test_pizza_components.TestOrderProcessingComponent.test_complete_order_creation_workflow:26",
      "location": {
        "kind": "file",
        "file": "test_pizza_components.py",
        "line": 26,
        "column": null
      },
      "name": "test_pizza_components.TestOrderProcessingComponent.test_complete_order_creation_workflow:26",
      "messages": [],
      "just_up": [],
      "just_down": [],
      "just_global": [],
      "refs": [
        "req pizza_example.order_processor",
        "req pizza_example.payment_gateway",
        "req pizza_example.ordering",
        "req pizza_example.payment"
      ],
      "framework": "PyUnit",
      "kind": "Test",
      "status": null
    },
    {
      "tag": "pyunit test_pizza_components.TestCookingComponent.test_recipe_to_cooking_workflow:62",
      "location": {
        "kind": "file",
        "file": "test_pizza_components.py",
        "line": 62,
        "column": null
      },
      "name": "test_pizza_components.TestCookingComponent.test_recipe_to_cooking_workflow:62",
      "messages": [],
      "just_up": [],
      "just_down": [],
      "just_global": [],
      "refs": [
        "req pizza_example.recipe_database",
        "req pizza_example.oven_controller",
        "req pizza_example.stock_manager",
        "req pizza_example.quality",
        "req pizza_example.oven",
        "req pizza_example.inventory"
      ],
      "framework": "PyUnit",
      "kind": "Test",
      "status": null
    },
    {
      "tag": "pyunit test_pizza_components.TestDeliveryComponent.test_delivery_tracking_workflow:102",
      "location": {
        "kind": "file",
        "file": "test_pizza_components.py",
        "line": 102,
        "column": null
      },
      "name": "test_pizza_components.TestDeliveryComponent.test_delivery_tracking_workflow:102",
      "messages": [],
      "just_up": [],
      "just_down": [],
      "just_global": [],
      "refs": [
        "req pizza_example.gps_tracker",
        "req pizza_example.route_planner",
        "req pizza_example.notification_system",
        "req pizza_example.tracking",
        "req pizza_example.delivery",
        "req pizza_example.communication"
      ],
      "framework": "PyUnit",
      "kind": "Test",
      "status": null
    },
    {
      "tag": "pyunit test_pizza_components.TestInventoryAlertComponent.test_low_stock_alert_workflow:142",
      "location": {
        "kind": "file",
        "file": "test_pizza_components.py",
        "line": 142,
        "column": null
      },
      "name": "test_pizza_components.TestInventoryAlertComponent.test_low_stock_alert_workflow:142",
      "messages": [],
      "just_up": [],
      "just_down": [],
      "just_global": [],
      "refs": [
        "req pizza_example.stock_manager",
        "req pizza_example.notification_system",
        "req pizza_example.inventory",
        "req pizza_example.communication"
      ],
      "framework": "PyUnit",
      "kind": "Test",
      "status": null
    },
    {
      "tag": "pyunit test_pizza_components.TestQualityControlComponent.test_quality_validation_workflow:173",
      "location": {
        "kind": "file",
        "file": "test_pizza_components.py",
        "line": 173,
        "column": null
      },
      "name": "test_pizza_components.TestQualityControlComponent.test_quality_validation_workflow:173",
      "messages": [],
      "just_up": [],
      "just_down": [],
      "just_global": [],
      "refs": [
        "req pizza_example.recipe_database",
        "req pizza_example.oven_controller",
        "req pizza_example.quality",
        "req pizza_example.oven"
      ],
      "framework": "PyUnit",
      "kind": "Test",
      "status": null
    },
    {
      "tag": "pyunit test_pizza_components.TestEndToEndOrderComponent.test_complete_pizza_order_system:205",
      "location": {
        "kind": "file",
        "file": "test_pizza_components.py",
        "line": 205,
        "column": null
      },
      "name": "test_pizza_components.TestEndToEndOrderComponent.test_complete_pizza_order_system:205",
      "messages": [],
      "just_up": [],
      "just_down": [],
      "just_global": [],
      "refs": [
        "req pizza_example.order_processor",
        "req pizza_example.payment_gateway",
        "req pizza_example.stock_manager",
        "req pizza_example.recipe_database",
        "req pizza_example.oven_controller",
        "req pizza_example.notification_system",
        "req pizza_example.gps_tracker",
        "req pizza_example.route_planner",
        "req pizza_example.ordering",
        "req pizza_example.payment",
        "req pizza_example.inventory",
        "req pizza_example.quality",
        "req pizza_example.oven",
        "req pizza_example.communication",
        "req pizza_example.tracking",
        "req pizza_example.delivery"
      ],
      "framework": "PyUnit",
      "kind": "Test",
      "status": null
    },
    {
      "tag": "pyunit test_pizza_components.TestErrorHandlingComponent.test_payment_failure_workflow:278",
      "location": {
        "kind": "file",
        "file": "test_pizza_components.py",
        "line": 278,
        "column": null
      },
      "name": "test_pizza_components.TestErrorHandlingComponent.test_payment_failure_workflow:278",
      "messages": [],
      "just_up": [],
      "just_down": [],
      "just_global": [],
      "refs": [
        "req pizza_example.order_processor",
        "req pizza_example.payment_gateway",
        "req pizza_example.ordering",
        "req pizza_example.payment"
      ],
      "framework": "PyUnit",
      "kind": "Test",
      "status": null
    }
  ],
  "generator": "lobster_python",
  "schema": "lobster-act-trace",
  "version": 3
}
