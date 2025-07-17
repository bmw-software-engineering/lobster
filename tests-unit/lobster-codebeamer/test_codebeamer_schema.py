from pathlib import Path
from os.path import isfile, isdir
import unittest
from lobster.tools.codebeamer.codebeamer import (
    load_config,
    parse_config_data,
    update_authentication_parameters,
)
from lobster.tools.codebeamer.config import AuthenticationConfig


class CbConfigTest(unittest.TestCase):
    def setUp(self):
        self._real_netrc_file=Path(__file__).resolve().parents[0] / "test.netrc"
        self.assertTrue(
            isfile(self._real_netrc_file),
            f"Invalid test setup: netrc file {self._real_netrc_file} does not exist!",
        )

    def test_missing_config_file(self):
        """
        Tests that FileNotFoundError is raised if config file is missing.
        """
        missing_config_path = "missing-config.yaml"
        self.assertFalse(
            isfile(missing_config_path),
            "Invalid test setup: file must not exist!",
        )

        with self.assertRaises(FileNotFoundError):
            load_config(missing_config_path)

    def test_directory_given_as_config(self):
        """
        Tests that FileNotFoundError is raised if path is a directory instead of a file.
        """
        real_path = str(Path(__file__).parent)
        self.assertTrue(
            isdir(real_path),
            "Invalid test setup: path shall be a real directory!",
        )
        # Note: PermissionError is raised on Windows, IsADirectoryError on other OS
        with self.assertRaises((IsADirectoryError, PermissionError)):
            load_config(real_path)

    def test_missing_config_field(self):
        with self.assertRaises(KeyError) as context:
            parse_config_data(
                {
                    'root': 'https://example.com',
                    'schema': 'Requirement',
                }
            )
        self.assertIn(
            "Either import_tagged or import_query must be provided!",
            str(context.exception),
        )

    def test_unsupported_config_keys(self):
        with self.assertRaises(KeyError) as context:
            parse_config_data(
                {
                    "unsupported_key": "value",
                    "out": "trlc-config.conf",
                    "import_query": 8805855
                }
            )
        self.assertIn("Unsupported config keys", str(context.exception))

    def test_cb_config_without_credentials_no_netrc(self):
        for user in (None, "some-user"):
            with self.subTest(user=user):
                auth_config = AuthenticationConfig(
                    token=None,
                    user=user,
                    password=None,
                    root="https://server.abc",
                )
                with self.assertRaises(KeyError) as cm:
                    update_authentication_parameters(
                        auth_config,
                        netrc_path="file-does-not-exist.netrc",
                    )
                self.assertEqual(
                    cm.exception.args[0],
                    "Please add your token to the config file, "
                    "or use user and pass in the config file, "
                    "or configure credentials in the .netrc file.",
                )

    def test_cb_config_with_token(self):
        # Both subtests verify that the authentication data is not modified.
        # The second subtest uses a netrc file that does really exist, but since a token
        # is given the netrc file shall be ignored.
        for netrc_path in ("file-does-not-exist.netrc", self._real_netrc_file):
            with self.subTest(netrc_path=netrc_path):
                auth_config = AuthenticationConfig(
                    token="1234",
                    user=None,
                    password=None,
                    root="https://example.com",
                )
                update_authentication_parameters(auth_config, netrc_path)
                self.assertEqual(auth_config.token, "1234")
                self.assertIsNone(auth_config.user)
                self.assertIsNone(auth_config.password)

    def test_cb_config_with_user_pass(self):
        for netrc_path in ("file-does-not-exist.netrc", self._real_netrc_file):
            with self.subTest(netrc_path=netrc_path):
                auth_config = AuthenticationConfig(
                    token=None,
                    user="admin",
                    password="secret",
                    root="https://example.com",
                )
                update_authentication_parameters(auth_config, netrc_path)
                self.assertIsNone(auth_config.token)
                self.assertEqual(auth_config.user, "admin")
                self.assertEqual(auth_config.password, "secret")

    def test_cb_config_with_netrc(self):
        auth_config = AuthenticationConfig(
            token=None,
            user=None,
            password=None,
            root="https://example.com",
        )
        update_authentication_parameters(auth_config, netrc_path=self._real_netrc_file)
        self.assertEqual(auth_config.user, "the-user-name")
        self.assertEqual(auth_config.password, "the-password")
        self.assertIsNone(auth_config.token)

    def test_cb_config_with_netrc_and_sub_root(self):
        auth_config = AuthenticationConfig(
            token=None,
            user=None,
            password=None,
            root="https://example.com/cb",
        )
        update_authentication_parameters(auth_config, netrc_path=self._real_netrc_file)
        self.assertEqual(auth_config.user, "the-user-name")
        self.assertEqual(auth_config.password, "the-password")
        self.assertIsNone(auth_config.token)

    def test_cb_config_netrc_missing_machine_entry(self):
        auth_config = AuthenticationConfig(
            token=None,
            user=None,
            password=None,
            root="https://missingmachine.com/cb",
        )
        with self.assertRaises(KeyError) as context:
            update_authentication_parameters(
                auth_config,
                netrc_path=self._real_netrc_file,
            )

        self.assertIn("Error parsing .netrc file", str(context.exception))


if __name__ == "__main__":
    unittest.main()
