document.addEventListener('DOMContentLoaded', () => {
  const samplesContainer = document.getElementById('samplesContainer');
  const speechActFilter = document.getElementById('speechActFilter');
  const rootFilter = document.getElementById('rootFilter');
  const searchInput = document.getElementById('searchInput');
  const statsCounter = document.getElementById('statsCounter');
  const exportBtn = document.getElementById('exportBtn');

  const sampleModal = document.getElementById('sampleModal');
  const modalCloseBtn = document.getElementById('modalCloseBtn');
  const modalBody = document.getElementById('modalBody');
  const modalJsonViewer = document.getElementById('modalJsonViewer');

  let allSamples = [];
  let currentFilteredSamples = [];

  // جلب البيانات عبر نظام الحزم والفهرس السريع (قابل للتمدد بلا نهاية وبسرعة فائقة)
  async function loadCorpus() {
    statsCounter.textContent = 'جاري تحميل الفهرس والحزم الدلالية بسرعة فائقة...';
    samplesContainer.innerHTML = '<p style="text-align: center; grid-column: 1/-1; color: #6c757d; padding: 2rem;">جاري تحميل عينات المدونة...</p>';
    
    try {
      // 1. جلب الفهرس السريع أولاً
      const manifestRes = await fetch('data/corpus_manifest.json');
      if (!manifestRes.ok) throw new Error('فشل تحميل فهرس المدونة.');
      const manifest = await manifestRes.json();
      
      const chunksCount = manifest.chunks_count || 1;
      const totalSamples = manifest.total || 0;

      // 2. جلب الحزم (Chunks) بالتوازي دفعة واحدة
      const chunkPromises = [];
      for (let i = 1; i <= chunksCount; i++) {
        chunkPromises.push(
          fetch(`data/chunk_${i}.json`)
            .then(res => res.ok ? res.json() : [])
            .catch(() => [])
        );
      }

      const chunkResults = await Promise.all(chunkPromises);
      allSamples = chunkResults.flat();

      if (allSamples.length === 0) {
        samplesContainer.innerHTML = '<p style="text-align: center; grid-column: 1/-1; color: #dc3545; padding: 2rem;">لم يتم العثور على بيانات حزم المدونة. يرجى التأكد من تشغيل سكربت التجميع أولاً.</p>';
        statsCounter.textContent = 'خطأ في التحميل';
        return;
      }

      populateRootFilter();
      filterAndSearch();

    } catch (error) {
      console.error('خطأ في تحميل المدونة:', error);
      samplesContainer.innerHTML = '<p style="text-align: center; grid-column: 1/-1; color: #dc3545; padding: 2rem;">حدث خطأ أثناء تحميل بيانات المدونة. يرجى التأكد من توليد ملفات البيانات عبر سكربت البناء.</p>';
      statsCounter.textContent = 'خطأ في الاتصال';
    }
  }

  // تعبئة قائمة الجذور اللغوية ديناميكياً
  function populateRootFilter() {
    const rootsSet = new Set();
    allSamples.forEach(sample => {
      const lemma = sample.predication_core?.topic_axis?.lemma;
      if (lemma) rootsSet.add(lemma);
    });

    rootFilter.innerHTML = '<option value="all">جميع الجذور (Roots)</option>';
    Array.from(rootsSet).sort().forEach(root => {
      const option = document.createElement('option');
      option.value = root;
      option.textContent = root;
      rootFilter.appendChild(option);
    });
  }

  // عرض البطاقات الدلالية
  function renderSamples(samples) {
    samplesContainer.innerHTML = '';
    if (samples.length === 0) {
      samplesContainer.innerHTML = '<p style="text-align: center; grid-column: 1/-1; color: #6c757d; padding: 2rem;">لا توجد عينات مطابقة لمعايير البحث.</p>';
      return;
    }

    samples.forEach(sample => {
      const card = document.createElement('div');
      card.className = 'sample-card';

      const speechAct = sample.pragmatic_intent?.speech_act || '';
      const rawText = sample.raw_text || '';
      const discourseId = sample.discourse_id || '';
      
      const topicLemma = sample.predication_core?.topic_axis?.lemma || '-';
      const topicRole = sample.predication_core?.topic_axis?.role || '-';
      const phoneticMarker = sample.predication_core?.topic_axis?.phonetic_marker || '-';
      
      const actionLemma = sample.predication_core?.action_event?.lemma || 'غير متاح';
      const temporalState = sample.predication_core?.action_event?.temporal_state || 'ثابت';
      const semanticAspect = sample.predication_core?.semantic_aspect || '-';

      const modifiers = sample.event_modifiers || [];
      const modifiersHtml = modifiers.map(m => `<div>• <strong>${m.modifier_type}:</strong> ${m.value} (${m.phonetic_marker})</div>`).join('') || '<span style="color:#adb5bd">لا توجد</span>';

      const links = sample.contextual_links || [];
      const linksHtml = links.map(l => `<div>• <strong>${l.link_type}:</strong> ${l.target_element} ➔ ${l.linked_value}</div>`).join('') || '<span style="color:#adb5bd">لا توجد</span>';

      card.innerHTML = `
        <div>
          <div class="card-header">
            <span class="discourse-id">${discourseId}</span>
            <span class="speech-act-badge">${speechAct}</span>
          </div>
          <div class="raw-text">${rawText}</div>
          
          <div class="section-box">
            <span class="section-title">نواة الإسناد (Predication Core)</span>
            <div class="detail-row"><strong>المحور:</strong> ${topicLemma} (${topicRole})</div>
            <div class="detail-row"><strong>الحركة الصوتية:</strong> ${phoneticMarker}</div>
            <div class="detail-row"><strong>الحدث:</strong> ${actionLemma} [${temporalState}]</div>
            <div class="detail-row"><strong>المظهر الدلالي:</strong> ${semanticAspect}</div>
          </div>

          <div class="section-box">
            <span class="section-title">المحددات (Event Modifiers)</span>
            <div class="detail-row">${modifiersHtml}</div>
          </div>

          <div class="section-box">
            <span class="section-title">الروابط السياقية (Contextual Links)</span>
            <div class="detail-row">${linksHtml}</div>
          </div>
        </div>

        <div class="card-footer">
          <button class="copy-btn" data-json='${JSON.stringify(sample, null, 2)}'>📋 نسخ JSON</button>
        </div>
      `;

      // فتح نافذة التفاصيل (Modal) عند النقر على البطاقة
      card.addEventListener('click', (e) => {
        if (e.target.classList.contains('copy-btn')) return;
        openModal(sample);
      });

      // زر النسخ المباشر
      const copyBtn = card.querySelector('.copy-btn');
      copyBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        const jsonString = copyBtn.getAttribute('data-json');
        navigator.clipboard.writeText(jsonString).then(() => {
          const originalText = copyBtn.textContent;
          copyBtn.textContent = '✨ تم النسخ!';
          copyBtn.style.backgroundColor = '#2d6a4f';
          copyBtn.style.color = '#fff';
          setTimeout(() => {
            copyBtn.textContent = originalText;
            copyBtn.style.backgroundColor = '';
            copyBtn.style.color = '';
          }, 2000);
        });
      });

      samplesContainer.appendChild(card);
    });
  }

  // فتح نافذة التفاصيل المنمقة (Modal)
  function openModal(sample) {
    modalBody.innerHTML = `
      <div style="margin-bottom: 1rem;"><strong>معرف الخطاب (Discourse ID):</strong> ${sample.discourse_id}</div>
      <div style="margin-bottom: 1rem;"><strong>النص الأصلي:</strong> <span style="color: var(--primary); font-size: 1.2rem; font-weight: bold;">${sample.raw_text}</span></div>
      <div style="margin-bottom: 1rem;"><strong>الأمر التداولي:</strong> ${sample.pragmatic_intent?.speech_act}</div>
      <div style="margin-bottom: 1rem;"><strong>المظهر الدلالي:</strong> ${sample.predication_core?.semantic_aspect}</div>
    `;
    modalJsonViewer.textContent = JSON.stringify(sample, null, 2);
    sampleModal.style.display = 'flex';
  }

  modalCloseBtn.addEventListener('click', () => {
    sampleModal.style.display = 'none';
  });
  window.addEventListener('click', (e) => {
    if (e.target === sampleModal) {
      sampleModal.style.display = 'none';
    }
  });

  // تصفية والبحث الفوري
  function filterAndSearch() {
    const actValue = speechActFilter.value;
    const rootValue = rootFilter.value;
    const query = searchInput.value.trim().toLowerCase();

    currentFilteredSamples = allSamples.filter(sample => {
      const matchesAct = (actValue === 'all') || (sample.pragmatic_intent?.speech_act === actValue);
      const lemma = sample.predication_core?.topic_axis?.lemma || '';
      const matchesRoot = (rootValue === 'all') || (lemma === rootValue);
      
      const raw = (sample.raw_text || '').toLowerCase();
      const id = (sample.discourse_id || '').toLowerCase();
      const matchesQuery = !query || raw.includes(query) || lemma.toLowerCase().includes(query) || id.includes(query);

      return matchesAct && matchesRoot && matchesQuery;
    });

    statsCounter.textContent = `عرض ${currentFilteredSamples.length} عينة من أصل ${allSamples.length} عينة معتمدة`;
    renderSamples(currentFilteredSamples);
  }

  // تصدير النتائج الحالية إلى JSON
  exportBtn.addEventListener('click', () => {
    if (currentFilteredSamples.length === 0) {
      alert('لا توجد عينات لتصديرها.');
      return;
    }
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(currentFilteredSamples, null, 2));
    const downloadAnchor = document.createElement('a');
    downloadAnchor.setAttribute("href", dataStr);
    downloadAnchor.setAttribute("download", `arabic_semantic_corpus_export_${Date.now()}.json`);
    document.body.appendChild(downloadAnchor);
    downloadAnchor.click();
    downloadAnchor.remove();
  });

  speechActFilter.addEventListener('change', filterAndSearch);
  rootFilter.addEventListener('change', filterAndSearch);
  searchInput.addEventListener('input', filterAndSearch);

  loadCorpus();
});