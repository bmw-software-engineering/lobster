from os import path
import os
from unittest import TestCase
from urllib.parse import quote
from lobster.tools.core.online_report_nogit.online_report_nogit import _file_ref_to_github_ref, RepoInfo
from lobster.location import File_Reference, Github_Reference


class LobsterOnlineReportNogitTest(TestCase):
    def test_fake_path_conversion(self):
        """Test that fake file reference can be converted to GitHub reference"""

        local_root = path.join("path", "to")
        file_ref = File_Reference(
            filename=path.join(local_root, "Munich", "Dostlerstraße.werk"),
            line=123,
            column=20000000000000,
        )
        self.assertFalse(
            path.isfile(file_ref.filename) or path.isdir(file_ref.filename),
            "Invalid test setup! The file must not exist!",
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
                    self.assertEqual(result.filename, f"Munich/Dostlerstra{escaped_char}e.werk")
                    self.assertEqual(
                        result.to_html(),
                        f'<a href="https://der.server.de/seashell/blob/the-commit-sha/' \
                        f'Munich/Dostlerstra{escaped_char}e.werk#L123" target="_blank">' \
                        f'Munich/Dostlerstra{escaped_char}e.werk:123</a>',
                    )
