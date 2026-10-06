import json
import tempfile
import unittest
from pathlib import Path

from lib.config import ConfigManager
from lib.audit import AuditLogger
from lib.job_engine import JobEngine, Job
from lib.state_engine import StateEngine


class CoreTests(unittest.TestCase):
    def test_config_default_values(self):
        with tempfile.TemporaryDirectory() as tmp:
            cfg = ConfigManager(Path(tmp))
            self.assertEqual(cfg.get("controller.name"), "vcc-x")
            self.assertTrue(cfg.get("security.require_approval"))

    def test_audit_chain_and_event(self):
        with tempfile.TemporaryDirectory() as tmp:
            audit = AuditLogger(Path(tmp) / "audit.log")
            audit.record("server.online", {"server": "node-01"}, request_id="REQ-TEST")
            data = json.loads((Path(tmp) / "audit.log").read_text())
            self.assertEqual(data[0]["event"], "server.online")
            self.assertIn("hash", data[0])
            self.assertIn("previous_hash", data[0])

    def test_job_engine_execution(self):
        engine = JobEngine()
        job = Job(name="health-check", priority="HIGH", payload={"server": "node-01"})
        engine.submit(job)
        result = engine.run_next()
        self.assertEqual(result["status"], "completed")

    def test_state_reconciliation(self):
        state = StateEngine()
        state.set_desired("docker", "running")
        state.set_observed("docker", "stopped")
        self.assertTrue(state.is_drifted("docker"))
        self.assertEqual(state.reconcile("docker")["status"], "drift")


if __name__ == "__main__":
    unittest.main()
