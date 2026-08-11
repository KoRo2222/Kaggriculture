"""Build a deterministic Kaggriculture submission.tar.gz."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import tarfile
from pathlib import Path


def build(source: Path, output: Path) -> tuple[str, str]:
    payload = source.read_bytes()
    compile(payload, str(source), "exec")

    output.parent.mkdir(parents=True, exist_ok=True)
    raw = io.BytesIO()
    with gzip.GzipFile(fileobj=raw, mode="wb", filename="", mtime=0) as zipped:
        with tarfile.open(fileobj=zipped, mode="w") as archive:
            info = tarfile.TarInfo("main.py")
            info.size = len(payload)
            info.mode = 0o644
            info.mtime = 0
            info.uid = info.gid = 0
            info.uname = info.gname = ""
            archive.addfile(info, io.BytesIO(payload))
    output.write_bytes(raw.getvalue())

    with tarfile.open(output, "r:gz") as archive:
        assert archive.getnames() == ["main.py"]
        restored = archive.extractfile("main.py")
        assert restored is not None and restored.read() == payload

    return hashlib.sha256(payload).hexdigest(), hashlib.sha256(output.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=Path("main.py"))
    parser.add_argument(
        "--output", type=Path, default=Path("submissions/submission.tar.gz")
    )
    args = parser.parse_args()

    source_hash, archive_hash = build(args.source, args.output)
    print(f"source={args.source}")
    print(f"source_sha256={source_hash}")
    print(f"archive={args.output}")
    print(f"archive_sha256={archive_hash}")


if __name__ == "__main__":
    main()

