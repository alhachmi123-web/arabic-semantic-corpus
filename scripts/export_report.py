import os
import json
from collections import Counter
from datetime import datetime

CORPUS_DIR = "corpus/seed_gold"
REPORTS_DIR = "reports"

def load_corpus():
    corpus = []
    if not os.path.exists(CORPUS_DIR):
        print(f"[خطأ] مجلد المدونة {CORPUS_DIR} غير موجود.")
        return corpus
    
    for filename in sorted(os.listdir(CORPUS_DIR)):
        if filename.endswith(".json"):
            filepath = os.path.join(CORPUS_DIR, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    corpus.append((filename, data))
                except Exception as e:
                    print(f"[تحذير] خطأ في قراءة الملف {filename}: {e}")
    return corpus

def generate_markdown_report():
    corpus = load_corpus()
    if not corpus:
        print("[!] لا توجد عينات لتوليد التقرير.")
        return

    total = len(corpus)
    speech_acts = Counter()
    semantic_aspects = Counter()
    lemmas = Counter()

    for filename, data in corpus:
        sa = data.get("pragmatic_intent", {}).get("speech_act")
        if sa:
            speech_acts[sa] += 1
        
        sa_aspect = data.get("predication_core", {}).get("semantic_aspect")
        if sa_aspect:
            semantic_aspects[sa_aspect] += 1
            
        lemma = data.get("predication_core", {}).get("topic_axis", {}).get("lemma")
        if lemma:
            lemmas[lemma] += 1

    # إنشاء مجلد التقارير إن لم يكن موجوداً
    if not os.path.exists(REPORTS_DIR):
        os.makedirs(REPORTS_DIR)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_filename = f"corpus_report_{timestamp}.md"
    report_path = os.path.join(REPORTS_DIR, report_filename)

    # بناء محتوى التقرير بصيغة Markdown
    md_content = f"""# 📊 تقرير التحليل الدلالي الشامل للمدونة العربية

- **تاريخ التقرير:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
- **إجمالي العينات الذهبية المحللة:** `{total}` عينة
- **مسار المدونة:** `{CORPUS_DIR}`

---

## 📋 1. توزيع أنواع الأفعال الكلامية (Speech Acts)
| الفعل الكلامي (Speech Act) | عدد العينات | النسبة التقديرية |
| :--- | :---: | :---: |
"""

    for act, count in speech_acts.most_common():
        percentage = (count / total) * 100
        md_content += f"| `{act}` | **{count}** | {percentage:.1f}% |\n"

    md_content += f"""
---

## 🔍 2. توزيع الجوانب الدلالية (Semantic Aspects)
| الجانب الدلالي (Semantic Aspect) | عدد العينات |
| :--- | :---: |
"""

    for aspect, count in semantic_aspects.most_common():
        md_content += f"| `{aspect}` | **{count}** |\n"

    md_content += f"""
---

## 🔤 3. أبرز الجذور والألفاظ الأساسية (Top Lemmas)
| الجذر / اللفظ (Lemma) | التكرار |
| :--- | :---: |
"""

    for lemma, count in lemmas.most_common(15):
        md_content += f"| `{lemma}` | **{count}** |\n"

    md_content += f"""
---

## 📁 4. قائمة العينات المسجلة في المدونة
| رقم الملف | المعرف (Discourse ID) | النص الأساسي | الفعل الكلامي |
| :--- | :--- | :--- | :--- |
"""

    for filename, data in corpus:
        d_id = data.get("discourse_id", "N/A")
        raw_text = data.get("raw_text", "N/A")
        sa = data.get("pragmatic_intent", {}).get("speech_act", "N/A")
        md_content += f"| `{filename}` | `{d_id}` | {raw_text} | `{sa}` |\n"

    md_content += "\n\n> *تم توليد هذا التقرير آلياً بواسطة أداة التصدير في مشروع المدونة الدلالية العربية.*\n"

    # كتابة الملف
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(md_content)

    print("=" * 60)
    print(f"✨ تم تصدير التقرير بنجاح إلى الملف:")
    print(f"📂 {report_path}")
    print("=" * 60)

if __name__ == "__main__":
    generate_markdown_report()