document.addEventListener('DOMContentLoaded', () => {
  const samplesContainer = document.getElementById('samplesContainer');
  const speechActFilter = document.getElementById('speechActFilter');
  const searchInput = document.getElementById('searchInput');

  let allSamples = [];

  // جلب كافة العينات الذهبية ديناميكياً حتى أول ملف غير موجود
  async function loadSamples() {
    let i = 1;
    let keepFetching = true;
    const promises = [];

    // حلقة جلب ديناميكية تتوقف فور عدم وجود الملف التالي (تغطي حتى 200 كحد أقصى كاحتياط)
    while (keepFetching && i <= 200) {
      const numStr = i < 10 ? `0${i}` : `${i}`;
      const path = `../corpus/seed_gold/sample_${numStr}.json`;
      
      try {
        const res = await fetch(path);
        if (!res.ok) {
          keepFetching = false;
          break;
        }
        const data = await res.json();
        allSamples.push(data);
      } catch (err) {
        keepFetching = false;
        break;
      }
      i++;
    }

    renderSamples(allSamples);
  }

  // عرض البطاقات الدلالية بناءً على المنهجية القياسية
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

      // معالجة المحددات والروابط السياقية
      const modifiers = sample.event_modifiers || [];
      const modifiersHtml = modifiers.map(m => `<div>• <strong>${m.modifier_type}:</strong> ${m.value} (${m.phonetic_marker})</div>`).join('') || '<span style="color:#adb5bd">لا توجد</span>';

      const links = sample.contextual_links || [];
      const linksHtml = links.map(l => `<div>• <strong>${l.link_type}:</strong> ${l.target_element} ➔ ${l.linked_value}</div>`).join('') || '<span style="color:#adb5bd">لا توجد</span>';

      card.innerHTML = `
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
      `;

      samplesContainer.appendChild(card);
    });
  }

  // تصفية والبحث في العينات
  function filterAndSearch() {
    const actValue = speechActFilter.value;
    const query = searchInput.value.trim().toLowerCase();

    const filtered = allSamples.filter(sample => {
      const matchesAct = (actValue === 'all') || (sample.pragmatic_intent?.speech_act === actValue);
      const raw = (sample.raw_text || '').toLowerCase();
      const lemma = (sample.predication_core?.topic_axis?.lemma || '').toLowerCase();
      const id = (sample.discourse_id || '').toLowerCase();
      const matchesQuery = !query || raw.includes(query) || lemma.includes(query) || id.includes(query);

      return matchesAct && matchesQuery;
    });

    renderSamples(filtered);
  }

  speechActFilter.addEventListener('change', filterAndSearch);
  searchInput.addEventListener('input', filterAndSearch);

  // التشغيل الأولي
  loadSamples();
});