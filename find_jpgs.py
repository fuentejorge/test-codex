import argparse
import ctypes
import os
import sys
from typing import Iterable, Iterator, Tuple


def get_logical_drives() -> Iterable[str]:
    bitmask = ctypes.windll.kernel32.GetLogicalDrives()
    for i in range(26):
        if bitmask & (1 << i):
            yield f"{chr(65 + i)}:\\"


def iter_image_files(roots: Iterable[str], include_jpeg: bool) -> Iterator[Tuple[str, str, int]]:
    extensions = {".jpg"}
    if include_jpeg:
        extensions.add(".jpeg")

    def onerror(err: OSError) -> None:
        # Skip directories we cannot access
        return None

    for root in roots:
        for dirpath, dirnames, filenames in os.walk(root, topdown=True, onerror=onerror):
            # Avoid following symlinked directories or junctions
            pruned = []
            for d in dirnames:
                full = os.path.join(dirpath, d)
                if os.path.islink(full):
                    continue
                pruned.append(d)
            dirnames[:] = pruned

            for name in filenames:
                _, ext = os.path.splitext(name)
                if ext.lower() not in extensions:
                    continue
                path = os.path.join(dirpath, name)
                try:
                    size = os.path.getsize(path)
                except OSError:
                    continue
                yield dirpath, name, size


def parse_args(argv: Iterable[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scan for JPG images and write a text inventory.")
    parser.add_argument(
        "--output",
        default="jpg_inventory.txt",
        help="Output text file path (default: jpg_inventory.txt)",
    )
    parser.add_argument(
        "--roots",
        nargs="*",
        help="Optional root folders or drives to scan. Defaults to all drives.",
    )
    parser.add_argument(
        "--jpg-only",
        action="store_true",
        help="Only include .jpg (exclude .jpeg).",
    )
    return parser.parse_args(list(argv))


def main(argv: Iterable[str]) -> int:
    args = parse_args(argv)
    roots = args.roots if args.roots else list(get_logical_drives())
    include_jpeg = not args.jpg_only

    count = 0
    with open(args.output, "w", encoding="utf-8", newline="\n") as f:
        f.write("directory\tfilename\tsize_bytes\n")
        for directory, filename, size in iter_image_files(roots, include_jpeg):
            f.write(f"{directory}\t{filename}\t{size}\n")
            count += 1

    print(f"Wrote {count} records to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
