import os
import json
import re
import subprocess


def get_next_sample_index(target_dir):
    highest_index = 0
    for filename in os.listdir(target_dir):
        match = re.fullmatch(r"sample_(\d+)\.json", filename)
        if match:
            highest_index = max(highest_index, int(match.group(1)))
    return highest_index + 1

def process_batch():
    input_file = "batch_input.json"
    target_dir = "corpus/seed_gold"
    
    if not os.path.exists(input_file):
        print(f"[خطأ] لم يتم العثور على ملف المدخلات المؤقت {input_file}")
        return

    # قراءة الدفعة الجديدة
    with open(input_file, "r", encoding="utf-8") as f:
        batch_data = json.load(f)
    
    if not isinstance(batch_data, list):
        print("[خطأ] يجب أن يكون محتوى ملف المدخلات عبارة عن مصفوفة [...] تحتوي على عينات متعددة.")
        return

    # اعتمد على أعلى رقم موجود لا على عدد الملفات؛ حذوف عينة لا يجب أن يعاد الاستخدام كرقم جديد.
    next_index = get_next_sample_index(target_dir)
    print(f"=== بدء حفظ وتوليد {len(batch_data)} عينات جديدة بدءاً من sample_{next_index:04d} ===")

    for item in batch_data:
        filename = f"sample_{next_index:04d}.json"
        filepath = os.path.join(target_dir, filename)
        
        # تحديث معرف الدلالة تلقائياً ليتوافق مع اسم الملف
        item["discourse_id"] = f"DISC_GOLD_{next_index:04d}"
        
        # كتابة الملف الجديد
        with open(filepath, "w", encoding="utf-8") as out_f:
            json.dump(item, out_f, ensure_ascii=False, indent=2)
        
        print(f"[تم الحفظ ✓] {filepath}")
        next_index += 1

    print("\n=== جاري تشغيل أداة التحقق (validator.py) للتأكد من سلامة العينات الجديدة ===")
    subprocess.run(["python", "scripts/validator.py"])

if __name__ == "__main__":
    process_batch()