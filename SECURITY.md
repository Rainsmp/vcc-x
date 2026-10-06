# Security Policy

## Security principles

- Treat infrastructure as untrusted until verified.
- Require approval for high-risk actions.
- Prefer explicit policies over implicit decisions.
- Preserve audit evidence and immutable event history.
- Redact secrets from logs and Discord output.
- Validate signatures and request metadata before privileged execution.

## Supported safeguards

- Request IDs propagated through CLI, jobs, API, and audit logs.
- Policy evaluation before execution.
- Audit hash chaining for tamper detection.
- Job queue and bounded retries.
- Secret redaction for tokens, passwords, and authorization headers.

## Reporting

Report security issues privately and include the exact environment, impacted systems, and reproduction steps.
