# Setup for Visual Studio Code

We recommend to use the following `.vscode/settings.json` if using Visual Studio Code:

```json
{
    "python.analysis.exclude": [
        "test_install*",
        ".git",
        "**/__pycache__",
        "packages"
    ],
    "python.analysis.include": [
        "lobster"
    ],
    "python.testing.unittestArgs": [
        "-v",
        "-s",
        ".",
        "-t",
        ".",
        "-p",
        "test_*.py"
    ],
    "python.testing.pytestEnabled": false,
    "python.testing.unittestEnabled": true
}
```
