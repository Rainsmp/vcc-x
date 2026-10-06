DEFAULT_CONFIG = {
    "controller": {
        "name": "vcc-x",
        "environment": "production",
        "api_port": 8080,
    },
    "security": {
        "require_approval": True,
        "require_two_person_approval": True,
        "audit_hash_chain": True,
        "redact_secrets": True,
    },
    "fleet": {
        "default_roles": ["GENERAL"],
    },
    "operations": {
        "max_parallel_jobs": 4,
        "max_retries": 3,
    },
}
