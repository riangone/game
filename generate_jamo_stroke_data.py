import os, glob, re, json

mapping = {
    '01_giyeok': 'ㄱ', '02_nieun': 'ㄴ', '03_digeut': 'ㄷ', '04_rieul': 'ㄹ',
    '05_mieum': 'ㅁ', '06_bieup': 'ㅂ', '07_siot': 'ㅅ', '08_ieung': 'ㅇ',
    '09_jieut': 'ㅈ', '10_chieut': 'ㅊ', '11_kieuk': 'ㅋ', '12_tieut': 'ㅌ',
    '13_pieup': 'ㅍ', '14_hieut': 'ㅎ', '15_a': 'ㅏ', '16_ya': 'ㅑ',
    '17_eo': 'ㅓ', '18_yeo': 'ㅕ', '19_o': 'ㅗ', '20_yo': 'ㅛ',
    '21_u': 'ㅜ', '22_yu': 'ㅠ', '23_eu': 'ㅡ', '24_i': 'ㅣ',
    '25_ae': 'ㅐ', '26_yae': 'ㅒ', '27_e': 'ㅔ', '28_ye': 'ㅖ',
    '29_oe': 'ㅚ', '30_wi': 'ㅟ', '31_ui': 'ㅢ', '32_wa': 'ㅘ',
    '33_wo': 'ㅝ', '34_wae': 'ㅙ', '35_we': 'ㅞ'
}

jamo_meta = {
    'ㄱ': {'name': '기역', 'ro': 'giyeok', 'strokes': 1, 'rule': '横折向左下微弧一笔成型'},
    'ㄴ': {'name': '니은', 'ro': 'nieun', 'strokes': 1, 'rule': '竖下折向右横一笔成型'},
    'ㄷ': {'name': '디귿', 'ro': 'digeut', 'strokes': 2, 'rule': '①上横 ②折竖向右横'},
    'ㄹ': {'name': '리을', 'ro': 'rieul', 'strokes': 3, 'rule': '①横折 ②横 ③折竖横'},
    'ㅁ': {'name': '미음', 'ro': 'mieum', 'strokes': 3, 'rule': '①左竖 ②横折 ③底横封闭'},
    'ㅂ': {'name': '비읍', 'ro': 'bieup', 'strokes': 4, 'rule': '①左竖 ②右竖 ③中横 ④底横'},
    'ㅅ': {'name': '시옷', 'ro': 'siot', 'strokes': 2, 'rule': '①撇向左下 ②捺向右下'},
    'ㅇ': {'name': '이응', 'ro': 'ieung', 'strokes': 1, 'rule': '从顶端逆时针画完整圆圈'},
    'ㅈ': {'name': '지읒', 'ro': 'jieut', 'strokes': 2, 'rule': '①横折撇 ②右侧向右下点撇'},
    'ㅊ': {'name': '치읓', 'ro': 'chieut', 'strokes': 3, 'rule': '①顶短横 ②横折撇 ③右侧捺点'},
    'ㅋ': {'name': '키읔', 'ro': 'kieuk', 'strokes': 2, 'rule': '①横折 ②中间穿横'},
    'ㅌ': {'name': '티읕', 'ro': 'tieut', 'strokes': 3, 'rule': '①上横 ②中横 ③折竖横'},
    'ㅍ': {'name': '피읖', 'ro': 'pieup', 'strokes': 4, 'rule': '①上长横 ②左竖 ③右竖 ④底横'},
    'ㅎ': {'name': '히읗', 'ro': 'hieut', 'strokes': 3, 'rule': '①顶短横 ②中长横 ③底圆圈'},
    'ㄲ': {'name': '쌍기역', 'ro': 'ssang-giyeok', 'strokes': 2, 'rule': '连续并排书写两个ㄱ'},
    'ㄸ': {'name': '쌍디귿', 'ro': 'ssang-digeut', 'strokes': 4, 'rule': '连续并排书写两个ㄷ'},
    'ㅃ': {'name': '쌍비읍', 'ro': 'ssang-bieup', 'strokes': 8, 'rule': '连续并排书写两个ㅂ'},
    'ㅆ': {'name': '쌍시옷', 'ro': 'ssang-siot', 'strokes': 4, 'rule': '连续并排书写两个ㅅ'},
    'ㅉ': {'name': '쌍지읒', 'ro': 'ssang-jieut', 'strokes': 4, 'rule': '连续并排书写两个ㅈ'},
    'ㅏ': {'name': '아', 'ro': 'a', 'strokes': 2, 'rule': '①长竖下行 ②中右短横'},
    'ㅑ': {'name': '야', 'ro': 'ya', 'strokes': 3, 'rule': '①长竖下行 ②上右短横 ③下右短横'},
    'ㅓ': {'name': '어', 'ro': 'eo', 'strokes': 2, 'rule': '①左短横 ②穿过长竖下行'},
    'ㅕ': {'name': '여', 'ro': 'yeo', 'strokes': 3, 'rule': '①上左短横 ②下左短横 ③长竖下行'},
    'ㅗ': {'name': '오', 'ro': 'o', 'strokes': 2, 'rule': '①上短竖 ②下长横向右'},
    'ㅛ': {'name': '요', 'ro': 'yo', 'strokes': 3, 'rule': '①左短竖 ②右短竖 ③下长横向右'},
    'ㅜ': {'name': '우', 'ro': 'u', 'strokes': 2, 'rule': '①上长横向右 ②中短竖下行'},
    'ㅠ': {'name': '유', 'ro': 'yu', 'strokes': 3, 'rule': '①上长横向右 ②左短竖 ③右短竖'},
    'ㅡ': {'name': '으', 'ro': 'eu', 'strokes': 1, 'rule': '平稳从左向右一笔长横'},
    'ㅣ': {'name': '이', 'ro': 'i', 'strokes': 1, 'rule': '挺拔从上至下一笔长竖'},
    'ㅐ': {'name': '애', 'ro': 'ae', 'strokes': 3, 'rule': '①竖 ②短横 ③右长竖'},
    'ㅒ': {'name': '얘', 'ro': 'yae', 'strokes': 4, 'rule': '①竖 ②双短横 ③右长竖'},
    'ㅔ': {'name': '에', 'ro': 'e', 'strokes': 3, 'rule': '①短横 ②左长竖 ③右长竖'},
    'ㅖ': {'name': '예', 'ro': 'ye', 'strokes': 4, 'rule': '①双短横 ②左长竖 ③右长竖'},
    'ㅚ': {'name': '외', 'ro': 'oe', 'strokes': 3, 'rule': '①短竖 ②长横 ③右长竖ㅣ'},
    'ㅟ': {'name': '위', 'ro': 'wi', 'strokes': 3, 'rule': '①长横 ②短竖 ③右长竖ㅣ'},
    'ㅢ': {'name': '의', 'ro': 'ui', 'strokes': 2, 'rule': '①长横ㅡ ②右长竖ㅣ'},
    'ㅘ': {'name': '와', 'ro': 'wa', 'strokes': 4, 'rule': '①短竖 ②长横 ③长竖 ④短横 (ㅗ+ㅏ)'},
    'ㅝ': {'name': '워', 'ro': 'wo', 'strokes': 4, 'rule': '①长横 ②短竖 ③短横 ④长竖 (ㅜ+ㅓ)'},
    'ㅙ': {'name': '왜', 'ro': 'wae', 'strokes': 5, 'rule': 'ㅗ拼写ㅐ (5笔连贯)'},
    'ㅞ': {'name': '웨', 'ro': 'we', 'strokes': 5, 'rule': 'ㅜ拼写ㅔ (5笔连贯)'}
}

svg_bodies = {}
for base_name, jamo in mapping.items():
    svg_path = f'assets/jamo-stroke/{base_name}.svg'
    with open(svg_path, 'r', encoding='utf-8') as f:
        c = f.read()
    m = re.search(r'<svg[^>]*>(.*)</svg>', c, re.DOTALL)
    if m:
        inner = m.group(1).strip()
        inner = re.sub(r'<style[^>]*>.*?</style>', '', inner, flags=re.DOTALL)
        inner = re.sub(r'\s+', ' ', inner).strip()
        svg_bodies[jamo] = inner

# Double jamos
double_map = {'ㄲ': 'ㄱ', 'ㄸ': 'ㄷ', 'ㅃ': 'ㅂ', 'ㅆ': 'ㅅ', 'ㅉ': 'ㅈ'}
for dj, sj in double_map.items():
    s_inner = svg_bodies[sj]
    svg_bodies[dj] = f'<g class="double-left" transform="matrix(0.56 0 0 0.56 8 110)">{s_inner}</g><g class="double-right" transform="matrix(0.56 0 0 0.56 212 110)">{s_inner}</g>'

os.makedirs('js', exist_ok=True)

with open('js/hangeul_stroke_data.js', 'w', encoding='utf-8') as f:
    f.write('/* ==========================================================================\n')
    f.write('   Hangeul Stroke Order Data & Vector Renderer\n')
    f.write('   Based on MagisterAdamus/hangeul-stroke-order (UnPen font, standard stroke order)\n')
    f.write('   ========================================================================== */\n\n')
    
    f.write('const HANGEUL_STROKE_META = ' + json.dumps(jamo_meta, ensure_ascii=False, indent=2) + ';\n\n')
    f.write('const HANGEUL_STROKE_SVG = ' + json.dumps(svg_bodies, ensure_ascii=False, indent=2) + ';\n\n')
    
    f.write('''/**
 * Renders an inline SVG for a given jamo.
 * @param {string} jamo - Hangul Jamo character (e.g. 'ㅎ', 'ㅏ', 'ㄴ')
 * @param {string} extraClass - Additional CSS class name(s)
 * @returns {string} SVG HTML string
 */
function getJamoStrokeSvg(jamo, extraClass){
  const body = HANGEUL_STROKE_SVG[jamo];
  if(!body){
    return `<svg class="jamo-svg ${extraClass || ''}" viewBox="0 0 500 500"><text x="250" y="320" font-size="280" font-weight="900" text-anchor="middle" fill="#334155">${jamo}</text></svg>`;
  }
  return `<svg class="jamo-svg ${extraClass || ''}" viewBox="0 0 500 500" aria-label="${jamo}">${body}</svg>`;
}

/**
 * Renders an interactive stroke breakdown card for a component.
 * @param {string} partKey - 'cho' | 'jung' | 'jong'
 * @param {string} partLabel - '初声' | '中声' | '终声'
 * @param {string} jamo - Hangul jamo
 * @returns {string} HTML string
 */
function renderJamoPartCard(partKey, partLabel, jamo){
  if(!jamo) return '';
  const meta = HANGEUL_STROKE_META[jamo] || { name: jamo, ro: '', strokes: 1, rule: '标准笔画' };
  const svg = getJamoStrokeSvg(jamo, 'jamo-thumb-svg');
  return `
    <div class="part-card part-card-${partKey}" data-part="${partKey}" data-jamo="${jamo}" onclick="openStrokeGuideModal('${jamo}')" title="点击查看【${jamo}】标准笔顺放大图">
      <div class="part-header">
        <span class="part-tag">${partLabel}</span>
        <span class="part-jamo-text">${jamo}</span>
        <span class="part-strokes-badge">${meta.strokes}画</span>
      </div>
      <div class="part-svg-wrap">
        ${svg}
      </div>
      <div class="part-footer">
        <span class="part-name">${meta.name}</span>
        <span class="part-ro">${meta.ro}</span>
      </div>
    </div>
  `;
}

/**
 * Opens full stroke guide modal for the given syllable character or single jamo.
 * @param {string|object} target - char object or jamo string
 */
function openStrokeGuideModal(target){
  let modal = document.getElementById('strokeGuideModal');
  if(!modal){
    modal = document.createElement('div');
    modal.id = 'strokeGuideModal';
    modal.className = 'stroke-modal-overlay';
    modal.innerHTML = `
      <div class="stroke-modal-box">
        <div class="stroke-modal-header">
          <div class="stroke-modal-title" id="strokeModalTitle">✍️ 标准笔画与运笔规范</div>
          <button class="stroke-modal-close" onclick="closeStrokeGuideModal()" aria-label="关闭">&times;</button>
        </div>
        <div class="stroke-modal-body" id="strokeModalBody"></div>
        <div class="stroke-modal-footer">
          <span style="font-size:12px;color:#64748b;">💡 依据韩国国立国语院标准笔顺规范 · 辅音自上而下/自左至右 · 元音先横后竖或先竖后横</span>
          <button class="btn ghost small" onclick="closeStrokeGuideModal()">关闭</button>
        </div>
      </div>
    `;
    document.body.appendChild(modal);
    modal.addEventListener('click', (e)=>{ if(e.target === modal) closeStrokeGuideModal(); });
  }

  const bodyEl = document.getElementById('strokeModalBody');
  const titleEl = document.getElementById('strokeModalTitle');

  // If target is single jamo
  if(typeof target === 'string' && target.length === 1 && HANGEUL_STROKE_META[target]){
    const meta = HANGEUL_STROKE_META[target];
    titleEl.innerHTML = `✍️ 字母笔顺图解：<strong style="color:var(--kr-blue);">${target}</strong> <span style="font-size:14px;color:#64748b;">(${meta.name} · ${meta.ro})</span>`;
    bodyEl.innerHTML = `
      <div class="modal-single-jamo">
        <div class="modal-big-svg-wrap">
          ${getJamoStrokeSvg(target, 'jamo-big-svg')}
        </div>
        <div class="modal-jamo-details">
          <div class="detail-row"><strong>字母名称：</strong> ${meta.name} (${meta.ro})</div>
          <div class="detail-row"><strong>标准笔画：</strong> ${meta.strokes} 画</div>
          <div class="detail-row"><strong>运笔要领：</strong> ${meta.rule}</div>
          <div class="detail-legend">
            <span class="legend-badge red">①②③ 笔画顺序</span>
            <span class="legend-badge blue">➜ 运笔方向箭头</span>
            <span class="legend-badge dark">■ UnPen书法墨韵</span>
          </div>
        </div>
      </div>
    `;
  } else {
    // Current character object
    const c = (typeof target === 'object' && target) ? target : (typeof CHARACTERS !== 'undefined' ? CHARACTERS[charIdx] : null);
    if(!c) return;
    titleEl.innerHTML = `✍️ 音节方块字笔顺图解：<strong style="font-size:24px;color:var(--kr-blue);">${c.zh}</strong> <span style="font-size:14px;color:#64748b;">[${c.py}] · 对应汉字【${c.hanja || ''}】</span>`;
    
    const parts = [
      { key: 'cho', label: '初声 (Cho)', jamo: c.cho },
      { key: 'jung', label: '中声 (Jung)', jamo: c.jung }
    ];
    if(c.jong) parts.push({ key: 'jong', label: '终声/收音 (Jong)', jamo: c.jong });

    let partsHtml = parts.map(p => {
      const meta = HANGEUL_STROKE_META[p.jamo] || { name: p.jamo, ro: '', strokes: 1, rule: '标准笔画' };
      return `
        <div class="modal-part-item">
          <div class="modal-part-badge">${p.label}</div>
          <div class="modal-part-svg">
            ${getJamoStrokeSvg(p.jamo, 'jamo-modal-svg')}
          </div>
          <div class="modal-part-meta">
            <div style="font-weight:800;font-size:16px;color:#1e293b;">${p.jamo} <span style="font-size:12px;color:#64748b;font-weight:normal;">(${meta.name})</span></div>
            <div style="font-size:12px;color:#2563eb;font-weight:700;">${meta.strokes} 画</div>
            <div style="font-size:12px;color:#475569;margin-top:4px;line-height:1.4;">${meta.rule}</div>
          </div>
        </div>
      `;
    }).join('<div class="modal-part-plus">+</div>');

    bodyEl.innerHTML = `
      <div class="modal-syllable-assembly">
        <div class="assembly-tip">
          韩语方块字由<strong>初声辅音 + 中声元音 (+ 终声收音)</strong>拼接而成。书写顺序严格遵循<strong>从初声到中声、最后写终声</strong>。
        </div>
        <div class="modal-parts-row">
          ${partsHtml}
        </div>
        <div class="detail-legend" style="margin-top:14px;justify-content:center;">
          <span class="legend-badge red">①②③ 笔画顺序</span>
          <span class="legend-badge blue">➜ 运笔方向箭头</span>
          <span class="legend-badge dark">■ UnPen书法墨韵</span>
        </div>
      </div>
    `;
  }

  modal.classList.add('active');
}

function closeStrokeGuideModal(){
  const modal = document.getElementById('strokeGuideModal');
  if(modal) modal.classList.remove('active');
}

if(typeof window !== 'undefined') window.addEventListener('keydown', (e)=>{
  if(e.key === 'Escape') closeStrokeGuideModal();
});

if (typeof globalThis !== 'undefined') {
  globalThis.HANGEUL_STROKE_META = HANGEUL_STROKE_META;
  globalThis.HANGEUL_STROKE_SVG = HANGEUL_STROKE_SVG;
  globalThis.getJamoStrokeSvg = getJamoStrokeSvg;
  globalThis.renderJamoPartCard = renderJamoPartCard;
  globalThis.openStrokeGuideModal = openStrokeGuideModal;
  globalThis.closeStrokeGuideModal = closeStrokeGuideModal;
}
''')

print('Successfully generated js/hangeul_stroke_data.js. File size:', os.path.getsize('js/hangeul_stroke_data.js'), 'bytes')

