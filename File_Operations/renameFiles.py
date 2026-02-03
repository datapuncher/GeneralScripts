#!/usr/bin/python

"""
bulk_rename.py
Usage:
 python bulk_rename.py /path/to/folder --pattern "IMG_(\d+)" --replace "photo_\\1" --ext .jpg
Or simple sequence:
 python bulk_rename.py /path/to/folder --seq "photo" --ext .png
"""
import argparse, re
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument('folder')
ap.add_argument('--pattern')
ap.add_argument('--replace')
ap.add_argument('--seq')
ap.add_argument('--ext', default='')
args = ap.parse_args()
folder = Path(args.folder)

if args.pattern and args.replace:
    rx = re.compile(args.pattern)
    for f in folder.iterdir():
        if f.is_file():
            m = rx.search(f.name)
            if m:
                new = rx.sub(args.replace, f.name)
                f.rename(folder / new)
                print("Renamed", f.name, "->", new)
elif args.seq:
    i = 1
    for f in sorted(folder.iterdir()):
        if f.is_file():
            ext = args.ext or f.suffix
            new = f"{args.seq}_{i}{ext}"
            f.rename(folder / new)
            print("Renamed", f.name, "->", new)
            i += 1
else:
    print("No action. Provide --pattern/--replace or --seq.")
