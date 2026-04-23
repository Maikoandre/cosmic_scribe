import os
import shutil
import re
from pathlib import Path

SOURCE_DIR = "docs/myriad_veil_cosmos"
TARGET_DIR = "knowledge"

# ------------------------
# Helpers
# ------------------------

def slugify(name):
    name = name.lower()
    name = re.sub(r'[^\w\s-]', '', name)
    name = re.sub(r'\s+', '_', name)
    return name

def classify(path, filename):
    full = f"{path}/{filename}".lower()

    if "technique" in full:
        return "cultivation/techniques"
    if "scripture" in full:
        return "cultivation/scriptures"
    if "cultivation" in full:
        return "cultivation/paths"
    if "realm" in full:
        return "cultivation/realms"

    if "sect" in full or "school" in full or "faction" in full:
        return "factions"

    if "character" in full or "ascendant" in full or "immortal" in full:
        return "characters"

    if "location" in full or "heaven" in full or "garden" in full or "map" in full:
        return "locations"

    if "battle" in full or "crisis" in full or "expedition" in full:
        return "events"

    if "dao" in full or "karma" in full or "concept" in full:
        return "concepts"

    return "core/misc"


def extract_affiliation(path):
    parts = path.lower().split(os.sep)
    for p in parts:
        if "sect" in p or "school" in p:
            return slugify(p)
    return None


def create_metadata(file_id, category, affiliation):
    meta = {
        "id": file_id,
        "type": category.split("/")[-1],
        "system": category.split("/")[0],
        "affiliation": affiliation or "unknown",
        "canon": True
    }

    yaml = "---\n"
    for k, v in meta.items():
        yaml += f"{k}: {v}\n"
    yaml += "---\n\n"

    return yaml


# ------------------------
# Main parser
# ------------------------

def process():
    for root, dirs, files in os.walk(SOURCE_DIR):
        for file in files:
            if not file.endswith(".md"):
                continue

            # Ignorar lixo
            if "copy" in file.lower() or "untitled" in file.lower():
                print(f"[SKIP] {file}")
                continue

            old_path = os.path.join(root, file)

            rel_path = os.path.relpath(root, SOURCE_DIR)

            category = classify(rel_path, file)

            filename = os.path.splitext(file)[0]
            file_id = slugify(filename)

            affiliation = extract_affiliation(rel_path)

            new_dir = os.path.join(TARGET_DIR, category)
            os.makedirs(new_dir, exist_ok=True)

            new_path = os.path.join(new_dir, f"{file_id}.md")

            with open(old_path, "r", encoding="utf-8") as f:
                content = f.read()

            metadata = create_metadata(file_id, category, affiliation)

            with open(new_path, "w", encoding="utf-8") as f:
                f.write(metadata + content)

            print(f"[OK] {file} -> {new_path}")


if __name__ == "__main__":
    process()