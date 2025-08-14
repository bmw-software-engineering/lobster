{
  "schema": "lobster-report",
  "version": 2,
  "generator": "lobster_report",
  "levels": [
    {
      "name": "System Requirements",
      "kind": "requirements",
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
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "system_requirement",
          "text": "The system shall find books that people actually want to read",
          "status": null
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
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "system_requirement",
          "text": "The system shall count pages read without making people feel guilty",
          "status": null
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
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "system_requirement",
          "text": "The system shall arrange books so they can be found again",
          "status": null
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
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "system_requirement",
          "text": "The system shall gather opinions about books from real humans",
          "status": null
        }
      ],
      "coverage": 100.0
    },
    {
      "name": "Software Requirements",
      "kind": "requirements",
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
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "software_requirement",
          "text": "The software shall implement book search functionality",
          "status": null
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
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "software_requirement",
          "text": "The software shall track reading progress and statistics",
          "status": null
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
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "software_requirement",
          "text": "The software shall organize and categorize books",
          "status": null
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
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "software_requirement",
          "text": "The software shall collect and display book reviews",
          "status": null
        }
      ],
      "coverage": 100.0
    },
    {
      "name": "Code",
      "kind": "implementation",
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
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
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
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
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
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
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
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
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
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        }
      ],
      "coverage": 100.0
    }
  ],
  "policy": {
    "System Requirements": {
      "name": "System Requirements",
      "kind": "requirements",
      "traces": [],
      "source": [
        {
          "file": "linear_system_requirements.lobster"
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
      "kind": "requirements",
      "traces": [
        "System Requirements"
      ],
      "source": [
        {
          "file": "linear_software_requirements.lobster"
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
      "kind": "implementation",
      "traces": [
        "Software Requirements"
      ],
      "source": [
        {
          "file": "code_linear.lobster"
        }
      ],
      "needs_tracing_up": true,
      "needs_tracing_down": false,
      "breakdown_requirements": []
    }
  },
  "matrix": []
}
