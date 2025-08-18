""" Provide a fallback for non pip repos for requirement()
    If the repo does not have requirement(), we emulate it.
"""

load("@pip//:requirements.bzl", pip_requirement = "requirement")

_mapping = {
    "certifi": "@certifi//:lib",
    "flask": "@flask//:lib",
    "libcst": "@libcst//:lib",
    "markdown": "@markdown//:lib",
    "packaging": "@packaging//:lib",
    "pyyaml": "@pyyaml//:lib",
    "requests": "@requests//:lib",
    "selenium": "@selenium//:lib",
    "setuptools": "@setuptools//:lib",
    "trlc": "@trlc//:lib",
    "urllib3": "@urllib3//:lib",
    "webdriver-manager": "@webdriver_manager//:lib",
}

def requirement(requested):
    mapping = pip_requirement(requested)
    if mapping:
        return mapping
    if requested in _mapping:
        return _mapping[requested]
    return "<UNHANDLED MAPPING for '" + requested + "' in third_party/requirements.bzl>"
