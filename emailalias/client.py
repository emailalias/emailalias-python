from typing import Any, Dict, List, Optional

import requests

from .errors import (
    AuthenticationError,
    EmailAliasError,
    NotFoundError,
    RateLimitError,
)

DEFAULT_BASE_URL = "https://emailalias.io"


class Client:
    """Synchronous client for the EmailAlias REST API.

    >>> from emailalias import Client
    >>> client = Client(api_key="ea_live_xxx")
    >>> client.list_aliases()
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = 30.0,
        session: Optional[requests.Session] = None,
    ):
        if not api_key:
            raise ValueError("api_key is required")
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._session = session or requests.Session()

    # ── Low-level transport ──────────────────────────────────────────────
    def _request(self, method: str, path: str, json: Any = None) -> Any:
        url = f"{self.base_url}{path}"
        res = self._session.request(
            method,
            url,
            json=json,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Accept": "application/json",
            },
            timeout=self.timeout,
        )

        if res.status_code == 204:
            return None

        try:
            body = res.json()
        except ValueError:
            body = {"detail": res.text}

        if not res.ok:
            detail = body.get("detail") if isinstance(body, dict) else None
            message = detail if isinstance(detail, str) else str(body)
            cls = {
                401: AuthenticationError,
                404: NotFoundError,
                429: RateLimitError,
            }.get(res.status_code, EmailAliasError)
            raise cls(message, status=res.status_code)

        return body

    # ── Aliases ───────────────────────────────────────────────────────────
    def list_aliases(self) -> List[Dict[str, Any]]:
        return self._request("GET", "/api/aliases")

    def create_alias(
        self,
        alias_type: str = "random",
        label: Optional[str] = None,
        domain: Optional[str] = None,
        destination_email: Optional[str] = None,
        custom_code: Optional[str] = None,
        tag: Optional[str] = None,
    ) -> Dict[str, Any]:
        body: Dict[str, Any] = {"alias_type": alias_type}
        if label is not None:
            body["label"] = label
        if domain is not None:
            body["domain"] = domain
        if destination_email is not None:
            body["destination_email"] = destination_email
        if custom_code is not None:
            body["custom_code"] = custom_code
        if tag is not None:
            body["tag"] = tag
        return self._request("POST", "/api/aliases", json=body)

    def update_alias(
        self,
        alias_id: str,
        *,
        active: Optional[bool] = None,
        label: Optional[str] = None,
    ) -> Dict[str, Any]:
        body: Dict[str, Any] = {}
        if active is not None:
            body["active"] = active
        if label is not None:
            body["label"] = label
        return self._request("PATCH", f"/api/aliases/{alias_id}", json=body)

    def delete_alias(self, alias_id: str) -> None:
        self._request("DELETE", f"/api/aliases/{alias_id}")

    def list_available_domains(self) -> List[Dict[str, Any]]:
        return self._request("GET", "/api/aliases/domains")

    # ── Destinations ──────────────────────────────────────────────────────
    def list_destinations(self) -> List[Dict[str, Any]]:
        return self._request("GET", "/api/destinations")

    def add_destination(self, email: str) -> Dict[str, Any]:
        return self._request("POST", "/api/destinations", json={"email": email})

    def resend_destination_verification(self, destination_id: str) -> Dict[str, Any]:
        return self._request("POST", f"/api/destinations/{destination_id}/resend")

    def delete_destination(self, destination_id: str) -> None:
        self._request("DELETE", f"/api/destinations/{destination_id}")

    # ── Send email ────────────────────────────────────────────────────────
    def send_email(
        self,
        alias_id: str,
        to_email: str,
        subject: str,
        body: str,
        html_body: Optional[str] = None,
    ) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "alias_id": alias_id,
            "to_email": to_email,
            "subject": subject,
            "body": body,
        }
        if html_body is not None:
            payload["html_body"] = html_body
        return self._request("POST", "/api/send-email", json=payload)

    # ── Custom Domains ────────────────────────────────────────────────────
    def list_domains(self) -> List[Dict[str, Any]]:
        return self._request("GET", "/api/domains")

    def add_domain(self, domain_name: str) -> Dict[str, Any]:
        return self._request("POST", "/api/domains", json={"domain_name": domain_name})

    def verify_domain(self, domain_id: str) -> Dict[str, Any]:
        return self._request("POST", f"/api/domains/{domain_id}/verify")

    def delete_domain(self, domain_id: str) -> None:
        self._request("DELETE", f"/api/domains/{domain_id}")

    # ── Analytics ─────────────────────────────────────────────────────────
    def get_dashboard_stats(self) -> Dict[str, Any]:
        return self._request("GET", "/api/analytics/dashboard")

    def list_logs(self, page: int = 1, per_page: int = 25) -> Dict[str, Any]:
        return self._request(
            "GET", f"/api/analytics/logs?page={page}&per_page={per_page}"
        )

    def list_exposure_events(
        self, page: int = 1, per_page: int = 25
    ) -> Dict[str, Any]:
        return self._request(
            "GET", f"/api/analytics/exposure?page={page}&per_page={per_page}"
        )
