"""Regression tests for WebAdmin login response handling."""

from unittest.mock import Mock

from requests import Response

from sfos.objects import SfosResponse
from sfos.static import exceptions as _ex
from sfos.static.constants import AUTH_SUCCESS_MSG
from sfos.webadmin.connector import Connector


def _response(status: int, text: str) -> Response:
    response = Response()
    response.status_code = status
    response._content = text.encode("utf-8")
    response.encoding = "utf-8"
    return response


def _connector_with_login_responses(monkeypatch, auth, token) -> Connector:
    connector = Connector(
        hostname="192.0.2.1",
        username="admin",
        password="password",
    )
    requests = (Mock(name="auth_request"), Mock(name="token_request"))
    monkeypatch.setattr(connector, "_get_login_req_cmds", lambda: requests)
    monkeypatch.setattr(
        connector,
        "send_requests",
        lambda *args, **kwargs: [auth, token],
    )
    return connector


def test_sfos_response_preserves_http_error_response() -> None:
    response = _response(403, "Forbidden")

    result = SfosResponse(response=response, trace="test")

    assert result.success is False
    assert result.status_code == 403
    assert result.text == "Forbidden"
    assert result.response is response


def test_login_returns_error_for_http_error_session_page(monkeypatch) -> None:
    auth = SfosResponse(response=_response(200, AUTH_SUCCESS_MSG), trace="auth")
    token = SfosResponse(response=_response(403, ""), trace="token")
    connector = _connector_with_login_responses(monkeypatch, auth, token)

    result = connector.login()

    assert result.success is False
    assert isinstance(result.error, _ex.LoginError)
    assert result.status_code == 403
    assert result.response is token.response
    assert "HTTP 403" in result.text


def test_login_returns_error_for_empty_success_session_page(monkeypatch) -> None:
    auth = SfosResponse(response=_response(200, AUTH_SUCCESS_MSG), trace="auth")
    token = SfosResponse(response=_response(200, ""), trace="token")
    connector = _connector_with_login_responses(monkeypatch, auth, token)

    result = connector.login()

    assert result.success is False
    assert isinstance(result.error, _ex.LoginError)
    assert result.status_code == 200
    assert "empty response" in result.text
