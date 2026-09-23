{
  "schema": "lobster-report",
  "version": 2,
  "generator": "universe",
  "levels": [
    {
      "name": "Atoms",
      "kind": "requirements",
      "items": [
        {
          "tag": "element xenon",
          "location": {
            "kind": "file",
            "file": "xenon.element",
            "line": 3,
            "column": 72000
          },
          "name": "xenon",
          "messages": [],
          "tracing_status": "OK",
          "framework": "lab-experiment",
          "kind": "chemical",
          "text": "This xenon atom has got all its 54 electrons"
        },
        {
          "tag": "element krypton",
          "location": {
            "kind": "file",
            "file": "krypton.element",
            "line": 999999,
            "column": 12
          },
          "name": "krypton",
          "messages": [],
          "tracing_status": "JUSTIFIED",
          "framework": "lab-experiment",
          "kind": "chemical",
          "text": "This krypton atom has got all its 36 electrons"
        }
      ],
      "coverage": 100.0
    }
  ],
  "policy": {
    "Atoms": {
      "name": "Atoms",
      "kind": "chemical",
      "traces": [],
      "source": [
        {
          "file": "my-noble-atoms.lobster"
        }
      ],
      "needs_tracing_up": false,
      "needs_tracing_down": false,
      "breakdown_requirements": []
    }
  },
  "matrix": []
}
