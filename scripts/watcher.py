import os
import time
import subprocess

CORPUS_DIR = "corpus/seed_gold"
VALIDATOR_SCRIPT = "scripts/validator.py"

def watch_corpus():
    print("=" * 65)
    print(f"👀 بدء أداة المراقبة التلقائية للمجلد: {CORPUS_DIR}")
    print(" أي تعديل أو إضافة لملفات الـ JSON سيتم فحصها فوراً تلقائياً.")
    print(" اضغط Ctrl+C في أي وقت لإيقاف المراقبة.")
    print("=" * 65)
    
    file_mtimes = {}
    
    # فحص أولي للملفات الحالية وتاريخ تعديلها
    if os.path.exists(CORPUS_DIR):
        for filename in os.listdir(CORPUS_DIR):
            if filename.endswith(".json"):
                filepath = os.path.join(CORPUS_DIR, filename)
                file_mtimes[filepath] = os.path.getmtime(filepath)
                
    try:
        while True:
            time.sleep(1) # فحص التغييرات كل ثانية
            if not os.path.exists(CORPUS_DIR):
                continue
                
            current_files = [f for f in os.listdir(CORPUS_DIR) if f.endswith(".json")]
            current_filepaths = {os.path.join(CORPUS_DIR, f) for f in current_files}
            
            changed = False
            # التحقق من الملفات الجديدة أو المعدلة
            for filepath in current_filepaths:
                if not os.path.exists(filepath):
                    continue
                mtime = os.path.getmtime(filepath)
                if filepath not in file_mtimes:
                    print(f"\n[+] تم اكتشاف عينة جديدة: {os.path.basename(filepath)}")
                    file_mtimes[filepath] = mtime
                    changed = True
                elif file_mtimes[filepath] != mtime:
                    print(f"\n[~] تم اكتشاف تعديل على الملف: {os.path.basename(filepath)}")
                    file_mtimes[filepath] = mtime
                    changed = True
                    
            # التحقق من الملفات المحذوفة
            deleted_files = set(file_mtimes.keys()) - current_filepaths
            for filepath in deleted_files:
                print(f"\n[-] تم حذف الملف: {os.path.basename(filepath)}")
                del file_mtimes[filepath]
                changed = True
                
            # تشغيل أداة التحقق تلقائياً عند أي تغيير
            if changed:
                print("[🔄] جاري تشغيل أداة التحقق (validator.py)...")
                result = subprocess.run(["python", VALIDATOR_SCRIPT], capture_output=True, text=True, encoding="utf-8")
                print(result.stdout)
                if result.stderr:
                    print(result.stderr)
                print("-" * 65)
                
    except KeyboardInterrupt:
        print("\n[!] تم إيقاف أداة المراقبة بنجاح.")

if __name__ == "__main__":
    watch_corpus()