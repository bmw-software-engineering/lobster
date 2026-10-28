{
  "data": [
    {
      "tag": "junit test_stack:test_GivenEmptyStack_WhenPopCalled_ExpectError",
      "location": {
        "kind": "void"
      },
      "name": "test_stack:test_GivenEmptyStack_WhenPopCalled_ExpectError",
      "messages": [],
      "just_up": [],
      "just_down": [],
      "just_global": [],
      "refs": [
        "req Pkg.Pop",
        "req Pkg.Error",
        "req Pkg.Stack@2"
      ],
      "framework": "pytest",
      "kind": "test",
      "text": ":Given: empty stack\n:When: pop called\n:Then: error",
      "status": "ok"
    },
    {
      "tag": "junit test_stack:test_failing",
      "location": {
        "kind": "void"
      },
      "name": "test_stack:test_failing",
      "messages": [],
      "just_up": [],
      "just_down": [],
      "just_global": [],
      "refs": [
        "req Pkg.Fail"
      ],
      "framework": "pytest",
      "kind": "test",
      "status": "fail"
    },
    {
      "tag": "junit test_stack:test_errored",
      "location": {
        "kind": "void"
      },
      "name": "test_stack:test_errored",
      "messages": [],
      "just_up": [],
      "just_down": [],
      "just_global": [],
      "framework": "pytest",
      "kind": "test",
      "status": "fail"
    },
    {
      "tag": "junit test_stack:test_skipped",
      "location": {
        "kind": "void"
      },
      "name": "test_stack:test_skipped",
      "messages": [],
      "just_up": [],
      "just_down": [],
      "just_global": [],
      "framework": "pytest",
      "kind": "test",
      "status": "not run"
    },
    {
      "tag": "junit test_stack:test_GivenValue_ExpectPositive[1]",
      "location": {
        "kind": "void"
      },
      "name": "test_stack:test_GivenValue_ExpectPositive[1]",
      "messages": [],
      "just_up": [],
      "just_down": [],
      "just_global": [],
      "refs": [
        "req Pkg.Value"
      ],
      "framework": "pytest",
      "kind": "test",
      "text": ":Given: value\n:Then: positive",
      "status": "ok"
    },
    {
      "tag": "junit test_stack:test_GivenValue_ExpectPositive[2]",
      "location": {
        "kind": "void"
      },
      "name": "test_stack:test_GivenValue_ExpectPositive[2]",
      "messages": [],
      "just_up": [],
      "just_down": [],
      "just_global": [],
      "refs": [
        "req Pkg.Value"
      ],
      "framework": "pytest",
      "kind": "test",
      "text": ":Given: value\n:Then: positive",
      "status": "ok"
    },
    {
      "tag": "junit test_stack:test_GivenRecorded_ExpectWarning",
      "location": {
        "kind": "void"
      },
      "name": "test_stack:test_GivenRecorded_ExpectWarning",
      "messages": [],
      "just_up": [],
      "just_down": [],
      "just_global": [],
      "refs": [
        "req Pkg.Warn"
      ],
      "framework": "pytest",
      "kind": "test",
      "text": ":Given: a recorded given",
      "status": "ok"
    },
    {
      "tag": "junit test_stack.TestPush:test_one",
      "location": {
        "kind": "void"
      },
      "name": "test_stack.TestPush:test_one",
      "messages": [],
      "just_up": [],
      "just_down": [],
      "just_global": [],
      "refs": [
        "req Pkg.Push"
      ],
      "framework": "pytest",
      "kind": "test",
      "status": "ok"
    }
  ],
  "generator": "lobster_junit",
  "schema": "lobster-act-trace",
  "version": 3
}
