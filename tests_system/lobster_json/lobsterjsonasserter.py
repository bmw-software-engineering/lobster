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

from tests_system.asserter import Asserter


# Setting this flag will tell unittest not to print tracebacks from this frame.
# This way our custom assertions will show the interesting line number from the caller
# frame, and not from this boring file.
__unittest = True


class LobsterJsonAsserter(Asserter):
    def assertStdOutNumAndFile(self, num_items: int, out_file: str):
        self.assertStdOutText(
            f"lobster-json: wrote {num_items} items to {out_file}\n"
        )
