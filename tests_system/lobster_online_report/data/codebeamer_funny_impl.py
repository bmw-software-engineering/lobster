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

"""
Funny implementation satisfying 4 codebeamer requirements
LOBSTER traces: 1@100, 2@200, 3@300, 4@400
"""


def translate_dog_barking():
    # lobster-trace: 1@100
    """Requirement 1: Decode what dogs are really saying"""
    return "Translation: 'I saw a squirrel 3 hours ago and I'm still excited!'"


def organize_cloud_shapes():
    # lobster-trace: 2@200
    """Requirement 2: Categorize clouds by their resemblance to food"""
    return "Classified 5 clouds: 2 hamburgers, 1 donut, 1 taco, 1 pizza slice!"


def schedule_cat_meetings():
    # lobster-trace: 3@300
    """Requirement 3: Coordinate neighborhood cat business meetings"""
    return "Meeting at 3 AM under the oak tree. Agenda:"
