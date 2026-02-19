load("//bazel:providers.bzl", _LobsterProvider = "LobsterProvider")
load("//bazel/private:lobster_test.bzl", _lobster_test = "lobster_test")
load("//bazel/private:lobster_trlc.bzl", _lobster_trlc = "lobster_trlc")
load("//bazel/private:lobster_raw.bzl", _lobster_raw = "lobster_raw")
load("//bazel/private:lobster_gtest.bzl", _lobster_gtest = "lobster_gtest")

# Re-export LobsterProvider so it can be loaded from this file
LobsterProvider = _LobsterProvider

def lobster_test(**kwargs):
    _lobster_test(**kwargs)

def lobster_trlc(**kwargs):
    _lobster_trlc(**kwargs)

def lobster_raw(**kwargs):
    _lobster_raw(**kwargs)

def lobster_gtest(**kwargs):
    _lobster_gtest(**kwargs)