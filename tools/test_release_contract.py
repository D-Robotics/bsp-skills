from pathlib import Path
import unittest
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


if __name__ == "__main__":
    unittest.main()
