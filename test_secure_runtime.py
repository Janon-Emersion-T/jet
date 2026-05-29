import json
import os
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.routes.ai_operations_routes import handle_ai_operations_routes
from tools.secure_runtime_tools import (
    encrypted_memory_storage,
    local_secrets_manager,
    offline_first_operation_mode,
    push_notification_system,
    secure_vault_integration,
    sync_engine_between_devices,
)


class SecureRuntimeTests(unittest.TestCase):
    def test_encrypted_memory_storage_reports_key_and_counts(self):
        with tempfile.TemporaryDirectory() as directory:
            storage = Path(directory)
            memory_db = storage / "memory.db"
            vector_meta = storage / "vector_memory.json"
            conn = sqlite3.connect(memory_db)
            try:
                conn.execute("CREATE TABLE memory (id INTEGER PRIMARY KEY, user_input TEXT, jarvis_response TEXT, created_at TEXT)")
                conn.execute("INSERT INTO memory (user_input, jarvis_response, created_at) VALUES ('hi', 'hello', 'now')")
                conn.commit()
            finally:
                conn.close()
            vector_meta.write_text(json.dumps([{"id": "a", "active": True}, {"id": "b", "active": False}]), encoding="utf-8")
            with patch("tools.secure_runtime_tools.MEMORY_DB", memory_db), \
                    patch("tools.secure_runtime_tools.VECTOR_META", vector_meta), \
                    patch.dict(os.environ, {"JARVIS_MEMORY_KEY": "configured-key"}, clear=False):
                report = encrypted_memory_storage()
        self.assertIn("SQLite conversation rows: 1", report)
        self.assertIn("Vector memory rows: 1", report)
        self.assertIn("Encryption key configured: YES", report)

    def test_vault_sync_and_local_secrets_render(self):
        with tempfile.TemporaryDirectory() as directory:
            storage = Path(directory)
            sync_queue = storage / "queue.json"
            secrets_file = storage / "local_secrets.json"
            sync_queue.write_text(json.dumps({"pending": [{"type": "memory_export"}]}), encoding="utf-8")
            secrets_file.write_text(json.dumps({"items": [{"name": "SMTP_PASSWORD"}]}), encoding="utf-8")
            with patch("tools.secure_runtime_tools.SYNC_QUEUE", sync_queue), \
                    patch("tools.secure_runtime_tools.LOCAL_SECRETS", secrets_file), \
                    patch.dict(os.environ, {"VAULT_ADDR": "http://vault.local", "VAULT_TOKEN": "token"}, clear=False):
                vault = secure_vault_integration()
                sync = sync_engine_between_devices()
                secrets = local_secrets_manager()
        self.assertIn("Backend: hashicorp_vault", vault)
        self.assertIn("Pending sync items: 1", sync)
        self.assertIn("Tracked secret entries: 1", secrets)
        self.assertIn("SMTP_PASSWORD", secrets)

    def test_offline_and_push_render(self):
        with patch.dict(
            os.environ,
            {
                "HF_HUB_OFFLINE": "1",
                "TRANSFORMERS_OFFLINE": "true",
                "NTFY_TOPIC": "jarvis-alerts",
            },
            clear=False,
        ), patch(
            "tools.secure_runtime_tools.load_notification_settings",
            return_value={"attention_email": "lkprofessionals234@gmail.com", "email_attention_events": True},
        ):
            offline = offline_first_operation_mode()
            push = push_notification_system()
        self.assertIn("HF_HUB_OFFLINE", offline)
        self.assertIn("Push provider: ntfy", push)

    def test_routes_cover_421_to_430(self):
        for phase in range(421, 431):
            result = handle_ai_operations_routes(f"{phase} help", f"{phase} help", f"{phase} help")
            self.assertIsNotNone(result, f"missing route for {phase}")


if __name__ == "__main__":
    unittest.main()
