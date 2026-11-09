"""Static YAML checks; the missing local custom component prevents a full firmware compile."""
import pathlib
import unittest
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]

class Loader(yaml.SafeLoader):
    pass

Loader.add_constructor("!secret", lambda loader, node: {"secret_reference": loader.construct_scalar(node)})

class FirmwareConfigTests(unittest.TestCase):
    def test_config_is_parseable_and_keeps_hardware(self):
        for name in ("QuietCool_v5.5_reference.yaml", "QuietCool_v5.6_candidate.yaml"):
            with self.subTest(name=name):
                doc = yaml.load((ROOT / "firmware" / name).read_text(), Loader=Loader)
                self.assertEqual(doc["esp32"]["board"], "ttgo-lora32-v21")
                self.assertEqual(doc["esphome"]["name"], "quietcool")
                self.assertEqual(doc["wifi"]["ap"]["ssid"], "QuietCool Fallback")
                self.assertEqual(doc["wifi"]["ap"]["password"]["secret_reference"], "quietcool_fallback_password")
                self.assertEqual(doc["web_server"]["auth"]["password"]["secret_reference"], "quietcool_web_password")
                self.assertEqual(doc["web_server"]["auth"]["username"]["secret_reference"], "quietcool_web_username")
                self.assertEqual(doc["external_components"][0]["source"]["path"], "quietcool-source/components")

    def test_candidate_settings(self):
        doc = yaml.load((ROOT / "firmware" / "QuietCool_v5.6_candidate.yaml").read_text(), Loader=Loader)
        self.assertEqual(doc["api"]["reboot_timeout"], "0s")
        self.assertEqual(doc["wifi"]["power_save_mode"], "NONE")

    def test_secrets_are_gitignored(self):
        self.assertIn("secrets.yaml", (ROOT / ".gitignore").read_text())
        self.assertFalse((ROOT / "secrets.yaml").exists())

if __name__ == "__main__":
    unittest.main()
