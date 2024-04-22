{
  "schema": "lobster-report",
  "version": 2,
  "generator": "lobster_report",
  "levels": [
    {
      "name": "Specification",
      "kind": "requirements",
      "items": [
        {
          "tag": "req LRM.Goals",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 14
          },
          "name": "LRM.Goals",
          "messages": [],
          "just_up": [],
          "just_down": [
            "Design goals are reflected in language design."
          ],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "framework": "TRLC",
          "kind": "Text",
          "text": "text: It is important to have design goals for a language. The\ndesign goals of TRLC are:\n\nbullets: ['The intended domain is requirements writing in an industrial\\nsafety-critical context, where requirements carry a\\nlot of meta-data and linkage.', 'Future language releases should be backwards compatible, as\\nwe anticipate that there will be a large body of\\nrequirements.', 'Language design should be extensible and flexible for future\\nchanges.', 'Requirement files (but not necessarily model and check\\nfiles) should be human-readable with minimal\\ntraining or understanding of the language.', 'No business logic should be encoded in the language design.']",
          "status": null
        },
        {
          "tag": "req LRM.File_Encoding",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 43
          },
          "name": "LRM.File_Encoding",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python lexer.TRLC_Lexer.__init__",
            "trlc-st file-encoding-not-utf8"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Text",
          "text": "text: All input files are encoded in UTF-8. Passing a file with a\ndifferent encoding to TRLC results in\nundefined behaviour.",
          "status": null
        },
        {
          "tag": "req LRM.File_Encoding_Fixed",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 49
          },
          "name": "LRM.File_Encoding_Fixed",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python lexer.TRLC_Lexer.__init__",
            "trlc-st file-encoding-not-utf8"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Recommendation",
          "text": "text: It is recommended to try to detect this in an implementation\nand raise a fatal error; but in the interest\nof compatibility and sanity an\nimplementation shall not provide a way to\nswitch the encoding (at the command-line or\notherwise).",
          "status": null
        },
        {
          "tag": "req LRM.Whitespace",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 60
          },
          "name": "LRM.Whitespace",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python lexer.Lexer_Base.skip_whitespace",
            "trlc-st whitespace"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Text",
          "text": "text: Whitespace is ignored.",
          "status": null
        },
        {
          "tag": "req LRM.Comments",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 64
          },
          "name": "LRM.Comments",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python lexer.TRLC_Lexer.token",
            "python parser.Parser_Base.advance",
            "trlc-st comments-1",
            "pyunit test_lexer.Test_Lexer.testComment"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Text",
          "text": "text: Comments are C-Style `/* .. */` and C++ style `//`, and are\nignored. The matching for C-style comments\nis non-greedy.",
          "status": null
        },
        {
          "tag": "req LRM.Identifier",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 72
          },
          "name": "LRM.Identifier",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python lexer.Lexer_Base.is_alpha",
            "python lexer.Lexer_Base.is_alnum",
            "python lexer.TRLC_Lexer.token",
            "pyunit test_lexer.Test_Lexer.testIdentifiers1",
            "pyunit test_lexer.Test_Lexer.testIdentifiers2",
            "pyunit test_lexer.Test_Lexer.testIdentifiers3"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Terminal",
          "text": "text: Identifiers start with a letter and are followed by letters,\nnumbers, or underscores.",
          "status": null
        },
        {
          "tag": "req LRM.TRLC_Keywords",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 81
          },
          "name": "LRM.TRLC_Keywords",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python lexer.TRLC_Lexer.token",
            "pyunit test_lexer.Test_Lexer.testKeywords"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Keywords",
          "text": "text: A keyword is an identifier that is one of the following\nreserved words:\n\nbullets: ['abs', 'abstract', 'and', 'checks', 'else', 'elsif', 'enum', 'error', 'exists', 'extends', 'false', 'fatal', 'final', 'forall', 'freeze', 'if', 'implies', 'import', 'in', 'not', 'null', 'optional', 'or', 'package', 'section', 'separator', 'then', 'true', 'tuple', 'type', 'warning', 'xor']",
          "status": null
        },
        {
          "tag": "req LRM.Single_Delimiters",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 123
          },
          "name": "LRM.Single_Delimiters",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python lexer.TRLC_Lexer.token",
            "pyunit test_lexer.Test_Lexer.testPunctuationSingle"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Punctuation",
          "text": "text: Single character delimiters:\n\nbullets: ['Brackets: `(` `)` `[` `]` `{` `}`', 'Punctuation: `,` `.` `=`', 'Operators: `*` `/` `%` `+` `-`', 'Boolean operators: `<` `>`', 'Symbols: `@` `:` `;`']",
          "status": null
        },
        {
          "tag": "req LRM.Double_Delimiters",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 134
          },
          "name": "LRM.Double_Delimiters",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python lexer.TRLC_Lexer.token",
            "pyunit test_lexer.Test_Lexer.testPunctuationDouble",
            "pyunit test_lexer.Test_Lexer.testIncompleteNEQ"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Punctuation",
          "text": "text: Double character delimiters:\n\nbullets: ['Operators: `**`', 'Boolean operators: `==` `<=` `>=` `!=`', 'Punctuation: `=>` `..`']",
          "status": null
        },
        {
          "tag": "req LRM.Lexing_Disambiguation",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 143
          },
          "name": "LRM.Lexing_Disambiguation",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python lexer.TRLC_Lexer.token",
            "pyunit test_lexer.Test_Lexer.testPunctuationDouble"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Text",
          "text": "text: Preference is (obviously) given to longer delimiters if\nthere is ambiguity; i.e. `==` takes\nprecedence over two `=` tokens.",
          "status": null
        },
        {
          "tag": "req LRM.Integers",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 151
          },
          "name": "LRM.Integers",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python lexer.Lexer_Base.is_numeric",
            "python lexer.TRLC_Lexer.token",
            "pyunit test_lexer.Test_Lexer.testIdentifiers1",
            "pyunit test_lexer.Test_Lexer.testIntegers1",
            "pyunit test_lexer.Test_Lexer.testIntegers2",
            "pyunit test_lexer.Test_Lexer.testIntegers3",
            "pyunit test_lexer.Test_Lexer.testIntegers4"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Terminal",
          "text": "text: Integers are base 2 (prefixed by `0b`), 10, or 16 (prefixed\nby `0x`), and leading zeros are effectively\nignored. It is possible to separate digit\ngroups with an underscore for\nreadability. It shall be a lexing error to\nuse digits that do not fit into the base.",
          "status": null
        },
        {
          "tag": "req LRM.Decimals",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 164
          },
          "name": "LRM.Decimals",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python lexer.Lexer_Base.is_numeric",
            "python lexer.TRLC_Lexer.token",
            "pyunit test_lexer.Test_Lexer.testDecimals1",
            "pyunit test_lexer.Test_Lexer.testDecimals2",
            "pyunit test_lexer.Test_Lexer.testDecimals3"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Terminal",
          "text": "text: Decimals are base 10, and leading and trailing zeros are\neffectively ignored.",
          "status": null
        },
        {
          "tag": "req LRM.Strings",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 173
          },
          "name": "LRM.Strings",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python lexer.TRLC_Lexer.token",
            "pyunit test_lexer.Test_Lexer.testStrings1",
            "pyunit test_lexer.Test_Lexer.testStrings2",
            "pyunit test_lexer.Test_Lexer.testStrings3",
            "pyunit test_lexer.Test_Lexer.testStrings4",
            "pyunit test_lexer.Test_Lexer.testStrings5",
            "pyunit test_lexer.Test_Lexer.testStrings6",
            "pyunit test_lexer.Test_Lexer.testStrings7"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Terminal",
          "text": "text: There are three versions of a string, double quoted,\ntriple single quoted, and triple double quoted:",
          "status": null
        },
        {
          "tag": "req LRM.Simple_String_Value",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 184
          },
          "name": "LRM.Simple_String_Value",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python lexer.TRLC_Lexer.token",
            "pyunit test_lexer.Test_Lexer.testStrings1"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: The value of a double quoted string is precisely the\ncharacters between the two double quotes,\nwith all instances of the `\\\"` escape\nsequence being replaced with `\"`.",
          "status": null
        },
        {
          "tag": "req LRM.Complex_String_Value",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 191
          },
          "name": "LRM.Complex_String_Value",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python lexer.triple_quoted_string_value",
            "pyunit test_lexer.Test_Lexer.testStrings2",
            "pyunit test_lexer.Test_Lexer.testStrings6"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: The value of a triple quoted string is the whitespace\ntrimmed string of characters between the triple quotes\n(including the line breaks), The common whitespace at\nthe beginning of each line (ignoring blank lines) starting\nat the second is removed. The trailing whitespace on\nevery line is removed. There is no escaping in a triple\nquoted string.",
          "status": null
        },
        {
          "tag": "req LRM.Layout",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 208
          },
          "name": "LRM.Layout",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python trlc.Source_Manager.register_file",
            "python trlc.Source_Manager.register_directory",
            "python parser.Parser.parse_preamble",
            "trlc-st simple"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Text",
          "text": "text: There are three types of files:\n\nbullets: ['`.rsl` They contains the user-defined type definitions and\\noptionally user-defined warnings or checks', '(deprecated) `.check` They contain only user-defined warning\\nor error messages for types declared in `.rsl`\\nfiles', '`.trlc` They contain instances of the types (this is where\\nyour requirements go)']",
          "status": null
        },
        {
          "tag": "req LRM.File_Parsing_Order",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 221
          },
          "name": "LRM.File_Parsing_Order",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python trlc.Source_Manager.process",
            "trlc-st delayed-references-1",
            "trlc-st simple"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Dynamic_Semantics",
          "text": "text: First, all `.rsl` files are parsed. Then, if no errors are\nraised, all `.check` files are parsed. Finally, if no errors\nare raised, all `.trlc` files are parsed.",
          "status": null
        },
        {
          "tag": "req LRM.File_Parsing_References",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 229
          },
          "name": "LRM.File_Parsing_References",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python trlc.Source_Manager.process",
            "trlc-st delayed-references-1"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Dynamic_Semantics",
          "text": "text: After all files are parsed, references are resolved and\nuser-defined checks are applied.",
          "status": null
        },
        {
          "tag": "req LRM.Errors_In_TRLC_Files",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 236
          },
          "name": "LRM.Errors_In_TRLC_Files",
          "messages": [],
          "just_up": [],
          "just_down": [
            "This recommendation is not followed, as it would make the\nqualification of the tool more difficult."
          ],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "framework": "TRLC",
          "kind": "Recommendation",
          "text": "text: It is unspecified how an implementation treats errors\nin `.trlc` files, but it is recommended to not stop\nprocessing after the first error.",
          "status": null
        },
        {
          "tag": "req LRM.Preamble",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 254
          },
          "name": "LRM.Preamble",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python trlc.Source_Manager.register_rsl_file",
            "python trlc.Source_Manager.register_check_file",
            "python trlc.Source_Manager.register_trlc_file",
            "python trlc.Source_Manager.build_graph",
            "python trlc.Source_Manager.parse_rsl_files",
            "python trlc.Source_Manager.parse_check_files",
            "python trlc.Source_Manager.parse_trlc_files",
            "python parser.Parser.parse_preamble",
            "trlc-st preamble-1",
            "trlc-st simple"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Grammar",
          "text": "text: All files start with a package indication and an optional import list.\n\nbnf: file_preamble ::= package_indication\n                  { import_clause }\n\npackage_indication ::= 'package' IDENTIFIER_name\n\nimport_clause ::= 'import' IDENTIFIER_name",
          "status": null
        },
        {
          "tag": "req LRM.Current_Package",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 268
          },
          "name": "LRM.Current_Package",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python parser.Parser.parse_preamble",
            "python ast.Compilation_Unit.set_package",
            "trlc-st delayed-references-1"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: The package indication defines the \"current package\".",
          "status": null
        },
        {
          "tag": "req LRM.Import_Visibility",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 272
          },
          "name": "LRM.Import_Visibility",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python parser.Parser.parse_preamble",
            "python ast.Compilation_Unit.add_import",
            "python ast.Compilation_Unit.resolve_imports",
            "python ast.Compilation_Unit.is_visible",
            "trlc-st multiple-models",
            "trlc-st visibility-1"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: A package may be imported, in which case its name may be\nused as the prefix of a `qualified_name`.",
          "status": null
        },
        {
          "tag": "req LRM.Self_Imports",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 277
          },
          "name": "LRM.Self_Imports",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python ast.Compilation_Unit.add_import",
            "trlc-st preamble-1"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: A package may not import itself.",
          "status": null
        },
        {
          "tag": "req LRM.RSL_File",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 287
          },
          "name": "LRM.RSL_File",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python trlc.Source_Manager.parse_rsl_files",
            "python parser.Parser.parse_rsl_file",
            "python ast.Compilation_Unit.add_item",
            "trlc-st simple"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Grammar",
          "text": "text: A `.rsl` file starts with a package declaration and is\nfollowed by type declarations.\n\nbnf: rsl_file ::= file_preamble\n{ type_declaration | check_block }",
          "status": null
        },
        {
          "tag": "req LRM.Package_Declaration",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 296
          },
          "name": "LRM.Package_Declaration",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python parser.Parser.parse_preamble",
            "trlc-st cross-refs-in-errors"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: A package indication in an `.rsl` file declares a\npackage. Any given package name may only be\ndeclared once globally.",
          "status": null
        },
        {
          "tag": "req LRM.Circular_Dependencies",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 302
          },
          "name": "LRM.Circular_Dependencies",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python trlc.Source_Manager.parse_rsl_files",
            "trlc-st cyclic-packages"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: In a `.rsl` file, a package may not import a package that\nimports itself, directly or indirectly.",
          "status": null
        },
        {
          "tag": "req LRM.Builtin_Types",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 307
          },
          "name": "LRM.Builtin_Types",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python ast.Builtin_Type",
            "python ast.Builtin_Numeric_Type",
            "python ast.Builtin_Integer",
            "python ast.Builtin_Decimal",
            "python ast.Builtin_Boolean",
            "python ast.Builtin_String",
            "python ast.Builtin_Markup_String",
            "python ast.Symbol_Table.create_global_table",
            "trlc-st rbt-builtin-types"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: An implementation shall support the following builtin types,\nthat shall be made available for all packages:\n\nbullets: ['Boolean', 'Integer', 'Decimal', 'String', 'Markup_String']",
          "status": null
        },
        {
          "tag": "req LRM.Boolean_Values",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 319
          },
          "name": "LRM.Boolean_Values",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python parser.Parser.parse_primary",
            "python parser.Parser.parse_boolean",
            "python ast.Value",
            "python ast.Boolean_Literal",
            "python ast.Builtin_Boolean",
            "trlc-st rbt-boolean-values"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: A `Boolean` has two values, `false` and `true`.",
          "status": null
        },
        {
          "tag": "req LRM.Integer_Values",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 323
          },
          "name": "LRM.Integer_Values",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python lexer.TRLC_Lexer.token",
            "python parser.Parser.parse_primary",
            "python parser.Parser.parse_value",
            "python ast.Value",
            "python ast.Integer_Literal",
            "python ast.Builtin_Integer",
            "trlc-st rbt-integer-values"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: An `Integer` is a signed integer, with an implementation\ndefined range. This range shall be at least\n-1000 to 1000, and this can be infinite.",
          "status": null
        },
        {
          "tag": "req LRM.Decimal_Values",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 329
          },
          "name": "LRM.Decimal_Values",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python lexer.TRLC_Lexer.token",
            "python parser.Parser.parse_primary",
            "python parser.Parser.parse_value",
            "python ast.Value",
            "python ast.Decimal_Literal",
            "python ast.Builtin_Decimal",
            "trlc-st rbt-decimal-values"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: A `Decimal` is a signed rational with a power-of-ten\ndenominator, with an implementation defined\nrange. This range for the numerator shall be\nat least -1000 to 1000, and denominator is\nalways a natural number with a range of at\nleast 1 to 1000. Any of these ranges can be\ninfinite (but the denominator is always\nnon-negative).",
          "status": null
        },
        {
          "tag": "req LRM.String_Values",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 340
          },
          "name": "LRM.String_Values",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python parser.Parser.parse_primary",
            "python parser.Parser.parse_value",
            "python ast.Value",
            "python ast.String_Literal",
            "python ast.Builtin_String",
            "trlc-st rbt-string-values"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: A `String` is a sequence of implementation defined\ncharacters. *(The decision to support Unicode\nor not is left unspecified.)* The maximum\nlength of a String, if any, is implementation\ndefined, but shall be at least 1000.",
          "status": null
        },
        {
          "tag": "req LRM.Markup_String_Values",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 348
          },
          "name": "LRM.Markup_String_Values",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python parser.Parser.parse_value",
            "python parser.Parser.parse_markup_string",
            "python ast.Value",
            "python ast.String_Literal",
            "python ast.Builtin_Markup_String",
            "trlc-st rbt-markup-string-values"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: A `Markup_String` is identical to a `String`, except for a\nfew additional constraints on the string\ncontents. Any value of type `Markup_String` is\na valid instance of `String`, but not the\nother way around.",
          "status": null
        },
        {
          "tag": "req LRM.Builtin_Functions",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 356
          },
          "name": "LRM.Builtin_Functions",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python parser.Parser.parse_builtin",
            "python parser.Parser.parse_name",
            "python ast.Builtin_Function",
            "python ast.Symbol_Table.create_global_table",
            "trlc-st rbt-builtin-functions"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: A package also includes a number of builtin functions that\nare made available:\n\nbullets: ['len', 'startswith', 'endswith', 'matches']",
          "status": null
        },
        {
          "tag": "req LRM.Builtin_Type_Conversion_Functions",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 367
          },
          "name": "LRM.Builtin_Type_Conversion_Functions",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python parser.Parser.parse_builtin",
            "python parser.Parser.parse_name",
            "python ast.Symbol_Table.create_global_table",
            "trlc-st decimal-1",
            "trlc-st decimal-5"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: A package also makes available a number of numeric type\nconversion functions:\n\nbullets: ['Integer', 'Decimal']",
          "status": null
        },
        {
          "tag": "req LRM.Described_Names",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 379
          },
          "name": "LRM.Described_Names",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python parser.Parser.parse_described_name",
            "trlc-st rbt-described-names"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Grammar",
          "text": "bnf: described_name ::= IDENTIFIER_name [ STRING_description ]",
          "status": null
        },
        {
          "tag": "req LRM.Described_Name_Description",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 385
          },
          "name": "LRM.Described_Name_Description",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python parser.Parser.parse_described_name",
            "python ast.Composite_Type.__init__",
            "python ast.Composite_Component.__init__",
            "python ast.Enumeration_Type.__init__",
            "python ast.Enumeration_Literal_Spec.__init__",
            "trlc-st rbt-described-names"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: A described name names an entity. The optional string\ndescription has no static or dynamic\nsemantics.",
          "status": null
        },
        {
          "tag": "req LRM.Described_Name_Equality",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 391
          },
          "name": "LRM.Described_Name_Equality",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python ast.Entity.__init__",
            "python ast.Symbol_Table.__contains__",
            "python ast.Symbol_Table.contains",
            "python ast.Symbol_Table.lookup_assuming",
            "python ast.Symbol_Table.lookup_direct",
            "python ast.Symbol_Table.lookup",
            "trlc-st rbt-described-name-equality"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: Two described names are considered equal if their names are\nequal.",
          "status": null
        },
        {
          "tag": "req LRM.Described_Name_Notes",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 396
          },
          "name": "LRM.Described_Name_Notes",
          "messages": [],
          "just_up": [],
          "just_down": [
            "Non-normative text"
          ],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "framework": "TRLC",
          "kind": "Note",
          "text": "text: The description has no bearing on equality. The string\ndescription should be exported to the API, so\nthat downstream tools can make use of it. This\nway we don't have to give some comments special meaning,\nand we don't have to implement error-prone heuristics in\ndownstream tools for discovering these descriptions.",
          "status": null
        },
        {
          "tag": "req LRM.Qualified_Name",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 409
          },
          "name": "LRM.Qualified_Name",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python parser.Markup_Parser.parse_qualified_name",
            "python parser.Parser.parse_qualified_name",
            "python ast.Name_Reference",
            "trlc-st rbt-qualified-name"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Grammar",
          "text": "bnf: qualified_name ::= [ IDENTIFIER_package_name '.' ] IDENTIFIER_name",
          "status": null
        },
        {
          "tag": "req LRM.Valid_Qualifier",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 415
          },
          "name": "LRM.Valid_Qualifier",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python parser.Markup_Parser.parse_qualified_name",
            "python parser.Parser.parse_qualified_name",
            "trlc-st rbt-qualified-name"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: The package name of a qualified name must be the current\npackage or an imported package.",
          "status": null
        },
        {
          "tag": "req LRM.Valid_Name",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 420
          },
          "name": "LRM.Valid_Name",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python parser.Markup_Parser.parse_qualified_name",
            "python parser.Parser.parse_qualified_name",
            "trlc-st rbt-qualified-name"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: The name must be a valid symbol in the current scope (if no\npackage is provided) or a valid symbol of the\nindicated package.",
          "status": null
        },
        {
          "tag": "req LRM.Type_Declarations",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 430
          },
          "name": "LRM.Type_Declarations",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python parser.Parser.parse_type_declaration",
            "python ast.Concrete_Type",
            "trlc-st rbt-described-names"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Grammar",
          "text": "bnf: type_declaration ::= enumeration_declaration\n| tuple_declaration\n| record_declaration",
          "status": null
        },
        {
          "tag": "req LRM.Duplicate_Types",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 438
          },
          "name": "LRM.Duplicate_Types",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python ast.Symbol_Table.register",
            "trlc-st rbt-duplicate-types"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: It is an error to create a type with a name that is already\nvisible. (Note: this especially includes\nshadowing one of the builtin types, but also\nmeans you cannot shadow packages.)",
          "status": null
        },
        {
          "tag": "req LRM.Enumeration_Declaration",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 447
          },
          "name": "LRM.Enumeration_Declaration",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python parser.Parser.parse_enum_declaration",
            "trlc-st enum",
            "trlc-st enum-ok"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Grammar",
          "text": "bnf: enumeration_declaration ::= 'enum' described_name\n                            '{' { enumeration_literal_specification } '}'\n\nenumeration_literal_specification ::= described_name",
          "status": null
        },
        {
          "tag": "req LRM.Unique_Enumeration_Literals",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 456
          },
          "name": "LRM.Unique_Enumeration_Literals",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python ast.Symbol_Table.register",
            "trlc-st rbt-unique-enumeration-literals"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: Each described name declares an enumeration literal\nspecification, which shall have a unique name\nin that enumeration.",
          "status": null
        },
        {
          "tag": "req LRM.Shared_Literals",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 462
          },
          "name": "LRM.Shared_Literals",
          "messages": [],
          "just_up": [],
          "just_down": [
            "Non-normative text"
          ],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "framework": "TRLC",
          "kind": "Note",
          "text": "text: It is not an error to have the same literal specification\nfor different enumerations.",
          "status": null
        },
        {
          "tag": "req LRM.Literals_Shadowing_Permitted",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 467
          },
          "name": "LRM.Literals_Shadowing_Permitted",
          "messages": [],
          "just_up": [],
          "just_down": [
            "Non-normative text"
          ],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "framework": "TRLC",
          "kind": "Note",
          "text": "text: It is not an error to have an enumeration literal with the\nsame name as a record or enumeration - as\nthere is no ambiguity - but it is recommended\nthat an implementation emits a warning in this\ncase.",
          "status": null
        },
        {
          "tag": "req LRM.No_Empty_Enumerations",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 475
          },
          "name": "LRM.No_Empty_Enumerations",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python parser.Parser.parse_enum_declaration",
            "trlc-st lint-vcg-empty-enum"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: It is an error to specify an (empty) enumeration without any\nliterals.",
          "status": null
        },
        {
          "tag": "req LRM.Enumeration_Example",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 480
          },
          "name": "LRM.Enumeration_Example",
          "messages": [],
          "just_up": [],
          "just_down": [
            "Non-normative example"
          ],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "framework": "TRLC",
          "kind": "Example",
          "text": null,
          "status": null
        },
        {
          "tag": "req LRM.Tuple_Declaration",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 500
          },
          "name": "LRM.Tuple_Declaration",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python parser.Parser.parse_tuple_declaration",
            "python ast.Tuple_Type.__init__",
            "python ast.Separator",
            "trlc-st rbt-tuple-declaration"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Grammar",
          "text": "bnf: tuple_declaration ::= 'tuple' described_name\n                      '{' field_declaration\n                          { [ separator_declaration ]\n                            field_declaration }\n                      '}'\n\nfield_declaration ::=\n  described_name [ 'optional' ] qualified_name_FIELD_TYPE\n\nseparator_declaration ::=\n  'separator' separator_symbol\n\nseparator_symbol ::= IDENTIFIER\n                   | '@'\n                   | ':'\n                   | ';'",
          "status": null
        },
        {
          "tag": "req LRM.Tuple_Field_Types",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 521
          },
          "name": "LRM.Tuple_Field_Types",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python parser.Parser.parse_tuple_field",
            "python parser.Parser.parse_tuple_declaration",
            "trlc-st rbt-tuple-field-types"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: A field type names any valid visible and complete\ntype. *(Specifically you may not have a recursive\ntuple reference.)*",
          "status": null
        },
        {
          "tag": "req LRM.Tuple_Separators_All_Or_None",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 529
          },
          "name": "LRM.Tuple_Separators_All_Or_None",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python parser.Parser.parse_tuple_declaration",
            "trlc-st rbt-tuple-separators-all-or-none"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: A tuple type shall declare separators between all\nfields, or none of them.",
          "status": null
        },
        {
          "tag": "req LRM.Restricted_Tuple_Nesting",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 536
          },
          "name": "LRM.Restricted_Tuple_Nesting",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python parser.Parser.parse_tuple_declaration",
            "trlc-st rbt-restricted-tuple-nesting-1",
            "trlc-st rbt-restricted-tuple-nesting-2"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: A tuple type with separators may not contain fields\nthat have tuple types with separators. *(This is to\navoid parsing ambiguities for values such as `1; 2;\n3`.)*",
          "status": null
        },
        {
          "tag": "req LRM.Tuple_Optional_Requires_Separators",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 545
          },
          "name": "LRM.Tuple_Optional_Requires_Separators",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python parser.Parser.parse_tuple_declaration",
            "trlc-st rbt-tuple-optional-requires-separators"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: Only tuples with separators may use optional fields. Tuples\nwithout separators cannot have optional fields.",
          "status": null
        },
        {
          "tag": "req LRM.Tuple_Optional_Fields",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 552
          },
          "name": "LRM.Tuple_Optional_Fields",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python parser.Parser.parse_tuple_declaration",
            "trlc-st rbt-tuple-optional-fields"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: After an optional field has been declared, all fields\nfollowing it must also be optional.",
          "status": null
        },
        {
          "tag": "req LRM.Tuple_Unique_Field_Names",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 559
          },
          "name": "LRM.Tuple_Unique_Field_Names",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python ast.Symbol_Table.register",
            "trlc-st rbt-tuple-unique-field-names"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: It is an error to declare two fields with the same\nname in the same tuple. *(Note that it is possible,\nbut a bad idea, to have a separator with the same\nidentifier as a field.)*",
          "status": null
        },
        {
          "tag": "req LRM.Tuple_Based_Literal_Ambiguity",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 568
          },
          "name": "LRM.Tuple_Based_Literal_Ambiguity",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python lint.Linter.verify_tuple_type",
            "trlc-st lint-ambiguous-literals"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Recommendation",
          "text": "text: There is a potential source of ambiguity between\ntuples with two or more integers separated by a `x`\nor `b`. This is resolved by giving precedence to the\nlexer. For example the string `0x123` should yield\nthe hex integer 291; but the string `0 x123` or `0 x\n123` will generate the tuple. It is recommended to\nwarn when building tuples where a `b` or `x`\nseparator follows an integer.",
          "status": null
        },
        {
          "tag": "req LRM.Tuple_Example",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 581
          },
          "name": "LRM.Tuple_Example",
          "messages": [],
          "just_up": [],
          "just_down": [
            "Non-normative example"
          ],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "framework": "TRLC",
          "kind": "Example",
          "text": null,
          "status": null
        },
        {
          "tag": "req LRM.Record_Declaration",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 612
          },
          "name": "LRM.Record_Declaration",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Grammar",
          "text": "bnf: record_declaration ::= [ inheritance_qualifier ] 'type' described_name\n                       [ 'extends' qualified_name_ROOT_TYPE ]\n                       '{' { component_declaration |\n                             component_freezing } '}'\n\ninheritance_qualifier ::= 'abstract' | 'final'\n\ncomponent_declaration ::=\n  described_name [ 'optional' ]\n  qualified_name_COMPONENT_TYPE  [ array_declaration ]\n\narray_declaration ::= '[' INTEGER_lower '..' '*' ']'\n                    | '[' INTEGER_lower '..' INTEGER_upper ']'\n\ncomponent_freezing ::= 'freeze' IDENTIFIER_component '=' value",
          "status": null
        },
        {
          "tag": "req LRM.Valid_Root_Type",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 632
          },
          "name": "LRM.Valid_Root_Type",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: The root type for a record extension must be a valid record type.",
          "status": null
        },
        {
          "tag": "req LRM.Abstract_Types",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 636
          },
          "name": "LRM.Abstract_Types",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: A record may be marked `abstract`, in which case no objects of this\ntype may be declared. It must be extended *(even if that extension is\nempty)* before instances of that type can be declared.\n*(Note that it is possible to have components of an abstract type.)*",
          "status": null
        },
        {
          "tag": "req LRM.Final_Types",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 645
          },
          "name": "LRM.Final_Types",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: A record may be marked `final`, and the extension of a `final` type\nis also considered to be final *(even if it is not explicitly marked\nas such)*. An extension of a final type may not contain any\ncomponent declarations.",
          "status": null
        },
        {
          "tag": "req LRM.Unique_Record_Components",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 654
          },
          "name": "LRM.Unique_Record_Components",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: Each component declaration shall have a unique name in that\nrecord declaration, or any of its root\ntypes. *(Two separate record extensions may\ndefined the same component, and they may even\nhave different types. But you cannot re-define\na component from a parent type.)*",
          "status": null
        },
        {
          "tag": "req LRM.Valid_Component_Type",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 663
          },
          "name": "LRM.Valid_Component_Type",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: Each component type shall refer to a valid type, or to the\nname of the record type itself. It is an error\nto refer to a type that has not been declared\nyet. *(As there are no forward declarations in\nthe language, this forces the user type\nhierarchy to be a DAG, but permitting\nself-references.)*",
          "status": null
        },
        {
          "tag": "req LRM.Anonymous_Arrays",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 673
          },
          "name": "LRM.Anonymous_Arrays",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: A component with an array declaration introduces an\nanonymous array type. This means the type of\nthe record component is not the type as\nspecified, but rather an array where the\nelement type is that type.",
          "status": null
        },
        {
          "tag": "req LRM.Upper_Bound_Greater_Than_Lower_Bound",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 681
          },
          "name": "LRM.Upper_Bound_Greater_Than_Lower_Bound",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: It is an error to specify an upper bound that is less than\nthe lower bound. *(Note that it is permitted\nfor them to be equal.)*",
          "status": null
        },
        {
          "tag": "req LRM.Freezing_Components",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 687
          },
          "name": "LRM.Freezing_Components",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: Any valid previously declared record component may be\nfrozen, providing a value of the correct type\nfor the given field in all instances of the\nrecord type. It is an error to freeze a\ncomponent that is already frozen.",
          "status": null
        },
        {
          "tag": "req LRM.Array_Indexing",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 695
          },
          "name": "LRM.Array_Indexing",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Dynamic_Semantics",
          "text": "text: Arrays are indexed by natural numbers and the first index is\n0.",
          "status": null
        },
        {
          "tag": "req LRM.Array_Lower_Bound",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 700
          },
          "name": "LRM.Array_Lower_Bound",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Dynamic_Semantics",
          "text": "text: An instance of an array shall not have fewer elements than\nits lower bound.",
          "status": null
        },
        {
          "tag": "req LRM.Array_Upper_Bound",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 705
          },
          "name": "LRM.Array_Upper_Bound",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Dynamic_Semantics",
          "text": "text: An array type has no upper bound if `*` is specified. An\narray instance for an array type with an upper\nbound shall not have more elements than its\nupper bound.",
          "status": null
        },
        {
          "tag": "req LRM.Array_Implementation_Upper_Bound",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 712
          },
          "name": "LRM.Array_Implementation_Upper_Bound",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Dynamic_Semantics",
          "text": "text: An implementation may impose an arbitrary limit to the\nactual upper bound of an array *(that is treat\nthe `*` as if it was that limit)*. This limit,\nif it exists, shall be greater than or equal\nto 1000.",
          "status": null
        },
        {
          "tag": "req LRM.Type_Extensions_Inherit_Everything",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 720
          },
          "name": "LRM.Type_Extensions_Inherit_Everything",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Dynamic_Semantics",
          "text": "text: A record type that extends another inherits all components,\nuser defined checks, and component freezes\nspecified for its root type.",
          "status": null
        },
        {
          "tag": "req LRM.Type_Extensions_Polymorphism",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 726
          },
          "name": "LRM.Type_Extensions_Polymorphism",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Dynamic_Semantics",
          "text": "text: Instances of an extension may be\nprovided as a reference where a root type is\nrequired; but not the other way around. *(This\nprovide a limited form of polymorphism, but\nwith the Liskov substitution principle\nguaranteed.)*",
          "status": null
        },
        {
          "tag": "req LRM.Zero_Upper_Bound",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 735
          },
          "name": "LRM.Zero_Upper_Bound",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Recommendation",
          "text": "text: It is recommended to emit a warning on array types with an\nupper bound of zero.",
          "status": null
        },
        {
          "tag": "req LRM.Arrays_Sized_One",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 740
          },
          "name": "LRM.Arrays_Sized_One",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Recommendation",
          "text": "text: It is recommended to emit a warning on array types with an\nupper bound of one.",
          "status": null
        },
        {
          "tag": "req LRM.Freezing_In_Same_Record",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 745
          },
          "name": "LRM.Freezing_In_Same_Record",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Recommendation",
          "text": "text: It is recommended to emit a warning on freezing a component\ndeclared in the same record.",
          "status": null
        },
        {
          "tag": "req LRM.Tuple_Separator_Clashes",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 750
          },
          "name": "LRM.Tuple_Separator_Clashes",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Recommendation",
          "text": "text: It is recommended that an implementation checks if a\nrecord type contains a tuple with a identifier\nseparator that is the same as one of its\ncomponents. While this is not an error (parsing for\nvalues is greedy) it is still highly confusing.",
          "status": null
        },
        {
          "tag": "req LRM.Record_Examples",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 760
          },
          "name": "LRM.Record_Examples",
          "messages": [],
          "just_up": [],
          "just_down": [
            "Non-normative example"
          ],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "framework": "TRLC",
          "kind": "Example",
          "text": null,
          "status": null
        },
        {
          "tag": "req LRM.Check_File",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 796
          },
          "name": "LRM.Check_File",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python trlc.Source_Manager.parse_check_files",
            "python parser.Parser.parse_check_file",
            "python ast.Compilation_Unit.add_item",
            "trlc-st simple"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Grammar",
          "text": "text: A `.check` file is simply a set of check blocks.\n\nbnf: check_file ::= file_preamble\n{ check_block }",
          "status": null
        },
        {
          "tag": "req LRM.Cannot_Declare_In_Check_File",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 804
          },
          "name": "LRM.Cannot_Declare_In_Check_File",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python parser.Parser.parse_preamble",
            "trlc-st rbt-cannot-declare-in-check-file"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: It is an error to indicate a package that has not been\ndeclared in an `.rsl` file.",
          "status": null
        },
        {
          "tag": "req LRM.Import_In_Check",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 809
          },
          "name": "LRM.Import_In_Check",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python parser.Parser.parse_check_file",
            "trlc-st rbt-import-in-check"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: A check file may not import any packages.",
          "status": null
        },
        {
          "tag": "req LRM.Deprecated_Check_Files",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 813
          },
          "name": "LRM.Deprecated_Check_Files",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python parser.Parser.parse_check_file",
            "trlc-st simple"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Recommendation",
          "text": "text: Check files are a deprecated feature that allows you to\nspecify checks separate from type\ndeclarations. While this seems like a good\nidea at first, in a large project this can\ncreate confusion: consider a global definition\nfor your requirement type stored in a central\nplace which everyone is supposed to use. In\nthis example some random user can create in\ntheir sub-project a check file that applies to\nthe global definitions, causing hassle for\neveryone. It is recommended that an\nimplementation suggests moving any check from\na `.check` file into the package `.rsl` file.",
          "status": null
        },
        {
          "tag": "req LRM.Check_Block",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 833
          },
          "name": "LRM.Check_Block",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python parser.Parser.parse_check_block",
            "python ast.Check_Block.__init__",
            "python ast.Check.__init__",
            "trlc-st simple"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Grammar",
          "text": "bnf: check_block ::= 'checks' IDENTIFIER_record_or_tuple_name\n                '{' { check_declaration } '}'\n\ncheck_declaration ::= expression ','\n                      [ severity ] STRING_message\n                      [ ',' STRING_details ]\n                      [ ',' IDENTIFIER_component_name ]\n\nseverity ::= 'warning'\n           | 'error'\n           | 'fatal'",
          "status": null
        },
        {
          "tag": "req LRM.Applicable_Types",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 849
          },
          "name": "LRM.Applicable_Types",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python parser.Parser.parse_check_block",
            "trlc-st rbt-applicable-types"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: It is an error to refer to a type that does not exist in the\ncurrent package, or is not a record or tuple type.",
          "status": null
        },
        {
          "tag": "req LRM.Applicable_Components",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 854
          },
          "name": "LRM.Applicable_Components",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python parser.Parser.parse_check_block",
            "trlc-st rbt-applicable-components"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: In a check declaration or expression, it is an error to\nrefer to a component name (or field name) that does not belong\nto the record (or tuple respectively) indicated.",
          "status": null
        },
        {
          "tag": "req LRM.No_Newlines_In_Message",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 862
          },
          "name": "LRM.No_Newlines_In_Message",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python parser.Parser.parse_check_block",
            "python ast.Check.__init__",
            "trlc-st checks-6"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: It is an error to include a newline in the message.",
          "status": null
        },
        {
          "tag": "req LRM.Only_Current_Package",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 868
          },
          "name": "LRM.Only_Current_Package",
          "messages": [],
          "just_up": [],
          "just_down": [
            "Non-normative text"
          ],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "framework": "TRLC",
          "kind": "Note",
          "text": "text: Note that it is never possible to add checks to a type from\na foreign package. In check files this is more\nobvious as you cannot have an import clause,\nbut this is also true for checks declared in\n`.rsl` files since it is not possible to\nspecify a qualified name.",
          "status": null
        },
        {
          "tag": "req LRM.Check_Evaluation_Order",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 877
          },
          "name": "LRM.Check_Evaluation_Order",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python ast.Check_Block.add_check",
            "python ast.Composite_Type.add_check",
            "python ast.Composite_Type.iter_checks",
            "python ast.Record_Type.iter_checks",
            "python ast.Tuple_Type.perform_type_checks",
            "python ast.Record_Object.perform_checks",
            "trlc-st rbt-check-evaluation-order"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Dynamic_Semantics",
          "text": "text: Each check inside a check block is evaluated in the specified\norder.",
          "status": null
        },
        {
          "tag": "req LRM.Check_Evaluation_Order_Across_Blocks",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 882
          },
          "name": "LRM.Check_Evaluation_Order_Across_Blocks",
          "messages": [],
          "just_up": [],
          "just_down": [
            "Non-normative text"
          ],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "framework": "TRLC",
          "kind": "Note",
          "text": "text: If multiple check blocks are declared for the same type,\nthen the order of evaluation of each check\nblock is unspecified.",
          "status": null
        },
        {
          "tag": "req LRM.Check_Evaluation_Order_For_Extensions",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 888
          },
          "name": "LRM.Check_Evaluation_Order_For_Extensions",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python ast.Record_Type.iter_checks",
            "trlc-st rbt-check-evaluation-order-for-extensions"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Dynamic_Semantics",
          "text": "text: For record extensions, all checks for the base record must\nbe evaluated before any check of the record\nextension is evaluated.",
          "status": null
        },
        {
          "tag": "req LRM.Check_Messages",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 894
          },
          "name": "LRM.Check_Messages",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python ast.Check.perform",
            "trlc-st rbt-check-evaluation-order-for-extensions"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Dynamic_Semantics",
          "text": "text: If the evaluated expression is true, no action is taken. If\nit is false, then a diagnostic is emitted with\nthe specified message and details. It is\nimplementation defined if and how the details\nare shown, for example in a \"brief\" mode they\ncould be omitted.",
          "status": null
        },
        {
          "tag": "req LRM.Check_Severity",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 903
          },
          "name": "LRM.Check_Severity",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python ast.Check.perform",
            "trlc-st rbt-check-severity-1",
            "trlc-st rbt-check-severity-2",
            "trlc-st rbt-check-severity-3"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Dynamic_Semantics",
          "text": "text: The severity, if provided, controls how future errors are\ntreated, and how the TRLC implementation\nterminates.\n\nbullets: ['A warning has no effect other than emitting the message.', 'An error (the default, in case severity is not specified)\\ncauses an implementation to eventually\\nreturn a non-zero error code, but further\\nchecks will be evaluated (potentially\\ncreating more messages).', 'A fatal message is like an error, except that no further\\nchecks from this check block shall be\\nevaluated for this object.']",
          "status": null
        },
        {
          "tag": "req LRM.Intended_Semantics_Of_Messages",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 918
          },
          "name": "LRM.Intended_Semantics_Of_Messages",
          "messages": [],
          "just_up": [],
          "just_down": [
            "Non-normative text"
          ],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "framework": "TRLC",
          "kind": "Note",
          "text": "text: The intended meaning of the message is a short description\nof what is wrong. The intended meaning for the\noptional details is a longer explanation,\nincluding perhaps on what to fix.",
          "status": null
        },
        {
          "tag": "req LRM.Anchoring",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 925
          },
          "name": "LRM.Anchoring",
          "messages": [],
          "just_up": [],
          "just_down": [
            "Non-normative text"
          ],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "framework": "TRLC",
          "kind": "Note",
          "text": "text: The component name (if specified) is a hint where the\nmessage should be anchored. It is\nimplementation defined how or if this is taken\ninto account. A suitable anchoring for a\nmessage without a component or field could be the\nobject declaration itself. If only a\nsingle component or field is used in the expression\nthen the message could be anchored the same\nway as if the component was indicated\nexplicitly in the check.",
          "status": null
        },
        {
          "tag": "req LRM.Sane_Typing",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 938
          },
          "name": "LRM.Sane_Typing",
          "messages": [],
          "just_up": [],
          "just_down": [
            "Non-normative text"
          ],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "framework": "TRLC",
          "kind": "Note",
          "text": "text: It is an important design goal to keep the type system sane\nand following LSP. I.e. each subtype may only\nnarrow the values permitted in a type. This\nmeans for a record R and its extension RE; any\nvalid instance of RE is always a valid\ninstance of R if a new binding of R is created\nconsidering only the components that are in R. It\nwill never be possible to delete, suppress,\nwiden, or omit checks in record extensions.",
          "status": null
        },
        {
          "tag": "req LRM.Check_Examples",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 950
          },
          "name": "LRM.Check_Examples",
          "messages": [],
          "just_up": [],
          "just_down": [
            "Non-normative example"
          ],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "framework": "TRLC",
          "kind": "Example",
          "text": null,
          "status": null
        },
        {
          "tag": "req LRM.Expression",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1003
          },
          "name": "LRM.Expression",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python parser.Parser.parse_expression",
            "python ast.Binary_Expression.__init__",
            "trlc-st rbt-expression"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Grammar",
          "text": "bnf: expression ::= relation { 'and' relation }\n| relation { 'or' relation }\n| relation [ 'xor' relation ]\n| relation [ 'implies' relation ]",
          "status": null
        },
        {
          "tag": "req LRM.Relation",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1012
          },
          "name": "LRM.Relation",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python parser.Parser.parse_relation",
            "python ast.Unary_Expression.__init__",
            "python ast.Binary_Expression.__init__",
            "python ast.Range_Test.__init__",
            "trlc-st rbt-expression"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Grammar",
          "text": "bnf: relation ::= simple_expression [ comparison_operator simple_expression ]\n           | simple_expression [ 'not' ] 'in' membership_choice\n           | simple_expression [ 'not' ] 'in' simple_expression\n\nmembership_choice ::= simple_expression '..' simple_expression",
          "status": null
        },
        {
          "tag": "req LRM.Simple_Expression",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1022
          },
          "name": "LRM.Simple_Expression",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python parser.Parser.parse_simple_expression",
            "python ast.Unary_Expression.__init__",
            "python ast.Binary_Expression.__init__",
            "trlc-st rbt-expression"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Grammar",
          "text": "bnf: simple_expression ::= [ adding_operator ]\nterm { adding_operator term }",
          "status": null
        },
        {
          "tag": "req LRM.Term",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1029
          },
          "name": "LRM.Term",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python parser.Parser.parse_term",
            "python ast.Binary_Expression.__init__",
            "trlc-st rbt-expression"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Grammar",
          "text": "bnf: term ::= factor { multiplying_operator factor }",
          "status": null
        },
        {
          "tag": "req LRM.Factor",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1033
          },
          "name": "LRM.Factor",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python parser.Parser.parse_factor",
            "python ast.Unary_Expression.__init__",
            "python ast.Binary_Expression.__init__",
            "trlc-st rbt-expression"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Grammar",
          "text": "bnf: factor ::= primary [ '**' primary ]\n| 'not' primary\n| 'abs' primary",
          "status": null
        },
        {
          "tag": "req LRM.Primary",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1041
          },
          "name": "LRM.Primary",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python parser.Parser.parse_primary",
            "python ast.Null_Literal",
            "python ast.Integer_Literal",
            "python ast.Decimal_Literal",
            "python ast.String_Literal",
            "python ast.Boolean_Literal",
            "trlc-st rbt-expression"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Grammar",
          "text": "bnf: primary ::= INTEGER\n| DECIMAL\n| STRING\n| 'true'\n| 'false'\n| 'null'\n| name\n| '(' expression ')'\n| '(' quantified_expression ')'\n| '(' conditional_expression ')'",
          "status": null
        },
        {
          "tag": "req LRM.Unary_Minus_Parsing",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1056
          },
          "name": "LRM.Unary_Minus_Parsing",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python parser.Parser.parse_simple_expression",
            "trlc-st rbt-unary-minus-parsing"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Recommendation",
          "text": "text: The parsing of unary minus can be confusing: `-a % b` is\nactually `- (a % b)`. The semantics of `%` are\ncarefully specified so that this does not\nmatter. It does also mean that `-a / -b` is\nnot legal and needs to be written as either\n`-a / (-b)` or even better `(-a) / (-b)`. It\nis recommended that a linter warns whenever a\nunary minus is encountered that has a\nnon-trivial `term` or `factor` as its operand.",
          "status": null
        },
        {
          "tag": "req LRM.Expression_Examples",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1068
          },
          "name": "LRM.Expression_Examples",
          "messages": [],
          "just_up": [],
          "just_down": [
            "Non-normative example"
          ],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "framework": "TRLC",
          "kind": "Example",
          "text": null,
          "status": null
        },
        {
          "tag": "req LRM.Names",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1098
          },
          "name": "LRM.Names",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Grammar",
          "text": "text: A name can be one of 5 things:\n\nbullets: ['A qualified name referring to either some object, a component\\n(in a record) or field (in a tuple), or an enumeration type.', 'A tuple field or enumeration literal.', 'An index into an array.', 'A (builtin) function call.']\n\nbnf: name ::= qualified_name\n       | name '.' IDENTIFIER\n       | name '[' expression ']'\n       | name '(' parameter_list ')'\n\nparameter_list ::= expression { ',' expression }",
          "status": null
        },
        {
          "tag": "req LRM.Valid_Base_Names",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1117
          },
          "name": "LRM.Valid_Base_Names",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: The `qualified_name` must resolve to record component or\ntuple field in scope, or a visible record\nobject, or a visible enumeration type.",
          "status": null
        },
        {
          "tag": "req LRM.Valid_Access_Prefixes",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1124
          },
          "name": "LRM.Valid_Access_Prefixes",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: If the prefix of a dot (`.`) access resolves to an\nenumeration type, then the identifier must be\na valid literal of that type. If the prefix of\na dot (`.`) access resolves to a tuple, then\nthe identifier must be a valid field of the\ntype of that tuple. Any other prefix is an\nerror.",
          "status": null
        },
        {
          "tag": "req LRM.Valid_Index_Prefixes",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1135
          },
          "name": "LRM.Valid_Index_Prefixes",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: The type of the `name` in an array indexing prefix (i.e. `[`\n.. `]`) must be an array type.",
          "status": null
        },
        {
          "tag": "req LRM.Valid_Function_Prefixes",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1141
          },
          "name": "LRM.Valid_Function_Prefixes",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: The `name` in a function call must resolve to one of the\nbuiltin functions.",
          "status": null
        },
        {
          "tag": "req LRM.Signature_Len",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1148
          },
          "name": "LRM.Signature_Len",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: The builtin function `len` is of arity 1. Its parameter must\nbe of type `String` or an array type. Its\nreturn type is `Integer`.",
          "status": null
        },
        {
          "tag": "req LRM.Signature_String_End_Functions",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1154
          },
          "name": "LRM.Signature_String_End_Functions",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: The builtin functions `startswith` and `endswith` are of\narity 2. All of their parameters must be of\ntype `String`. The return type of either\nfunction is `Boolean`.",
          "status": null
        },
        {
          "tag": "req LRM.Signature_Matches",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1161
          },
          "name": "LRM.Signature_Matches",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: The builtin function `matches` is of arity 2. Its parameters\nmust be of type `String`. The return type is\n`Boolean`. The second parameter must be a\nvalid regular expression. *(It is\nimplementation defined which regular\nexpression language is used, but it is highly,\n_highly_ recommended to implement the standard\nPOSIX regular expressions.)*",
          "status": null
        },
        {
          "tag": "req LRM.Static_Regular_Expression",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1172
          },
          "name": "LRM.Static_Regular_Expression",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: In addition, the second parameter to the `matches` function\nmust be a static compile-time constant,\ni.e. it must not depend on the value of a\nrecord field or the value of a quantified\nvariable.",
          "status": null
        },
        {
          "tag": "req LRM.Signature_Type_Conversion",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1180
          },
          "name": "LRM.Signature_Type_Conversion",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: The numeric type conversion functions are of arity 1 and\npolymorphic (they are defined for both integer and\nrationals). They return the type indicated by the function\nname. *(They are polymorphic in case we want to introduce\na true rational type, or a floating point type.)*",
          "status": null
        },
        {
          "tag": "req LRM.Len_Semantics",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1188
          },
          "name": "LRM.Len_Semantics",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Dynamic_Semantics",
          "text": "text: The `len` function computes the length of the given string\nor array.",
          "status": null
        },
        {
          "tag": "req LRM.Startswith_Semantics",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1193
          },
          "name": "LRM.Startswith_Semantics",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Dynamic_Semantics",
          "text": "text: The `startswith` function returns true iff the first\nparameter fully contains the second parameter\nat its start.",
          "status": null
        },
        {
          "tag": "req LRM.Endswith_Semantics",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1199
          },
          "name": "LRM.Endswith_Semantics",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Dynamic_Semantics",
          "text": "text: The `endswith` function returns true iff the first parameter\nfully contains the second parameter at its\nend.",
          "status": null
        },
        {
          "tag": "req LRM.Matches_Semantics",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1205
          },
          "name": "LRM.Matches_Semantics",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Dynamic_Semantics",
          "text": "text: The `matches` function returns true iff the first parameter\nis matched by the regular expression given in\nthe second parameter.",
          "status": null
        },
        {
          "tag": "req LRM.Integer_Conversion_Semantics",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1211
          },
          "name": "LRM.Integer_Conversion_Semantics",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Dynamic_Semantics",
          "text": "text: The `Integer` type conversion rounds to the nearest\nintegral, away from zero in the case of ties.",
          "status": null
        },
        {
          "tag": "req LRM.Decimal_Conversion_Semantics",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1216
          },
          "name": "LRM.Decimal_Conversion_Semantics",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Dynamic_Semantics",
          "text": "text: The `Decimal` type conversion simply converts\nthe given integer to the exact same rational.",
          "status": null
        },
        {
          "tag": "req LRM.Case_Sensitive",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1221
          },
          "name": "LRM.Case_Sensitive",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Name_Resolution",
          "text": "text: Name resolution is case sensitive.",
          "status": null
        },
        {
          "tag": "req LRM.Name_Examples",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1225
          },
          "name": "LRM.Name_Examples",
          "messages": [],
          "just_up": [],
          "just_down": [
            "Non-normative example"
          ],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "framework": "TRLC",
          "kind": "Example",
          "text": null,
          "status": null
        },
        {
          "tag": "req LRM.Operators",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1267
          },
          "name": "LRM.Operators",
          "messages": [
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python parser.Parser.parse_relation",
            "python parser.Parser.parse_simple_expression",
            "python parser.Parser.parse_term"
          ],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Grammar",
          "text": "bnf: comparison_operator ::= '==' | '!=' | '<' | '<=' | '>' | '>='\n\nadding_operator ::= '+' | '-'\n\nmultiplying_operator ::= '*' | '/' | '%'",
          "status": null
        },
        {
          "tag": "req LRM.Association",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1277
          },
          "name": "LRM.Association",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: For a chain of operators of the same category, the\nassociation is left to right.",
          "status": null
        },
        {
          "tag": "req LRM.Range_Checks",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1282
          },
          "name": "LRM.Range_Checks",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Dynamic_Semantics",
          "text": "text: It is implementation defined if type checks (range or\nlength) are performed for intermediate values;\nif type checks are not performed then the\nresulting expression must not be an error.",
          "status": null
        },
        {
          "tag": "req LRM.Range_Checks_Example",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1289
          },
          "name": "LRM.Range_Checks_Example",
          "messages": [],
          "just_up": [],
          "just_down": [
            "Non-normative text"
          ],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "framework": "TRLC",
          "kind": "Note",
          "text": "text: This means you either type check all the time, or you\nguarantee that any intermediate will not\ncreate an error in the implementation, as long\nas the final value fits in the relevant\ntype. For example if A and B are maximum\nlength Strings, then `\"potato\" in A + B` may\neither create an error when attempting to\nconcatenate the strings, OR it must work\ncorrectly. What you cannot do is cause\nundefined behaviour in the evaluation.",
          "status": null
        },
        {
          "tag": "req LRM.Logical_Operators",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1304
          },
          "name": "LRM.Logical_Operators",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: There are five Boolean operators defined (not, and, or, xor,\nimplies) for expressions of Boolean type.\nThe type of the result is Boolean.",
          "status": null
        },
        {
          "tag": "req LRM.Shortcut_Logical_Operators",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1310
          },
          "name": "LRM.Shortcut_Logical_Operators",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Dynamic_Semantics",
          "text": "text: Operators with short-cut semantics are `and`, `or`, and\n`implies`. They first evaluate their\nleft-hand side and proceed to evaluate the\nright-hand side if it could influence the\nfinal result. The semantics of these\noperators are the usual ones.",
          "status": null
        },
        {
          "tag": "req LRM.Regular_Logical_Operators",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1319
          },
          "name": "LRM.Regular_Logical_Operators",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Dynamic_Semantics",
          "text": "text: Operators with standard semantics are `xor`, and `not`. They\ndo the usual thing.",
          "status": null
        },
        {
          "tag": "req LRM.Equality_Domain",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1328
          },
          "name": "LRM.Equality_Domain",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: The equality operators `==` and `!=` are defined for all\ntypes, as long as the types are compatible,\ni.e. they are the same types or one type is\na (transitive) record extension of the other. The\nresult is a Boolean.",
          "status": null
        },
        {
          "tag": "req LRM.Relational_Domain",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1336
          },
          "name": "LRM.Relational_Domain",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: The ordering relations `<`, `<=`, `>=`, and `>` are defined\nfor pairs of integers or pairs of rationals only. The result\nis a Boolean.",
          "status": null
        },
        {
          "tag": "req LRM.Membership_Domain",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1342
          },
          "name": "LRM.Membership_Domain",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: Range membership tests `not in` and `in` are defined for\nintegers and rationals only. All operands\nmust have the same type, and the result is a\nBoolean.",
          "status": null
        },
        {
          "tag": "req LRM.Substring_Domain",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1349
          },
          "name": "LRM.Substring_Domain",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: Substring tests `not in` and `in` are defined for\nStrings only. The result is a Boolean.",
          "status": null
        },
        {
          "tag": "req LRM.Array_Membership_Domain",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1354
          },
          "name": "LRM.Array_Membership_Domain",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: Array membership tests `not in` and `in` are defined for all\narrays. The type of the left-hand side must\nmatch the element type of the array. The\nresult is a Boolean.",
          "status": null
        },
        {
          "tag": "req LRM.Equality_On_Null",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1361
          },
          "name": "LRM.Equality_On_Null",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Dynamic_Semantics",
          "text": "text: Null is only equal to itself.",
          "status": null
        },
        {
          "tag": "req LRM.Equality_On_Tuples",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1366
          },
          "name": "LRM.Equality_On_Tuples",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Dynamic_Semantics",
          "text": "text: Two tuple instances are equal if they both\ncontain the same values for all their components.",
          "status": null
        },
        {
          "tag": "req LRM.Equality_On_Record_References",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1372
          },
          "name": "LRM.Equality_On_Record_References",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Dynamic_Semantics",
          "text": "text: Two record references are equal if they both\nrefer to the same record.",
          "status": null
        },
        {
          "tag": "req LRM.Equality_On_Arrays",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1378
          },
          "name": "LRM.Equality_On_Arrays",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Dynamic_Semantics",
          "text": "text: Two arrays are equal if they both have the same length\nand items (in the same order).",
          "status": null
        },
        {
          "tag": "req LRM.Simple_Relational_Semantics",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1384
          },
          "name": "LRM.Simple_Relational_Semantics",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Dynamic_Semantics",
          "text": "text: The meaning of the relationship operators are the usual.",
          "status": null
        },
        {
          "tag": "req LRM.Inclusive_Membership_Test_Semantics",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1388
          },
          "name": "LRM.Inclusive_Membership_Test_Semantics",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Dynamic_Semantics",
          "text": "text: An inclusive range membership test `x in a .. b` has the\nsame meaning as the Boolean expression `x >=\na and x <= b`. *(This means if a is less\nthan b, it is not an error. Instead the\nresult of such a test is always false.)*",
          "status": null
        },
        {
          "tag": "req LRM.Exclusive_Membership_Test_Semantics",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1396
          },
          "name": "LRM.Exclusive_Membership_Test_Semantics",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Dynamic_Semantics",
          "text": "text: An exclusive range membership test `x not in a .. b` has the\nsame meaning as the Boolean expression `x <\na or x > b`.",
          "status": null
        },
        {
          "tag": "req LRM.Simple_Substring_Semantics",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1402
          },
          "name": "LRM.Simple_Substring_Semantics",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Dynamic_Semantics",
          "text": "text: The meaning of the substring test is the usual. Note that\nthe substring test is of course performed on\nthe value of the string, not the original\nliteral.",
          "status": null
        },
        {
          "tag": "req LRM.Array_Membership_Semantics",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1409
          },
          "name": "LRM.Array_Membership_Semantics",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Dynamic_Semantics",
          "text": "text: The array membership test `X in A` is equivalent to `(exists\nitem in A => item == X)`. The array\nnon-membership test `X not in A` is\nequivalent to `(forall item in A => item !=\nX)`.",
          "status": null
        },
        {
          "tag": "req LRM.Binary_Addition_Domain",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1421
          },
          "name": "LRM.Binary_Addition_Domain",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: The binary adding operator `+` is defined for integers,\nrationals, and strings. The binary\nsubtraction operator `-` is defined for only\nintegers and rationals.",
          "status": null
        },
        {
          "tag": "req LRM.String_Concatenation_Downgrade",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1428
          },
          "name": "LRM.String_Concatenation_Downgrade",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: When `+` is used to concatenate strings, the result is\nalways a `String`, even if one or both\noperands if of type `Markup_String`. *(This\nmeans the only way you can create a markup\nstring is when you construct it at record\nobject declaration.)*",
          "status": null
        },
        {
          "tag": "req LRM.Unary_Addition_Domain",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1437
          },
          "name": "LRM.Unary_Addition_Domain",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: The unary adding operator `+`, and the unary subtraction\noperator `-` is defined only for integers\nand rationals.",
          "status": null
        },
        {
          "tag": "req LRM.Adding_Types",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1443
          },
          "name": "LRM.Adding_Types",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: For binary adding operators the types of the operands have\nto match, and the result is the same type as\nthe two operands. For unary adding operators\nthe result is always the same as the\noperand.",
          "status": null
        },
        {
          "tag": "req LRM.Adding_Semantics",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1451
          },
          "name": "LRM.Adding_Semantics",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Dynamic_Semantics",
          "text": "text: The definition of `+` and `-` for integers and rationals is\nthe usual one.",
          "status": null
        },
        {
          "tag": "req LRM.Concatenation_Semantics",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1456
          },
          "name": "LRM.Concatenation_Semantics",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Dynamic_Semantics",
          "text": "text: The definition of `+` for strings is string concatenation.",
          "status": null
        },
        {
          "tag": "req LRM.Multiplying_Domain",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1464
          },
          "name": "LRM.Multiplying_Domain",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: The multiplying operators `*`, `/` are defined for integers\nand rational types. The remainder operator\n`%` is defined for integers only. For any of\nthese the result is always the same type as\nthe operands.",
          "status": null
        },
        {
          "tag": "req LRM.Multiplying_Semantics",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1473
          },
          "name": "LRM.Multiplying_Semantics",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Dynamic_Semantics",
          "text": "text: The definition of `*` is the usual one.",
          "status": null
        },
        {
          "tag": "req LRM.Integer_Division_Semantics",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1477
          },
          "name": "LRM.Integer_Division_Semantics",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Dynamic_Semantics",
          "text": "text: The definition of `/` for integers is floor division. *(For\nexample `5 / 2` is `2` and `-5 / 2` is\n`-3`.)*",
          "status": null
        },
        {
          "tag": "req LRM.Rational_Division_Semantics",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1483
          },
          "name": "LRM.Rational_Division_Semantics",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Dynamic_Semantics",
          "text": "text: The definition of `/` for rationals is the usual one.",
          "status": null
        },
        {
          "tag": "req LRM.Remainder_Semantics",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1487
          },
          "name": "LRM.Remainder_Semantics",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Dynamic_Semantics",
          "text": "text: The modulus division for `x % y` satisfies the relation `x =\ny*N + (x % y)`, for some (signed) value of\n`N`, with one of the following constraints\nmet:\n\nbullets: ['`x % y` is `0`', '`x % y` has the same sign as `y` and an absolute\\nvalue less than `y`']",
          "status": null
        },
        {
          "tag": "req LRM.Division_By_Zero",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1497
          },
          "name": "LRM.Division_By_Zero",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Dynamic_Semantics",
          "text": "text: Division by zero or modulo division by 0 is an error.",
          "status": null
        },
        {
          "tag": "req LRM.Power_Domain",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1505
          },
          "name": "LRM.Power_Domain",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: The exponentiation operator `**` is defined for integers and\nrational bases, and returns the same type as\nits base. The exponent type is always an\nInteger.",
          "status": null
        },
        {
          "tag": "req LRM.Power_Static_Exponent",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1512
          },
          "name": "LRM.Power_Static_Exponent",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: The right-hand side parameter of `**` must be a static\ncompile-time constant, i.e. it must not\ndepend on the value of a record field or the\nvalue of a quantified variable. It must not\nbe negative.",
          "status": null
        },
        {
          "tag": "req LRM.Absolute_Value_Domain",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1520
          },
          "name": "LRM.Absolute_Value_Domain",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: The absolute value prefix operator `abs` is defined for\nintegers and rationals, and returns a\n(positive) integer or rational respectively.",
          "status": null
        },
        {
          "tag": "req LRM.Negation_Domain",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1526
          },
          "name": "LRM.Negation_Domain",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: The logical negation prefix operator `not` is defined for\nBooleans only, and returns a Boolean.",
          "status": null
        },
        {
          "tag": "req LRM.Power_Semantics",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1531
          },
          "name": "LRM.Power_Semantics",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: The definition of exponentiation `**` is the usual one.",
          "status": null
        },
        {
          "tag": "req LRM.Absolute_Value_Semantics",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1535
          },
          "name": "LRM.Absolute_Value_Semantics",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: The definition of absolute value `abs` is the usual one.",
          "status": null
        },
        {
          "tag": "req LRM.Negation_Semantics",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1539
          },
          "name": "LRM.Negation_Semantics",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: The definition of logical negation `not` is the usual one.",
          "status": null
        },
        {
          "tag": "req LRM.Quantified_Expression",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1549
          },
          "name": "LRM.Quantified_Expression",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Grammar",
          "text": "bnf: quantified_expression ::=\n  quantifier IDENTIFIER_name 'in' IDENTIFIER_component_name '=>'\n  expression_PREDICATE\n\nquantifier ::= 'forall' | 'exists'",
          "status": null
        },
        {
          "tag": "req LRM.Quantification_Object",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1559
          },
          "name": "LRM.Quantification_Object",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Name_Resolution",
          "text": "text: The component name must be defined in the current record,\nand must be an array type.",
          "status": null
        },
        {
          "tag": "req LRM.Quantification_Naming_Scope",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1564
          },
          "name": "LRM.Quantification_Naming_Scope",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: A quantified expression introduces a new name, that is valid\nonly inside the predicate. This new name must\nnot shadow any other. *(This means two\nseparate quantified expressions may use the\nsame name, but you may not nest and shadow,\nand you may not shadow a component name\neither.)*",
          "status": null
        },
        {
          "tag": "req LRM.Quantification_Type",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1574
          },
          "name": "LRM.Quantification_Type",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: The type of the predicate must be Boolean. The result of a\nquantified expression is Boolean.",
          "status": null
        },
        {
          "tag": "req LRM.Quantification_Evaluation",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1579
          },
          "name": "LRM.Quantification_Evaluation",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Dynamic_Semantics",
          "text": "text: During evaluation of the quantified expression, each element\nof the array is evaluated in sequence and its\nvalue is bound to the declared name. The\npredicated is then evaluated with this\nbinding.",
          "status": null
        },
        {
          "tag": "req LRM.Universal_Quantification_Semantics",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1587
          },
          "name": "LRM.Universal_Quantification_Semantics",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Dynamic_Semantics",
          "text": "text: For universal *(forall)* quantification the final value is\ntrue iff all predicates evaluate to\ntrue. *(This means universal quantification\nover an empty array is vacuously true.)*",
          "status": null
        },
        {
          "tag": "req LRM.Existential_Quantification_Semantics",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1594
          },
          "name": "LRM.Existential_Quantification_Semantics",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Dynamic_Semantics",
          "text": "text: For existential *(exists)* quantification the final value is\ntrue iff the predicate evaluate to true at\nleast once. *(This means existential\nquantification over an empty array is\nvacuously false.)*",
          "status": null
        },
        {
          "tag": "req LRM.Quantification_Short_Circuit_Evaluation",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1602
          },
          "name": "LRM.Quantification_Short_Circuit_Evaluation",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Recommendation",
          "text": "text: In general Quantification is equivalent to a chain of `and`\nor `or` expressions, however it is left\nunspecified if quantification is using\nshort-circuit semantics or not. It is\nrecommended (for sanity) to do the following:\n\nbullets: ['For actual evaluation, use short-circuit semantics, as speed\\nis important.', 'For static analysis or linting, use non-short-circuit\\nsemantics, as using a quantifier as a\\ncomplex guard is not reasonable.']",
          "status": null
        },
        {
          "tag": "req LRM.Conditional_Expression",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1619
          },
          "name": "LRM.Conditional_Expression",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python parser.Parser.parse_conditional_expression",
            "python ast.Action.__init__",
            "python ast.Conditional_Expression.__init__",
            "python ast.Conditional_Expression.add_elsif",
            "python ast.Conditional_Expression.set_else_part",
            "trlc-st rbt-conditional-expression"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Grammar",
          "text": "bnf: conditional_expression ::=\n'if' expression_CONDITION 'then' expression_DEPENDENT\n{'elsif' expression_CONDITION 'then' expression_DEPENDENT }\n'else' expression_DEPENDENT",
          "status": null
        },
        {
          "tag": "req LRM.Conditional_Expression_Types",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1628
          },
          "name": "LRM.Conditional_Expression_Types",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python ast.Action.__init__",
            "trlc-st rbt-conditional-expression-types"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: The condition expressions must be of Boolean type. The\ndependent expressions must all be of the same\ntype, and the type of the entire conditional\nexpression is also of that type.",
          "status": null
        },
        {
          "tag": "req LRM.Conditional_Expression_Evaluation",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1635
          },
          "name": "LRM.Conditional_Expression_Evaluation",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python ast.Conditional_Expression.evaluate",
            "trlc-st rbt-conditional-expression"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Dynamic_Semantics",
          "text": "text: Each condition is evaluated in sequence. Evaluation stops on\nthe first condition that evaluates to true;\nafter which the corresponding dependent\nexpression is evaluated and returned.",
          "status": null
        },
        {
          "tag": "req LRM.Conditional_Expression_Else",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1642
          },
          "name": "LRM.Conditional_Expression_Else",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python ast.Conditional_Expression.evaluate",
            "trlc-st rbt-conditional-expression"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Dynamic_Semantics",
          "text": "text: If all conditions are evaluated to false, then the else\ndependent expression is evaluated and\nreturned.",
          "status": null
        },
        {
          "tag": "req LRM.TRLC_File",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1652
          },
          "name": "LRM.TRLC_File",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python trlc.Source_Manager.register_trlc_file",
            "python trlc.Source_Manager.parse_trlc_files",
            "python parser.Parser.parse_trlc_entry",
            "python parser.Parser.parse_trlc_file",
            "python ast.Compilation_Unit.add_item",
            "trlc-st simple"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Grammar",
          "text": "text: A `.trlc` file is simply a set of record object declarations.\n\nbnf: trlc_file ::= file_preamble\n              { trlc_entry }\n\ntrlc_entry ::= section_declaration\n             | record_object_declaration",
          "status": null
        },
        {
          "tag": "req LRM.Late_Package_Declarations",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1663
          },
          "name": "LRM.Late_Package_Declarations",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python parser.Parser.parse_preamble",
            "trlc-st rbt-late-package-declarations"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: It is permitted to indicate a package that has\nnot been declared in an `.rsl` file, in which\ncase it is declared by the\npackage_indication in the `.trlc` file. Such a package is\ndeclared late. If two `.trlc` files declare the same\npackage, then it is unspecified which file actually\ndeclares it.",
          "status": null
        },
        {
          "tag": "req LRM.Duplicate_Late_Packages",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1673
          },
          "name": "LRM.Duplicate_Late_Packages",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python parser.Parser.parse_preamble",
            "trlc-st rbt-late-package-declarations"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Recommendation",
          "text": "text: It is recommended to issue a warning if two `.trlc` files\ndeclare the same package.",
          "status": null
        },
        {
          "tag": "req LRM.TRLC_Parse_Issue",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1678
          },
          "name": "LRM.TRLC_Parse_Issue",
          "messages": [],
          "just_up": [],
          "just_down": [
            "Non-normative text"
          ],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "framework": "TRLC",
          "kind": "Note",
          "text": "text: For TRLC files it is impossible fully parse a file\nin isolation, since we must process at least the package\nindication of every other trlc file to know which import\nstatements are valid.",
          "status": null
        },
        {
          "tag": "req LRM.Section_Declaration",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1689
          },
          "name": "LRM.Section_Declaration",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python parser.Parser.parse_section_declaration",
            "python parser.Parser.parse_record_object_declaration",
            "python ast.Record_Object.__init__",
            "python ast.Section",
            "trlc-st rbt-section-declaration"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Grammar",
          "text": "text: A section has no semantic impact, and no impact on name\nresolution. Section names do not have to be\nunique. It may be exposed in an API, for\nexample to section a HTML view of\nrequirements.\n\nbnf: section_declaration ::= 'section' STRING_section_name\n'{' { trlc_entry } '}'",
          "status": null
        },
        {
          "tag": "req LRM.Record_Object_Declaration",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1705
          },
          "name": "LRM.Record_Object_Declaration",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Grammar",
          "text": "bnf: record_object_declaration ::=\n  qualified_name_RECORD_TYPE IDENTIFIER_object_name\n  '{' { component_association } '}'\n\ncomponent_association ::= IDENTIFIER_component_name '=' value\n\nvalue ::= [ adding_operator ] INTEGER\n        | [ adding_operator ] DECIMAL\n        | STRING\n        | qualified_name_RECORD_OBJECT\n        | qualified_name_ENUM_TYPE '.' IDENTIFIER_enumeration_literal\n        | '[' [ value { ',' value } ] ']'\n        | tuple_aggregate\n\ntuple_aggregate ::= '(' value { ',' value } ')'\n                  | value { separator_symbol value }",
          "status": null
        },
        {
          "tag": "req LRM.Valid_Record_Types",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1726
          },
          "name": "LRM.Valid_Record_Types",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: The type of the declaration must be a valid, non-abstract\nrecord type. If no qualified name is given, the record type\nmust be in the indicated package. *(Note that it is not\nlegal to declare a tuple object.)*",
          "status": null
        },
        {
          "tag": "req LRM.Unique_Object_Names",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1734
          },
          "name": "LRM.Unique_Object_Names",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: The name of the declaration must be a unique name and\nsufficiently distinct in the current\npackage. *(See name resolution for a\ndefinition of sufficiently distinct.)* The\nname of the declaration must not shadow a type\nname or package.",
          "status": null
        },
        {
          "tag": "req LRM.Valid_Components",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1743
          },
          "name": "LRM.Valid_Components",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: Each component name must be a valid, non-frozen component\nof the record type. It is an error to attempt to assign to\na frozen component *(even if the value assigned would be the\nsame value as it's frozen value)*.",
          "status": null
        },
        {
          "tag": "req LRM.Valid_Enumeration_Literals",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1750
          },
          "name": "LRM.Valid_Enumeration_Literals",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: Each enumeration must be a valid enumeration type in the\nindicated (or qualified) package. Each\nenumeration literal must be a valid literal of\nthe indicated enumeration in the prefix.",
          "status": null
        },
        {
          "tag": "req LRM.Matching_Value_Types",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1757
          },
          "name": "LRM.Matching_Value_Types",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: The type of each value must match each component or array\nelement type. Records are specified through\nreferences *(there is no way to specify an\ninline anonymous instance)*.",
          "status": null
        },
        {
          "tag": "req LRM.Mandatory_Components",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1764
          },
          "name": "LRM.Mandatory_Components",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: It is an error to not provide a value for a non-optional\ncomponent.",
          "status": null
        },
        {
          "tag": "req LRM.Tuple_Syntax_Correct_Form",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1769
          },
          "name": "LRM.Tuple_Syntax_Correct_Form",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: The aggregate of a tuple must use the correct form. A\ntuple without separators uses the bracket syntax\n(e.g. `(1, 2, 3)`, and a tuple with separators must\nuse the separator syntax (e.g. `12345@42`).",
          "status": null
        },
        {
          "tag": "req LRM.Tuple_Generic_Form",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1776
          },
          "name": "LRM.Tuple_Generic_Form",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: A tuple value for a tuple without separators must\ncontain one value, in order, for each of its fields.",
          "status": null
        },
        {
          "tag": "req LRM.Tuple_Separator_Form",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1781
          },
          "name": "LRM.Tuple_Separator_Form",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: A tuple value for a tuple with separators must\ncontain the separator symbols as indicated in the type,\nin order. Optional fields and their preceding separator\nmay be omitted. Once an optional field has been omitted,\nall following (optional) fields must also be omitted.",
          "status": null
        },
        {
          "tag": "req LRM.Evaluation_Of_Checks",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1789
          },
          "name": "LRM.Evaluation_Of_Checks",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Dynamic_Semantics",
          "text": "text: A record object declaration creates a new binding for a\nrecord. The value of any frozen components is the value\nprovided in the freezing declaration. After references\nare resolved, all applicable checks on the object, including\nany checks for tuples, are evaluated in the context\nof this binding.",
          "status": null
        },
        {
          "tag": "req LRM.Late_Reference_Checking",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1798
          },
          "name": "LRM.Late_Reference_Checking",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Dynamic_Semantics",
          "text": "text: It is an error to refer to a record by name that does not\nexist. It is legal to refer to an record that\nhas not been encountered yet, as references\nare resolved after parsing.",
          "status": null
        },
        {
          "tag": "req LRM.References_To_Extensions",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1805
          },
          "name": "LRM.References_To_Extensions",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Dynamic_Semantics",
          "text": "text: A record reference must match in type, i.e. be of the\ncorrect type or any record extension of that\ntype. *(For example if RE extends R, then a\nlist of R may contain references to instances\nof R and RE. A list of RE may not contain any\nreferences to R.)*",
          "status": null
        },
        {
          "tag": "req LRM.Tuple_Checks",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1814
          },
          "name": "LRM.Tuple_Checks",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: The checks for a tuple aggregate are immediately evaluated\nafter the last value is parsed.",
          "status": null
        },
        {
          "tag": "req LRM.Sufficiently_Distinct",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1819
          },
          "name": "LRM.Sufficiently_Distinct",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Name_Resolution",
          "text": "text: When declaring record objects there are wider rules that\nindicate name clashes. Specifically a record\nmay not be declared if its \"simplified name\"\nclashes with any other \"simplified name\". A\n\"simplified name\" is the name converted to\nlowercase and all underscored removed.",
          "status": null
        },
        {
          "tag": "req LRM.Simplified_Name_Example",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1828
          },
          "name": "LRM.Simplified_Name_Example",
          "messages": [],
          "just_up": [],
          "just_down": [
            "Non-normative text"
          ],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "framework": "TRLC",
          "kind": "Note",
          "text": "text: For example the simplified name of `Foo_Bar` is `foobar`\nand therefore it clashes with `Foobar`,\n`F_Oobar`, or `Foo_B_A_R`. But only at record\ndeclaration; when referring to other object\nyou still have to use a precise match.",
          "status": null
        },
        {
          "tag": "req LRM.Simplified_Name_Rationale",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1836
          },
          "name": "LRM.Simplified_Name_Rationale",
          "messages": [],
          "just_up": [],
          "just_down": [
            "Non-normative text"
          ],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "framework": "TRLC",
          "kind": "Note",
          "text": "text: The purpose of this rule is to avoid requirements that\nhave hard to distinguish names.",
          "status": null
        },
        {
          "tag": "req LRM.Record_Object_API",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1841
          },
          "name": "LRM.Record_Object_API",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Recommendation",
          "text": "text: When exposing record instances through the API, it is\nrequired to make the type of the instance\navailable. There are some alternatives,\nnone of which are required:\n\nbullets: ['Provide an implicit String record field named `type` that\\ncarries this information (it is safe to do\\nthat, as it is impossible to specify a\\nrecord type with a field named `type`).', 'Provide a function or attribute that, when called, provides\\nthe type information.', 'Provide the type information through the type system of the\\nAPI language (e.g. the Python type system).']",
          "status": null
        },
        {
          "tag": "req LRM.Record_Object_Examples",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1856
          },
          "name": "LRM.Record_Object_Examples",
          "messages": [],
          "just_up": [],
          "just_down": [
            "Non-normative example"
          ],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "framework": "TRLC",
          "kind": "Example",
          "text": null,
          "status": null
        },
        {
          "tag": "req LRM.Markup_String_Format",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1891
          },
          "name": "LRM.Markup_String_Format",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Text",
          "text": "text: A `Markup_String` allows you to inline references to TRLC\nrecord in a string. The format is limited and\nsimple: any name or comma-separated list of\nnames enclosed in double square brackets\n(i.e. `[[` and `]]`) is considered a\nreference.",
          "status": null
        },
        {
          "tag": "req LRM.Markup_String_Errors",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1900
          },
          "name": "LRM.Markup_String_Errors",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Text",
          "text": "text: Attempting to nest, or close a list that does not exist, or\nnot close an open list before the end of the\nstring is an error.",
          "status": null
        },
        {
          "tag": "req LRM.Markup_String_Types",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1906
          },
          "name": "LRM.Markup_String_Types",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: The fragment of BNF grammar applicable is\nqualified_name. The type of each named object\nmust be a record type. *(This means you cannot\nreference types or enumerations.)*",
          "status": null
        },
        {
          "tag": "req LRM.Markup_String_Late_Reference_Resolution",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1913
          },
          "name": "LRM.Markup_String_Late_Reference_Resolution",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Dynamic_Semantics",
          "text": "text: The references are resolved late, just like an ordinary\nrecord reference. *(This means you can\nforward-reference objects, or reference\nyourself.)*",
          "status": null
        },
        {
          "tag": "req LRM.Markup_String_Resolution",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1920
          },
          "name": "LRM.Markup_String_Resolution",
          "messages": [
            "missing reference to Code",
            "missing reference to Test"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "TRLC",
          "kind": "Name_Resolution",
          "text": "text: The name resolution rules for the qualified_name are exactly\nthe same as they are for any other\nqualified_name. *(This means you need to\nimport all packages from which you reference\nobjects.)*",
          "status": null
        },
        {
          "tag": "req LRM.Markup_String_Examples",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1928
          },
          "name": "LRM.Markup_String_Examples",
          "messages": [],
          "just_up": [],
          "just_down": [
            "Non-normative example"
          ],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "framework": "TRLC",
          "kind": "Example",
          "text": null,
          "status": null
        },
        {
          "tag": "req LRM.Restricted_Null",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1976
          },
          "name": "LRM.Restricted_Null",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python parser.Parser.parse_conditional_expression",
            "python ast.Expression.ensure_type",
            "trlc-st rbt-restricted-null-1",
            "trlc-st rbt-restricted-null-2"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: The literal null value is only permitted to appear in\nan equality or inequality. Any other context (such as\n`(if a then null else b)` is rejected statically.",
          "status": null
        },
        {
          "tag": "req LRM.Null_Equivalence",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1982
          },
          "name": "LRM.Null_Equivalence",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python ast.Binary_Expression.evaluate",
            "trlc-st rbt-restricted-null-1"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Static_Semantics",
          "text": "text: The expression `null == null` is statically true.",
          "status": null
        },
        {
          "tag": "req LRM.Unspecified_Optional_Components",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1986
          },
          "name": "LRM.Unspecified_Optional_Components",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python ast.Implicit_Null.__init__",
            "python ast.Implicit_Null.evaluate",
            "python ast.Tuple_Aggregate.__init__",
            "python ast.Record_Object.__init__",
            "trlc-st rbt-restricted-null-1"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Dynamic_Semantics",
          "text": "text: The value of an optional component or field that is\nnot specified is `null`.",
          "status": null
        },
        {
          "tag": "req LRM.Null_Is_Invalid",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "language-reference-manual/lrm.trlc",
            "line": 1991
          },
          "name": "LRM.Null_Is_Invalid",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [],
          "ref_down": [
            "python ast.Expression.ensure_type",
            "python ast.Unary_Expression.evaluate",
            "python ast.Binary_Expression.evaluate",
            "python ast.Range_Test.evaluate",
            "python ast.Conditional_Expression.evaluate",
            "python ast.Quantified_Expression.evaluate",
            "trlc-st rbt-restricted-null-2"
          ],
          "tracing_status": "OK",
          "framework": "TRLC",
          "kind": "Dynamic_Semantics",
          "text": "text: For any other operator or operation, the null value is\nconsidered out of bounds and raises an\nerror. *(This means you can check if something\nis null or not, but any other use will cause\nan error.)*",
          "status": null
        }
      ],
      "coverage": 50.0
    },
    {
      "name": "Code",
      "kind": "implementation",
      "items": [
        {
          "tag": "python lint.Linter.__init__",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/lint.py",
            "line": 27
          },
          "name": "lint.Linter.__init__",
          "messages": [],
          "just_up": [
            "Not safety relevant"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "language": "Python",
          "kind": "Constructor"
        },
        {
          "tag": "python lint.Linter.verify",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/lint.py",
            "line": 44
          },
          "name": "lint.Linter.verify",
          "messages": [],
          "just_up": [
            "Not safety relevant"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python lint.Linter.verify_type",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/lint.py",
            "line": 66
          },
          "name": "lint.Linter.verify_type",
          "messages": [],
          "just_up": [
            "Not safety relevant"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python lint.Linter.verify_tuple_type",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/lint.py",
            "line": 84
          },
          "name": "lint.Linter.verify_tuple_type",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Tuple_Based_Literal_Ambiguity"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python lint.Linter.verify_record_type",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/lint.py",
            "line": 149
          },
          "name": "lint.Linter.verify_record_type",
          "messages": [],
          "just_up": [
            "Not safety relevant"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python lint.Linter.verify_array_type",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/lint.py",
            "line": 175
          },
          "name": "lint.Linter.verify_array_type",
          "messages": [],
          "just_up": [
            "Not safety relevant"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python math.remainder",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/math.py",
            "line": 25
          },
          "name": "math.remainder",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Function"
        },
        {
          "tag": "python math.round_nearest_away",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/math.py",
            "line": 37
          },
          "name": "math.round_nearest_away",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Function"
        },
        {
          "tag": "python errors.Location.__init__",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/errors.py",
            "line": 43
          },
          "name": "errors.Location.__init__",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Constructor"
        },
        {
          "tag": "python errors.Location.to_string",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/errors.py",
            "line": 55
          },
          "name": "errors.Location.to_string",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python errors.Location.context_lines",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/errors.py",
            "line": 77
          },
          "name": "errors.Location.context_lines",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python errors.Location.get_end_location",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/errors.py",
            "line": 80
          },
          "name": "errors.Location.get_end_location",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python errors.Kind.__str__",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/errors.py",
            "line": 106
          },
          "name": "errors.Kind.__str__",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python errors.TRLC_Error.__init__",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/errors.py",
            "line": 126
          },
          "name": "errors.TRLC_Error.__init__",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Constructor"
        },
        {
          "tag": "python errors.Message_Handler.__init__",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/errors.py",
            "line": 162
          },
          "name": "errors.Message_Handler.__init__",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Constructor"
        },
        {
          "tag": "python errors.Message_Handler.suppress",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/errors.py",
            "line": 172
          },
          "name": "errors.Message_Handler.suppress",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python errors.Message_Handler.cross_file_reference",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/errors.py",
            "line": 176
          },
          "name": "errors.Message_Handler.cross_file_reference",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python errors.Message_Handler.emit",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/errors.py",
            "line": 184
          },
          "name": "errors.Message_Handler.emit",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python errors.Message_Handler.lex_error",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/errors.py",
            "line": 238
          },
          "name": "errors.Message_Handler.lex_error",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python errors.Message_Handler.error",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/errors.py",
            "line": 247
          },
          "name": "errors.Message_Handler.error",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python errors.Message_Handler.warning",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/errors.py",
            "line": 297
          },
          "name": "errors.Message_Handler.warning",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python errors.Message_Handler.check",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/errors.py",
            "line": 324
          },
          "name": "errors.Message_Handler.check",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python errors.Message_Handler.ice_loc",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/errors.py",
            "line": 338
          },
          "name": "errors.Message_Handler.ice_loc",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python nested.Nested_Lexer.__init__",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/nested.py",
            "line": 28
          },
          "name": "nested.Nested_Lexer.__init__",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Constructor"
        },
        {
          "tag": "python nested.Nested_Lexer.source_location",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/nested.py",
            "line": 44
          },
          "name": "nested.Nested_Lexer.source_location",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python nested.Nested_Lexer.file_location",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/nested.py",
            "line": 84
          },
          "name": "nested.Nested_Lexer.file_location",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python nested.Nested_Lexer.token",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/nested.py",
            "line": 88
          },
          "name": "nested.Nested_Lexer.token",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python lexer.triple_quoted_string_value",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/lexer.py",
            "line": 28
          },
          "name": "lexer.triple_quoted_string_value",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Complex_String_Value"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Function"
        },
        {
          "tag": "python lexer.Source_Reference.__init__",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/lexer.py",
            "line": 71
          },
          "name": "lexer.Source_Reference.__init__",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Constructor"
        },
        {
          "tag": "python lexer.Source_Reference.text",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/lexer.py",
            "line": 85
          },
          "name": "lexer.Source_Reference.text",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python lexer.Source_Reference.context_lines",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/lexer.py",
            "line": 88
          },
          "name": "lexer.Source_Reference.context_lines",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python lexer.Source_Reference.get_end_location",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/lexer.py",
            "line": 112
          },
          "name": "lexer.Source_Reference.get_end_location",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python lexer.Token_Base.__init__",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/lexer.py",
            "line": 128
          },
          "name": "lexer.Token_Base.__init__",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Constructor"
        },
        {
          "tag": "python lexer.Token.__init__",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/lexer.py",
            "line": 161
          },
          "name": "lexer.Token.__init__",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Constructor"
        },
        {
          "tag": "python lexer.Token.__repr__",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/lexer.py",
            "line": 174
          },
          "name": "lexer.Token.__repr__",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python lexer.Lexer_Base.__init__",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/lexer.py",
            "line": 182
          },
          "name": "lexer.Lexer_Base.__init__",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Constructor"
        },
        {
          "tag": "python lexer.Lexer_Base.is_alpha",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/lexer.py",
            "line": 200
          },
          "name": "lexer.Lexer_Base.is_alpha",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Identifier"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python lexer.Lexer_Base.is_numeric",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/lexer.py",
            "line": 205
          },
          "name": "lexer.Lexer_Base.is_numeric",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Decimals",
            "req LRM.Integers"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python lexer.Lexer_Base.is_alnum",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/lexer.py",
            "line": 211
          },
          "name": "lexer.Lexer_Base.is_alnum",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Identifier"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python lexer.Lexer_Base.file_location",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/lexer.py",
            "line": 216
          },
          "name": "lexer.Lexer_Base.file_location",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python lexer.Lexer_Base.token",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/lexer.py",
            "line": 220
          },
          "name": "lexer.Lexer_Base.token",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python lexer.Lexer_Base.skip_whitespace",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/lexer.py",
            "line": 223
          },
          "name": "lexer.Lexer_Base.skip_whitespace",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Whitespace"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python lexer.Lexer_Base.advance",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/lexer.py",
            "line": 229
          },
          "name": "lexer.Lexer_Base.advance",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python lexer.TRLC_Lexer.__init__",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/lexer.py",
            "line": 296
          },
          "name": "lexer.TRLC_Lexer.__init__",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.File_Encoding_Fixed",
            "req LRM.File_Encoding"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Constructor"
        },
        {
          "tag": "python lexer.TRLC_Lexer.current_location",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/lexer.py",
            "line": 311
          },
          "name": "lexer.TRLC_Lexer.current_location",
          "messages": [],
          "just_up": [
            "Utility function"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python lexer.TRLC_Lexer.file_location",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/lexer.py",
            "line": 319
          },
          "name": "lexer.TRLC_Lexer.file_location",
          "messages": [],
          "just_up": [
            "Utility function"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python lexer.TRLC_Lexer.token",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/lexer.py",
            "line": 323
          },
          "name": "lexer.TRLC_Lexer.token",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Decimal_Values",
            "req LRM.Integer_Values",
            "req LRM.Simple_String_Value",
            "req LRM.TRLC_Keywords",
            "req LRM.Decimals",
            "req LRM.Integers",
            "req LRM.Strings",
            "req LRM.Lexing_Disambiguation",
            "req LRM.Double_Delimiters",
            "req LRM.Single_Delimiters",
            "req LRM.Identifier",
            "req LRM.Comments"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python lexer.sanity_test",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/lexer.py",
            "line": 635
          },
          "name": "lexer.sanity_test",
          "messages": [],
          "just_up": [
            "Developer test function"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "language": "Python",
          "kind": "Function"
        },
        {
          "tag": "python trlc.Source_Manager.__init__",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/trlc.py",
            "line": 76
          },
          "name": "trlc.Source_Manager.__init__",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Constructor"
        },
        {
          "tag": "python trlc.Source_Manager.callback_parse_begin",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/trlc.py",
            "line": 115
          },
          "name": "trlc.Source_Manager.callback_parse_begin",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python trlc.Source_Manager.callback_parse_progress",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/trlc.py",
            "line": 118
          },
          "name": "trlc.Source_Manager.callback_parse_progress",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python trlc.Source_Manager.callback_parse_end",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/trlc.py",
            "line": 121
          },
          "name": "trlc.Source_Manager.callback_parse_end",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python trlc.Source_Manager.signal_progress",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/trlc.py",
            "line": 124
          },
          "name": "trlc.Source_Manager.signal_progress",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python trlc.Source_Manager.cross_file_reference",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/trlc.py",
            "line": 132
          },
          "name": "trlc.Source_Manager.cross_file_reference",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python trlc.Source_Manager.update_common_root",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/trlc.py",
            "line": 145
          },
          "name": "trlc.Source_Manager.update_common_root",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python trlc.Source_Manager.create_parser",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/trlc.py",
            "line": 158
          },
          "name": "trlc.Source_Manager.create_parser",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python trlc.Source_Manager.register_include",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/trlc.py",
            "line": 173
          },
          "name": "trlc.Source_Manager.register_include",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python trlc.Source_Manager.register_file",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/trlc.py",
            "line": 201
          },
          "name": "trlc.Source_Manager.register_file",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Layout"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python trlc.Source_Manager.register_directory",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/trlc.py",
            "line": 243
          },
          "name": "trlc.Source_Manager.register_directory",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Layout"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python trlc.Source_Manager.register_rsl_file",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/trlc.py",
            "line": 279
          },
          "name": "trlc.Source_Manager.register_rsl_file",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Preamble"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python trlc.Source_Manager.register_check_file",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/trlc.py",
            "line": 295
          },
          "name": "trlc.Source_Manager.register_check_file",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Preamble"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python trlc.Source_Manager.register_trlc_file",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/trlc.py",
            "line": 311
          },
          "name": "trlc.Source_Manager.register_trlc_file",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Preamble",
            "req LRM.TRLC_File"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python trlc.Source_Manager.build_graph",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/trlc.py",
            "line": 332
          },
          "name": "trlc.Source_Manager.build_graph",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Preamble"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python trlc.Source_Manager.parse_rsl_files",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/trlc.py",
            "line": 411
          },
          "name": "trlc.Source_Manager.parse_rsl_files",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Circular_Dependencies",
            "req LRM.RSL_File",
            "req LRM.Preamble"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python trlc.Source_Manager.parse_check_files",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/trlc.py",
            "line": 465
          },
          "name": "trlc.Source_Manager.parse_check_files",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Check_File",
            "req LRM.Preamble"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python trlc.Source_Manager.parse_trlc_files",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/trlc.py",
            "line": 485
          },
          "name": "trlc.Source_Manager.parse_trlc_files",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Preamble",
            "req LRM.TRLC_File"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python trlc.Source_Manager.resolve_record_references",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/trlc.py",
            "line": 507
          },
          "name": "trlc.Source_Manager.resolve_record_references",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python trlc.Source_Manager.perform_checks",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/trlc.py",
            "line": 518
          },
          "name": "trlc.Source_Manager.perform_checks",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python trlc.Source_Manager.perform_sanity_checks",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/trlc.py",
            "line": 530
          },
          "name": "trlc.Source_Manager.perform_sanity_checks",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python trlc.Source_Manager.process",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/trlc.py",
            "line": 538
          },
          "name": "trlc.Source_Manager.process",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.File_Parsing_References",
            "req LRM.File_Parsing_Order"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python trlc.main",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/trlc.py",
            "line": 609
          },
          "name": "trlc.main",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Function"
        },
        {
          "tag": "python parser.Markup_Token.__init__",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/parser.py",
            "line": 39
          },
          "name": "parser.Markup_Token.__init__",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Constructor"
        },
        {
          "tag": "python parser.Markup_Lexer.__init__",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/parser.py",
            "line": 45
          },
          "name": "parser.Markup_Lexer.__init__",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Constructor"
        },
        {
          "tag": "python parser.Markup_Lexer.file_location",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/parser.py",
            "line": 50
          },
          "name": "parser.Markup_Lexer.file_location",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python parser.Markup_Lexer.token",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/parser.py",
            "line": 53
          },
          "name": "parser.Markup_Lexer.token",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python parser.Parser_Base.__init__",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/parser.py",
            "line": 122
          },
          "name": "parser.Parser_Base.__init__",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Constructor"
        },
        {
          "tag": "python parser.Parser_Base.advance",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/parser.py",
            "line": 139
          },
          "name": "parser.Parser_Base.advance",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Comments"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python parser.Parser_Base.skip_until_newline",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/parser.py",
            "line": 147
          },
          "name": "parser.Parser_Base.skip_until_newline",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python parser.Parser_Base.peek",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/parser.py",
            "line": 154
          },
          "name": "parser.Parser_Base.peek",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python parser.Parser_Base.peek_eof",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/parser.py",
            "line": 159
          },
          "name": "parser.Parser_Base.peek_eof",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python parser.Parser_Base.peek_kw",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/parser.py",
            "line": 162
          },
          "name": "parser.Parser_Base.peek_kw",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python parser.Parser_Base.match",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/parser.py",
            "line": 167
          },
          "name": "parser.Parser_Base.match",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python parser.Parser_Base.match_eof",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/parser.py",
            "line": 186
          },
          "name": "parser.Parser_Base.match_eof",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python parser.Parser_Base.match_kw",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/parser.py",
            "line": 193
          },
          "name": "parser.Parser_Base.match_kw",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python parser.Markup_Parser.__init__",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/parser.py",
            "line": 219
          },
          "name": "parser.Markup_Parser.__init__",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Constructor"
        },
        {
          "tag": "python parser.Markup_Parser.parse_all_references",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/parser.py",
            "line": 228
          },
          "name": "parser.Markup_Parser.parse_all_references",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python parser.Markup_Parser.parse_ref_list",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/parser.py",
            "line": 237
          },
          "name": "parser.Markup_Parser.parse_ref_list",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python parser.Markup_Parser.parse_qualified_name",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/parser.py",
            "line": 245
          },
          "name": "parser.Markup_Parser.parse_qualified_name",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Valid_Name",
            "req LRM.Valid_Qualifier",
            "req LRM.Qualified_Name"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python parser.Parser.__init__",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/parser.py",
            "line": 277
          },
          "name": "parser.Parser.__init__",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Constructor"
        },
        {
          "tag": "python parser.Parser.parse_described_name",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/parser.py",
            "line": 325
          },
          "name": "parser.Parser.parse_described_name",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Described_Name_Description",
            "req LRM.Described_Names"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python parser.Parser.parse_qualified_name",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/parser.py",
            "line": 337
          },
          "name": "parser.Parser.parse_qualified_name",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Valid_Name",
            "req LRM.Valid_Qualifier",
            "req LRM.Qualified_Name"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python parser.Parser.parse_type_declaration",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/parser.py",
            "line": 363
          },
          "name": "parser.Parser.parse_type_declaration",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Type_Declarations"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python parser.Parser.parse_enum_declaration",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/parser.py",
            "line": 374
          },
          "name": "parser.Parser.parse_enum_declaration",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.No_Empty_Enumerations",
            "req LRM.Enumeration_Declaration"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python parser.Parser.parse_tuple_field",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/parser.py",
            "line": 404
          },
          "name": "parser.Parser.parse_tuple_field",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Tuple_Field_Types"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python parser.Parser.parse_tuple_declaration",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/parser.py",
            "line": 438
          },
          "name": "parser.Parser.parse_tuple_declaration",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Tuple_Field_Types",
            "req LRM.Restricted_Tuple_Nesting",
            "req LRM.Tuple_Optional_Fields",
            "req LRM.Tuple_Optional_Requires_Separators",
            "req LRM.Tuple_Separators_All_Or_None",
            "req LRM.Tuple_Declaration"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python parser.Parser.parse_record_component",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/parser.py",
            "line": 510
          },
          "name": "parser.Parser.parse_record_component",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python parser.Parser.parse_record_declaration",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/parser.py",
            "line": 554
          },
          "name": "parser.Parser.parse_record_declaration",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python parser.Parser.parse_expression",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/parser.py",
            "line": 633
          },
          "name": "parser.Parser.parse_expression",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Expression"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python parser.Parser.parse_relation",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/parser.py",
            "line": 691
          },
          "name": "parser.Parser.parse_relation",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Operators",
            "req LRM.Relation"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python parser.Parser.parse_simple_expression",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/parser.py",
            "line": 777
          },
          "name": "parser.Parser.parse_simple_expression",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Unary_Minus_Parsing",
            "req LRM.Operators",
            "req LRM.Simple_Expression"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python parser.Parser.parse_term",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/parser.py",
            "line": 835
          },
          "name": "parser.Parser.parse_term",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Operators",
            "req LRM.Term"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python parser.Parser.parse_factor",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/parser.py",
            "line": 860
          },
          "name": "parser.Parser.parse_factor",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Factor"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python parser.Parser.parse_primary",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/parser.py",
            "line": 905
          },
          "name": "parser.Parser.parse_primary",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Boolean_Values",
            "req LRM.String_Values",
            "req LRM.Decimal_Values",
            "req LRM.Integer_Values",
            "req LRM.Primary"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python parser.Parser.parse_quantified_expression",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/parser.py",
            "line": 947
          },
          "name": "parser.Parser.parse_quantified_expression",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python parser.Parser.parse_conditional_expression",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/parser.py",
            "line": 993
          },
          "name": "parser.Parser.parse_conditional_expression",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Restricted_Null",
            "req LRM.Conditional_Expression"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python parser.Parser.parse_builtin",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/parser.py",
            "line": 1026
          },
          "name": "parser.Parser.parse_builtin",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Builtin_Type_Conversion_Functions",
            "req LRM.Builtin_Functions"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python parser.Parser.parse_name",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/parser.py",
            "line": 1126
          },
          "name": "parser.Parser.parse_name",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Builtin_Type_Conversion_Functions",
            "req LRM.Builtin_Functions"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python parser.Parser.parse_check_block",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/parser.py",
            "line": 1246
          },
          "name": "parser.Parser.parse_check_block",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.No_Newlines_In_Message",
            "req LRM.Applicable_Components",
            "req LRM.Applicable_Types",
            "req LRM.Check_Block"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python parser.Parser.parse_section_declaration",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/parser.py",
            "line": 1334
          },
          "name": "parser.Parser.parse_section_declaration",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Section_Declaration"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python parser.Parser.parse_boolean",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/parser.py",
            "line": 1353
          },
          "name": "parser.Parser.parse_boolean",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Boolean_Values"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python parser.Parser.parse_value",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/parser.py",
            "line": 1362
          },
          "name": "parser.Parser.parse_value",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.String_Values",
            "req LRM.Markup_String_Values",
            "req LRM.Decimal_Values",
            "req LRM.Integer_Values"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python parser.Parser.parse_markup_string",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/parser.py",
            "line": 1532
          },
          "name": "parser.Parser.parse_markup_string",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Markup_String_Values"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python parser.Parser.parse_record_object_declaration",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/parser.py",
            "line": 1540
          },
          "name": "parser.Parser.parse_record_object_declaration",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Section_Declaration"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python parser.Parser.parse_trlc_entry",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/parser.py",
            "line": 1588
          },
          "name": "parser.Parser.parse_trlc_entry",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.TRLC_File"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python parser.Parser.parse_preamble",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/parser.py",
            "line": 1595
          },
          "name": "parser.Parser.parse_preamble",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Import_Visibility",
            "req LRM.Current_Package",
            "req LRM.Duplicate_Late_Packages",
            "req LRM.Package_Declaration",
            "req LRM.Late_Package_Declarations",
            "req LRM.Cannot_Declare_In_Check_File",
            "req LRM.Preamble",
            "req LRM.Layout"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python parser.Parser.parse_rsl_file",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/parser.py",
            "line": 1647
          },
          "name": "parser.Parser.parse_rsl_file",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.RSL_File"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python parser.Parser.parse_check_file",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/parser.py",
            "line": 1682
          },
          "name": "parser.Parser.parse_check_file",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Import_In_Check",
            "req LRM.Deprecated_Check_Files",
            "req LRM.Check_File"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python parser.Parser.parse_trlc_file",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/parser.py",
            "line": 1716
          },
          "name": "parser.Parser.parse_trlc_file",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.TRLC_File"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python vcg.Unsupported",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/vcg.py",
            "line": 50
          },
          "name": "vcg.Unsupported",
          "messages": [],
          "just_up": [
            "Not safety relevant"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "language": "Python",
          "kind": "Class"
        },
        {
          "tag": "python vcg.Feedback",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/vcg.py",
            "line": 61
          },
          "name": "vcg.Feedback",
          "messages": [],
          "just_up": [
            "Not safety relevant"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "language": "Python",
          "kind": "Class"
        },
        {
          "tag": "python vcg.VCG",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/vcg.py",
            "line": 74
          },
          "name": "vcg.VCG",
          "messages": [],
          "just_up": [
            "Not safety relevant"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "language": "Python",
          "kind": "Class"
        },
        {
          "tag": "python ast.Value",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 49
          },
          "name": "ast.Value",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Markup_String_Values",
            "req LRM.String_Values",
            "req LRM.Decimal_Values",
            "req LRM.Integer_Values",
            "req LRM.Boolean_Values"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Class"
        },
        {
          "tag": "python ast.Node.__init__",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 110
          },
          "name": "ast.Node.__init__",
          "messages": [],
          "just_up": [
            "Constructor only declares variables"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "language": "Python",
          "kind": "Constructor"
        },
        {
          "tag": "python ast.Node.write_indent",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 115
          },
          "name": "ast.Node.write_indent",
          "messages": [],
          "just_up": [
            "Debugging feature"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Node.dump",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 123
          },
          "name": "ast.Node.dump",
          "messages": [],
          "just_up": [
            "Debugging feature"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Check_Block.__init__",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 181
          },
          "name": "ast.Check_Block.__init__",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Check_Block"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Constructor"
        },
        {
          "tag": "python ast.Check_Block.add_check",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 188
          },
          "name": "ast.Check_Block.add_check",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Check_Evaluation_Order"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Check_Block.dump",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 193
          },
          "name": "ast.Check_Block.dump",
          "messages": [],
          "just_up": [
            "Debugging feature"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Compilation_Unit.__init__",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 214
          },
          "name": "ast.Compilation_Unit.__init__",
          "messages": [],
          "just_up": [
            "Constructor only declares variables"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "language": "Python",
          "kind": "Constructor"
        },
        {
          "tag": "python ast.Compilation_Unit.dump",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 222
          },
          "name": "ast.Compilation_Unit.dump",
          "messages": [],
          "just_up": [
            "Debugging feature"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Compilation_Unit.set_package",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 231
          },
          "name": "ast.Compilation_Unit.set_package",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Current_Package"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Compilation_Unit.add_import",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 236
          },
          "name": "ast.Compilation_Unit.add_import",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Self_Imports",
            "req LRM.Import_Visibility"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Compilation_Unit.resolve_imports",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 256
          },
          "name": "ast.Compilation_Unit.resolve_imports",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Import_Visibility"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Compilation_Unit.is_visible",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 269
          },
          "name": "ast.Compilation_Unit.is_visible",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Import_Visibility"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Compilation_Unit.add_item",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 275
          },
          "name": "ast.Compilation_Unit.add_item",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.TRLC_File",
            "req LRM.Check_File",
            "req LRM.RSL_File"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Check.__init__",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 312
          },
          "name": "ast.Check.__init__",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.No_Newlines_In_Message",
            "req LRM.Check_Block"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Constructor"
        },
        {
          "tag": "python ast.Check.dump",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 340
          },
          "name": "ast.Check.dump",
          "messages": [],
          "just_up": [
            "Debugging feature"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Check.get_real_location",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 352
          },
          "name": "ast.Check.get_real_location",
          "messages": [],
          "just_up": [
            "LRM.Anchoring"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Check.perform",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 366
          },
          "name": "ast.Check.perform",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Check_Severity",
            "req LRM.Check_Messages"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Unary_Operator",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 401
          },
          "name": "ast.Unary_Operator",
          "messages": [],
          "just_up": [
            "Utility enumeration for unary operators"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "language": "Python",
          "kind": "Class"
        },
        {
          "tag": "python ast.Binary_Operator",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 415
          },
          "name": "ast.Binary_Operator",
          "messages": [],
          "just_up": [
            "Utility enumeration for binary operators"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "language": "Python",
          "kind": "Class"
        },
        {
          "tag": "python ast.Expression.__init__",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 453
          },
          "name": "ast.Expression.__init__",
          "messages": [],
          "just_up": [
            "Constructor only declares variables"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "language": "Python",
          "kind": "Constructor"
        },
        {
          "tag": "python ast.Expression.evaluate",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 459
          },
          "name": "ast.Expression.evaluate",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Expression.to_string",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 481
          },
          "name": "ast.Expression.to_string",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Expression.ensure_type",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 485
          },
          "name": "ast.Expression.ensure_type",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Null_Is_Invalid",
            "req LRM.Restricted_Null"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Expression.resolve_references",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 503
          },
          "name": "ast.Expression.resolve_references",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Expression.can_be_null",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 507
          },
          "name": "ast.Expression.can_be_null",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Implicit_Null.__init__",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 550
          },
          "name": "ast.Implicit_Null.__init__",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Unspecified_Optional_Components"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Constructor"
        },
        {
          "tag": "python ast.Implicit_Null.to_string",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 557
          },
          "name": "ast.Implicit_Null.to_string",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Implicit_Null.evaluate",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 560
          },
          "name": "ast.Implicit_Null.evaluate",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Unspecified_Optional_Components"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Implicit_Null.to_python_object",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 566
          },
          "name": "ast.Implicit_Null.to_python_object",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Implicit_Null.dump",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 569
          },
          "name": "ast.Implicit_Null.dump",
          "messages": [],
          "just_up": [
            "Debugging feature"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Implicit_Null.can_be_null",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 573
          },
          "name": "ast.Implicit_Null.can_be_null",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Literal.to_python_object",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 588
          },
          "name": "ast.Literal.to_python_object",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Null_Literal",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 592
          },
          "name": "ast.Null_Literal",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Primary"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Class"
        },
        {
          "tag": "python ast.Integer_Literal",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 629
          },
          "name": "ast.Integer_Literal",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Primary",
            "req LRM.Integer_Values"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Class"
        },
        {
          "tag": "python ast.Decimal_Literal",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 676
          },
          "name": "ast.Decimal_Literal",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Primary",
            "req LRM.Decimal_Values"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Class"
        },
        {
          "tag": "python ast.String_Literal",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 723
          },
          "name": "ast.String_Literal",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Primary",
            "req LRM.Markup_String_Values",
            "req LRM.String_Values"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Class"
        },
        {
          "tag": "python ast.Boolean_Literal",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 780
          },
          "name": "ast.Boolean_Literal",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Primary",
            "req LRM.Boolean_Values"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Class"
        },
        {
          "tag": "python ast.Enumeration_Literal.__init__",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 835
          },
          "name": "ast.Enumeration_Literal.__init__",
          "messages": [],
          "just_up": [
            "Constructor only declares variables"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "language": "Python",
          "kind": "Constructor"
        },
        {
          "tag": "python ast.Enumeration_Literal.dump",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 842
          },
          "name": "ast.Enumeration_Literal.dump",
          "messages": [],
          "just_up": [
            "Debugging feature"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Enumeration_Literal.to_string",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 848
          },
          "name": "ast.Enumeration_Literal.to_string",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Enumeration_Literal.evaluate",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 851
          },
          "name": "ast.Enumeration_Literal.evaluate",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Enumeration_Literal.to_python_object",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 856
          },
          "name": "ast.Enumeration_Literal.to_python_object",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Enumeration_Literal.can_be_null",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 859
          },
          "name": "ast.Enumeration_Literal.can_be_null",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Array_Aggregate.__init__",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 882
          },
          "name": "ast.Array_Aggregate.__init__",
          "messages": [],
          "just_up": [
            "Constructor only declares variables"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "language": "Python",
          "kind": "Constructor"
        },
        {
          "tag": "python ast.Array_Aggregate.dump",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 887
          },
          "name": "ast.Array_Aggregate.dump",
          "messages": [],
          "just_up": [
            "Debugging feature"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Array_Aggregate.append",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 893
          },
          "name": "ast.Array_Aggregate.append",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Array_Aggregate.to_string",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 901
          },
          "name": "ast.Array_Aggregate.to_string",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Array_Aggregate.evaluate",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 904
          },
          "name": "ast.Array_Aggregate.evaluate",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Array_Aggregate.resolve_references",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 912
          },
          "name": "ast.Array_Aggregate.resolve_references",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Array_Aggregate.to_python_object",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 918
          },
          "name": "ast.Array_Aggregate.to_python_object",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Array_Aggregate.can_be_null",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 921
          },
          "name": "ast.Array_Aggregate.can_be_null",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Tuple_Aggregate.__init__",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 946
          },
          "name": "ast.Tuple_Aggregate.__init__",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Unspecified_Optional_Components"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Constructor"
        },
        {
          "tag": "python ast.Tuple_Aggregate.assign",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 952
          },
          "name": "ast.Tuple_Aggregate.assign",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Tuple_Aggregate.dump",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 963
          },
          "name": "ast.Tuple_Aggregate.dump",
          "messages": [],
          "just_up": [
            "Debugging feature"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Tuple_Aggregate.to_string",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 971
          },
          "name": "ast.Tuple_Aggregate.to_string",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Tuple_Aggregate.evaluate",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 993
          },
          "name": "ast.Tuple_Aggregate.evaluate",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Tuple_Aggregate.resolve_references",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 1001
          },
          "name": "ast.Tuple_Aggregate.resolve_references",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Tuple_Aggregate.to_python_object",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 1007
          },
          "name": "ast.Tuple_Aggregate.to_python_object",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Tuple_Aggregate.can_be_null",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 1011
          },
          "name": "ast.Tuple_Aggregate.can_be_null",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Record_Reference.__init__",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 1046
          },
          "name": "ast.Record_Reference.__init__",
          "messages": [],
          "just_up": [
            "Constructor only declares variables"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "language": "Python",
          "kind": "Constructor"
        },
        {
          "tag": "python ast.Record_Reference.dump",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 1058
          },
          "name": "ast.Record_Reference.dump",
          "messages": [],
          "just_up": [
            "Debugging feature"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Record_Reference.to_string",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 1064
          },
          "name": "ast.Record_Reference.to_string",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Record_Reference.evaluate",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 1067
          },
          "name": "ast.Record_Reference.evaluate",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Record_Reference.resolve_references",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 1072
          },
          "name": "ast.Record_Reference.resolve_references",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Record_Reference.to_python_object",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 1088
          },
          "name": "ast.Record_Reference.to_python_object",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Record_Reference.can_be_null",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 1091
          },
          "name": "ast.Record_Reference.can_be_null",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Name_Reference",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 1095
          },
          "name": "ast.Name_Reference",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Qualified_Name"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Class"
        },
        {
          "tag": "python ast.Unary_Expression.__init__",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 1171
          },
          "name": "ast.Unary_Expression.__init__",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Factor",
            "req LRM.Relation",
            "req LRM.Simple_Expression"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Constructor"
        },
        {
          "tag": "python ast.Unary_Expression.to_string",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 1200
          },
          "name": "ast.Unary_Expression.to_string",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Unary_Expression.dump",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 1225
          },
          "name": "ast.Unary_Expression.dump",
          "messages": [],
          "just_up": [
            "Debugging feature"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Unary_Expression.evaluate",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 1231
          },
          "name": "ast.Unary_Expression.evaluate",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Null_Is_Invalid"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Unary_Expression.to_python_object",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 1282
          },
          "name": "ast.Unary_Expression.to_python_object",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Unary_Expression.can_be_null",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 1291
          },
          "name": "ast.Unary_Expression.can_be_null",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Binary_Expression.__init__",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 1338
          },
          "name": "ast.Binary_Expression.__init__",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Factor",
            "req LRM.Term",
            "req LRM.Simple_Expression",
            "req LRM.Relation",
            "req LRM.Expression"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Constructor"
        },
        {
          "tag": "python ast.Binary_Expression.dump",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 1420
          },
          "name": "ast.Binary_Expression.dump",
          "messages": [],
          "just_up": [
            "Debugging feature"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Binary_Expression.to_string",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 1427
          },
          "name": "ast.Binary_Expression.to_string",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Binary_Expression.evaluate",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 1471
          },
          "name": "ast.Binary_Expression.evaluate",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Null_Is_Invalid",
            "req LRM.Null_Equivalence"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Binary_Expression.can_be_null",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 1679
          },
          "name": "ast.Binary_Expression.can_be_null",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Field_Access_Expression.__init__",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 1698
          },
          "name": "ast.Field_Access_Expression.__init__",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Constructor"
        },
        {
          "tag": "python ast.Field_Access_Expression.dump",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 1708
          },
          "name": "ast.Field_Access_Expression.dump",
          "messages": [],
          "just_up": [
            "Debugging feature"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Field_Access_Expression.to_string",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 1713
          },
          "name": "ast.Field_Access_Expression.to_string",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Field_Access_Expression.evaluate",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 1716
          },
          "name": "ast.Field_Access_Expression.evaluate",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Field_Access_Expression.can_be_null",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 1722
          },
          "name": "ast.Field_Access_Expression.can_be_null",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Range_Test.__init__",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 1747
          },
          "name": "ast.Range_Test.__init__",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Relation"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Constructor"
        },
        {
          "tag": "python ast.Range_Test.to_string",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 1762
          },
          "name": "ast.Range_Test.to_string",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Range_Test.dump",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 1767
          },
          "name": "ast.Range_Test.dump",
          "messages": [],
          "just_up": [
            "Debugging feature"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Range_Test.evaluate",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 1775
          },
          "name": "ast.Range_Test.evaluate",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Null_Is_Invalid"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Range_Test.can_be_null",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 1805
          },
          "name": "ast.Range_Test.can_be_null",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Action.__init__",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 1832
          },
          "name": "ast.Action.__init__",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Conditional_Expression_Types",
            "req LRM.Conditional_Expression"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Constructor"
        },
        {
          "tag": "python ast.Action.dump",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 1847
          },
          "name": "ast.Action.dump",
          "messages": [],
          "just_up": [
            "Debugging feature"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Action.to_string",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 1855
          },
          "name": "ast.Action.to_string",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Conditional_Expression.__init__",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 1885
          },
          "name": "ast.Conditional_Expression.__init__",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Conditional_Expression"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Constructor"
        },
        {
          "tag": "python ast.Conditional_Expression.add_elsif",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 1893
          },
          "name": "ast.Conditional_Expression.add_elsif",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Conditional_Expression"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Conditional_Expression.set_else_part",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 1903
          },
          "name": "ast.Conditional_Expression.set_else_part",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Conditional_Expression"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Conditional_Expression.dump",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 1912
          },
          "name": "ast.Conditional_Expression.dump",
          "messages": [],
          "just_up": [
            "Debugging feature"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Conditional_Expression.to_string",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 1920
          },
          "name": "ast.Conditional_Expression.to_string",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Conditional_Expression.evaluate",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 1927
          },
          "name": "ast.Conditional_Expression.evaluate",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Null_Is_Invalid",
            "req LRM.Conditional_Expression_Evaluation",
            "req LRM.Conditional_Expression_Else"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Conditional_Expression.can_be_null",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 1946
          },
          "name": "ast.Conditional_Expression.can_be_null",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Quantified_Expression.__init__",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 1980
          },
          "name": "ast.Quantified_Expression.__init__",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Constructor"
        },
        {
          "tag": "python ast.Quantified_Expression.dump",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 1998
          },
          "name": "ast.Quantified_Expression.dump",
          "messages": [],
          "just_up": [
            "Debugging feature"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Quantified_Expression.to_string",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 2007
          },
          "name": "ast.Quantified_Expression.to_string",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Quantified_Expression.evaluate",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 2015
          },
          "name": "ast.Quantified_Expression.evaluate",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Null_Is_Invalid"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Quantified_Expression.can_be_null",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 2059
          },
          "name": "ast.Quantified_Expression.can_be_null",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Entity.__init__",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 2078
          },
          "name": "ast.Entity.__init__",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Described_Name_Equality"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Constructor"
        },
        {
          "tag": "python ast.Typed_Entity.__init__",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 2096
          },
          "name": "ast.Typed_Entity.__init__",
          "messages": [],
          "just_up": [
            "Constructor only declares variables"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "language": "Python",
          "kind": "Constructor"
        },
        {
          "tag": "python ast.Quantified_Variable.dump",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 2119
          },
          "name": "ast.Quantified_Variable.dump",
          "messages": [],
          "just_up": [
            "Debugging feature"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Type.perform_type_checks",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 2129
          },
          "name": "ast.Type.perform_type_checks",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Type.get_example_value",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 2134
          },
          "name": "ast.Type.get_example_value",
          "messages": [],
          "just_up": [
            "utility method"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Concrete_Type",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 2139
          },
          "name": "ast.Concrete_Type",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Type_Declarations"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Class"
        },
        {
          "tag": "python ast.Builtin_Type",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 2167
          },
          "name": "ast.Builtin_Type",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Builtin_Types"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Class"
        },
        {
          "tag": "python ast.Builtin_Numeric_Type",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 2181
          },
          "name": "ast.Builtin_Numeric_Type",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Builtin_Types"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Class"
        },
        {
          "tag": "python ast.Builtin_Function",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 2190
          },
          "name": "ast.Builtin_Function",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Builtin_Functions"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Class"
        },
        {
          "tag": "python ast.Array_Type.__init__",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 2237
          },
          "name": "ast.Array_Type.__init__",
          "messages": [],
          "just_up": [
            "Constructor only declares variables"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "language": "Python",
          "kind": "Constructor"
        },
        {
          "tag": "python ast.Array_Type.dump",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 2275
          },
          "name": "ast.Array_Type.dump",
          "messages": [],
          "just_up": [
            "Debugging feature"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Array_Type.perform_type_checks",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 2286
          },
          "name": "ast.Array_Type.perform_type_checks",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Array_Type.get_example_value",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 2295
          },
          "name": "ast.Array_Type.get_example_value",
          "messages": [],
          "just_up": [
            "utility method"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Builtin_Integer",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 2300
          },
          "name": "ast.Builtin_Integer",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Integer_Values",
            "req LRM.Builtin_Types"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Class"
        },
        {
          "tag": "python ast.Builtin_Decimal",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 2312
          },
          "name": "ast.Builtin_Decimal",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Decimal_Values",
            "req LRM.Builtin_Types"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Class"
        },
        {
          "tag": "python ast.Builtin_Boolean",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 2324
          },
          "name": "ast.Builtin_Boolean",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Boolean_Values",
            "req LRM.Builtin_Types"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Class"
        },
        {
          "tag": "python ast.Builtin_String",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 2336
          },
          "name": "ast.Builtin_String",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.String_Values",
            "req LRM.Builtin_Types"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Class"
        },
        {
          "tag": "python ast.Builtin_Markup_String",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 2348
          },
          "name": "ast.Builtin_Markup_String",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Markup_String_Values",
            "req LRM.Builtin_Types"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Class"
        },
        {
          "tag": "python ast.Package.__init__",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 2379
          },
          "name": "ast.Package.__init__",
          "messages": [],
          "just_up": [
            "Constructor only declares variables"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "language": "Python",
          "kind": "Constructor"
        },
        {
          "tag": "python ast.Package.dump",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 2388
          },
          "name": "ast.Package.dump",
          "messages": [],
          "just_up": [
            "Debugging feature"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Composite_Type.__init__",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 2410
          },
          "name": "ast.Composite_Type.__init__",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Described_Name_Description"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Constructor"
        },
        {
          "tag": "python ast.Composite_Type.add_check",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 2426
          },
          "name": "ast.Composite_Type.add_check",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Check_Evaluation_Order"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Composite_Type.iter_checks",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 2431
          },
          "name": "ast.Composite_Type.iter_checks",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Check_Evaluation_Order"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Composite_Type.all_components",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 2435
          },
          "name": "ast.Composite_Type.all_components",
          "messages": [],
          "just_up": [
            "Convenience function"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Composite_Component.__init__",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 2466
          },
          "name": "ast.Composite_Component.__init__",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Described_Name_Description"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Constructor"
        },
        {
          "tag": "python ast.Composite_Component.dump",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 2482
          },
          "name": "ast.Composite_Component.dump",
          "messages": [],
          "just_up": [
            "Debugging feature"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Record_Type.__init__",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 2515
          },
          "name": "ast.Record_Type.__init__",
          "messages": [],
          "just_up": [
            "Constructor only declares variables"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "language": "Python",
          "kind": "Constructor"
        },
        {
          "tag": "python ast.Record_Type.iter_checks",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 2535
          },
          "name": "ast.Record_Type.iter_checks",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Check_Evaluation_Order_For_Extensions",
            "req LRM.Check_Evaluation_Order"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Record_Type.dump",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 2542
          },
          "name": "ast.Record_Type.dump",
          "messages": [],
          "just_up": [
            "Debugging feature"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Record_Type.all_components",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 2557
          },
          "name": "ast.Record_Type.all_components",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Record_Type.is_subclass_of",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 2568
          },
          "name": "ast.Record_Type.is_subclass_of",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Record_Type.is_frozen",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 2587
          },
          "name": "ast.Record_Type.is_frozen",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Record_Type.get_freezing_expression",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 2604
          },
          "name": "ast.Record_Type.get_freezing_expression",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Record_Type.get_example_value",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 2625
          },
          "name": "ast.Record_Type.get_example_value",
          "messages": [],
          "just_up": [
            "utility method"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Tuple_Type.__init__",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 2648
          },
          "name": "ast.Tuple_Type.__init__",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Tuple_Declaration"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Constructor"
        },
        {
          "tag": "python ast.Tuple_Type.add_separator",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 2656
          },
          "name": "ast.Tuple_Type.add_separator",
          "messages": [],
          "just_up": [
            "utility method"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Tuple_Type.iter_separators",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 2662
          },
          "name": "ast.Tuple_Type.iter_separators",
          "messages": [],
          "just_up": [
            "utility method"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Tuple_Type.iter_sequence",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 2667
          },
          "name": "ast.Tuple_Type.iter_sequence",
          "messages": [],
          "just_up": [
            "utility method"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Tuple_Type.has_separators",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 2678
          },
          "name": "ast.Tuple_Type.has_separators",
          "messages": [],
          "just_up": [
            "utility method"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Tuple_Type.dump",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 2683
          },
          "name": "ast.Tuple_Type.dump",
          "messages": [],
          "just_up": [
            "Debugging feature"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Tuple_Type.perform_type_checks",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 2698
          },
          "name": "ast.Tuple_Type.perform_type_checks",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Check_Evaluation_Order"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Tuple_Type.get_example_value",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 2711
          },
          "name": "ast.Tuple_Type.get_example_value",
          "messages": [],
          "just_up": [
            "utility method"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Separator",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 2725
          },
          "name": "ast.Separator",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Tuple_Declaration"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Class"
        },
        {
          "tag": "python ast.Enumeration_Type.__init__",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 2771
          },
          "name": "ast.Enumeration_Type.__init__",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Described_Name_Description"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Constructor"
        },
        {
          "tag": "python ast.Enumeration_Type.dump",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 2778
          },
          "name": "ast.Enumeration_Type.dump",
          "messages": [],
          "just_up": [
            "Debugging feature"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Enumeration_Type.get_example_value",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 2785
          },
          "name": "ast.Enumeration_Type.get_example_value",
          "messages": [],
          "just_up": [
            "utility method"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Enumeration_Literal_Spec.__init__",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 2810
          },
          "name": "ast.Enumeration_Literal_Spec.__init__",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Described_Name_Description"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Constructor"
        },
        {
          "tag": "python ast.Enumeration_Literal_Spec.dump",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 2817
          },
          "name": "ast.Enumeration_Literal_Spec.dump",
          "messages": [],
          "just_up": [
            "Debugging feature"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Record_Object.__init__",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 2860
          },
          "name": "ast.Record_Object.__init__",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Unspecified_Optional_Components",
            "req LRM.Section_Declaration"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Constructor"
        },
        {
          "tag": "python ast.Record_Object.fully_qualified_name",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 2874
          },
          "name": "ast.Record_Object.fully_qualified_name",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Record_Object.to_python_dict",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 2882
          },
          "name": "ast.Record_Object.to_python_dict",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Record_Object.assign",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 2898
          },
          "name": "ast.Record_Object.assign",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Record_Object.dump",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 2909
          },
          "name": "ast.Record_Object.dump",
          "messages": [],
          "just_up": [
            "Debugging feature"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Record_Object.resolve_references",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 2919
          },
          "name": "ast.Record_Object.resolve_references",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Record_Object.perform_checks",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 2924
          },
          "name": "ast.Record_Object.perform_checks",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Check_Evaluation_Order"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Section",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 2946
          },
          "name": "ast.Section",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Section_Declaration"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Class"
        },
        {
          "tag": "python ast.Symbol_Table.__init__",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 2982
          },
          "name": "ast.Symbol_Table.__init__",
          "messages": [],
          "just_up": [
            "Constructor only declares variables"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "language": "Python",
          "kind": "Constructor"
        },
        {
          "tag": "python ast.Symbol_Table.all_names",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 2989
          },
          "name": "ast.Symbol_Table.all_names",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Symbol_Table.iter_record_objects",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 2999
          },
          "name": "ast.Symbol_Table.iter_record_objects",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Symbol_Table.values",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 3011
          },
          "name": "ast.Symbol_Table.values",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Symbol_Table.make_visible",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 3019
          },
          "name": "ast.Symbol_Table.make_visible",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Symbol_Table.register",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 3023
          },
          "name": "ast.Symbol_Table.register",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Tuple_Unique_Field_Names",
            "req LRM.Unique_Enumeration_Literals",
            "req LRM.Duplicate_Types"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Symbol_Table.__contains__",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 3039
          },
          "name": "ast.Symbol_Table.__contains__",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Described_Name_Equality"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Symbol_Table.contains",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 3043
          },
          "name": "ast.Symbol_Table.contains",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Described_Name_Equality"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Symbol_Table.lookup_assuming",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 3063
          },
          "name": "ast.Symbol_Table.lookup_assuming",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Described_Name_Equality"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Symbol_Table.lookup_direct",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 3107
          },
          "name": "ast.Symbol_Table.lookup_direct",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Described_Name_Equality"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Symbol_Table.lookup",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 3184
          },
          "name": "ast.Symbol_Table.lookup",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Described_Name_Equality"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Symbol_Table.write_indent",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 3197
          },
          "name": "ast.Symbol_Table.write_indent",
          "messages": [],
          "just_up": [
            "Debugging feature"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Symbol_Table.dump",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 3204
          },
          "name": "ast.Symbol_Table.dump",
          "messages": [],
          "just_up": [
            "Debugging feature"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Symbol_Table.create_global_table",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 3218
          },
          "name": "ast.Symbol_Table.create_global_table",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Builtin_Type_Conversion_Functions",
            "req LRM.Builtin_Functions",
            "req LRM.Builtin_Types"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Scope.__init__",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 3243
          },
          "name": "ast.Scope.__init__",
          "messages": [],
          "just_up": [
            "Constructor only declares variables"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "language": "Python",
          "kind": "Constructor"
        },
        {
          "tag": "python ast.Scope.push",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 3247
          },
          "name": "ast.Scope.push",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Scope.pop",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 3251
          },
          "name": "ast.Scope.pop",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Scope.contains",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 3254
          },
          "name": "ast.Scope.contains",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Scope.lookup",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 3262
          },
          "name": "ast.Scope.lookup",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        },
        {
          "tag": "python ast.Scope.size",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "trlc/ast.py",
            "line": 3274
          },
          "name": "ast.Scope.size",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "language": "Python",
          "kind": "Method"
        }
      ],
      "coverage": 57.142857142857146
    },
    {
      "name": "Test",
      "kind": "activity",
      "items": [
        {
          "tag": "trlc-st checks-6",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-system/checks-6",
            "line": null
          },
          "name": "checks-6",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.No_Newlines_In_Message"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "TRLCST",
          "kind": "Test Directory",
          "status": null
        },
        {
          "tag": "trlc-st comments-1",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-system/comments-1",
            "line": null
          },
          "name": "comments-1",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Comments"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "TRLCST",
          "kind": "Test Directory",
          "status": null
        },
        {
          "tag": "trlc-st cross-refs-in-errors",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-system/cross-refs-in-errors",
            "line": null
          },
          "name": "cross-refs-in-errors",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Package_Declaration"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "TRLCST",
          "kind": "Test Directory",
          "status": null
        },
        {
          "tag": "trlc-st cyclic-packages",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-system/cyclic-packages",
            "line": null
          },
          "name": "cyclic-packages",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Circular_Dependencies"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "TRLCST",
          "kind": "Test Directory",
          "status": null
        },
        {
          "tag": "trlc-st decimal-1",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-system/decimal-1",
            "line": null
          },
          "name": "decimal-1",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Builtin_Type_Conversion_Functions"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "TRLCST",
          "kind": "Test Directory",
          "status": null
        },
        {
          "tag": "trlc-st decimal-5",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-system/decimal-5",
            "line": null
          },
          "name": "decimal-5",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Builtin_Type_Conversion_Functions"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "TRLCST",
          "kind": "Test Directory",
          "status": null
        },
        {
          "tag": "trlc-st delayed-references-1",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-system/delayed-references-1",
            "line": null
          },
          "name": "delayed-references-1",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Current_Package",
            "req LRM.File_Parsing_References",
            "req LRM.File_Parsing_Order"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "TRLCST",
          "kind": "Test Directory",
          "status": null
        },
        {
          "tag": "trlc-st enum",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-system/enum",
            "line": null
          },
          "name": "enum",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Enumeration_Declaration"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "TRLCST",
          "kind": "Test Directory",
          "status": null
        },
        {
          "tag": "trlc-st enum-ok",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-system/enum-ok",
            "line": null
          },
          "name": "enum-ok",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Enumeration_Declaration"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "TRLCST",
          "kind": "Test Directory",
          "status": null
        },
        {
          "tag": "trlc-st file-encoding-not-utf8",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-system/file-encoding-not-utf8",
            "line": null
          },
          "name": "file-encoding-not-utf8",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.File_Encoding_Fixed",
            "req LRM.File_Encoding"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "TRLCST",
          "kind": "Test Directory",
          "status": null
        },
        {
          "tag": "trlc-st lint-ambiguous-literals",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-system/lint-ambiguous-literals",
            "line": null
          },
          "name": "lint-ambiguous-literals",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Tuple_Based_Literal_Ambiguity"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "TRLCST",
          "kind": "Test Directory",
          "status": null
        },
        {
          "tag": "trlc-st lint-vcg-empty-enum",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-system/lint-vcg-empty-enum",
            "line": null
          },
          "name": "lint-vcg-empty-enum",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.No_Empty_Enumerations"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "TRLCST",
          "kind": "Test Directory",
          "status": null
        },
        {
          "tag": "trlc-st multiple-models",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-system/multiple-models",
            "line": null
          },
          "name": "multiple-models",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Import_Visibility"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "TRLCST",
          "kind": "Test Directory",
          "status": null
        },
        {
          "tag": "trlc-st preamble-1",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-system/preamble-1",
            "line": null
          },
          "name": "preamble-1",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Self_Imports",
            "req LRM.Preamble"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "TRLCST",
          "kind": "Test Directory",
          "status": null
        },
        {
          "tag": "trlc-st rbt-applicable-components",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-system/rbt-applicable-components",
            "line": null
          },
          "name": "rbt-applicable-components",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Applicable_Components"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "TRLCST",
          "kind": "Test Directory",
          "status": null
        },
        {
          "tag": "trlc-st rbt-applicable-types",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-system/rbt-applicable-types",
            "line": null
          },
          "name": "rbt-applicable-types",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Applicable_Types"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "TRLCST",
          "kind": "Test Directory",
          "status": null
        },
        {
          "tag": "trlc-st rbt-boolean-values",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-system/rbt-boolean-values",
            "line": null
          },
          "name": "rbt-boolean-values",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Boolean_Values"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "TRLCST",
          "kind": "Test Directory",
          "status": null
        },
        {
          "tag": "trlc-st rbt-builtin-functions",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-system/rbt-builtin-functions",
            "line": null
          },
          "name": "rbt-builtin-functions",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Builtin_Functions"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "TRLCST",
          "kind": "Test Directory",
          "status": null
        },
        {
          "tag": "trlc-st rbt-builtin-types",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-system/rbt-builtin-types",
            "line": null
          },
          "name": "rbt-builtin-types",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Builtin_Types"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "TRLCST",
          "kind": "Test Directory",
          "status": null
        },
        {
          "tag": "trlc-st rbt-cannot-declare-in-check-file",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-system/rbt-cannot-declare-in-check-file",
            "line": null
          },
          "name": "rbt-cannot-declare-in-check-file",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Cannot_Declare_In_Check_File"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "TRLCST",
          "kind": "Test Directory",
          "status": null
        },
        {
          "tag": "trlc-st rbt-check-evaluation-order",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-system/rbt-check-evaluation-order",
            "line": null
          },
          "name": "rbt-check-evaluation-order",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Check_Evaluation_Order"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "TRLCST",
          "kind": "Test Directory",
          "status": null
        },
        {
          "tag": "trlc-st rbt-check-evaluation-order-for-extensions",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-system/rbt-check-evaluation-order-for-extensions",
            "line": null
          },
          "name": "rbt-check-evaluation-order-for-extensions",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Check_Evaluation_Order_For_Extensions",
            "req LRM.Check_Messages"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "TRLCST",
          "kind": "Test Directory",
          "status": null
        },
        {
          "tag": "trlc-st rbt-check-severity-1",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-system/rbt-check-severity-1",
            "line": null
          },
          "name": "rbt-check-severity-1",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Check_Severity"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "TRLCST",
          "kind": "Test Directory",
          "status": null
        },
        {
          "tag": "trlc-st rbt-check-severity-2",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-system/rbt-check-severity-2",
            "line": null
          },
          "name": "rbt-check-severity-2",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Check_Severity"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "TRLCST",
          "kind": "Test Directory",
          "status": null
        },
        {
          "tag": "trlc-st rbt-check-severity-3",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-system/rbt-check-severity-3",
            "line": null
          },
          "name": "rbt-check-severity-3",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Check_Severity"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "TRLCST",
          "kind": "Test Directory",
          "status": null
        },
        {
          "tag": "trlc-st rbt-conditional-expression",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-system/rbt-conditional-expression",
            "line": null
          },
          "name": "rbt-conditional-expression",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Conditional_Expression",
            "req LRM.Conditional_Expression_Else",
            "req LRM.Conditional_Expression_Evaluation"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "TRLCST",
          "kind": "Test Directory",
          "status": null
        },
        {
          "tag": "trlc-st rbt-conditional-expression-types",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-system/rbt-conditional-expression-types",
            "line": null
          },
          "name": "rbt-conditional-expression-types",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Conditional_Expression_Types"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "TRLCST",
          "kind": "Test Directory",
          "status": null
        },
        {
          "tag": "trlc-st rbt-decimal-values",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-system/rbt-decimal-values",
            "line": null
          },
          "name": "rbt-decimal-values",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Decimal_Values"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "TRLCST",
          "kind": "Test Directory",
          "status": null
        },
        {
          "tag": "trlc-st rbt-described-name-equality",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-system/rbt-described-name-equality",
            "line": null
          },
          "name": "rbt-described-name-equality",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Described_Name_Equality"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "TRLCST",
          "kind": "Test Directory",
          "status": null
        },
        {
          "tag": "trlc-st rbt-described-names",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-system/rbt-described-names",
            "line": null
          },
          "name": "rbt-described-names",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Described_Names",
            "req LRM.Type_Declarations",
            "req LRM.Described_Name_Description"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "TRLCST",
          "kind": "Test Directory",
          "status": null
        },
        {
          "tag": "trlc-st rbt-duplicate-types",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-system/rbt-duplicate-types",
            "line": null
          },
          "name": "rbt-duplicate-types",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Duplicate_Types"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "TRLCST",
          "kind": "Test Directory",
          "status": null
        },
        {
          "tag": "trlc-st rbt-expression",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-system/rbt-expression",
            "line": null
          },
          "name": "rbt-expression",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Expression",
            "req LRM.Primary",
            "req LRM.Factor",
            "req LRM.Term",
            "req LRM.Simple_Expression",
            "req LRM.Relation"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "TRLCST",
          "kind": "Test Directory",
          "status": null
        },
        {
          "tag": "trlc-st rbt-import-in-check",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-system/rbt-import-in-check",
            "line": null
          },
          "name": "rbt-import-in-check",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Import_In_Check"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "TRLCST",
          "kind": "Test Directory",
          "status": null
        },
        {
          "tag": "trlc-st rbt-integer-values",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-system/rbt-integer-values",
            "line": null
          },
          "name": "rbt-integer-values",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Integer_Values"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "TRLCST",
          "kind": "Test Directory",
          "status": null
        },
        {
          "tag": "trlc-st rbt-late-package-declarations",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-system/rbt-late-package-declarations",
            "line": null
          },
          "name": "rbt-late-package-declarations",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Late_Package_Declarations",
            "req LRM.Duplicate_Late_Packages"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "TRLCST",
          "kind": "Test Directory",
          "status": null
        },
        {
          "tag": "trlc-st rbt-markup-string-values",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-system/rbt-markup-string-values",
            "line": null
          },
          "name": "rbt-markup-string-values",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Markup_String_Values"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "TRLCST",
          "kind": "Test Directory",
          "status": null
        },
        {
          "tag": "trlc-st rbt-qualified-name",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-system/rbt-qualified-name",
            "line": null
          },
          "name": "rbt-qualified-name",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Qualified_Name",
            "req LRM.Valid_Name",
            "req LRM.Valid_Qualifier"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "TRLCST",
          "kind": "Test Directory",
          "status": null
        },
        {
          "tag": "trlc-st rbt-restricted-null-1",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-system/rbt-restricted-null-1",
            "line": null
          },
          "name": "rbt-restricted-null-1",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Restricted_Null",
            "req LRM.Unspecified_Optional_Components",
            "req LRM.Null_Equivalence"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "TRLCST",
          "kind": "Test Directory",
          "status": null
        },
        {
          "tag": "trlc-st rbt-restricted-null-2",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-system/rbt-restricted-null-2",
            "line": null
          },
          "name": "rbt-restricted-null-2",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Restricted_Null",
            "req LRM.Null_Is_Invalid"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "TRLCST",
          "kind": "Test Directory",
          "status": null
        },
        {
          "tag": "trlc-st rbt-restricted-tuple-nesting-1",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-system/rbt-restricted-tuple-nesting-1",
            "line": null
          },
          "name": "rbt-restricted-tuple-nesting-1",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Restricted_Tuple_Nesting"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "TRLCST",
          "kind": "Test Directory",
          "status": null
        },
        {
          "tag": "trlc-st rbt-restricted-tuple-nesting-2",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-system/rbt-restricted-tuple-nesting-2",
            "line": null
          },
          "name": "rbt-restricted-tuple-nesting-2",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Restricted_Tuple_Nesting"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "TRLCST",
          "kind": "Test Directory",
          "status": null
        },
        {
          "tag": "trlc-st rbt-section-declaration",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-system/rbt-section-declaration",
            "line": null
          },
          "name": "rbt-section-declaration",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Section_Declaration"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "TRLCST",
          "kind": "Test Directory",
          "status": null
        },
        {
          "tag": "trlc-st rbt-string-values",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-system/rbt-string-values",
            "line": null
          },
          "name": "rbt-string-values",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.String_Values"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "TRLCST",
          "kind": "Test Directory",
          "status": null
        },
        {
          "tag": "trlc-st rbt-tuple-declaration",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-system/rbt-tuple-declaration",
            "line": null
          },
          "name": "rbt-tuple-declaration",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Tuple_Declaration"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "TRLCST",
          "kind": "Test Directory",
          "status": null
        },
        {
          "tag": "trlc-st rbt-tuple-field-types",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-system/rbt-tuple-field-types",
            "line": null
          },
          "name": "rbt-tuple-field-types",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Tuple_Field_Types"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "TRLCST",
          "kind": "Test Directory",
          "status": null
        },
        {
          "tag": "trlc-st rbt-tuple-optional-fields",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-system/rbt-tuple-optional-fields",
            "line": null
          },
          "name": "rbt-tuple-optional-fields",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Tuple_Optional_Fields"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "TRLCST",
          "kind": "Test Directory",
          "status": null
        },
        {
          "tag": "trlc-st rbt-tuple-optional-requires-separators",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-system/rbt-tuple-optional-requires-separators",
            "line": null
          },
          "name": "rbt-tuple-optional-requires-separators",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Tuple_Optional_Requires_Separators"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "TRLCST",
          "kind": "Test Directory",
          "status": null
        },
        {
          "tag": "trlc-st rbt-tuple-separators-all-or-none",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-system/rbt-tuple-separators-all-or-none",
            "line": null
          },
          "name": "rbt-tuple-separators-all-or-none",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Tuple_Separators_All_Or_None"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "TRLCST",
          "kind": "Test Directory",
          "status": null
        },
        {
          "tag": "trlc-st rbt-tuple-unique-field-names",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-system/rbt-tuple-unique-field-names",
            "line": null
          },
          "name": "rbt-tuple-unique-field-names",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Tuple_Unique_Field_Names"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "TRLCST",
          "kind": "Test Directory",
          "status": null
        },
        {
          "tag": "trlc-st rbt-unary-minus-parsing",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-system/rbt-unary-minus-parsing",
            "line": null
          },
          "name": "rbt-unary-minus-parsing",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Unary_Minus_Parsing"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "TRLCST",
          "kind": "Test Directory",
          "status": null
        },
        {
          "tag": "trlc-st rbt-unique-enumeration-literals",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-system/rbt-unique-enumeration-literals",
            "line": null
          },
          "name": "rbt-unique-enumeration-literals",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Unique_Enumeration_Literals"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "TRLCST",
          "kind": "Test Directory",
          "status": null
        },
        {
          "tag": "trlc-st simple",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-system/simple",
            "line": null
          },
          "name": "simple",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.TRLC_File",
            "req LRM.Check_Block",
            "req LRM.Deprecated_Check_Files",
            "req LRM.Check_File",
            "req LRM.RSL_File",
            "req LRM.Preamble",
            "req LRM.File_Parsing_Order",
            "req LRM.Layout"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "TRLCST",
          "kind": "Test Directory",
          "status": null
        },
        {
          "tag": "trlc-st visibility-1",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-system/visibility-1",
            "line": null
          },
          "name": "visibility-1",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Import_Visibility"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "TRLCST",
          "kind": "Test Directory",
          "status": null
        },
        {
          "tag": "trlc-st whitespace",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-system/whitespace",
            "line": null
          },
          "name": "whitespace",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Whitespace"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "TRLCST",
          "kind": "Test Directory",
          "status": null
        },
        {
          "tag": "pyunit test_lexer_base.Test_Lexer_Base.testIsAlpha",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-unit/test_lexer_base.py",
            "line": 43
          },
          "name": "test_lexer_base.Test_Lexer_Base.testIsAlpha",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "PyUnit",
          "kind": "Test",
          "status": null
        },
        {
          "tag": "pyunit test_lexer_base.Test_Lexer_Base.testIsDigit",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-unit/test_lexer_base.py",
            "line": 50
          },
          "name": "test_lexer_base.Test_Lexer_Base.testIsDigit",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "PyUnit",
          "kind": "Test",
          "status": null
        },
        {
          "tag": "pyunit test_lexer_base.Test_Lexer_Base.testIsAlnum",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-unit/test_lexer_base.py",
            "line": 57
          },
          "name": "test_lexer_base.Test_Lexer_Base.testIsAlnum",
          "messages": [
            "missing up reference"
          ],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "tracing_status": "MISSING",
          "framework": "PyUnit",
          "kind": "Test",
          "status": null
        },
        {
          "tag": "pyunit test_lexer.Test_Lexer.testIdentifiers1",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-unit/test_lexer.py",
            "line": 73
          },
          "name": "test_lexer.Test_Lexer.testIdentifiers1",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Integers",
            "req LRM.Identifier"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "PyUnit",
          "kind": "Test",
          "status": null
        },
        {
          "tag": "pyunit test_lexer.Test_Lexer.testIdentifiers2",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-unit/test_lexer.py",
            "line": 80
          },
          "name": "test_lexer.Test_Lexer.testIdentifiers2",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Identifier"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "PyUnit",
          "kind": "Test",
          "status": null
        },
        {
          "tag": "pyunit test_lexer.Test_Lexer.testIdentifiers3",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-unit/test_lexer.py",
            "line": 86
          },
          "name": "test_lexer.Test_Lexer.testIdentifiers3",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Identifier"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "PyUnit",
          "kind": "Test",
          "status": null
        },
        {
          "tag": "pyunit test_lexer.Test_Lexer.testKeywords",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-unit/test_lexer.py",
            "line": 92
          },
          "name": "test_lexer.Test_Lexer.testKeywords",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.TRLC_Keywords"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "PyUnit",
          "kind": "Test",
          "status": null
        },
        {
          "tag": "pyunit test_lexer.Test_Lexer.testPunctuationSingle",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-unit/test_lexer.py",
            "line": 132
          },
          "name": "test_lexer.Test_Lexer.testPunctuationSingle",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Single_Delimiters"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "PyUnit",
          "kind": "Test",
          "status": null
        },
        {
          "tag": "pyunit test_lexer.Test_Lexer.testPunctuationDouble",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-unit/test_lexer.py",
            "line": 163
          },
          "name": "test_lexer.Test_Lexer.testPunctuationDouble",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Lexing_Disambiguation",
            "req LRM.Double_Delimiters"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "PyUnit",
          "kind": "Test",
          "status": null
        },
        {
          "tag": "pyunit test_lexer.Test_Lexer.testIncompleteNEQ",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-unit/test_lexer.py",
            "line": 181
          },
          "name": "test_lexer.Test_Lexer.testIncompleteNEQ",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Double_Delimiters"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "PyUnit",
          "kind": "Test",
          "status": null
        },
        {
          "tag": "pyunit test_lexer.Test_Lexer.testIntegers1",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-unit/test_lexer.py",
            "line": 188
          },
          "name": "test_lexer.Test_Lexer.testIntegers1",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Integers"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "PyUnit",
          "kind": "Test",
          "status": null
        },
        {
          "tag": "pyunit test_lexer.Test_Lexer.testIntegers2",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-unit/test_lexer.py",
            "line": 196
          },
          "name": "test_lexer.Test_Lexer.testIntegers2",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Integers"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "PyUnit",
          "kind": "Test",
          "status": null
        },
        {
          "tag": "pyunit test_lexer.Test_Lexer.testIntegers3",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-unit/test_lexer.py",
            "line": 202
          },
          "name": "test_lexer.Test_Lexer.testIntegers3",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Integers"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "PyUnit",
          "kind": "Test",
          "status": null
        },
        {
          "tag": "pyunit test_lexer.Test_Lexer.testIntegers4",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-unit/test_lexer.py",
            "line": 209
          },
          "name": "test_lexer.Test_Lexer.testIntegers4",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Integers"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "PyUnit",
          "kind": "Test",
          "status": null
        },
        {
          "tag": "pyunit test_lexer.Test_Lexer.testDecimals1",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-unit/test_lexer.py",
            "line": 215
          },
          "name": "test_lexer.Test_Lexer.testDecimals1",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Decimals"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "PyUnit",
          "kind": "Test",
          "status": null
        },
        {
          "tag": "pyunit test_lexer.Test_Lexer.testDecimals2",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-unit/test_lexer.py",
            "line": 222
          },
          "name": "test_lexer.Test_Lexer.testDecimals2",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Decimals"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "PyUnit",
          "kind": "Test",
          "status": null
        },
        {
          "tag": "pyunit test_lexer.Test_Lexer.testDecimals3",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-unit/test_lexer.py",
            "line": 228
          },
          "name": "test_lexer.Test_Lexer.testDecimals3",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Decimals"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "PyUnit",
          "kind": "Test",
          "status": null
        },
        {
          "tag": "pyunit test_lexer.Test_Lexer.testStrings1",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-unit/test_lexer.py",
            "line": 234
          },
          "name": "test_lexer.Test_Lexer.testStrings1",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Simple_String_Value",
            "req LRM.Strings"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "PyUnit",
          "kind": "Test",
          "status": null
        },
        {
          "tag": "pyunit test_lexer.Test_Lexer.testStrings2",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-unit/test_lexer.py",
            "line": 247
          },
          "name": "test_lexer.Test_Lexer.testStrings2",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Complex_String_Value",
            "req LRM.Strings"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "PyUnit",
          "kind": "Test",
          "status": null
        },
        {
          "tag": "pyunit test_lexer.Test_Lexer.testStrings3",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-unit/test_lexer.py",
            "line": 260
          },
          "name": "test_lexer.Test_Lexer.testStrings3",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Strings"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "PyUnit",
          "kind": "Test",
          "status": null
        },
        {
          "tag": "pyunit test_lexer.Test_Lexer.testStrings4",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-unit/test_lexer.py",
            "line": 266
          },
          "name": "test_lexer.Test_Lexer.testStrings4",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Strings"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "PyUnit",
          "kind": "Test",
          "status": null
        },
        {
          "tag": "pyunit test_lexer.Test_Lexer.testStrings5",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-unit/test_lexer.py",
            "line": 272
          },
          "name": "test_lexer.Test_Lexer.testStrings5",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Strings"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "PyUnit",
          "kind": "Test",
          "status": null
        },
        {
          "tag": "pyunit test_lexer.Test_Lexer.testStrings6",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-unit/test_lexer.py",
            "line": 278
          },
          "name": "test_lexer.Test_Lexer.testStrings6",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Complex_String_Value",
            "req LRM.Strings"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "PyUnit",
          "kind": "Test",
          "status": null
        },
        {
          "tag": "pyunit test_lexer.Test_Lexer.testStrings7",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-unit/test_lexer.py",
            "line": 288
          },
          "name": "test_lexer.Test_Lexer.testStrings7",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Strings"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "PyUnit",
          "kind": "Test",
          "status": null
        },
        {
          "tag": "pyunit test_lexer.Test_Lexer.testComment",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-unit/test_lexer.py",
            "line": 294
          },
          "name": "test_lexer.Test_Lexer.testComment",
          "messages": [],
          "just_up": [],
          "just_down": [],
          "just_global": [],
          "ref_up": [
            "req LRM.Comments"
          ],
          "ref_down": [],
          "tracing_status": "OK",
          "framework": "PyUnit",
          "kind": "Test",
          "status": null
        },
        {
          "tag": "pyunit test_lexer.Test_Lexer.testLocation1",
          "location": {
            "kind": "github",
            "gh_root": "https://github.com/ankushsonare1/trlc",
            "commit": "main",
            "file": "tests-unit/test_lexer.py",
            "line": 300
          },
          "name": "test_lexer.Test_Lexer.testLocation1",
          "messages": [],
          "just_up": [
            "api functionality not used inside TRLC"
          ],
          "just_down": [],
          "just_global": [],
          "tracing_status": "JUSTIFIED",
          "framework": "PyUnit",
          "kind": "Test",
          "status": null
        }
      ],
      "coverage": 96.25
    }
  ],
  "policy": {
    "Specification": {
      "name": "Specification",
      "kind": "requirements",
      "traces": [],
      "source": [
        {
          "file": "requirements.lobster",
          "filters": [],
          "valid_status": []
        }
      ],
      "needs_tracing_up": false,
      "needs_tracing_down": true,
      "breakdown_requirements": [
        [
          "Code"
        ],
        [
          "Test"
        ]
      ]
    },
    "Code": {
      "name": "Code",
      "kind": "implementation",
      "traces": [
        "Specification"
      ],
      "source": [
        {
          "file": "code.lobster",
          "filters": []
        }
      ],
      "needs_tracing_up": true,
      "needs_tracing_down": false,
      "breakdown_requirements": []
    },
    "Test": {
      "name": "Test",
      "kind": "activity",
      "traces": [
        "Specification"
      ],
      "source": [
        {
          "file": "system-tests.lobster",
          "filters": []
        },
        {
          "file": "unit-tests.lobster",
          "filters": []
        }
      ],
      "needs_tracing_up": true,
      "needs_tracing_down": false,
      "breakdown_requirements": []
    }
  },
  "matrix": []
}