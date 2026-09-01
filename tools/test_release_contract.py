from pathlib import Path
import unittest
import yaml
from tools import validate

ROOT = Path(__file__).resolve().parent.parent
SKILL_NAMES = (
    "bsp-env-setup", "bsp-source-sync", "bsp-image-build", "bsp-kernel-build",
    "bsp-deb-build", "bsp-bootloader-build", "bsp-rootfs-custom", "bsp-s-series",
)


class ReleaseContractTests(unittest.TestCase):
    def test_every_bsp_skill_uses_v1_release_frontmatter(self):
        for name in SKILL_NAMES:
            content = (ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
            frontmatter, _ = validate.parse_frontmatter(content)
            self.assertEqual(frontmatter["version"], "1.0.0", name)
            self.assertEqual(frontmatter["name"], name)
            self.assertTrue(frontmatter["description"], name)

    def test_published_release_notifies_hub_with_verified_payload(self):
        workflow_path = ROOT / ".github" / "workflows" / "notify-hub-release.yml"
        workflow = workflow_path.read_text(encoding="utf-8")
        document = yaml.load(workflow, Loader=yaml.BaseLoader)

        self.assertEqual(document["on"], {"release": {"types": ["published"]}})
        self.assertEqual(document["permissions"], {"contents": "read"})
        self.assertIn("rdk-component-release", workflow)
        self.assertIn("RDK_RELEASE_BOT_PRIVATE_KEY", workflow)
        self.assertIn("github.event.release.prerelease", workflow)
        self.assertIn("actions/create-github-app-token@v2", workflow)
        self.assertIn("repos/D-Robotics/rdk-skills/dispatches", workflow)
        self.assertIn("^[0-9a-fA-F]{40}$", workflow)

        expected_payload_fields = {
            "schema_version",
            "source_repo",
            "tag",
            "release_url",
            "target_sha",
            "published_at",
        }
        self.assertEqual(
            set(document["jobs"]["notify-hub"]["steps"][-1]["env"]),
            expected_payload_fields,
        )


if __name__ == "__main__":
    unittest.main()
