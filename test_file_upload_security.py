import tempfile
import unittest
from pathlib import Path

from core.routes.security_routes import handle_security_routes
from tools.file_upload_security_tools import file_upload_security_checker, inspect_file_upload_security


class FileUploadSecurityTests(unittest.TestCase):
    def test_detects_public_php_upload_and_executable_allowlist(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "upload.php").write_text(
                "move_uploaded_file($tmp, 'public/uploads/' . $name);\n"
                "$allowed_extensions = ['jpg', 'php'];\n",
                encoding="utf-8",
            )
            _, findings, error = inspect_file_upload_security(root)
        self.assertIsNone(error)
        self.assertTrue(any(item.framework == "PHP" for item in findings))
        self.assertTrue(any(item.severity == "critical" for item in findings))

    def test_private_validated_storage_has_no_configured_indicator(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "upload.php").write_text(
                "$allowed_extensions = ['jpg', 'png'];\n$file->store('private/quarantine');\n",
                encoding="utf-8",
            )
            report = file_upload_security_checker(root)
        self.assertIn("Review points: 0", report)

    def test_route_exposes_phase_360_help(self):
        report = handle_security_routes("360 help", "360 help", "")
        self.assertIn("FILE UPLOAD SECURITY CHECKER COMMANDS - PHASE 360", report)


if __name__ == "__main__":
    unittest.main()
