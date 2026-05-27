import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.conversational_interface import interpret_conversation
from core.nlp.domain_understanding import understand_domain
from core.persona_registry import get_persona, set_default_persona
from tools.email_tools import send_system_email
from tools.environment_config import save_environment_settings
from tools.event_tools import emit_event
from tools.live_environment_tools import get_live_location, get_live_weather


class AssistantConfigurationTests(unittest.TestCase):
    def test_natural_persona_address_rewrites_a_weather_question(self):
        request = interpret_conversation("Ada, what is the weather like in Colombo?")
        self.assertEqual(request.persona.name, "Ada")
        self.assertEqual(request.routed_text, "weather in Colombo")

    def test_specialists_can_be_addressed_or_selected_by_domain(self):
        request = interpret_conversation("Talk to Grace about a dangerous command")
        self.assertEqual(request.persona.name, "Grace")
        self.assertEqual(request.routed_text, "a dangerous command")
        self.assertEqual(understand_domain("help me improve this sales pitch").domain, "sales")
        self.assertEqual(get_persona(domain="sales").name, "Jordan")

    def test_everyday_requests_translate_to_existing_safe_routes(self):
        self.assertEqual(
            interpret_conversation("Ada, could you review main.py?").routed_text,
            "review file main.py",
        )
        self.assertEqual(
            interpret_conversation("Linus, can you check the repo status?").routed_text,
            "git status",
        )
        self.assertEqual(
            interpret_conversation("Alfred, notify me whenever something needs my attention").routed_text,
            "enable attention emails",
        )

    def test_default_persona_is_configurable(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "persona.json"
            with patch("core.persona_registry.CONFIG_FILE", path):
                self.assertTrue(set_default_persona("turing"))
                self.assertEqual(get_persona().name, "Turing")

    def test_only_attention_events_send_alert_email(self):
        with tempfile.TemporaryDirectory() as directory:
            event_path = Path(directory) / "events.log"
            settings_path = Path(directory) / "notifications.json"
            with patch("tools.event_tools.EVENT_LOG", event_path), \
                    patch("tools.notification_config.CONFIG_FILE", settings_path), \
                    patch("tools.event_tools.send_system_email") as mailer:
                emit_event("PROJECT_CONTEXT_SET", "Project selected", "A project was selected.")
                mailer.assert_not_called()
                emit_event("SECURITY_COMMAND_BLOCKED", "Blocked", "rm -rf", requires_attention=True)
                mailer.assert_called_once()
                self.assertEqual(
                    mailer.call_args.kwargs["to_email"],
                    "lkprofessionals234@gmail.com",
                )

    def test_system_email_honors_dry_run(self):
        with patch("tools.email_tools._smtp_config", return_value={
            "host": "smtp.gmail.com",
            "port": 587,
            "email": "configured@example.com",
            "password": "configured",
            "from_name": "JARVIS",
            "dry_run": True,
        }):
            result = send_system_email("person@example.com", "Attention", "Message")
        self.assertIn("dry run", result.lower())

    def test_weather_uses_configured_default_city(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "environment.json"
            with patch("tools.environment_config.CONFIG_FILE", path):
                save_environment_settings({"default_weather_city": "Colombo"})
                with patch("tools.live_environment_tools._geocode_city", return_value={
                    "latitude": 1,
                    "longitude": 2,
                    "place": "Colombo, Sri Lanka",
                }) as geocode, patch("tools.live_environment_tools._get_json", return_value={
                    "current": {},
                    "current_units": {},
                }):
                    report = get_live_weather()
                geocode.assert_called_once_with("Colombo")
        self.assertIn("Colombo, Sri Lanka", report)

    def test_ip_location_can_be_disabled(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "environment.json"
            with patch("tools.environment_config.CONFIG_FILE", path):
                save_environment_settings({"use_ip_location": False})
                with patch("tools.live_environment_tools._get_json") as lookup:
                    report = get_live_location()
                lookup.assert_not_called()
        self.assertIn("OFF", report)


if __name__ == "__main__":
    unittest.main()
