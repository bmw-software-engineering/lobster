{
  "schema": "lobster-report",
  "version": 2,
  "generator": "lobster_report",
  "levels": [
    {
      "name": "System Requirements",
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
            "req example.req_implication@10",
            "req example.req_xor",
            "req example.req_nand@30"
          ],
          "tracing_status": "OK"
        }
      ],
      "coverage": 100.0
    },
    {
      "name": "Software Requirements",
      "items": [
        {
          "tag": "req example.req_implication@10",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "c550086fafeab2b3b490a57286f2a1cb219a74a1",
            "file": "tests_integration/projects/basic/potato.trlc",
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
            "req example.req_important",
            "cpp foo.cpp:1:implication:3",
            "gtest ImplicationTest:BasicTest"
          ],
          "tracing_status": "OK"
        },
        {
          "tag": "req example.req_xor",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "c550086fafeab2b3b490a57286f2a1cb219a74a1",
            "file": "tests_integration/projects/basic/potato.trlc",
            "line": 10
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
          "tracing_status": "MISSING"
        },
        {
          "tag": "req example.req_nand@30",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "c550086fafeab2b3b490a57286f2a1cb219a74a1",
            "file": "tests_integration/projects/basic/potato.trlc",
            "line": 16
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
          "tracing_status": "OK"
        },
        {
          "tag": "req example.req_nor@40",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "c550086fafeab2b3b490a57286f2a1cb219a74a1",
            "file": "tests_integration/projects/basic/potato.trlc",
            "line": 24
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
            "itm nor.Example.helper_function",
            "itm nor.Example.nor"
          ],
          "tracing_status": "MISSING"
        },
        {
          "tag": "req example.req_implies",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "c550086fafeab2b3b490a57286f2a1cb219a74a1",
            "file": "tests_integration/projects/basic/potato.trlc",
            "line": 30
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
          "tracing_status": "JUSTIFIED"
        },
        {
          "tag": "req example.req_important",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "c550086fafeab2b3b490a57286f2a1cb219a74a1",
            "file": "tests_integration/projects/basic/potato.trlc",
            "line": 42
          },
          "name": "example.req_important",
          "messages": [
            "tracing destination req example.req_nand has version 30 (expected 31)",
            "missing reference to Code",
            "missing reference to Verification Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req example.req_nand@31",
            "req example.req_nor@40",
            "req example.req_implication"
          ],
          "ref_down": [],
          "tracing_status": "MISSING"
        }
      ],
      "coverage": 50.0
    },
    {
      "name": "Code",
      "items": [
        {
          "tag": "cpp foo.cpp:1:implication:3",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "c550086fafeab2b3b490a57286f2a1cb219a74a1",
            "file": "tests_integration/projects/basic/foo.cpp",
            "line": 3
          },
          "name": "foo.cpp:1:implication:3",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req example.req_implication"
          ],
          "ref_down": [],
          "tracing_status": "OK"
        },
        {
          "tag": "cpp foo.cpp:1:exclusive_or:9",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "c550086fafeab2b3b490a57286f2a1cb219a74a1",
            "file": "tests_integration/projects/basic/foo.cpp",
            "line": 9
          },
          "name": "foo.cpp:1:exclusive_or:9",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING"
        },
        {
          "tag": "cpp foo.cpp:1:potato:14",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "c550086fafeab2b3b490a57286f2a1cb219a74a1",
            "file": "tests_integration/projects/basic/foo.cpp",
            "line": 14
          },
          "name": "foo.cpp:1:potato:14",
          "messages": [
            "unknown tracing target req example.doesnt_exist",
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING"
        },
        {
          "tag": "matlab nand",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "c550086fafeab2b3b490a57286f2a1cb219a74a1",
            "file": "tests_integration/projects/basic/nand.m",
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
          "tracing_status": "OK"
        },
        {
          "tag": "matlab exclusive_or/MATLAB Function",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "c550086fafeab2b3b490a57286f2a1cb219a74a1",
            "file": "tests_integration/projects/basic/exclusive_or.slx",
            "line": 1
          },
          "name": "exclusive_or/MATLAB Function",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING"
        },
        {
          "tag": "simulink exclusive_or",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "c550086fafeab2b3b490a57286f2a1cb219a74a1",
            "file": "tests_integration/projects/basic/exclusive_or.slx",
            "line": null
          },
          "name": "exclusive_or",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING"
        },
        {
          "tag": "simulink exclusive_or/My_Exclusive_Or",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "c550086fafeab2b3b490a57286f2a1cb219a74a1",
            "file": "tests_integration/projects/basic/exclusive_or.slx",
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
          "tracing_status": "OK"
        },
        {
          "tag": "itm nor.trlc_reference",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "c550086fafeab2b3b490a57286f2a1cb219a74a1",
            "file": "tests_integration/projects/basic/nor.py",
            "line": 5
          },
          "name": "nor.trlc_reference",
          "messages": [],
          "just_up": [
            "helper function"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "JUSTIFIED"
        },
        {
          "tag": "itm nor.Example.helper_function",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "c550086fafeab2b3b490a57286f2a1cb219a74a1",
            "file": "tests_integration/projects/basic/nor.py",
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
          "tracing_status": "OK"
        },
        {
          "tag": "itm nor.Example.nor",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "c550086fafeab2b3b490a57286f2a1cb219a74a1",
            "file": "tests_integration/projects/basic/nor.py",
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
          "tracing_status": "OK"
        }
      ],
      "coverage": 60.0
    },
    {
      "name": "Verification Test",
      "items": [
        {
          "tag": "gtest ImplicationTest:BasicTest",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "c550086fafeab2b3b490a57286f2a1cb219a74a1",
            "file": "tests_integration/projects/basic/test.cpp",
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
          "tracing_status": "OK"
        },
        {
          "tag": "matlab nand_test::test_1",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "c550086fafeab2b3b490a57286f2a1cb219a74a1",
            "file": "tests_integration/projects/basic/nand_test.m",
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
          "tracing_status": "OK"
        },
        {
          "tag": "json example.json:XOR Test 1",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "c550086fafeab2b3b490a57286f2a1cb219a74a1",
            "file": "tests_integration/projects/basic/example.json",
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
          "tracing_status": "OK"
        },
        {
          "tag": "json example.json:XOR Test 2",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "c550086fafeab2b3b490a57286f2a1cb219a74a1",
            "file": "tests_integration/projects/basic/example.json",
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
          "tracing_status": "OK"
        },
        {
          "tag": "json example.json:Potato Test 1",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/bmw-software-engineering/lobster",
            "commit": "c550086fafeab2b3b490a57286f2a1cb219a74a1",
            "file": "tests_integration/projects/basic/example.json",
            "line": null
          },
          "name": "example.json:Potato Test 1",
          "messages": [],
          "just_up": [
            "Unlinked on purpose"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "JUSTIFIED"
        }
      ],
      "coverage": 100.0
    }
  ],
  "policy": {
    "System Requirements": {
      "name": "System Requirements",
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
