from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict

from config.defaults import DEFAULT_CONFIG


class ConfigManager:
    """Load, validate, and persist configuration for VCC-X."""

    def __init__(self, base_dir: str | Path | None = None):
        self.base_dir = Path(base_dir) if base_dir else Path(__file__).resolve().parents[1]
        self.config_path = self.base_dir / "config" / "vcc.json"
        self._config: Dict[str, Any] = deepcopy(DEFAULT_CONFIG)
        self._load()

    def _load(self) -> None:
        if self.config_path.exists():
            with self.config_path.open("r", encoding="utf-8") as handle:
                loaded = json.load(handle)
            self._merge(self._config, loaded)

    @staticmethod
    def _merge(target: Dict[str, Any], source: Dict[str, Any]) -> None:
        for key, value in source.items():
            if isinstance(value, dict) and isinstance(target.get(key), dict):
                ConfigManager._merge(target[key], value)
            else:
                target[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        cursor: Any = self._config
        for part in key.split("."):
            if not isinstance(cursor, dict) or part not in cursor:
                return default
            cursor = cursor[part]
        return cursor

    def set(self, key: str, value: Any) -> None:
        nodes = key.split(".")
        cursor = self._config
        for node in nodes[:-1]:
            if node not in cursor or not isinstance(cursor[node], dict):
                cursor[node] = {}
            cursor = cursor[node]
        cursor[nodes[-1]] = value

    def save(self) -> None:
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with self.config_path.open("w", encoding="utf-8") as handle:
            json.dump(self._config, handle, indent=2, sort_keys=True)
            handle.write("\n")

    def as_dict(self) -> Dict[str, Any]:
        return deepcopy(self._config)
