{
  "data": [
    {
      "tag": "python test_pizza_components.TestOrderProcessingComponent.test_complete_order_creation_workflow",
      "location": {
        "kind": "file",
        "file": "test_pizza_components.py",
        "line": 26,
        "column": null
      },
      "name": "test_pizza_components.TestOrderProcessingComponent.test_complete_order_creation_workflow",
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
      "language": "Python",
      "kind": "Method"
    },
    {
      "tag": "python test_pizza_components.TestCookingComponent.test_recipe_to_cooking_workflow",
      "location": {
        "kind": "file",
        "file": "test_pizza_components.py",
        "line": 62,
        "column": null
      },
      "name": "test_pizza_components.TestCookingComponent.test_recipe_to_cooking_workflow",
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
      "language": "Python",
      "kind": "Method"
    },
    {
      "tag": "python test_pizza_components.TestDeliveryComponent.test_delivery_tracking_workflow",
      "location": {
        "kind": "file",
        "file": "test_pizza_components.py",
        "line": 102,
        "column": null
      },
      "name": "test_pizza_components.TestDeliveryComponent.test_delivery_tracking_workflow",
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
      "language": "Python",
      "kind": "Method"
    },
    {
      "tag": "python test_pizza_components.TestInventoryAlertComponent.test_low_stock_alert_workflow",
      "location": {
        "kind": "file",
        "file": "test_pizza_components.py",
        "line": 142,
        "column": null
      },
      "name": "test_pizza_components.TestInventoryAlertComponent.test_low_stock_alert_workflow",
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
      "language": "Python",
      "kind": "Method"
    },
    {
      "tag": "python test_pizza_components.TestQualityControlComponent.test_quality_validation_workflow",
      "location": {
        "kind": "file",
        "file": "test_pizza_components.py",
        "line": 173,
        "column": null
      },
      "name": "test_pizza_components.TestQualityControlComponent.test_quality_validation_workflow",
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
      "language": "Python",
      "kind": "Method"
    },
    {
      "tag": "python test_pizza_components.TestEndToEndOrderComponent.test_complete_pizza_order_system",
      "location": {
        "kind": "file",
        "file": "test_pizza_components.py",
        "line": 205,
        "column": null
      },
      "name": "test_pizza_components.TestEndToEndOrderComponent.test_complete_pizza_order_system",
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
      "language": "Python",
      "kind": "Method"
    },
    {
      "tag": "python test_pizza_components.TestErrorHandlingComponent.test_payment_failure_workflow",
      "location": {
        "kind": "file",
        "file": "test_pizza_components.py",
        "line": 278,
        "column": null
      },
      "name": "test_pizza_components.TestErrorHandlingComponent.test_payment_failure_workflow",
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
      "language": "Python",
      "kind": "Method"
    }
  ],
  "generator": "lobster_python",
  "schema": "lobster-imp-trace",
  "version": 3
}
