import unittest
from requests.auth import HTTPBasicAuth
from lobster.tools.codebeamer.bearer_auth import BearerAuth
from lobster.tools.codebeamer.codebeamer import get_authentication
from lobster.tools.codebeamer.config import AuthenticationConfig


class AuthenticationTest(unittest.TestCase):

    _USERS = [None, "Procyon"]
    _PASSWORDS = [None, "Andromeda"]

    def test_get_bearer_auth(self):
        # This test verifies that the bearer authentication always takes precedence over
        # basic authentication.

        for password in self._PASSWORDS:
            for user in self._USERS:
                with self.subTest(user=user, password=password):
                    cb_auth_conf=AuthenticationConfig(
                        token="local bubble",
                        user=None,
                        password=None,
                        root="milky way",
                    )
                    auth = get_authentication(cb_auth_conf)
                    self.assertIsInstance(auth, BearerAuth)

    def test_get_basic_auth(self):
        # This test verifies that the basic authentication is returned,
        # even if the user name and/or password are missing.

        for password in self._PASSWORDS:
            for user in self._USERS:
                with self.subTest(user=user, password=password):
                    cb_auth_conf=AuthenticationConfig(
                        token=None,
                        user=user,
                        password=password,
                        root="orion arm",
                    )
                    auth = get_authentication(cb_auth_conf)
                    self.assertIsInstance(auth, HTTPBasicAuth)


if __name__ == '__main__':
    unittest.main()
