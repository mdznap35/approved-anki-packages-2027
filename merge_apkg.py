import glob, os

print("=== Reassembling Anki .apkg packages ===")
for part in sorted(glob.glob("*.part_aa")):
    base = part.split(".part_aa")[0]
    print(f"Reassembling {base}...")
    with open(base, "wb") as outfile:
        for p in sorted(glob.glob(f"{base}.part_*")):
            with open(p, "rb") as infile:
                outfile.write(infile.read())
    print(f"✅ Reassembled {base} ({os.path.getsize(base)} bytes)")

print("=== All packages successfully reassembled! ===")
