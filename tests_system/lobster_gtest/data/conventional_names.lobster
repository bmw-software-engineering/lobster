{
  "data": [
    {
      "tag": "gtest Stack:GivenEmptyStack_WhenPopCalled_ExpectError",
      "location": {
        "kind": "file",
        "file": "stack.cpp",
        "line": 10,
        "column": null
      },
      "name": "Stack:GivenEmptyStack_WhenPopCalled_ExpectError",
      "messages": [],
      "just_up": [],
      "just_down": [],
      "just_global": [],
      "refs": [
        "req req.one"
      ],
      "framework": "GoogleTest",
      "kind": "test",
      "text": ":Description: Popping fails\n:Given: empty stack\n:When: pop called\n:Then: error",
      "status": "ok"
    },
    {
      "tag": "gtest Stack:GivenEmptyStack_ThenSizeIsZero",
      "location": {
        "kind": "file",
        "file": "stack.cpp",
        "line": 20,
        "column": null
      },
      "name": "Stack:GivenEmptyStack_ThenSizeIsZero",
      "messages": [],
      "just_up": [],
      "just_down": [],
      "just_global": [],
      "framework": "GoogleTest",
      "kind": "test",
      "text": ":Given: empty stack\n:Then: size is zero",
      "status": "ok"
    },
    {
      "tag": "gtest Stack:Push_GivenFullStack_WhenPushCalled_ExpectOverflow",
      "location": {
        "kind": "file",
        "file": "stack.cpp",
        "line": 30,
        "column": null
      },
      "name": "Stack:Push_GivenFullStack_WhenPushCalled_ExpectOverflow",
      "messages": [],
      "just_up": [],
      "just_down": [],
      "just_global": [],
      "framework": "GoogleTest",
      "kind": "test",
      "text": ":Given: full stack\n:When: push called\n:Then: overflow",
      "status": "ok"
    },
    {
      "tag": "gtest Stack:GivenHTTPServerOnPort80_WhenABCArrives_ThenOkIsSent",
      "location": {
        "kind": "file",
        "file": "stack.cpp",
        "line": 40,
        "column": null
      },
      "name": "Stack:GivenHTTPServerOnPort80_WhenABCArrives_ThenOkIsSent",
      "messages": [],
      "just_up": [],
      "just_down": [],
      "just_global": [],
      "framework": "GoogleTest",
      "kind": "test",
      "text": ":Given: http server on port 80\n:When: abc arrives\n:Then: ok is sent",
      "status": "ok"
    },
    {
      "tag": "gtest Stack:Given3Items_Expect3Results",
      "location": {
        "kind": "file",
        "file": "stack.cpp",
        "line": 50,
        "column": null
      },
      "name": "Stack:Given3Items_Expect3Results",
      "messages": [],
      "just_up": [],
      "just_down": [],
      "just_global": [],
      "framework": "GoogleTest",
      "kind": "test",
      "text": ":Given: 3 items\n:Then: 3 results",
      "status": "ok"
    },
    {
      "tag": "gtest Stack:GivenInput_ExpectOutput/0",
      "location": {
        "kind": "file",
        "file": "stack.cpp",
        "line": 60,
        "column": null
      },
      "name": "Stack:GivenInput_ExpectOutput/0",
      "messages": [],
      "just_up": [],
      "just_down": [],
      "just_global": [],
      "framework": "GoogleTest",
      "kind": "test",
      "text": ":Given: input\n:Then: output",
      "status": "ok"
    }
  ],
  "generator": "lobster_gtest",
  "schema": "lobster-act-trace",
  "version": 3
}
