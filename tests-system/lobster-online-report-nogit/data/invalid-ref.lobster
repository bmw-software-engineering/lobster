{
  "schema": "lobster-report",
  "version": 2,
  "generator": "lobster_report",
  "levels": [
    {
      "name": "code",
      "kind": "implementation",
      "items": [
        {
          "tag": "imp tag1",
          "location": {
            "kind": "file",
            "file": "does-not-exist.file",
            "line": 8,
            "column": null
          },
          "name": "name of file which does not exist",
          "tracing_status": "JUSTIFIED",
          "language": "Python",
          "kind": "Expert"
        }
      ],
      "coverage": 0.0
    }
  ],
  "policy": {
    "code": {
      "name": "code",
      "kind": "implementation",
      "traces": [],
      "source": [
        {
          "file": "implementation.lobster",
          "filters": []
        }
      ]
    }
  },
  "matrix": []
}
