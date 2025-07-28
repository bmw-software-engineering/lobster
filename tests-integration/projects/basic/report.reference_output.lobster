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
          "tag": "req 12345@42",
          "location": {
            "kind": "codebeamer",
            "cb_root": "https://potato.kitten",
            "tracker": 12345,
            "item": 666,
            "version": 42,
            "name": "LOBSTER demo"
          },
          "name": "LOBSTER demo",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "req example.req_implication",
            "req example.req_xor",
            "req example.req_nand"
          ],
          "tracing_status": "OK",
          "framework": "codebeamer",
          "kind": "functional requirement",
          "text": "Provide a nice demonstration of LOBSTER through four examples",
          "status": "Potato"
        }
      ],
      "coverage": 100.0
    },
    {
      "name": "Software Requirements",
      "kind": "requirements",
      "items": [
        {
          "tag": "req example.req_implication",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "this string will be replaced by the current commit during test execution",
            "file": "tests-integration/projects/basic/potato.trlc",
            "line": 3
          },
          "name": "example.req_implication",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req 12345"
          ],
          "ref_down": [
            "cpp foo.cpp:1:implication:3",
            "gtest ImplicationTest:BasicTest"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Tagged_Requirement",
          "text": "text: provide a utility function for logical implication",
          "status": null
        },
        {
          "tag": "req example.req_xor",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "this string will be replaced by the current commit during test execution",
            "file": "tests-integration/projects/basic/potato.trlc",
            "line": 9
          },
          "name": "example.req_xor",
          "messages": [
            "tracing destination req 12345 has version 42 (expected 5)"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req 12345@5"
          ],
          "ref_down": [
            "simulink exclusive_or/My_Exclusive_Or",
            "json example.json:XOR Test 1",
            "json example.json:XOR Test 2"
          ],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Tagged_Requirement",
          "text": "text: provide a utility function for logical exclusive or",
          "status": null
        },
        {
          "tag": "req example.req_nand",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "this string will be replaced by the current commit during test execution",
            "file": "tests-integration/projects/basic/potato.trlc",
            "line": 15
          },
          "name": "example.req_nand",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req 12345@42"
          ],
          "ref_down": [
            "req example.req_important",
            "matlab nand",
            "matlab nand_test::test_1"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Tagged_Requirement",
          "text": "text: provide a utility function for logical negated and\n\nextra_text: potato",
          "status": null
        },
        {
          "tag": "req example.req_nor",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "this string will be replaced by the current commit during test execution",
            "file": "tests-integration/projects/basic/potato.trlc",
            "line": 22
          },
          "name": "example.req_nor",
          "messages": [
            "missing up reference",
            "missing reference to Verification Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "req example.req_important",
            "python nor.Example.helper_function",
            "python nor.Example.nor"
          ],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Requirement",
          "text": "provide a utility function for logical negated or",
          "status": null
        },
        {
          "tag": "req example.req_implies",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "this string will be replaced by the current commit during test execution",
            "file": "tests-integration/projects/basic/potato.trlc",
            "line": 27
          },
          "name": "example.req_implies",
          "messages": [],
          "just_up": [
            "not needed"
          ],
          "just_down": [
            "also not needed"
          ],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "framework": "TRLC",
          "kind": "Requirement",
          "text": "provide a utility function for logical implication",
          "status": null
        },
        {
          "tag": "req example.req_important",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "this string will be replaced by the current commit during test execution",
            "file": "tests-integration/projects/basic/potato.trlc",
            "line": 39
          },
          "name": "example.req_important",
          "messages": [
            "missing reference to Code",
            "missing reference to Verification Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req example.req_nand",
            "req example.req_nor"
          ],
          "ref_down": [],
          "tracing_status": "PARTIAL",
          "framework": "TRLC",
          "kind": "Linked_Requirement",
          "text": "this is important",
          "status": null
        }
      ],
      "coverage": 50.0
    },
    {
      "name": "Code",
      "kind": "implementation",
      "items": [
        {
          "tag": "cpp foo.cpp:1:implication:3",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "this string will be replaced by the current commit during test execution",
            "file": "tests-integration/projects/basic/foo.cpp",
            "line": 3
          },
          "name": "implication",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req example.req_implication"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "C/C++",
          "kind": "function"
        },
        {
          "tag": "cpp foo.cpp:1:exclusive_or:9",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "this string will be replaced by the current commit during test execution",
            "file": "tests-integration/projects/basic/foo.cpp",
            "line": 9
          },
          "name": "exclusive_or",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "C/C++",
          "kind": "function"
        },
        {
          "tag": "cpp foo.cpp:1:potato:14",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "this string will be replaced by the current commit during test execution",
            "file": "tests-integration/projects/basic/foo.cpp",
            "line": 14
          },
          "name": "potato",
          "messages": [
            "unknown tracing target req example.doesnt_exist",
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "C/C++",
          "kind": "function"
        },
        {
          "tag": "matlab nand",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "this string will be replaced by the current commit during test execution",
            "file": "tests-integration/projects/basic/nand.m",
            "line": 1
          },
          "name": "nand",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req example.req_nand"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "MATLAB",
          "kind": "Function"
        },
        {
          "tag": "matlab exclusive_or/MATLAB Function",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "this string will be replaced by the current commit during test execution",
            "file": "tests-integration/projects/basic/exclusive_or.slx",
            "line": 1
          },
          "name": "exclusive_or/MATLAB Function",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "MATLAB",
          "kind": "Function"
        },
        {
          "tag": "simulink exclusive_or",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "this string will be replaced by the current commit during test execution",
            "file": "tests-integration/projects/basic/exclusive_or.slx",
            "line": null
          },
          "name": "exclusive_or",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Simulink",
          "kind": "Block"
        },
        {
          "tag": "simulink exclusive_or/My_Exclusive_Or",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "this string will be replaced by the current commit during test execution",
            "file": "tests-integration/projects/basic/exclusive_or.slx",
            "line": null
          },
          "name": "exclusive_or/My Exclusive Or",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req example.req_xor"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Simulink",
          "kind": "Block"
        },
        {
          "tag": "python nor.trlc_reference",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "this string will be replaced by the current commit during test execution",
            "file": "tests-integration/projects/basic/nor.py",
            "line": 5
          },
          "name": "nor.trlc_reference",
          "messages": [],
          "just_up": [
            "helper function"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "language": "Python",
          "kind": "Function"
        },
        {
          "tag": "python nor.Example.helper_function",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "this string will be replaced by the current commit during test execution",
            "file": "tests-integration/projects/basic/nor.py",
            "line": 13
          },
          "name": "nor.Example.helper_function",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req example.req_nor"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python nor.Example.nor",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "this string will be replaced by the current commit during test execution",
            "file": "tests-integration/projects/basic/nor.py",
            "line": 17
          },
          "name": "nor.Example.nor",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req example.req_nor"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        }
      ],
      "coverage": 60.0
    },
    {
      "name": "Verification Test",
      "kind": "activity",
      "items": [
        {
          "tag": "gtest ImplicationTest:BasicTest",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "this string will be replaced by the current commit during test execution",
            "file": "tests-integration/projects/basic/test.cpp",
            "line": 7
          },
          "name": "ImplicationTest:BasicTest",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req example.req_implication"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "GoogleTest",
          "kind": "test",
          "status": "ok"
        },
        {
          "tag": "matlab nand_test::test_1",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "this string will be replaced by the current commit during test execution",
            "file": "tests-integration/projects/basic/nand_test.m",
            "line": 3
          },
          "name": "nand_test::test_1",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req example.req_nand"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "MATLAB",
          "kind": "Test",
          "status": null
        },
        {
          "tag": "json example.json:XOR Test 1",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "this string will be replaced by the current commit during test execution",
            "file": "tests-integration/projects/basic/example.json",
            "line": null
          },
          "name": "example.json:XOR Test 1",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req example.req_xor"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "JSON",
          "kind": "Test Vector",
          "status": null
        },
        {
          "tag": "json example.json:XOR Test 2",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "this string will be replaced by the current commit during test execution",
            "file": "tests-integration/projects/basic/example.json",
            "line": null
          },
          "name": "example.json:XOR Test 2",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req example.req_xor"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "JSON",
          "kind": "Test Vector",
          "status": null
        },
        {
          "tag": "json example.json:Potato Test 1",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "this string will be replaced by the current commit during test execution",
            "file": "tests-integration/projects/basic/example.json",
            "line": null
          },
          "name": "example.json:Potato Test 1",
          "messages": [],
          "just_up": [
            "Unlinked on purpose"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "framework": "JSON",
          "kind": "Test Vector",
          "status": null
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
          "file": "system-requirements.lobster"
        }
      ],
      "needs_tracing_up": false,
      "needs_tracing_down": true,
      "breakdown_requirements": [
        [
          "Software Requirements"
        ]
      ]
    },
    "Software Requirements": {
      "name": "Software Requirements",
      "kind": "requirements",
      "traces": [
        "System Requirements"
      ],
      "source": [
        {
          "file": "software-requirements.lobster"
        }
      ],
      "needs_tracing_up": true,
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
        },
        {
          "file": "mcode.lobster"
        },
        {
          "file": "pycode.lobster"
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
        },
        {
          "file": "mtests.lobster"
        },
        {
          "file": "json.lobster"
        }
      ],
      "needs_tracing_up": true,
      "needs_tracing_down": false,
      "breakdown_requirements": []
    }
  },
  "matrix": []
}
