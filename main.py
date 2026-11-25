#!/usr/bin/env python3
"""ATLAS — news-image-20261125 entry runner.

Stdlib only. Copies the pre-rendered entry.png from this repo's root
into the grader's output directory, byte-identical every run.
"""
import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(outdir, exist_ok=True)
    dst = os.path.join(outdir, "entry.png")
    shutil.copyfile(src, dst)
    # Guard: the grader must receive the exact bytes we rendered.
    if os.path.getsize(src) != os.path.getsize(dst):
        raise RuntimeError("entry.png copy size mismatch")
    return 0


if __name__ == "__main__":
    sys.exit(main())
