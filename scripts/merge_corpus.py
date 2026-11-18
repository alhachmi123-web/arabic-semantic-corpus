import json
import os
import re

SOURCE_DIR = os.path.join("corpus", "seed_gold")
OUTPUT_DIR = os.path.join("corpus", "releases")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "full_corpus_500.json")

def natural_sort_key(filename):
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', filename)]

def merge_samples():
    if not os.path.exists(SOURCE_DIR):
        print(f"المجلد غير موجود: {SOURCE_DIR}")
        return

    files = [f for f in os.listdir(SOURCE_DIR) if f.startswith("sample_") and f.endswith(".json")]
    files.sort(key=natural_sort_key)

    merged_data = []
    for filename in files:
        filepath = os.path.join(SOURCE_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            merged_data.append(data)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(merged_data, f, ensure_ascii=False, indent=2)

    print(f"✅ تم دمج {len(merged_data)} عينة بنجاح في الملف: {OUTPUT_FILE}")

if __name__ == "__main__":
    merge_samples()