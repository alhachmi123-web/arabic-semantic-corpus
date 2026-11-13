import json
import os
import glob
from jsonschema import validate, ValidationError

def load_json(file_path):
    """دالة لقراءة ملف JSON بأمان"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"[خطأ في قراءة الملف] {file_path}: {e}")
        return None

def validate_corpus():
    """دالة التحقق الشامل من جميع ملفات المدونة الدلالية"""
    schema_path = os.path.join("schema", "arabic-semantic-engine.schema.json")
    
    # التحقق من وجود ملف الـ Schema
    if not os.path.exists(schema_path):
        print(f"[فشل حرج] لم يتم العثور على ملف المخطط القياسي في المسار: {schema_path}")
        return False

    schema = load_json(schema_path)
    if not schema:
        return False

    # البحث عن جميع ملفات JSON داخل مجلدات المدونة
    corpus_pattern = os.path.join("corpus", "**", "*.json")
    json_files = glob.glob(corpus_pattern, recursive=True)

    if not json_files:
        print("[تنبيه] لم يتم العثور على أي ملفات JSON داخل مجلد corpus حتى الآن.")
        return True

    # طباعة عدد الملفات المكتشفة بشكل آمن
    print(f"=== بدء فحص {len(json_files)} ملفاً دلالياً للمدونة ===")
    
    has_errors = False
    for file_path in json_files:
        instance = load_json(file_path)
        if instance is None:
            has_errors = True
            continue

        try:
            # عملية التحقق الأساسية ضد الـ Schema المعيارية
            validate(instance=instance, schema=schema)
            print(f"[صحيح ✓] {file_path}")
        except ValidationError as e:
            has_errors = True
            print(f"[خطأ دلالي ✗] الملف غير مطابق للمعيار: {file_path}")
            print(f"   └── السبب: {e.message}")

    if has_errors:
        print("\n[نتيجة الفحص] فشل الاختبار: وُجدت أخطاء برمجية أو دلالية في بعض الملفات.")
        return False
    else:
        print("\n[نتيجة الفحص] نجاح تام: جميع ملفات المدونة مطابقة للمعيار القياسي تماماً!")
        return True

if __name__ == "__main__":
    success = validate_corpus()
    import sys
    sys.exit(0 if success else 1)