# LOBSTER - Lightweight Open BMW Software Traceability Evidence Report
# Copyright (C) 2025 Bayerische Motoren Werke Aktiengesellschaft (BMW AG)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with this program. If not, see
# <https://www.gnu.org/licenses/>.

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
