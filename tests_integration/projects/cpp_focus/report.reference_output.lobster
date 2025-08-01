{
  "schema": "lobster-report",
  "version": 2,
  "generator": "lobster_report",
  "levels": [
    {
      "name": "Software Requirements",
      "kind": "requirements",
      "items": [
        {
          "tag": "req fruits.Buy_Banana1",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "this string will be replaced by the current commit during test execution",
            "file": "tests_integration/projects/cpp_focus/fruit.trlc",
            "line": 3
          },
          "name": "fruits.Buy_Banana1",
          "messages": [
            "missing reference to Verification Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "cpp fruit.cpp:1:buyBanana:90"
          ],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "FruityRequirement",
          "text": "Add one banana to the basket!",
          "status": null
        },
        {
          "tag": "req fruits.Buy_Banana2",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "this string will be replaced by the current commit during test execution",
            "file": "tests_integration/projects/cpp_focus/fruit.trlc",
            "line": 8
          },
          "name": "fruits.Buy_Banana2",
          "messages": [
            "missing reference to Verification Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "cpp fruit.cpp:1:buyBanana:90"
          ],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "FruityRequirement",
          "text": "Add one banana to the basket quickly!",
          "status": null
        },
        {
          "tag": "req fruits.Sell_Banana1",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "this string will be replaced by the current commit during test execution",
            "file": "tests_integration/projects/cpp_focus/fruit.trlc",
            "line": 13
          },
          "name": "fruits.Sell_Banana1",
          "messages": [
            "missing reference to Verification Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "cpp fruit.cpp:1:sellBanana:96"
          ],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "FruityRequirement",
          "text": "Sell one banana from the basket!",
          "status": null
        },
        {
          "tag": "req fruits.Sell_Banana2",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "this string will be replaced by the current commit during test execution",
            "file": "tests_integration/projects/cpp_focus/fruit.trlc",
            "line": 18
          },
          "name": "fruits.Sell_Banana2",
          "messages": [
            "missing reference to Verification Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "cpp fruit.cpp:1:sellBanana:96"
          ],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "FruityRequirement",
          "text": "Sell one banana from the basket quickly!",
          "status": null
        },
        {
          "tag": "req fruits.Clear_Basket",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "this string will be replaced by the current commit during test execution",
            "file": "tests_integration/projects/cpp_focus/fruit.trlc",
            "line": 23
          },
          "name": "fruits.Clear_Basket",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "cpp fruit.cpp:1:clearBasket:113",
            "gtest FruitTest:BasicProperties",
            "gtest CitrusTest:Sweetness"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "FruityRequirement",
          "text": "Clear the basket upon request.",
          "status": null
        },
        {
          "tag": "req fruits.Check_Basket",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "this string will be replaced by the current commit during test execution",
            "file": "tests_integration/projects/cpp_focus/fruit.trlc",
            "line": 28
          },
          "name": "fruits.Check_Basket",
          "messages": [
            "missing reference to Verification Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "cpp fruit.cpp:1:checkBasket:121"
          ],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "FruityRequirement",
          "text": "Only go shopping if the basket is empty.",
          "status": null
        },
        {
          "tag": "req fruits.Throw_Banana",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "this string will be replaced by the current commit during test execution",
            "file": "tests_integration/projects/cpp_focus/fruit.trlc",
            "line": 33
          },
          "name": "fruits.Throw_Banana",
          "messages": [
            "missing reference to Verification Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "cpp fruit.cpp:1:throwBanana:132"
          ],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "FruityRequirement",
          "text": "Throw the banana away!",
          "status": null
        },
        {
          "tag": "req fruits.Sweet_Banana",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "this string will be replaced by the current commit during test execution",
            "file": "tests_integration/projects/cpp_focus/fruit.trlc",
            "line": 38
          },
          "name": "fruits.Sweet_Banana",
          "messages": [
            "missing reference to Code"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "gtest BasketTest:ClearBasket"
          ],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "FruityRequirement",
          "text": "The banana shall contain at least 12 grams of natural sugar\nper 100 grams of fruit.",
          "status": null
        },
        {
          "tag": "req fruits.Fruit_Less_Than_Operator",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "this string will be replaced by the current commit during test execution",
            "file": "tests_integration/projects/cpp_focus/fruit.trlc",
            "line": 45
          },
          "name": "fruits.Fruit_Less_Than_Operator",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "cpp fruit.cpp:1:orchard::Fruit<double>::operator<:33",
            "gtest BasketTest:FindInBasketTemplate"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "FruityRequirement",
          "text": "The operator < shall compare the weight of two fruits.",
          "status": null
        },
        {
          "tag": "req fruits.Fruit_Copy_Constructor",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "this string will be replaced by the current commit during test execution",
            "file": "tests_integration/projects/cpp_focus/fruit.trlc",
            "line": 50
          },
          "name": "fruits.Fruit_Copy_Constructor",
          "messages": [
            "missing reference to Verification Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "cpp fruit.cpp:1:orchard::Fruit<double>::operator=:14"
          ],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "FruityRequirement",
          "text": "The operator = shall copy the name and weight of the fruit.",
          "status": null
        },
        {
          "tag": "req fruits.Magic",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "this string will be replaced by the current commit during test execution",
            "file": "tests_integration/projects/cpp_focus/fruit.trlc",
            "line": 55
          },
          "name": "fruits.Magic",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "cpp fruit.cpp:1:orchard::Fruit<double>::operator<:33",
            "gtest BasketTest:AddAndShowContents"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "FruityRequirement",
          "text": "The one who eats the fruit shall be happy!",
          "status": null
        },
        {
          "tag": "req fruits.SameLine1",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "this string will be replaced by the current commit during test execution",
            "file": "tests_integration/projects/cpp_focus/fruit.trlc",
            "line": 60
          },
          "name": "fruits.SameLine1",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "cpp fruit.cpp:1:orchard::Fruit<double>::operator=:14",
            "gtest CitrusTest:Sweetness"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "FruityRequirement",
          "text": "lobster-cpp shall support comma-separated lists of tags in one line.",
          "status": null
        },
        {
          "tag": "req fruits.SameLine2",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "this string will be replaced by the current commit during test execution",
            "file": "tests_integration/projects/cpp_focus/fruit.trlc",
            "line": 65
          },
          "name": "fruits.SameLine2",
          "messages": [
            "missing reference to Verification Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "cpp fruit.cpp:1:orchard::Fruit<double>::operator=:14"
          ],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "FruityRequirement",
          "text": "see SameLine1",
          "status": null
        },
        {
          "tag": "req fruits.SameLine3",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "this string will be replaced by the current commit during test execution",
            "file": "tests_integration/projects/cpp_focus/fruit.trlc",
            "line": 70
          },
          "name": "fruits.SameLine3",
          "messages": [
            "missing reference to Verification Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "cpp fruit.cpp:1:orchard::Fruit<double>::operator=:14"
          ],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "FruityRequirement",
          "text": "see SameLine1",
          "status": null
        },
        {
          "tag": "req fruits.SameLine4",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "this string will be replaced by the current commit during test execution",
            "file": "tests_integration/projects/cpp_focus/fruit.trlc",
            "line": 75
          },
          "name": "fruits.SameLine4",
          "messages": [
            "missing reference to Verification Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "cpp fruit.cpp:1:orchard::Fruit<double>::operator=:14"
          ],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "FruityRequirement",
          "text": "see SameLine1",
          "status": null
        }
      ],
      "coverage": 26.666666666666668
    },
    {
      "name": "Code",
      "kind": "implementation",
      "items": [
        {
          "tag": "cpp fruit.cpp:1:orchard::Fruit<double>::operator=:14",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "this string will be replaced by the current commit during test execution",
            "file": "tests_integration/projects/cpp_focus/fruit.cpp",
            "line": 14
          },
          "name": "orchard::Fruit<double>::operator=",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req fruits.SameLine4",
            "req fruits.SameLine3",
            "req fruits.SameLine2",
            "req fruits.SameLine1",
            "req fruits.Fruit_Copy_Constructor"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "C/C++",
          "kind": "method"
        },
        {
          "tag": "cpp fruit.cpp:1:orchard::Fruit<double>::operator*:26",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "this string will be replaced by the current commit during test execution",
            "file": "tests_integration/projects/cpp_focus/fruit.cpp",
            "line": 26
          },
          "name": "orchard::Fruit<double>::operator*",
          "messages": [
            "unknown tracing target req cd-456",
            "unknown tracing target req ab-123",
            "unknown tracing target req 89",
            "unknown tracing target req 456",
            "unknown tracing target req 123",
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "C/C++",
          "kind": "method"
        },
        {
          "tag": "cpp fruit.cpp:1:orchard::Fruit<double>::operator<:33",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "this string will be replaced by the current commit during test execution",
            "file": "tests_integration/projects/cpp_focus/fruit.cpp",
            "line": 33
          },
          "name": "orchard::Fruit<double>::operator<",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req fruits.Magic",
            "req fruits.Fruit_Less_Than_Operator"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "C/C++",
          "kind": "method"
        },
        {
          "tag": "cpp fruit.cpp:1:orchard::Fruit<double>::operator>:39",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "this string will be replaced by the current commit during test execution",
            "file": "tests_integration/projects/cpp_focus/fruit.cpp",
            "line": 39
          },
          "name": "orchard::Fruit<double>::operator>",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "C/C++",
          "kind": "method"
        },
        {
          "tag": "cpp fruit.cpp:1:orchard::Fruit<double>::operator&:44",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "this string will be replaced by the current commit during test execution",
            "file": "tests_integration/projects/cpp_focus/fruit.cpp",
            "line": 44
          },
          "name": "orchard::Fruit<double>::operator&",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "C/C++",
          "kind": "method"
        },
        {
          "tag": "cpp fruit.cpp:1:orchard::Fruit<double>::operator|:49",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "this string will be replaced by the current commit during test execution",
            "file": "tests_integration/projects/cpp_focus/fruit.cpp",
            "line": 49
          },
          "name": "orchard::Fruit<double>::operator|",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "C/C++",
          "kind": "method"
        },
        {
          "tag": "cpp fruit.cpp:1:orchard::Fruit<double>::operator/:54",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "this string will be replaced by the current commit during test execution",
            "file": "tests_integration/projects/cpp_focus/fruit.cpp",
            "line": 54
          },
          "name": "orchard::Fruit<double>::operator/",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "C/C++",
          "kind": "method"
        },
        {
          "tag": "cpp fruit.cpp:1:orchard::Fruit<double>::operator[]:59",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "this string will be replaced by the current commit during test execution",
            "file": "tests_integration/projects/cpp_focus/fruit.cpp",
            "line": 59
          },
          "name": "orchard::Fruit<double>::operator[]",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "C/C++",
          "kind": "method"
        },
        {
          "tag": "cpp fruit.cpp:1:orchard::Fruit<double>::operator~:64",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "this string will be replaced by the current commit during test execution",
            "file": "tests_integration/projects/cpp_focus/fruit.cpp",
            "line": 64
          },
          "name": "orchard::Fruit<double>::operator~",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "C/C++",
          "kind": "method"
        },
        {
          "tag": "cpp fruit.cpp:1:orchard::Fruit<double>::complicatedFunc:79",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "this string will be replaced by the current commit during test execution",
            "file": "tests_integration/projects/cpp_focus/fruit.cpp",
            "line": 79
          },
          "name": "orchard::Fruit<double>::complicatedFunc",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "C/C++",
          "kind": "method"
        },
        {
          "tag": "cpp fruit.cpp:1:orchard::Fruit<double>::refAndPtrFunc:83",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "this string will be replaced by the current commit during test execution",
            "file": "tests_integration/projects/cpp_focus/fruit.cpp",
            "line": 83
          },
          "name": "orchard::Fruit<double>::refAndPtrFunc",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "C/C++",
          "kind": "method"
        },
        {
          "tag": "cpp fruit.cpp:1:orchard::Fruit<double>::crazySignature:87",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "this string will be replaced by the current commit during test execution",
            "file": "tests_integration/projects/cpp_focus/fruit.cpp",
            "line": 87
          },
          "name": "orchard::Fruit<double>::crazySignature",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "C/C++",
          "kind": "method"
        },
        {
          "tag": "cpp fruit.cpp:1:buyBanana:90",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "this string will be replaced by the current commit during test execution",
            "file": "tests_integration/projects/cpp_focus/fruit.cpp",
            "line": 90
          },
          "name": "buyBanana",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req fruits.Buy_Banana2",
            "req fruits.Buy_Banana1"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "C/C++",
          "kind": "function"
        },
        {
          "tag": "cpp fruit.cpp:1:sellBanana:96",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "this string will be replaced by the current commit during test execution",
            "file": "tests_integration/projects/cpp_focus/fruit.cpp",
            "line": 96
          },
          "name": "sellBanana",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req fruits.Sell_Banana2",
            "req fruits.Sell_Banana1"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "C/C++",
          "kind": "function"
        },
        {
          "tag": "cpp fruit.cpp:1:clearBasket:113",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "this string will be replaced by the current commit during test execution",
            "file": "tests_integration/projects/cpp_focus/fruit.cpp",
            "line": 113
          },
          "name": "clearBasket",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req fruits.Clear_Basket"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "C/C++",
          "kind": "function"
        },
        {
          "tag": "cpp fruit.cpp:1:checkBasket:121",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "this string will be replaced by the current commit during test execution",
            "file": "tests_integration/projects/cpp_focus/fruit.cpp",
            "line": 121
          },
          "name": "checkBasket",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req fruits.Check_Basket"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "C/C++",
          "kind": "function"
        },
        {
          "tag": "cpp fruit.cpp:1:throwBanana:132",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "this string will be replaced by the current commit during test execution",
            "file": "tests_integration/projects/cpp_focus/fruit.cpp",
            "line": 132
          },
          "name": "throwBanana",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req fruits.Throw_Banana"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "C/C++",
          "kind": "function"
        },
        {
          "tag": "cpp fruit.cpp:1:main:148",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "this string will be replaced by the current commit during test execution",
            "file": "tests_integration/projects/cpp_focus/fruit.cpp",
            "line": 148
          },
          "name": "main",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "C/C++",
          "kind": "main function"
        }
      ],
      "coverage": 38.888888888888886
    },
    {
      "name": "Verification Test",
      "kind": "activity",
      "items": [
        {
          "tag": "gtest FruitTest:BasicProperties",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "this string will be replaced by the current commit during test execution",
            "file": "tests_integration/projects/cpp_focus/fruit_test.cpp",
            "line": 9
          },
          "name": "FruitTest:BasicProperties",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req fruits.Clear_Basket"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "GoogleTest",
          "kind": "test",
          "status": "ok"
        },
        {
          "tag": "gtest CitrusTest:Sweetness",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "this string will be replaced by the current commit during test execution",
            "file": "tests_integration/projects/cpp_focus/fruit_test.cpp",
            "line": 17
          },
          "name": "CitrusTest:Sweetness",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req fruits.SameLine1",
            "req fruits.Clear_Basket"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "GoogleTest",
          "kind": "test",
          "status": "ok"
        },
        {
          "tag": "gtest BasketTest:AddAndShowContents",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "this string will be replaced by the current commit during test execution",
            "file": "tests_integration/projects/cpp_focus/fruit_test.cpp",
            "line": 29
          },
          "name": "BasketTest:AddAndShowContents",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req fruits.Magic"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "GoogleTest",
          "kind": "test",
          "status": "ok"
        },
        {
          "tag": "gtest BasketTest:ClearBasket",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "this string will be replaced by the current commit during test execution",
            "file": "tests_integration/projects/cpp_focus/fruit_test.cpp",
            "line": 47
          },
          "name": "BasketTest:ClearBasket",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req fruits.Sweet_Banana"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "GoogleTest",
          "kind": "test",
          "status": "fail"
        },
        {
          "tag": "gtest BasketTest:FindInBasketTemplate",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "this string will be replaced by the current commit during test execution",
            "file": "tests_integration/projects/cpp_focus/fruit_test.cpp",
            "line": 65
          },
          "name": "BasketTest:FindInBasketTemplate",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req fruits.Fruit_Less_Than_Operator"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "GoogleTest",
          "kind": "test",
          "status": "ok"
        }
      ],
      "coverage": 100.0
    }
  ],
  "policy": {
    "Software Requirements": {
      "name": "Software Requirements",
      "kind": "requirements",
      "traces": [],
      "source": [
        {
          "file": "software-requirements.lobster"
        }
      ],
      "needs_tracing_up": false,
      "needs_tracing_down": true,
      "breakdown_requirements": [
        [
          "Code"
        ],
        [
          "Verification Test"
        ]
      ]
    },
    "Code": {
      "name": "Code",
      "kind": "implementation",
      "traces": [
        "Software Requirements"
      ],
      "source": [
        {
          "file": "cppcode.lobster"
        }
      ],
      "needs_tracing_up": true,
      "needs_tracing_down": false,
      "breakdown_requirements": []
    },
    "Verification Test": {
      "name": "Verification Test",
      "kind": "activity",
      "traces": [
        "Software Requirements"
      ],
      "source": [
        {
          "file": "gtests.lobster"
        }
      ],
      "needs_tracing_up": true,
      "needs_tracing_down": false,
      "breakdown_requirements": []
    }
  },
  "matrix": []
}
