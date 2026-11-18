import os
import json

def audit_project():
    print("=" * 60)
    print(" تقرير التقويم التقني لبنية مشروع المدونة الدلالية العربية")
    print("=" * 60)
    
    # 1. فحص المجلدات الأساسية من الجذر
    directories = ["corpus/seed_gold", "schema", "scripts", "web"]
    print("\n[1] فحص الهيكل التنظيمي للمجلدات:")
    for directory in directories:
        exists = os.path.isdir(directory)
        status = "موجود ✓ (نشط)" if exists else "غير موجود ✗"
        print(f"   - {directory}: {status}")

    # 2. فحص الملفات التقنية والحساسة
    key_files = [
        "schema/arabic-semantic-engine.schema.json",
        "scripts/validator.py",
        "scripts/batch_builder.py",
        "web/index.html",
        "web/app.js"
    ]
    print("\n[2] فحص الملفات التقنية والححرجة:")
    for file_path in key_files:
        exists = os.path.isfile(file_path)
        if exists:
            size_kb = os.path.getsize(file_path) / 1024
            print(f"   - {file_path}: موجود ✓ ({size_kb:.2f} KB)")
        else:
            print(f"   - {file_path}: غير موجود ✗")

    # 3. إحصائيات عينات المدونة الذهبية (seed_gold)
    corpus_dir = "corpus/seed_gold"
    if os.path.isdir(corpus_dir):
        json_files = [f for f in os.listdir(corpus_dir) if f.endswith(".json")]
        print(f"\n[3] فحص بيانات المدونة (Corpus Status):")
        print(f"   - إجمالي عدد العينات المخزنة: {len(json_files)} عينة")
        
        expected_samples = {f"sample_{i:02d}.json" for i in range(1, len(json_files) + 1)}
        actual_samples = set(json_files)
        if expected_samples.issubset(actual_samples):
            print("   - سلامة التسلسل الهرمي للعينات: سليم تماماً ✓")
        else:
            print("   - تنبيه: يوجد نقص أو اختلاف في تسلسل أسماء العينات!")
    else:
        print("\n[3] مجلد العينات غير موجود!")

    print("\n" + "=" * 60)
    print("انتهى الفحص بنجاح. أرسل لي النتائج لنحدد الخطوة التقنية القادمة.")
    print("=" * 60)

if __name__ == "__main__":
    audit_project()