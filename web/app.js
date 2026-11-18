<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>المدونة المفتوحة للهندسة الدلالية العربية</title>
  <style>
    :root {
      --bg-color: #f8f9fa;
      --card-bg: #ffffff;
      --primary: #1b4332;
      --accent: #2d6a4f;
      --border: #dee2e6;
      --text-main: #212529;
      --text-muted: #6c757d;
    }

    body {
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      background-color: var(--bg-color);
      color: var(--text-main);
      margin: 0;
      padding: 0;
      display: flex;
      flex-direction: column;
      height: 100vh;
      overflow: hidden;
      line-height: 1.6;
    }

    /* ترويسة ثابتة */
    header {
      background: linear-gradient(135deg, var(--primary), var(--accent));
      color: #ffffff;
      padding: 1.25rem 2rem;
      text-align: center;
      border-bottom: 4px solid #52b788;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
      flex-shrink: 0;
      position: relative;
      z-index: 100;
    }

    header h1 {
      margin: 0;
      font-size: 1.7rem;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 0.5rem;
    }

    header p {
      margin: 0.3rem 0 0;
      font-size: 0.9rem;
      opacity: 0.95;
    }

    .header-badges {
      display: flex;
      justify-content: center;
      gap: 1rem;
      margin-top: 0.5rem;
      flex-wrap: wrap;
    }

    .rights-badge {
      background: rgba(255, 255, 255, 0.2);
      padding: 0.2rem 0.6rem;
      border-radius: 4px;
      font-size: 0.8rem;
      border: 1px solid rgba(255, 255, 255, 0.35);
      backdrop-filter: blur(4px);
    }

    /* منطقة المحتوى القابلة للتمرير */
    .main-viewport {
      flex: 1;
      overflow-y: auto;
      padding: 2rem 1rem;
    }

    .container {
      max-width: 1100px;
      margin: 0 auto;
    }

    .controls {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 1rem;
      margin-bottom: 1.5rem;
      flex-wrap: wrap;
      background: var(--card-bg);
      padding: 1rem;
      border-radius: 8px;
      border: 1px solid var(--border);
      box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }

    .filters-group {
      display: flex;
      gap: 0.75rem;
      flex-wrap: wrap;
      flex: 1;
    }

    select, input, .action-btn {
      padding: 0.5rem 0.75rem;
      border: 1px solid var(--border);
      border-radius: 6px;
      font-size: 0.95rem;
      font-family: inherit;
    }

    .action-btn {
      background-color: var(--accent);
      color: #fff;
      cursor: pointer;
      border: none;
      transition: background 0.2s;
    }

    .action-btn:hover {
      background-color: var(--primary);
    }

    .stats-counter {
      font-size: 0.9rem;
      font-weight: bold;
      color: var(--accent);
      background: #f1f8f5;
      padding: 0.5rem 1rem;
      border-radius: 6px;
      border: 1px solid #d8f3dc;
    }

    .samples-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
      gap: 1.25rem;
    }

    .sample-card {
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 1.25rem;
      box-shadow: 0 2px 4px rgba(0,0,0,0.04);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      cursor: pointer;
      transition: transform 0.2s, box-shadow 0.2s;
    }

    .sample-card:hover {
      transform: translateY(-3px);
      box-shadow: 0 6px 12px rgba(0,0,0,0.08);
      border-color: var(--accent);
    }

    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid var(--border);
      padding-bottom: 0.75rem;
      margin-bottom: 1rem;
    }

    .discourse-id {
      font-family: monospace;
      font-size: 0.85rem;
      background: #e9ecef;
      padding: 0.2rem 0.5rem;
      border-radius: 4px;
      color: var(--primary);
    }

    .speech-act-badge {
      background: var(--accent);
      color: #fff;
      font-size: 0.8rem;
      padding: 0.25rem 0.6rem;
      border-radius: 20px;
    }

    .raw-text {
      font-size: 1.3rem;
      font-weight: bold;
      color: var(--primary);
      text-align: center;
      padding: 1rem;
      background: #f1f8f5;
      border-radius: 8px;
      margin-bottom: 1rem;
    }

    .section-box {
      margin-bottom: 0.75rem;
      padding: 0.75rem;
      border: 1px solid #edf2f4;
      border-radius: 6px;
      background: #fcfcfc;
    }

    .section-title {
      font-size: 0.85rem;
      font-weight: bold;
      color: var(--text-muted);
      margin-bottom: 0.4rem;
      display: block;
    }

    .detail-row {
      font-size: 0.9rem;
      margin: 0.2rem 0;
    }

    .card-footer {
      display: flex;
      justify-content: flex-end;
      gap: 0.5rem;
      margin-top: 1rem;
      border-top: 1px solid var(--border);
      padding-top: 0.75rem;
    }

    .copy-btn {
      background-color: #e9ecef;
      color: var(--primary);
      border: 1px solid var(--border);
      padding: 0.35rem 0.75rem;
      border-radius: 4px;
      font-size: 0.85rem;
      cursor: pointer;
      font-family: inherit;
      transition: all 0.2s;
    }

    .copy-btn:hover {
      background-color: var(--accent);
      color: #fff;
      border-color: var(--accent);
    }

    /* Modal (نافذة التفاصيل العائمة) */
    .modal-overlay {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0, 0, 0, 0.6);
      display: none;
      justify-content: center;
      align-items: center;
      z-index: 1000;
      backdrop-filter: blur(4px);
    }

    .modal-content {
      background: #fff;
      width: 90%;
      max-width: 750px;
      max-height: 85vh;
      border-radius: 12px;
      padding: 2rem;
      overflow-y: auto;
      box-shadow: 0 10px 25px rgba(0,0,0,0.2);
      position: relative;
    }

    .modal-close {
      position: absolute;
      top: 1rem;
      left: 1rem;
      background: #e9ecef;
      border: none;
      font-size: 1.2rem;
      width: 35px;
      height: 35px;
      border-radius: 50%;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      color: var(--text-main);
      transition: background 0.2s;
    }

    .modal-close:hover {
      background: #dc3545;
      color: #fff;
    }

    .json-viewer {
      background: #212529;
      color: #f8f9fa;
      padding: 1rem;
      border-radius: 8px;
      font-family: monospace;
      font-size: 0.85rem;
      white-space: pre-wrap;
      direction: ltr;
      text-align: left;
      margin-top: 1rem;
      max-height: 350px;
      overflow-y: auto;
    }

    /* تذييل ثابت */
    footer {
      text-align: center;
      padding: 0.8rem 2rem;
      background-color: #1b4332;
      color: #e9ecef;
      font-size: 0.85rem;
      border-top: 3px solid #52b788;
      flex-shrink: 0;
      z-index: 100;
      box-shadow: 0 -4px 12px rgba(0, 0, 0, 0.1);
    }

    footer p {
      margin: 0.2rem 0;
    }

    footer .owner {
      color: #52b788;
      font-weight: bold;
    }
  </style>
</head>
<body>

  <!-- ترويسة ثابتة -->
  <header>
    <h1>📖 المدونة المفتوحة للهندسة الدلالية العربية</h1>
    <p>منصة بحثية متقدمة لاستعراض وتحليل العينات الدلالية وفق المخطط القياسي المعياري</p>
    <div class="header-badges">
      <span class="rights-badge">✨ محتوى ذهبي معتمد</span>
      <span class="rights-badge">🛡️ محمية لحفظ حقوق البحث العلمي والأكاديمي</span>
    </div>
  </header>

  <!-- محتوى قابل للتمرير -->
  <div class="main-viewport">
    <main class="container">
      <!-- شريط التحكم والبحث والفلترة -->
      <section class="controls">
        <div class="filters-group">
          <select id="speechActFilter">
            <option value="all">جميع الأفعال الكلامية (speech_act)</option>
            <option value="assertion_إخبار">إخبار (assertion_إخبار)</option>
            <option value="directive_طلب">طلب (directive_طلب)</option>
            <option value="exclamation_تعجب">تعجب (exclamation_تعجب)</option>
            <option value="restriction_قصر_وحصر">قصر وحصر (restriction_قصر_وحصر)</option>
            <option value="supplication_دعاء">دعاء (supplication_دعاء)</option>
            <option value="oath_قسم">قسم (oath_قسم)</option>
          </select>

          <!-- قائمة فلترة الجذور اللغوية -->
          <select id="rootFilter">
            <option value="all">جميع الجذور (Roots)</option>
          </select>

          <input type="text" id="searchInput" placeholder="ابحث في النص أو الجذر...">

          <button id="exportBtn" class="action-btn">📥 تصدير النتائج (JSON)</button>
        </div>
        
        <div id="statsCounter" class="stats-counter">جاري التحميل...</div>
      </section>

      <!-- شبكة البطاقات -->
      <section id="samplesContainer" class="samples-grid">
        <!-- سيتم حقن البطاقات هنا -->
      </section>
    </main>
  </div>

  <!-- نافذة التفاصيل (Modal) -->
  <div id="sampleModal" class="modal-overlay">
    <div class="modal-content">
      <button class="modal-close" id="modalCloseBtn">&times;</button>
      <h2 style="color: var(--primary); margin-top: 0; border-bottom: 2px solid var(--border); padding-bottom: 0.5rem;">تفاصيل العينة الدلالية</h2>
      <div id="modalBody"></div>
      <div style="margin-top: 1rem;">
        <strong>الهيكل المصدري (JSON):</strong>
        <div id="modalJsonViewer" class="json-viewer"></div>
      </div>
    </div>
  </div>

  <!-- تذييل ثابت -->
  <footer>
    <p>© 2026 <span class="owner">Mohamed Al-Hashmi</span> — جميع الحقوق محفوظة.</p>
    <p>هذه المدونة مخصصة للبحث العلمي والأكاديمي، ويُحظر تماماً استخدامها أو استغلالها تجارياً دون إذن خطي صريح.</p>
  </footer>

  <script src="app.js"></script>
</body>
</html>