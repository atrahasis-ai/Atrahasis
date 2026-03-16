from __future__ import annotations

import shutil
import sys
import unittest
import uuid
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from aas5.spec_path_resolver import resolve_spec_path, resolve_spec_ref


class SpecPathResolverTests(unittest.TestCase):
    def setUp(self) -> None:
        temp_parent = Path.home() / ".codex" / "memories" / "spec_path_tests"
        temp_parent.mkdir(parents=True, exist_ok=True)
        self.tempdir = temp_parent / f"localtmp_spec_path_{uuid.uuid4().hex}"
        self.repo_root = self.tempdir / "Atrahasis-Agent-System"
        specs_root = self.repo_root / "docs" / "specifications"
        specs_root.mkdir(parents=True, exist_ok=True)

        c42_dir = specs_root / "C42 - Lease-Primed Execution Mesh"
        c42_dir.mkdir(parents=True, exist_ok=True)
        (c42_dir / "C42_Lease-Primed_Execution_Mesh_Master_Tech_Spec.md").write_text(
            "# C42\n", encoding="utf-8"
        )

        c45_dir = specs_root / "C45 - AACP Sovereign Compiler Framework"
        c45_dir.mkdir(parents=True, exist_ok=True)
        (c45_dir / "MASTER_TECH_SPEC.md").write_text("# C45\n", encoding="utf-8")

    def tearDown(self) -> None:
        shutil.rmtree(self.tempdir, ignore_errors=True)

    def test_resolve_spec_path_finds_titled_master_spec(self) -> None:
        resolved = resolve_spec_path(self.repo_root, "C42")
        self.assertEqual(
            str(resolved.relative_to(self.repo_root)).replace("\\", "/"),
            "docs/specifications/C42 - Lease-Primed Execution Mesh/C42_Lease-Primed_Execution_Mesh_Master_Tech_Spec.md",
        )

    def test_resolve_spec_ref_prefers_master_tech_spec_shortcut_when_present(self) -> None:
        resolved = resolve_spec_ref(self.repo_root, "C45")
        self.assertEqual(
            resolved,
            "docs/specifications/C45 - AACP Sovereign Compiler Framework/MASTER_TECH_SPEC.md",
        )


if __name__ == "__main__":
    unittest.main()
