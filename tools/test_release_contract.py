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
        app_token_action = (
            "actions/create-github-app-token@"
            "fee1f7d63c2ff003460e3d139729b119787bc349"
        )

        self.assertEqual(document["on"], {"release": {"types": ["published"]}})
        self.assertEqual(document["permissions"], {"contents": "read"})
        self.assertIn("RDK_RELEASE_DISPATCHER_PRIVATE_KEY", workflow)
        self.assertIn("github.event.release.prerelease", workflow)
        self.assertEqual(
            [
                step["uses"]
                for step in document["jobs"]["notify-hub"]["steps"]
                if "uses" in step
            ],
            [app_token_action],
        )
        self.assertIn(
            "repos/D-Robotics/rdk-skills/actions/workflows/component-upgrade.yml/dispatches",
            workflow,
        )
        self.assertIn("^[0-9a-fA-F]{40}$", workflow)

        token_step = next(
            step
            for step in document["jobs"]["notify-hub"]["steps"]
            if step.get("uses") == app_token_action
        )
        self.assertEqual(
            token_step["with"]["app-id"],
            "${{ vars.RDK_RELEASE_DISPATCHER_APP_ID }}",
        )
        self.assertEqual(
            token_step["with"]["private-key"],
            "${{ secrets.RDK_RELEASE_DISPATCHER_PRIVATE_KEY }}",
        )
        self.assertEqual(token_step["with"]["permission-actions"], "write")
        self.assertNotIn("permission-contents", token_step["with"])

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
