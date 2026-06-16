import os

with open('public/app.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = lines[:1992]

new_lines.append('''
async function updateMultiYearCheckboxes() {
    filterYearContainer.innerHTML = '';
    filterYearContainer.style.display = 'block';
    
    const selectedSubjects = Array.from(document.querySelectorAll('.multi-subject-cb:checked')).map(cb => cb.value);
    if (selectedSubjects.length === 0) {
        filterYearContainer.innerHTML = '<div style="color:var(--text-muted); font-size:12px;">請先選擇科目...</div>';
        return;
    }
    
    filterYearContainer.innerHTML = '<div style="color:var(--text-muted); font-size:12px;">載入年份中...</div>';
    
    const allYears = new Set();
    for (let sub of selectedSubjects) {
        let subQuestions = [];
        try {
            const res = await fetch(`../data/${sub}.json?v=${Date.now()}`);
            if (res.ok) {
                subQuestions = await res.json();
                subQuestions.forEach(q => {
                    if (q.tags && q.tags.length > 0) {
                        const match = q.tags[0].match(/\\d{3}-\\d/);
                        if (match) allYears.add(match[0]);
                    }
                });
            }
        } catch(e) {}
    }
    
    filterYearContainer.innerHTML = '';
    
    const selectAllLbl = document.createElement('label');
    selectAllLbl.style.display = 'block';
    selectAllLbl.style.marginBottom = '8px';
    selectAllLbl.style.cursor = 'pointer';
    selectAllLbl.style.fontWeight = '600';
    selectAllLbl.style.borderBottom = '1px solid rgba(255,255,255,0.1)';
    selectAllLbl.style.paddingBottom = '8px';
    selectAllLbl.innerHTML = `<input type="checkbox" id="year-select-all-multi" checked style="margin-right:8px;"> 全選 / 全不選`;
    selectAllLbl.querySelector('input').addEventListener('change', (e) => {
        const isChecked = e.target.checked;
        document.querySelectorAll('.year-checkbox').forEach(cb => { cb.checked = isChecked; });
        applyFilters();
    });
    filterYearContainer.appendChild(selectAllLbl);

    const sortedYears = Array.from(allYears).sort((a,b) => b.toString().localeCompare(a.toString()));
    
    sortedYears.forEach(y => {
        const lbl = document.createElement('label');
        lbl.style.display = 'block';
        lbl.style.marginBottom = '6px';
        lbl.style.cursor = 'pointer';
        lbl.innerHTML = `<input type="checkbox" value="${y}" class="year-checkbox" checked style="margin-right:8px;"> ${y}`;
        lbl.querySelector('input').addEventListener('change', () => {
            const allChecked = Array.from(document.querySelectorAll('.year-checkbox')).every(cb => cb.checked);
            const selectAll = document.getElementById('year-select-all-multi');
            if(selectAll) selectAll.checked = allChecked;
            applyFilters();
        });
        filterYearContainer.appendChild(lbl);
    });
}
''')

new_lines.extend(lines[2089:])

with open('public/app.js', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

