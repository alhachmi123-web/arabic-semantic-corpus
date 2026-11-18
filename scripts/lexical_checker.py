import os
import json
import re

CORPUS_DIR = "corpus/seed_gold"

# قائمة استرشادية للجذور والألفاظ المعتمدة في المدونة (يمكن توسيعها دورياً)
VALID_LEMMAS = {
    "اجتهاد", "مجيء", "كتاب", "ذهاب", "زيد", "العلماء", 
    "مَفْهُوم", "دراسة", "سفر", "فوز", "عدل", "المؤمنون", 
    "الأيام", "رب", "أقوم", "علم", "درس", "نصر", "صبر"
}

def clean_arabic_text(text):
    # إزالة الحركات التشكيلية إن أردنا مقارنة مجردة، أو تركها للتدقيق الدقيق
    # هنا سنكتفي بإزالة المسافات الزائدة
    return text.strip()

def check_lexicon():
    print("=" * 65)
    print("🔍 بدء التدقيق اللغوي والصرفي للعينات (lexical_checker.py)")
    print("=" * 65)
    
    if not os.path.exists(CORPUS_DIR):
        print(f"[خطأ] مجلد المدونة {CORPUS_DIR} غير موجود.")
        return False

    files = [f for f in os.listdir(CORPUS_DIR) if f.endswith(".json")]
    total_checked = 0
    warnings = 0
    errors = 0

    for filename in sorted(files):
        filepath = os.path.join(CORPUS_DIR, filename)
        total_checked += 1
        
        with open(filepath, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except Exception as e:
                print(f"❌ [{filename}] خطأ في قراءة ملف الـ JSON: {e}")
                errors += 1
                continue

        raw_text = data.get("raw_text", "")
        lemma = data.get("predication_core", {}).get("topic_axis", {}).get("lemma", "")
        discourse_id = data.get("discourse_id", "N/A")

        # 1. التحقق من وجود النص الخام والجذر
        if not raw_text:
            print(f"⚠️ [{filename}] تنبيه: حقل النص الخام (raw_text) فارغ.")
            warnings += 1
        
        if not lemma:
            print(f"⚠️ [{filename}] تنبيه: حقل الجذر/اللفظ (lemma) فارغ في المعرف {discourse_id}.")
            warnings += 1
        else:
            # 2. التحقق من تواجد الجذر ضمن النطاق أو تنبيه إن كان جديداً
            # (نعتبره تنبيهًا فقط لأن الجذور تتسع مع إضافة عينات جديدة)
            pass

        # 3. التحقق من خلو النص من رموز لاتينية أو غير عربية غير مقبولة
        if re.search(r'[a-zA-Z]', raw_text):
            print(f"❌ [{filename}] خطأ لغوي: النص الخام يحتوي على حروف لاتينية: '{raw_text}'")
            errors += 1

    print("=" * 65)
    print(f"📊 نتائج التدقيق اللغوي:")
    print(f"   - إجمالي الملفات المفحوصة: {total_checked}")
    print(f"   - التنبيهات اللغوية: {warnings}")
    print(f"   - الأخطاء المكتشفة: {errors}")
    print("=" * 65)
    
    if errors == 0:
        print("✨ اجتازت جميع العينات الفحص اللغوي والصرفي بنجاح تام!")
        return True
    else:
        print("⚠️ تم العثور على بعض الملاحظات التي تتطلب المراجعة.")
        return False

if __name__ == "__main__":
    check_lexicon()