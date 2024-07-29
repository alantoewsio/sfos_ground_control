""" SFOS Ground Control
Copyright 2024 Sophos Ltd.  All rights reserved.
Licensed under the Apache License, Version 2.0 (the "License"); you may not use this
file except in compliance with the License.You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed
to in writing, software distributed under the License is distributed on an "AS IS"
BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See
the License for the specific language governing permissions and limitations under the
License.
"""

from sfos.objects.service_address import ServiceAddress


def test_service_address_simple() -> None:
    t_host = "testhost"
    t_expected = "testhost:4444"
    t_address = ServiceAddress(hostname=t_host)

    assert t_address() == t_expected


def test_service_address_and_port() -> None:
    t_host = "testhost"
    t_port = 5555
    t_expected = "testhost:5555"
    t_address = ServiceAddress(hostname=t_host, port=t_port)

    assert t_address() == t_expected


def test_service_base_url() -> None:
    t_host = "testhost"
    t_port = 5555
    t_expected = "https://testhost:5555/"
    t_expected2 = "https://testhost:5555/webconsole/Controller"
    t_expected3 = "https://testhost:5555/webconsole/webpages/index.jsp"
    t_address = ServiceAddress(hostname=t_host, port=t_port)

    assert t_address.url_base == t_expected
    assert t_address.url_controller == t_expected2
    assert t_address.url_index_jsp == t_expected3
