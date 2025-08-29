{
  "schema": "lobster-report",
  "version": 2,
  "generator": "lobster_report",
  "levels": [
    {
      "name": "System Requirements",
      "kind": "requirements",
      "items": [
        {
          "tag": "req pizza_example.oven",
          "location": {
            "kind": "file",
            "file": "pizza_system_requirements.trlc",
            "line": 4,
            "column": 28
          },
          "name": "pizza_example.oven",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python pizza_implementation.OvenController.start_cooking",
            "python pizza_implementation.OvenController.check_cooking_status",
            "python test_pizza_components.TestCookingComponent.test_recipe_to_cooking_workflow",
            "python test_pizza_components.TestQualityControlComponent.test_quality_validation_workflow",
            "python test_pizza_components.TestEndToEndOrderComponent.test_complete_pizza_order_system"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "system_requirement",
          "text": "The system shall heat pizzas to perfect crispy goodness",
          "status": null
        },
        {
          "tag": "req pizza_example.delivery",
          "location": {
            "kind": "file",
            "file": "pizza_system_requirements.trlc",
            "line": 8,
            "column": 28
          },
          "name": "pizza_example.delivery",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python pizza_implementation.RouteOptimizer.calculate_route",
            "python test_pizza_components.TestDeliveryComponent.test_delivery_tracking_workflow",
            "python test_pizza_components.TestEndToEndOrderComponent.test_complete_pizza_order_system"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "system_requirement",
          "text": "The system shall transport pizzas while they are still hot",
          "status": null
        },
        {
          "tag": "req pizza_example.ordering",
          "location": {
            "kind": "file",
            "file": "pizza_system_requirements.trlc",
            "line": 12,
            "column": 28
          },
          "name": "pizza_example.ordering",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python pizza_implementation.OrderProcessor.create_customer",
            "python pizza_implementation.OrderProcessor.place_order",
            "python test_pizza_components.TestOrderProcessingComponent.test_complete_order_creation_workflow",
            "python test_pizza_components.TestEndToEndOrderComponent.test_complete_pizza_order_system",
            "python test_pizza_components.TestErrorHandlingComponent.test_payment_failure_workflow"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "system_requirement",
          "text": "The system shall accept pizza orders from hungry customers",
          "status": null
        },
        {
          "tag": "req pizza_example.payment",
          "location": {
            "kind": "file",
            "file": "pizza_system_requirements.trlc",
            "line": 16,
            "column": 28
          },
          "name": "pizza_example.payment",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python pizza_implementation.PaymentGateway.process_payment",
            "python test_pizza_components.TestOrderProcessingComponent.test_complete_order_creation_workflow",
            "python test_pizza_components.TestEndToEndOrderComponent.test_complete_pizza_order_system",
            "python test_pizza_components.TestErrorHandlingComponent.test_payment_failure_workflow"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "system_requirement",
          "text": "The system shall process money without stealing tips",
          "status": null
        },
        {
          "tag": "req pizza_example.tracking",
          "location": {
            "kind": "file",
            "file": "pizza_system_requirements.trlc",
            "line": 20,
            "column": 28
          },
          "name": "pizza_example.tracking",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python pizza_implementation.DeliveryTracker.start_delivery",
            "python test_pizza_components.TestDeliveryComponent.test_delivery_tracking_workflow",
            "python test_pizza_components.TestEndToEndOrderComponent.test_complete_pizza_order_system"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "system_requirement",
          "text": "The system shall show where the pizza is on its journey",
          "status": null
        },
        {
          "tag": "req pizza_example.inventory",
          "location": {
            "kind": "file",
            "file": "pizza_system_requirements.trlc",
            "line": 24,
            "column": 28
          },
          "name": "pizza_example.inventory",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python pizza_implementation.InventoryManager.use_ingredients",
            "python pizza_implementation.InventoryManager.check_for_alerts",
            "python test_pizza_components.TestCookingComponent.test_recipe_to_cooking_workflow",
            "python test_pizza_components.TestInventoryAlertComponent.test_low_stock_alert_workflow",
            "python test_pizza_components.TestEndToEndOrderComponent.test_complete_pizza_order_system"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "system_requirement",
          "text": "The system shall keep track of cheese and pepperoni supplies",
          "status": null
        },
        {
          "tag": "req pizza_example.communication",
          "location": {
            "kind": "file",
            "file": "pizza_system_requirements.trlc",
            "line": 28,
            "column": 28
          },
          "name": "pizza_example.communication",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python pizza_implementation.NotificationSystem.send_sms",
            "python pizza_implementation.NotificationSystem.notify_order_status",
            "python test_pizza_components.TestDeliveryComponent.test_delivery_tracking_workflow",
            "python test_pizza_components.TestInventoryAlertComponent.test_low_stock_alert_workflow",
            "python test_pizza_components.TestEndToEndOrderComponent.test_complete_pizza_order_system"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "system_requirement",
          "text": "The system shall notify customers when pizza arrives",
          "status": null
        },
        {
          "tag": "req pizza_example.quality",
          "location": {
            "kind": "file",
            "file": "pizza_system_requirements.trlc",
            "line": 32,
            "column": 28
          },
          "name": "pizza_example.quality",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python pizza_implementation.RecipeDatabase.get_recipe",
            "python pizza_implementation.RecipeDatabase.validate_quality",
            "python test_pizza_components.TestCookingComponent.test_recipe_to_cooking_workflow",
            "python test_pizza_components.TestQualityControlComponent.test_quality_validation_workflow",
            "python test_pizza_components.TestEndToEndOrderComponent.test_complete_pizza_order_system"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "system_requirement",
          "text": "The system shall ensure pizzas taste better than cardboard",
          "status": null
        }
      ],
      "coverage": 100.0
    },
    {
      "name": "Software Requirements",
      "kind": "requirements",
      "items": [
        {
          "tag": "req pizza_example.oven_controller",
          "location": {
            "kind": "file",
            "file": "pizza_software_requirements.trlc",
            "line": 4,
            "column": 30
          },
          "name": "pizza_example.oven_controller",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python pizza_implementation.OvenController.start_cooking",
            "python pizza_implementation.OvenController.check_cooking_status",
            "python test_pizza_components.TestCookingComponent.test_recipe_to_cooking_workflow",
            "python test_pizza_components.TestQualityControlComponent.test_quality_validation_workflow",
            "python test_pizza_components.TestEndToEndOrderComponent.test_complete_pizza_order_system",
            "python test_pizza_implementation.TestOvenController.test_start_cooking"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "software_requirement",
          "text": "The software shall control oven temperature and cooking timer",
          "status": null
        },
        {
          "tag": "req pizza_example.route_planner",
          "location": {
            "kind": "file",
            "file": "pizza_software_requirements.trlc",
            "line": 8,
            "column": 30
          },
          "name": "pizza_example.route_planner",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python pizza_implementation.RouteOptimizer.calculate_route",
            "python test_pizza_components.TestDeliveryComponent.test_delivery_tracking_workflow",
            "python test_pizza_components.TestEndToEndOrderComponent.test_complete_pizza_order_system",
            "python test_pizza_implementation.TestRouteOptimizer.test_calculate_route_empty"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "software_requirement",
          "text": "The software shall calculate fastest delivery routes",
          "status": null
        },
        {
          "tag": "req pizza_example.order_processor",
          "location": {
            "kind": "file",
            "file": "pizza_software_requirements.trlc",
            "line": 12,
            "column": 30
          },
          "name": "pizza_example.order_processor",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python pizza_implementation.OrderProcessor.create_customer",
            "python pizza_implementation.OrderProcessor.place_order",
            "python test_pizza_components.TestOrderProcessingComponent.test_complete_order_creation_workflow",
            "python test_pizza_components.TestEndToEndOrderComponent.test_complete_pizza_order_system",
            "python test_pizza_components.TestErrorHandlingComponent.test_payment_failure_workflow",
            "python test_pizza_implementation.TestOrderProcessor.test_create_customer",
            "python test_pizza_implementation.TestOrderProcessor.test_place_order"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "software_requirement",
          "text": "The software shall manage pizza orders and customer details",
          "status": null
        },
        {
          "tag": "req pizza_example.payment_gateway",
          "location": {
            "kind": "file",
            "file": "pizza_software_requirements.trlc",
            "line": 16,
            "column": 30
          },
          "name": "pizza_example.payment_gateway",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python pizza_implementation.PaymentGateway.process_payment",
            "python test_pizza_components.TestOrderProcessingComponent.test_complete_order_creation_workflow",
            "python test_pizza_components.TestEndToEndOrderComponent.test_complete_pizza_order_system",
            "python test_pizza_components.TestErrorHandlingComponent.test_payment_failure_workflow",
            "python test_pizza_implementation.TestPaymentGateway.test_process_payment_valid"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "software_requirement",
          "text": "The software shall handle credit card transactions securely",
          "status": null
        },
        {
          "tag": "req pizza_example.gps_tracker",
          "location": {
            "kind": "file",
            "file": "pizza_software_requirements.trlc",
            "line": 20,
            "column": 30
          },
          "name": "pizza_example.gps_tracker",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python pizza_implementation.DeliveryTracker.start_delivery",
            "python test_pizza_components.TestDeliveryComponent.test_delivery_tracking_workflow",
            "python test_pizza_components.TestEndToEndOrderComponent.test_complete_pizza_order_system"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "software_requirement",
          "text": "The software shall provide real-time delivery location updates",
          "status": null
        },
        {
          "tag": "req pizza_example.stock_manager",
          "location": {
            "kind": "file",
            "file": "pizza_software_requirements.trlc",
            "line": 24,
            "column": 30
          },
          "name": "pizza_example.stock_manager",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python pizza_implementation.InventoryManager.use_ingredients",
            "python pizza_implementation.InventoryManager.check_for_alerts",
            "python test_pizza_components.TestCookingComponent.test_recipe_to_cooking_workflow",
            "python test_pizza_components.TestInventoryAlertComponent.test_low_stock_alert_workflow",
            "python test_pizza_components.TestEndToEndOrderComponent.test_complete_pizza_order_system",
            "python test_pizza_implementation.TestInventoryManager.test_use_ingredients"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "software_requirement",
          "text": "The software shall monitor ingredient levels and send alerts",
          "status": null
        },
        {
          "tag": "req pizza_example.notification_system",
          "location": {
            "kind": "file",
            "file": "pizza_software_requirements.trlc",
            "line": 28,
            "column": 30
          },
          "name": "pizza_example.notification_system",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python pizza_implementation.NotificationSystem.send_sms",
            "python pizza_implementation.NotificationSystem.notify_order_status",
            "python test_pizza_components.TestDeliveryComponent.test_delivery_tracking_workflow",
            "python test_pizza_components.TestInventoryAlertComponent.test_low_stock_alert_workflow",
            "python test_pizza_components.TestEndToEndOrderComponent.test_complete_pizza_order_system",
            "python test_pizza_implementation.TestNotificationSystem.test_send_sms"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "software_requirement",
          "text": "The software shall send SMS and email updates to customers",
          "status": null
        },
        {
          "tag": "req pizza_example.recipe_database",
          "location": {
            "kind": "file",
            "file": "pizza_software_requirements.trlc",
            "line": 32,
            "column": 30
          },
          "name": "pizza_example.recipe_database",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python pizza_implementation.RecipeDatabase.get_recipe",
            "python pizza_implementation.RecipeDatabase.validate_quality",
            "python test_pizza_components.TestCookingComponent.test_recipe_to_cooking_workflow",
            "python test_pizza_components.TestQualityControlComponent.test_quality_validation_workflow",
            "python test_pizza_components.TestEndToEndOrderComponent.test_complete_pizza_order_system",
            "python test_pizza_implementation.TestRecipeDatabase.test_get_recipe"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "software_requirement",
          "text": "The software shall store pizza recipes and quality standards",
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
          "tag": "python pizza_implementation.OvenController.start_cooking",
          "location": {
            "kind": "file",
            "file": "pizza_implementation.py",
            "line": 37,
            "column": null
          },
          "name": "pizza_implementation.OvenController.start_cooking",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req pizza_example.oven",
            "req pizza_example.oven_controller"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python pizza_implementation.OvenController.check_cooking_status",
          "location": {
            "kind": "file",
            "file": "pizza_implementation.py",
            "line": 45,
            "column": null
          },
          "name": "pizza_implementation.OvenController.check_cooking_status",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req pizza_example.oven",
            "req pizza_example.oven_controller"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python pizza_implementation.RouteOptimizer.calculate_route",
          "location": {
            "kind": "file",
            "file": "pizza_implementation.py",
            "line": 66,
            "column": null
          },
          "name": "pizza_implementation.RouteOptimizer.calculate_route",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req pizza_example.delivery",
            "req pizza_example.route_planner"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python pizza_implementation.OrderProcessor.create_customer",
          "location": {
            "kind": "file",
            "file": "pizza_implementation.py",
            "line": 95,
            "column": null
          },
          "name": "pizza_implementation.OrderProcessor.create_customer",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req pizza_example.ordering",
            "req pizza_example.order_processor"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python pizza_implementation.OrderProcessor.place_order",
          "location": {
            "kind": "file",
            "file": "pizza_implementation.py",
            "line": 105,
            "column": null
          },
          "name": "pizza_implementation.OrderProcessor.place_order",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req pizza_example.ordering",
            "req pizza_example.order_processor"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python pizza_implementation.PaymentGateway.process_payment",
          "location": {
            "kind": "file",
            "file": "pizza_implementation.py",
            "line": 122,
            "column": null
          },
          "name": "pizza_implementation.PaymentGateway.process_payment",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req pizza_example.payment",
            "req pizza_example.payment_gateway"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python pizza_implementation.DeliveryTracker.start_delivery",
          "location": {
            "kind": "file",
            "file": "pizza_implementation.py",
            "line": 150,
            "column": null
          },
          "name": "pizza_implementation.DeliveryTracker.start_delivery",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req pizza_example.tracking",
            "req pizza_example.gps_tracker"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python pizza_implementation.InventoryManager.use_ingredients",
          "location": {
            "kind": "file",
            "file": "pizza_implementation.py",
            "line": 177,
            "column": null
          },
          "name": "pizza_implementation.InventoryManager.use_ingredients",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req pizza_example.inventory",
            "req pizza_example.stock_manager"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python pizza_implementation.InventoryManager.check_for_alerts",
          "location": {
            "kind": "file",
            "file": "pizza_implementation.py",
            "line": 195,
            "column": null
          },
          "name": "pizza_implementation.InventoryManager.check_for_alerts",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req pizza_example.inventory",
            "req pizza_example.stock_manager"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python pizza_implementation.NotificationSystem.send_sms",
          "location": {
            "kind": "file",
            "file": "pizza_implementation.py",
            "line": 213,
            "column": null
          },
          "name": "pizza_implementation.NotificationSystem.send_sms",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req pizza_example.communication",
            "req pizza_example.notification_system"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python pizza_implementation.NotificationSystem.notify_order_status",
          "location": {
            "kind": "file",
            "file": "pizza_implementation.py",
            "line": 226,
            "column": null
          },
          "name": "pizza_implementation.NotificationSystem.notify_order_status",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req pizza_example.communication",
            "req pizza_example.notification_system"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python pizza_implementation.RecipeDatabase.get_recipe",
          "location": {
            "kind": "file",
            "file": "pizza_implementation.py",
            "line": 258,
            "column": null
          },
          "name": "pizza_implementation.RecipeDatabase.get_recipe",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req pizza_example.quality",
            "req pizza_example.recipe_database"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python pizza_implementation.RecipeDatabase.validate_quality",
          "location": {
            "kind": "file",
            "file": "pizza_implementation.py",
            "line": 264,
            "column": null
          },
          "name": "pizza_implementation.RecipeDatabase.validate_quality",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req pizza_example.quality",
            "req pizza_example.recipe_database"
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
      "name": "Component Tests",
      "kind": "activity",
      "items": [
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
          "ref_up": [
            "req pizza_example.payment",
            "req pizza_example.ordering",
            "req pizza_example.payment_gateway",
            "req pizza_example.order_processor"
          ],
          "ref_down": [],
          "tracing_status": "OK",
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
          "ref_up": [
            "req pizza_example.inventory",
            "req pizza_example.oven",
            "req pizza_example.quality",
            "req pizza_example.stock_manager",
            "req pizza_example.oven_controller",
            "req pizza_example.recipe_database"
          ],
          "ref_down": [],
          "tracing_status": "OK",
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
          "ref_up": [
            "req pizza_example.communication",
            "req pizza_example.delivery",
            "req pizza_example.tracking",
            "req pizza_example.notification_system",
            "req pizza_example.route_planner",
            "req pizza_example.gps_tracker"
          ],
          "ref_down": [],
          "tracing_status": "OK",
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
          "ref_up": [
            "req pizza_example.communication",
            "req pizza_example.inventory",
            "req pizza_example.notification_system",
            "req pizza_example.stock_manager"
          ],
          "ref_down": [],
          "tracing_status": "OK",
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
          "ref_up": [
            "req pizza_example.oven",
            "req pizza_example.quality",
            "req pizza_example.oven_controller",
            "req pizza_example.recipe_database"
          ],
          "ref_down": [],
          "tracing_status": "OK",
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
          "ref_up": [
            "req pizza_example.delivery",
            "req pizza_example.tracking",
            "req pizza_example.communication",
            "req pizza_example.oven",
            "req pizza_example.quality",
            "req pizza_example.inventory",
            "req pizza_example.payment",
            "req pizza_example.ordering",
            "req pizza_example.route_planner",
            "req pizza_example.gps_tracker",
            "req pizza_example.notification_system",
            "req pizza_example.oven_controller",
            "req pizza_example.recipe_database",
            "req pizza_example.stock_manager",
            "req pizza_example.payment_gateway",
            "req pizza_example.order_processor"
          ],
          "ref_down": [],
          "tracing_status": "OK",
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
          "ref_up": [
            "req pizza_example.payment",
            "req pizza_example.ordering",
            "req pizza_example.payment_gateway",
            "req pizza_example.order_processor"
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
      "name": "Unit Tests",
      "kind": "activity",
      "items": [
        {
          "tag": "python test_pizza_implementation.TestOvenController.test_start_cooking",
          "location": {
            "kind": "file",
            "file": "test_pizza_implementation.py",
            "line": 18,
            "column": null
          },
          "name": "test_pizza_implementation.TestOvenController.test_start_cooking",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req pizza_example.oven_controller"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python test_pizza_implementation.TestOrderProcessor.test_create_customer",
          "location": {
            "kind": "file",
            "file": "test_pizza_implementation.py",
            "line": 33,
            "column": null
          },
          "name": "test_pizza_implementation.TestOrderProcessor.test_create_customer",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req pizza_example.order_processor"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python test_pizza_implementation.TestOrderProcessor.test_place_order",
          "location": {
            "kind": "file",
            "file": "test_pizza_implementation.py",
            "line": 43,
            "column": null
          },
          "name": "test_pizza_implementation.TestOrderProcessor.test_place_order",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req pizza_example.order_processor"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python test_pizza_implementation.TestPaymentGateway.test_process_payment_valid",
          "location": {
            "kind": "file",
            "file": "test_pizza_implementation.py",
            "line": 57,
            "column": null
          },
          "name": "test_pizza_implementation.TestPaymentGateway.test_process_payment_valid",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req pizza_example.payment_gateway"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python test_pizza_implementation.TestInventoryManager.test_use_ingredients",
          "location": {
            "kind": "file",
            "file": "test_pizza_implementation.py",
            "line": 71,
            "column": null
          },
          "name": "test_pizza_implementation.TestInventoryManager.test_use_ingredients",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req pizza_example.stock_manager"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python test_pizza_implementation.TestNotificationSystem.test_send_sms",
          "location": {
            "kind": "file",
            "file": "test_pizza_implementation.py",
            "line": 86,
            "column": null
          },
          "name": "test_pizza_implementation.TestNotificationSystem.test_send_sms",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req pizza_example.notification_system"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python test_pizza_implementation.TestRecipeDatabase.test_get_recipe",
          "location": {
            "kind": "file",
            "file": "test_pizza_implementation.py",
            "line": 100,
            "column": null
          },
          "name": "test_pizza_implementation.TestRecipeDatabase.test_get_recipe",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req pizza_example.recipe_database"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python test_pizza_implementation.TestRouteOptimizer.test_calculate_route_empty",
          "location": {
            "kind": "file",
            "file": "test_pizza_implementation.py",
            "line": 114,
            "column": null
          },
          "name": "test_pizza_implementation.TestRouteOptimizer.test_calculate_route_empty",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req pizza_example.route_planner"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        }
      ],
      "coverage": 100.0
    }
  ],
  "policy": {
    "System Requirements": {
      "name": "System Requirements",
      "kind": "requirements",
      "traces": [],
      "source": [
        {
          "file": "pizza_system_requirements.lobster"
        }
      ],
      "needs_tracing_up": false,
      "needs_tracing_down": true,
      "breakdown_requirements": [
        [
          "Component Tests"
        ]
      ]
    },
    "Software Requirements": {
      "name": "Software Requirements",
      "kind": "requirements",
      "traces": [],
      "source": [
        {
          "file": "pizza_software_requirements.lobster"
        }
      ],
      "needs_tracing_up": false,
      "needs_tracing_down": true,
      "breakdown_requirements": [
        [
          "Component Tests",
          "Unit Tests"
        ]
      ]
    },
    "Code": {
      "name": "Code",
      "kind": "implementation",
      "traces": [
        "System Requirements",
        "Software Requirements"
      ],
      "source": [
        {
          "file": "pizza_code.lobster"
        }
      ],
      "needs_tracing_up": true,
      "needs_tracing_down": false,
      "breakdown_requirements": []
    },
    "Component Tests": {
      "name": "Component Tests",
      "kind": "activity",
      "traces": [
        "System Requirements",
        "Software Requirements"
      ],
      "source": [
        {
          "file": "pizza_component_tests.lobster"
        }
      ],
      "needs_tracing_up": true,
      "needs_tracing_down": false,
      "breakdown_requirements": []
    },
    "Unit Tests": {
      "name": "Unit Tests",
      "kind": "activity",
      "traces": [
        "Software Requirements"
      ],
      "source": [
        {
          "file": "pizza_unit_tests.lobster"
        }
      ],
      "needs_tracing_up": true,
      "needs_tracing_down": false,
      "breakdown_requirements": []
    }
  },
  "matrix": []
}
