from __future__ import annotations

from unittest.mock import Mock, patch

import pytest

from clients.todoist_client import TodoistClient, TodoistError


def test_headers_raises_when_token_is_placeholder() -> None:
    client = TodoistClient(api_token="REPLACE_WITH_TOKEN")
    with pytest.raises(TodoistError):
        client._headers()


@patch("clients.todoist_client.requests.request")
def test_add_task_posts_expected_payload(mock_request: Mock) -> None:
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"id": "123", "content": "Test task"}
    mock_response.text = ""
    mock_request.return_value = mock_response

    client = TodoistClient(api_token="real_token_123")
    result = client.add_task("Test task")

    assert result["id"] == "123"
    mock_request.assert_called_once_with(
        method="POST",
        url="https://api.todoist.com/api/v1/tasks",
        headers={
            "Authorization": "Bearer real_token_123",
            "Content-Type": "application/json",
        },
        params=None,
        json={"content": "Test task"},
        timeout=15,
    )


@patch("clients.todoist_client.requests.request")
def test_close_task_uses_close_endpoint_and_handles_204(mock_request: Mock) -> None:
    mock_response = Mock()
    mock_response.status_code = 204
    mock_response.text = ""
    mock_request.return_value = mock_response

    client = TodoistClient(api_token="real_token_123")
    result = client.close_task("abc123")

    assert result is None
    mock_request.assert_called_once_with(
        method="POST",
        url="https://api.todoist.com/api/v1/tasks/abc123/close",
        headers={
            "Authorization": "Bearer real_token_123",
            "Content-Type": "application/json",
        },
        params=None,
        json=None,
        timeout=15,
    )
