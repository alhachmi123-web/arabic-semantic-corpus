import os
import json
import argparse
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

def print_statistics(corpus):
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

    print("=" * 65)
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

def search_corpus(query_type, query_val):
    corpus = load_corpus()
    results = []

    for filename, data in corpus:
        match = False
        if query_type == "speech_act":
            if data.get("pragmatic_intent", {}).get("speech_act") == query_val:
                match = True
        elif query_type == "lemma":
            if data.get("predication_core", {}).get("topic_axis", {}).get("lemma") == query_val:
                match = True
        elif query_type == "text":
            if query_val in data.get("raw_text", ""):
                match = True
        
        if match:
            results.append((filename, data))

    print("=" * 65)
    print(f"🔍 نتائج البحث عن ({query_type} = '{query_val}'): تم العثور على {len(results)} عينة")
    print("=" * 65)
    for filename, data in results:
        print(f"📁 الملف: {filename} | النص: {data.get('raw_text')} | المعرف: {data.get('discourse_id')}")
    print("=" * 65)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="محرك البحث والتحليل الدلالي لمدونة النصوص العربية")
    parser.add_argument("--stats", action="store_true", help="عرض الإحصاءات الشاملة للمدونة")
    parser.add_argument("--speech-act", type=str, help="البحث حسب نوع الفعل الكلامي (speech_act)")
    parser.add_argument("--lemma", type=str, help="البحث حسب الجذر / اللفظ الأساسي (lemma)")
    parser.add_argument("--text", type=str, help="البحث النصي المباشر داخل النصوص")

    args = parser.parse_args()
    corpus = load_corpus()

    if args.stats or (not args.speech_act and not args.lemma and not args.text):
        print_statistics(corpus)
    if args.speech_act:
        search_corpus("speech_act", args.speech_act)
    if args.lemma:
        search_corpus("lemma", args.lemma)
    if args.text:
        search_corpus("text", args.text)