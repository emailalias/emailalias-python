# emailalias-python

Official Python client for the [EmailAlias.io](https://emailalias.io) REST API.

API access is a **Premium** feature. Generate a key from **Settings → API Keys** in the web dashboard.

## Install

```bash
pip install emailalias
```

Or from source:

```bash
pip install git+https://github.com/emailalias/emailalias-python.git
```

## Quick start

```python
from emailalias import Client

client = Client(api_key="ea_live_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

# Create an alias
alias = client.create_alias(alias_type="random", label="Shopping")
print(alias["alias_email"])   # e.g. "x7k9m@email91.com"

# List aliases
for a in client.list_aliases():
    print(a["alias_email"], "→", a["destination_email"])

# Forward to a verified additional destination
alias = client.create_alias(
    alias_type="custom",
    custom_code="work-signup",
    label="Work",
    destination_email="work@mycompany.com",  # must be verified on your account first
)

# Send email from an alias
client.send_email(
    alias_id=alias["id"],
    to_email="recipient@example.com",
    subject="Hello",
    body="Sent from my alias.",
)

# Disable an alias
client.update_alias(alias_id=alias["id"], active=False)
```

## Error handling

```python
from emailalias import Client, AuthenticationError, RateLimitError

client = Client(api_key="ea_live_xxx")
try:
    client.list_aliases()
except AuthenticationError:
    # Invalid key, or account is no longer Premium
    ...
except RateLimitError:
    # Respect X-RateLimit-Reset and retry
    ...
```

## Configuration

```python
client = Client(
    api_key="ea_live_xxx",
    base_url="https://api.emailalias.io",  # override for staging/self-host
    timeout=30.0,
)
```

## Available methods

| Method | Endpoint |
|---|---|
| `list_aliases()` | `GET /api/aliases` |
| `create_alias(...)` | `POST /api/aliases` |
| `update_alias(id, active=, label=)` | `PATCH /api/aliases/{id}` |
| `delete_alias(id)` | `DELETE /api/aliases/{id}` |
| `list_available_domains()` | `GET /api/aliases/domains` |
| `list_destinations()` | `GET /api/destinations` |
| `add_destination(email)` | `POST /api/destinations` |
| `resend_destination_verification(id)` | `POST /api/destinations/{id}/resend` |
| `delete_destination(id)` | `DELETE /api/destinations/{id}` |
| `send_email(alias_id, to_email, subject, body, html_body=)` | `POST /api/send-email` |
| `list_domains()` | `GET /api/domains` |
| `add_domain(name)` | `POST /api/domains` |
| `verify_domain(id)` | `POST /api/domains/{id}/verify` |
| `delete_domain(id)` | `DELETE /api/domains/{id}` |
| `get_dashboard_stats()` | `GET /api/analytics/dashboard` |
| `list_logs(page=, per_page=)` | `GET /api/analytics/logs` |
| `list_exposure_events(page=, per_page=)` | `GET /api/analytics/exposure` |

Full API reference: <https://emailalias.io/documentation>

## License

MIT
