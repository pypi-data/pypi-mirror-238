# Copyright 2021 EMBL - European Bioinformatics Institute
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import re


def are_all_elements_unique(elements):
    """Check if there are any repeated element in the list of elements. If yes return False otherwise return True."""
    unique_elements = set()
    for element in elements:
        if element in unique_elements:
            return False
        unique_elements.add(element)
    return True


def get_valid_filename(s):
    """Return string with characters not allowed in filenames replaced by underscore."""
    return re.sub(r'[^-.0-9a-zA-Z]+', '_', s)


def validate_aliases(aliases):
    """Checks that each alias remains unique when converted to a valid filename."""
    return len(set(get_valid_filename(s) for s in aliases)) == len(aliases)
