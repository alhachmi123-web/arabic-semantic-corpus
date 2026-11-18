import os
import json
from collections import Counter

CORPUS_DIR = "corpus/seed_gold"

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

def show_statistics(corpus):
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

    print("\n" + "=" * 65)
    print(f"📊 تقرير الإحصاءات الشامل للمدونة الدلالية (إجمالي العينات: {total})")
    print("=" * 65)
    
    print("\n[1] توزيع أنواع الأفعال الكلامية (Speech Acts):")
    for act, count in speech_acts.most_common():
        print(f"   - {act}: {count} عينة")

    print("\n[2] توزيع الجوانب الدلالية (Semantic Aspects):")
    for aspect, count in semantic_aspects.most_common():
        print(f"   - {aspect}: {count} عينة")

    print("\n[3] أبرز الجذور / اللفظ الأساسي (Top Lemmas):")
    for lemma, count in lemmas.most_common(10):
        print(f"   - {lemma}: {count} مرة")
    print("=" * 65)

def search_by_field(corpus, field_path, query_val):
    results = []
    for filename, data in corpus:
        val = data
        for key in field_path:
            if isinstance(val, dict):
                val = val.get(key)
            else:
                val = None
                break
        if val and query_val in str(val):
            results.append((filename, data))
            
    print("\n" + "=" * 65)
    print(f"🔍 نتائج البحث عن ('{query_val}'): تم العثور على {len(results)} عينة")
    print("=" * 65)
    for filename, data in results:
        print(f"📁 الملف: {filename} | النص: {data.get('raw_text')} | المعرف: {data.get('discourse_id')}")
    print("=" * 65)

def interactive_cli():
    corpus = load_corpus()
    if not corpus:
        print("[!] لا توجد عينات محملة.")
        return

    while True:
        print("\n" + "=" * 50)
        print("💡 واجهة الاستعلام التفاعلية للمدونة الدلالية العربية")
        print("=" * 50)
        print("1. عرض الإحصاءات الشاملة للمدونة")
        print("2. البحث حسب الفعل الكلامي (Speech Act)")
        print("3. البحث حسب الجذر / اللفظ الأساسي (Lemma)")
        print("4. البحث حسب الجانب الدلالي (Semantic Aspect)")
        print("5. البحث النصي المباشر في النصوص")
        print("6. الخروج من النظام")
        print("-" * 50)
        
        choice = input("اختر رقماً من القائمة (1-6): ").strip()
        
        if choice == "1":
            show_statistics(corpus)
        elif choice == "2":
            val = input("أدخل اسم الفعل الكلامي (مثل: directive_طلب أو assertion_إخبار): ").strip()
            search_by_field(corpus, ["pragmatic_intent", "speech_act"], val)
        elif choice == "3":
            val = input("أدخل الجذر أو اللفظ الأساسي (مثل: سفر أو علم): ").strip()
            search_by_field(corpus, ["predication_core", "topic_axis", "lemma"], val)
        elif choice == "4":
            val = input("أدخل الجانب الدلالي (مثل: dynamic_renewal_تجدد_وحدوث): ").strip()
            search_by_field(corpus, ["predication_core", "semantic_aspect"], val)
        elif choice == "5":
            val = input("أدخل الكلمة أو العبارة للبحث النصي: ").strip()
            results = [(f, d) for f, d in corpus if val in d.get("raw_text", "")]
            print("\n" + "=" * 65)
            print(f"🔍 نتائج البحث النصي عن ('{val}'): تم العثور على {len(results)} عينة")
            print("=" * 65)
            for filename, data in results:
                print(f"📁 الملف: {filename} | النص: {data.get('raw_text')} | المعرف: {data.get('discourse_id')}")
            print("=" * 65)
        elif choice == "6":
            print("\n✨ شكراً لاستخدامك النظام الدلالي. مع السلامة!")
            break
        else:
            print("[!] خيار غير صحيح، يرجى اختيار رقم بين 1 و 6.")

if __name__ == "__main__":
    interactive_cli()