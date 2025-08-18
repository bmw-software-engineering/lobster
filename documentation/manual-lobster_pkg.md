# lobster-pkg

**lobster-pkg** is a tool for extracting tracing tags and activities from ECU-TEST `.pkg` files for use with the LOBSTER traceability framework.

## Features

- Parses `.pkg` files (or directories containing them) to extract traceability information.
- Supports both standard tracing tags and those found in `TRACE-ANALYSIS` blocks.
- Outputs results in a format compatible with LOBSTER.
- Handles misplaced or malformed trace tags with clear warnings.
