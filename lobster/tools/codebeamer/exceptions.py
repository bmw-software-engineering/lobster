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

class QueryException(Exception):
    """This exception is raised when a query to the Codebeamer API fails."""


class NotFileException(Exception):
    """This exception is raised when a file is expected but the path does not point to
       a file.
    """


class MismatchException(Exception):
    """This exception is raised when there is a mismatch in the data retrieved from a
       codebeamer api call.
       For example, query page 7 has been requested, but the response data indicates
       page 8.
    """
