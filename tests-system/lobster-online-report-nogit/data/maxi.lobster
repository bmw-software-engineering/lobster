{
  "schema": "lobster-report",
  "version": 2,
  "generator": "lobster_report",
  "levels": [
    {
      "name": "level A",
      "kind": "implementation",
      "items": [
        {
          "tag": "imp tag01",
          "location": {
            "kind": "file",
            "file": "file_01.txt",
            "line": 1,
            "column": null
          },
          "name": "name of tag01",
          "tracing_status": "JUSTIFIED",
          "language": "language_01",
          "kind": "kind_01"
        },
        {
          "tag": "imp tag02",
          "location": {
            "kind": "file",
            "file": "file_02.txt",
            "line": 2,
            "column": null
          },
          "name": "name of tag02",
          "tracing_status": "OK",
          "language": "language_02",
          "kind": "kind_02"
        }
      ],
      "coverage": 0.0
    },
    {
      "name": "level B",
      "kind": "activity",
      "items": [
        {
          "tag": "act tag03",
          "location": {
            "kind": "file",
            "file": "file_03.txt",
            "line": 3,
            "column": null
          },
          "tracing_status": "PARTIAL",
          "framework": "framework_03",
          "kind": "kind_03"
        },
        {
          "tag": "act tag04",
          "location": {
            "kind": "file",
            "file": "file_04.txt",
            "line": 4,
            "column": null
          },
          "tracing_status": "MISSING",
          "framework": "framework_04",
          "kind": "kind_04"
        }
      ],
      "coverage": 0.0
    },
    {
      "name": "level C",
      "kind": "requirements",
      "items": [
        {
          "tag": "req tag05",
          "location": {
            "kind": "file",
            "file": "file_05.txt",
            "line": 5,
            "column": null
          },
          "name": "name of tag05",
          "tracing_status": "ERROR",
          "framework": "framework_05",
          "kind": "kind_05",
          "text": "text 05"
        },
        {
          "tag": "req tag06",
          "location": {
            "kind": "file",
            "file": "very/deeply/nested/file_06.txt",
            "line": 6,
            "column": null
          },
          "name": "name of tag06",
          "tracing_status": "OK",
          "framework": "framework_06",
          "kind": "kind_06",
          "text": "text 06"
        }
      ],
      "coverage": 0.0
    },
    {
      "name": "level D",
      "kind": "requirements",
      "items": [
        {
          "tag": "req tag07",
          "location": {
            "kind": "codebeamer",
            "cb_root": "https://the.server.07",
            "tracker": 77,
            "item": 7,
            "version": 777,
            "name": "name of tag07"
          },
          "name": "name of tag07",
          "tracing_status": "OK",
          "framework": "framework_07",
          "kind": "kind_07",
          "text": "text 07"
        }
      ],
      "coverage": 0.0
    }
  ],
  "policy": {
    "level A": {
      "name": "level A",
      "kind": "implementation",
      "traces": [],
      "source": [
        {
          "file": "level_a.lobster"
        }
      ]
    },
    "level B": {
      "name": "level B",
      "kind": "activity",
      "traces": [],
      "source": [
        {
          "file": "level_b.lobster"
        }
      ]
    },
    "level C": {
      "name": "level C",
      "kind": "requirements",
      "traces": [],
      "source": [
        {
          "file": "level_c.lobster"
        }
      ]
    },
    "level D": {
      "name": "level D",
      "kind": "requirements",
      "traces": [],
      "source": [
        {
          "file": "level_d.lobster"
        }
      ]
    }
  },
  "matrix": []
}
