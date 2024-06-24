""" SFOS Ground Control
Copyright 2024 Sophos Ltd.  All rights reserved.
Licensed under the Apache License, Version 2.0 (the "License"); you may not use this
file except in compliance with the License.
You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software distributed under
the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing
permissions and limitations under the License.
"""

from argparse import ArgumentParser as _ap


def setup_report_arguments(parser: _ap) -> _ap:
    """_summary_

    Args:
        parser (_ap): _description_
    """
    help = "Name of report to run"
    parser.add_argument("report_name", nargs=1, help=help)
    return parser
