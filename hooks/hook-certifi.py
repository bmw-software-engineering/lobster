"""
PyInstaller hook for certifi.
Ensures that certifi's CA bundle is included in the PyInstaller bundle.
"""
from PyInstaller.utils.hooks import get_module_file_attribute
import os

# Get the certifi module root directory
certifi_root = os.path.dirname(get_module_file_attribute("certifi"))

# Include the entire certifi package
datas = [(certifi_root, "certifi")]
