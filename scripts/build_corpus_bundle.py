import os
import json
import re
from pathlib import Path


def natural_sort_key(path):
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(r"(\d+)", path.name)]

def build_corpus_bundles():
    seed_gold_dir = Path("corpus/seed_gold")
    output_dir = Path("web/data")
    output_dir.mkdir(parents=True, exist_ok=True)

    if not seed_gold_dir.exists():
        print("❌ مجلد العينات غير موجود!")
        return

    # العثور على كافة ملفات العينات بصيغة JSON ديناميكياً مهما بلغ عددها
    sample_files = sorted(seed_gold_dir.glob("sample_*.json"), key=natural_sort_key)
    total_samples = len(sample_files)
    print(f"🔍 تم اكتشاف {total_samples} عينة في المدونة.")

    manifest_entries = []
    chunk_size = 250  # كل 250 عينة في ملف حزمة مستقل لضمان خفة التحميل
    chunks = {}

    for index, file_path in enumerate(sample_files, start=1):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            discourse_id = data.get("discourse_id", f"DISC_{index}")
            speech_act = data.get("pragmatic_intent", {}).get("speech_act", "")
            lemma = data.get("predication_core", {}).get("topic_axis", {}).get("lemma", "")
            raw_text = data.get("raw_text", "")

            # تحديد رقم الحزمة
            chunk_id = (index - 1) // chunk_size + 1
            if chunk_id not in chunks:
                chunks[chunk_id] = []

            chunks[chunk_id].append(data)

            # إضافة البيانات الوصفية للفهرس السريع
            manifest_entries.append({
                "id": discourse_id,
                "file_index": index,
                "chunk_id": chunk_id,
                "speech_act": speech_act,
                "lemma": lemma,
                "raw_text": raw_text
            })
        except Exception as e:
            print(f"⚠️ خطأ في قراءة الملف {file_path.name}: {e}")

    # حفظ ملف الفهرس السريع (Manifest)
    manifest_data = {
        "total": total_samples,
        "chunks_count": len(chunks),
        "entries": manifest_entries
    }
    
    with open(output_dir / "corpus_manifest.json", 'w', encoding='utf-8') as f:
        json.dump(manifest_data, f, ensure_ascii=False, indent=2)
    print(f"✅ تم حفظ الفهرس الرئيسي بنجاح في {output_dir / 'corpus_manifest.json'}")

    # حفظ ملفات الحزم (Chunks)
    for chunk_id, chunk_samples in chunks.items():
        chunk_path = output_dir / f"chunk_{chunk_id}.json"
        with open(chunk_path, 'w', encoding='utf-8') as f:
            json.dump(chunk_samples, f, ensure_ascii=False, indent=2)
        print(f"📦 تم حفظ الحزمة رقم {chunk_id} تحتوي على {len(chunk_samples)} عينة.")

    print("✨ تمت عملية البناء والتجميع للتمدد اللانهائي بنجاح تام!")

if __name__ == "__main__":
    build_corpus_bundles()