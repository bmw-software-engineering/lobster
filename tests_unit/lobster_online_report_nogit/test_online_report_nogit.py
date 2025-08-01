from os import path
import os
from pathlib import Path
from unittest import TestCase
from urllib.parse import quote
from lobster.tools.core.online_report_nogit.online_report_nogit import (
    _file_ref_to_github_ref,
    RepoInfo,
)
from lobster.location import File_Reference, Github_Reference


class LobsterOnlineReportNogitTest(TestCase):
    def test_fake_file_conversion(self):
        """Test that a fake file reference can be converted to GitHub reference
        
           Also tests that the URL is built properly regardless of slashes
           at the end of the input strings.
        """

        local_root = path.join("path", "to")
        file_ref = File_Reference(
            filename=path.join(local_root, "Munich", "Dostlerstraße.werk"),
            line=123,
            column=20000000000000,
        )
        self.assertFalse(
            path.isfile(file_ref.filename) or path.isdir(file_ref.filename),
            "Invalid test setup! The path must not exist!",
        )
        repository_name = "seashell"
        gh_root = f"https://der.server.de/{repository_name}"
        for append_url_slash in ("/", ""):
            for append_path_slash in (os.sep, ""):
                repo_info = RepoInfo(
                    remote_url=f"{gh_root}{append_url_slash}",
                    root=f"{local_root}{append_path_slash}",
                    commit="the-commit-sha"
                )
                with self.subTest(f"{append_url_slash=}, {append_path_slash=}"):
                    result = _file_ref_to_github_ref(
                        file_ref=file_ref,
                        repo_info=repo_info,
                        paths_must_exist=False,
                    )
                    self.assertIsInstance(result, Github_Reference)
                    self.assertEqual(result.gh_root, gh_root)
                    self.assertEqual(result.gh_repo, repository_name)
                    self.assertEqual(result.commit, repo_info.commit)
                    self.assertEqual(result.line, file_ref.line)
                    escaped_char = quote("ß")
                    self.assertEqual(
                        result.filename,
                        f"Munich/Dostlerstra{escaped_char}e.werk",
                    )
                    self.assertEqual(
                        result.to_html(),
                        f'<a href="{gh_root}/blob/{repo_info.commit}/' \
                        f'Munich/Dostlerstra{escaped_char}e.werk#L{file_ref.line}" ' \
                        f'target="_blank">Munich/Dostlerstra{escaped_char}e.werk:' \
                        f'{file_ref.line}</a>',
                    )

    def test_real_file_conversion(self):
        """Test that a path reference of a truly existing path can be converted
           to GitHub reference

           The test is executed one with a file, and once with a directory.
           Each time the parameter 'paths_must_exist' is set to True.
        """

        # Run test on a) file and b) directory. For simplicity we use the current
        # file and its parent.
        for path_to_convert in (Path(__file__), Path(__file__).parent):
            with self.subTest(f"{path_to_convert=}"):
                file_ref = File_Reference(
                    filename=str(path_to_convert),
                    line=1,
                    column=2,
                )
                self.assertTrue(
                    path.isfile(file_ref.filename) or path.isdir(file_ref.filename),
                    "Invalid test setup! The path must exist!",
                )
                repository_name = "bluewhale"
                gh_root = f"https://the.other.server.org/{repository_name}"
                repo_info = RepoInfo(
                    remote_url=gh_root,
                    root=str(path_to_convert.parent),
                    commit="the-nice-guy"
                )
                result = _file_ref_to_github_ref(
                    file_ref=file_ref,
                    repo_info=repo_info,
                    paths_must_exist=True,
                )
                self.assertIsInstance(result, Github_Reference)
                self.assertEqual(result.gh_root, gh_root)
                self.assertEqual(result.gh_repo, repository_name)
                self.assertEqual(result.commit, repo_info.commit)
                self.assertEqual(result.line, file_ref.line)
                self.assertEqual(result.filename, path_to_convert.name,
                                 "filename mismatch")
                self.assertEqual(
                    result.to_html(),
                    f'<a href="{gh_root}/blob/{repo_info.commit}/' \
                    f'{path_to_convert.name}#L{file_ref.line}" target="_blank">' \
                    f'{path_to_convert.name}:{file_ref.line}</a>',
                    "HTML mismatch"
                )

    def test_error_on_missing_file(self):
        """Test that an exception is raised if the path does not exist"""
        file_ref = File_Reference(
            filename="does-not-exist",
            line=1,
            column=2,
        )
        self.assertFalse(
            path.isfile(file_ref.filename) or path.isdir(file_ref.filename),
            "Invalid test setup! The path must not exist!",
        )
        repo_info = RepoInfo(
            remote_url="http://abc.def.ghi",
            root=str(Path(__file__).parent),
            commit="the-bad-guy"
        )
        with self.assertRaises(FileNotFoundError):
            _file_ref_to_github_ref(
                file_ref=file_ref,
                repo_info=repo_info,
                paths_must_exist=True,
            )
