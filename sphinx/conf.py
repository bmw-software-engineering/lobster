# Minimal Sphinx configuration for the lobster project
import os
import sys
from datetime import datetime

# Ensure project root is on sys.path so autodoc can import lobster.*
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

project = "lobster"
author = "BMW Software Engineering"
copyright = f"{datetime.now().year}, {author}"

# General configuration
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",  # Google/NumPy style docstrings (optional)
]

# Source file parsers and suffixes
source_suffix = {
    ".rst": "restructuredtext",
}

# The master toctree document
master_doc = "index"

# Autodoc settings
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
}

# HTML output options
html_theme = "alabaster"
html_theme_options = {
    "description": "Traceability tooling APIs for requirements, code, tests, and reports",
    "sidebar_width": "250px",
    "page_width": "1080px",
    "fixed_sidebar": True,
    "font_family": "Segoe UI, Roboto, Helvetica, Arial, sans-serif",
    "head_font_family": "Segoe UI, Roboto, Helvetica, Arial, sans-serif",
}

# Syntax highlighting & HTML polish
pygments_style = "friendly"
html_static_path = ["_static"]
html_css_files = ["custom.css"]

# Prevent cluttered sidebars (focus on pages, not every symbol)
toc_object_entries = False
