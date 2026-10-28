{
  "data": [
    {
      "tag": "junit com.example.StackTest:GivenEmptyStack_ExpectSizeZero",
      "location": {
        "kind": "void"
      },
      "name": "com.example.StackTest:GivenEmptyStack_ExpectSizeZero",
      "messages": [],
      "just_up": [],
      "just_down": [],
      "just_global": [],
      "refs": [
        "req Stack.Size"
      ],
      "framework": "JUnit",
      "kind": "test",
      "text": ":Given: empty stack\n:Then: size zero",
      "status": "ok"
    },
    {
      "tag": "junit com.example.StackTest:peekOfFullStack",
      "location": {
        "kind": "void"
      },
      "name": "com.example.StackTest:peekOfFullStack",
      "messages": [],
      "just_up": [],
      "just_down": [],
      "just_global": [],
      "refs": [
        "req Stack.Peek"
      ],
      "framework": "JUnit",
      "kind": "test",
      "status": "not run"
    },
    {
      "tag": "junit com.example.StackTest$Nested:pushIncreasesSize",
      "location": {
        "kind": "file",
        "file": "src/test/StackTest.java",
        "line": 12,
        "column": null
      },
      "name": "com.example.StackTest$Nested:pushIncreasesSize",
      "messages": [],
      "just_up": [],
      "just_down": [],
      "just_global": [],
      "refs": [
        "req Stack.Push"
      ],
      "framework": "JUnit",
      "kind": "test",
      "status": "ok"
    },
    {
      "tag": "junit com.example.StackTest$Nested:popOfEmptyStack",
      "location": {
        "kind": "file",
        "file": "src/test/StackPopTest.java",
        "line": 7,
        "column": null
      },
      "name": "com.example.StackTest$Nested:popOfEmptyStack",
      "messages": [],
      "just_up": [],
      "just_down": [],
      "just_global": [],
      "refs": [
        "req Stack.Pop"
      ],
      "framework": "JUnit",
      "kind": "test",
      "status": "fail"
    }
  ],
  "generator": "lobster_junit",
  "schema": "lobster-act-trace",
  "version": 3
}
