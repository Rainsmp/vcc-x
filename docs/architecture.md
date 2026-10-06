# VCC-X Architecture

VCC-X follows a layered, verification-first design:

CLI / Discord / API -> Authentication -> Authorization -> Policy Engine -> Approval Engine -> Command Dispatcher -> Job Engine -> Workflow Engine -> State Engine -> Service Modules -> Linux / Docker / Pterodactyl / Cloudflare.

The control plane is intentionally separated from the data plane. The CLI never performs arbitrary privileged operations directly; instead, it submits work to a validated job and approval pipeline.
