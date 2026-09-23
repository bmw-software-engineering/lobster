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
          "tag": "element charge.neutral",
          "location": {
            "kind": "file",
            "file": "hydrogen.element",
            "line": 3,
            "column": 72000
          },
          "name": "charge.neutral",
          "messages": [],
          "tracing_status": "OK",
          "framework": "lab-experiment",
          "kind": "chemical",
          "text": "This hydrogen atom has got one electron"
        },
        {
          "tag": "element charge.ionized",
          "location": {
            "kind": "file",
            "file": "hydrogen.element",
            "line": 8,
            "column": 5
          },
          "name": "charge.ionized",
          "messages": [
            "missing electron"
          ],
          "tracing_status": "MISSING",
          "framework": "lab-experiment",
          "kind": "chemical",
          "text": "This hydrogen atom has lost its electron"
        }
      ],
      "coverage": 50.0
    }
  ],
  "policy": {
    "Atoms": {
      "name": "Atoms",
      "kind": "chemical",
      "traces": [],
      "source": [
        {
          "file": "my-lovely-atoms.lobster"
        }
      ],
      "needs_tracing_up": false,
      "needs_tracing_down": false,
      "breakdown_requirements": []
    }
  },
  "matrix": []
}
