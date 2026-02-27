{
  "schema": "lobster-report",
  "version": 2,
  "generator": "lobster_report",
  "levels": [
    {
      "name": "System Requirements",
      "items": [
        {
          "tag": "req software_example.finder",
          "location": {
            "kind": "file",
            "file": "linear_requirements.trlc",
            "line": 4,
            "column": 28
          },
          "name": "software_example.finder",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "req software_example.search_books"
          ],
          "tracing_status": "OK"
        },
        {
          "tag": "req software_example.tracker",
          "location": {
            "kind": "file",
            "file": "linear_requirements.trlc",
            "line": 8,
            "column": 28
          },
          "name": "software_example.tracker",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "req software_example.reading_tracker"
          ],
          "tracing_status": "OK"
        },
        {
          "tag": "req software_example.organizer",
          "location": {
            "kind": "file",
            "file": "linear_requirements.trlc",
            "line": 12,
            "column": 28
          },
          "name": "software_example.organizer",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "req software_example.library_manager"
          ],
          "tracing_status": "OK"
        },
        {
          "tag": "req software_example.reviews",
          "location": {
            "kind": "file",
            "file": "linear_requirements.trlc",
            "line": 16,
            "column": 28
          },
          "name": "software_example.reviews",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "req software_example.book_reviews"
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
          "tag": "req software_example.search_books",
          "location": {
            "kind": "file",
            "file": "linear_requirements.trlc",
            "line": 20,
            "column": 30
          },
          "name": "software_example.search_books",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req software_example.finder"
          ],
          "ref_down": [
            "python simple_book_system.SimpleBookSystem.search_books"
          ],
          "tracing_status": "OK"
        },
        {
          "tag": "req software_example.reading_tracker",
          "location": {
            "kind": "file",
            "file": "linear_requirements.trlc",
            "line": 25,
            "column": 30
          },
          "name": "software_example.reading_tracker",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req software_example.tracker"
          ],
          "ref_down": [
            "python simple_book_system.SimpleBookSystem.track_progress"
          ],
          "tracing_status": "OK"
        },
        {
          "tag": "req software_example.library_manager",
          "location": {
            "kind": "file",
            "file": "linear_requirements.trlc",
            "line": 30,
            "column": 30
          },
          "name": "software_example.library_manager",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req software_example.organizer"
          ],
          "ref_down": [
            "python simple_book_system.SimpleBookSystem.organize_library"
          ],
          "tracing_status": "OK"
        },
        {
          "tag": "req software_example.book_reviews",
          "location": {
            "kind": "file",
            "file": "linear_requirements.trlc",
            "line": 35,
            "column": 30
          },
          "name": "software_example.book_reviews",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req software_example.reviews"
          ],
          "ref_down": [
            "python simple_book_system.SimpleBookSystem.add_review",
            "python simple_book_system.SimpleBookSystem.show_reviews"
          ],
          "tracing_status": "OK"
        }
      ],
      "coverage": 100.0
    },
    {
      "name": "Code",
      "items": [
        {
          "tag": "python simple_book_system.SimpleBookSystem.search_books",
          "location": {
            "kind": "file",
            "file": "simple_book_system.py",
            "line": 24,
            "column": null
          },
          "name": "simple_book_system.SimpleBookSystem.search_books",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req software_example.search_books"
          ],
          "ref_down": [],
          "tracing_status": "OK"
        },
        {
          "tag": "python simple_book_system.SimpleBookSystem.track_progress",
          "location": {
            "kind": "file",
            "file": "simple_book_system.py",
            "line": 41,
            "column": null
          },
          "name": "simple_book_system.SimpleBookSystem.track_progress",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req software_example.reading_tracker"
          ],
          "ref_down": [],
          "tracing_status": "OK"
        },
        {
          "tag": "python simple_book_system.SimpleBookSystem.organize_library",
          "location": {
            "kind": "file",
            "file": "simple_book_system.py",
            "line": 59,
            "column": null
          },
          "name": "simple_book_system.SimpleBookSystem.organize_library",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req software_example.library_manager"
          ],
          "ref_down": [],
          "tracing_status": "OK"
        },
        {
          "tag": "python simple_book_system.SimpleBookSystem.add_review",
          "location": {
            "kind": "file",
            "file": "simple_book_system.py",
            "line": 74,
            "column": null
          },
          "name": "simple_book_system.SimpleBookSystem.add_review",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req software_example.book_reviews"
          ],
          "ref_down": [],
          "tracing_status": "OK"
        },
        {
          "tag": "python simple_book_system.SimpleBookSystem.show_reviews",
          "location": {
            "kind": "file",
            "file": "simple_book_system.py",
            "line": 90,
            "column": null
          },
          "name": "simple_book_system.SimpleBookSystem.show_reviews",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req software_example.book_reviews"
          ],
          "ref_down": [],
          "tracing_status": "OK"
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
          "file": "linear_system_requirements_no_schema.lobster"
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
          "file": "linear_software_requirements_no_schema.lobster"
        }
      ],
      "needs_tracing_up": true,
      "needs_tracing_down": true,
      "breakdown_requirements": [
        [
          "Code"
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
          "file": "code_linear_no_schema.lobster"
        }
      ],
      "needs_tracing_up": true,
      "needs_tracing_down": false,
      "breakdown_requirements": []
    }
  },
  "matrix": []
}
