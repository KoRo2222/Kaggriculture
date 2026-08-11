from __future__ import annotations

import ast
import hashlib
import importlib.util
import tarfile
from pathlib import Path

from scripts.build_submission import build


ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / "main.py"
PUBLIC_HASH = "97e5de08ed8f43f7fd2c196dd943e13bb71278477fcdeaec8e0ad8f1357ac515"


def test_main_is_exact_public_baseline() -> None:
    assert hashlib.sha256(MAIN.read_bytes()).hexdigest() == PUBLIC_HASH


def test_agent_is_importable() -> None:
    ast.parse(MAIN.read_text(encoding="utf-8"))
    spec = importlib.util.spec_from_file_location("candidate_agent", MAIN)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert callable(module.agent)


def test_no_external_io_dependencies() -> None:
    source = MAIN.read_text(encoding="utf-8").lower()
    banned = ("requests", "urllib", "socket", "/kaggle/input", "open(", "subprocess")
    assert all(token not in source for token in banned)


def test_archive_contains_only_main(tmp_path: Path) -> None:
    output = tmp_path / "submission.tar.gz"
    build(MAIN, output)
    with tarfile.open(output, "r:gz") as archive:
        assert archive.getnames() == ["main.py"]

