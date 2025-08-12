`invalid_xml.pkg`: This XML file is invalid because the information Tag is not closed.

`misplaced_tags.pkg`: Only the first-level `<TsBlock>` under `<TESTSTEPS>`, and its direct `<TsBlock>` children, are allowed to contain lobster-trace: tags.
If a lobster-trace: tag is found in a `<TsBlock>` that is nested deeper (e.g., a grandchild or deeper), or in a `<TsBlock>` that is not a direct child of the first `<TsBlock>`, the exception is raised. This problem exists in line 63 of this file.

`misplaced_lobster_trace.pkg`: Line 12 of this file is the case.
There is a warning when a `<DESCRIPTION>` with lobster-trace exists under `<TRACE-ANALYSIS>`, such as:

- Nested deeper (e.g., inside a nested `<ANALYSISITEM>`)
- Not a direct child of the correct `<ANALYSISITEM>`
- Or in any other invalid location under `<TRACE-ANALYSIS>`

