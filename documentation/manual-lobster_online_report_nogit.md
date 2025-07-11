# Turning File References into GitHub References
If you want to publish your LOBSTER report or send it to a colleague,
then most likely you wish that the report does not contain references to files on your
local system, but instead it shall use URLs to the files in the remote repository.
LOBSTER supports GitHub repositories.

There are two tools, `lobster-online-report` and `lobster-online-report-nogit`.
Both tools replace file references in a `*.lobster` file with GitHub references,
with the following difference:
- `lobster-online-report` calls `git` and extracts the necessary information like
  remote URL by itself,
- `lobster-online-report-nogit` does not call `git`, but the user provides the
  necessary information through command line arguments.

Depending on your CI environment one or the other tool mab be better suited.

Example on Windows:
```
> lobster-online-report-nogit --repo-root="C:\path\to\repository" --remote-url="https://github.com/bmw-software-engineering/lobster" --commit=af10137b15c98ab6ebde09f4b7fa4ae9e0931bac --out="C:\path\modified_report.lobster" "C:\path\original_report.lobster"
```

## API

There is also an API function that works similar:

```python
from lobster.tools.core.online_report_nogit.online_report_nogit import apply_github_urls
```