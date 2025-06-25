{
  "schema": "lobster-report",
  "version": 2,
  "generator": "sparrow",
  "levels": [
    {
      "name": "code",
      "kind": "implementation",
      "items": [
        {
          "tag": "imp tag-in-file-which-does-not-exist",
          "location": {
            "kind": "file",
            "file": "does-not-exist.file",
            "line": 8,
            "column": null
          },
          "name": "name of file which does not exist",
          "tracing_status": "JUSTIFIED",
          "language": "French",
          "kind": "beautiful"
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
