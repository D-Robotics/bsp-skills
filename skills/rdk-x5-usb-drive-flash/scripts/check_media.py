"""Check one raw full-image payload using the X5 SDK 2.0.0 public USB layout."""
import argparse
import hashlib
from pathlib import Path
import re
import sys

STEMS = {"sd": "sd_disk.img", "emmc": "emmc_disk.img", "nand": "nand_disk.img"}
MAX_PARTS = 32
FAT32_MAX_FILE = 2**32 - 1


def sha256(paths):
    result = hashlib.sha256()
    for path in paths:
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                result.update(chunk)
    return result.hexdigest()


def check(root, target, source):
    folder = root / "update_img"
    if folder.is_symlink() or not folder.is_dir():
        raise ValueError("Expected update_img/ under the supplied USB root")
    stem = STEMS[target]
    pattern = re.compile(re.escape(stem) + r"\.([0-9]+)")
    whole = None
    parts = {}
    for path in folder.iterdir():
        if path.is_symlink() or not path.is_file():
            raise ValueError(f"Unexpected non-regular entry: {path.name}")
        if not 0 < path.stat().st_size <= FAT32_MAX_FILE:
            raise ValueError(f"Invalid file size: {path.name}")
        if path.name == stem:
            whole = path
            continue
        match = pattern.fullmatch(path.name)
        if not match:
            raise ValueError(f"Unexpected file for single-target {target}: {path.name}")
        number = int(match[1])
        if number >= MAX_PARTS or number in parts:
            raise ValueError(f"Duplicate or out-of-range part number: {number}")
        parts[number] = path
    if whole is not None and parts:
        raise ValueError("Use one complete image OR its parts")
    if whole is not None:
        ordered = [whole]
    elif not parts or set(parts) != set(range(len(parts))):
        raise ValueError("Expected an image or consecutive parts starting with zero")
    else:
        ordered = [parts[i] for i in range(len(parts))]
    size = sum(p.stat().st_size for p in ordered)
    if source is None:
        return f"Layout only: {len(ordered)} file(s), {size} bytes; content not verified."
    if not source.is_file() or any(source.samefile(p) for p in ordered):
        raise ValueError("Provide a separate original raw image")
    if source.stat().st_size != size or sha256(ordered) != sha256([source]):
        raise ValueError("USB payload differs from the original image")
    return f"Verified {size} bytes against the original image for {target}."


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True, help="USB mount point or staging root")
    parser.add_argument("--target", required=True, choices=sorted(STEMS))
    parser.add_argument("--source-image", type=Path, help="Original raw image for size and SHA-256 comparison")
    args = parser.parse_args()
    try:
        print(check(args.root, args.target, args.source_image))
    except (OSError, ValueError) as exc:
        print(f"Check failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
