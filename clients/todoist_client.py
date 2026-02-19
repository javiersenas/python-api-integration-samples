from __future__ import annotations

from typing import Any

import requests


class TodoistError(Exception):
    """Domain-specific exception for Todoist client errors."""


class TodoistClient:
    base_url = "https://api.todoist.com/api/v1"
    timeout_s = 15

    def __init__(self, api_token: str) -> None:
        self.api_token = api_token

    def _headers(self) -> dict[str, str]:
        token = (self.api_token or "").strip()
        if not token or token.startswith("REPLACE_"):
            raise TodoistError("Missing or placeholder TODOIST_API_TOKEN.")
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
    ) -> Any:
        url = f"{self.base_url}{path}"
        try:
            resp = requests.request(
                method=method,
                url=url,
                headers=self._headers(),
                params=params,
                json=json,
                timeout=self.timeout_s,
            )
        except requests.RequestException as exc:
            raise TodoistError(f"Network error: {exc}") from exc

        if resp.status_code >= 400:
            snippet = (resp.text or "").strip().replace("\n", " ")[:200]
            raise TodoistError(f"HTTP {resp.status_code} error: {snippet}")

        if resp.status_code == 204:
            return None

        try:
            return resp.json()
        except ValueError as exc:
            raise TodoistError("Invalid JSON response from Todoist API.") from exc

    def list_tasks(self, filter_query: str | None, limit: int = 10) -> list[dict[str, Any]]:
        if filter_query:
            data = self._request("GET", "/tasks/filter", params={"query": filter_query, "limit": limit})
        else:
            data = self._request("GET", "/tasks", params={"limit": limit})

        if isinstance(data, list):
            return data[:limit]
        if isinstance(data, dict):
            results = data.get("results")
            if isinstance(results, list):
                return results[:limit]
        return []

    def add_task(self, content: str, due_string: str | None = None) -> dict[str, Any]:
        payload: dict[str, Any] = {"content": content}
        if due_string:
            payload["due_string"] = due_string
        data = self._request("POST", "/tasks", json=payload)
        return data if isinstance(data, dict) else {}

    def close_task(self, task_id: str) -> None:
        self._request("POST", f"/tasks/{task_id}/close")
