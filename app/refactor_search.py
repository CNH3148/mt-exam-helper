import re

with open('app/public/app.js', 'r', encoding='utf-8') as f:
    code = f.read()

# Replace applyFilters() calls in checkbox onchange handlers
code = re.sub(
    r'cb\.onchange = \(\) => applyFilters\(\);',
    r"cb.onchange = () => { if (currentMode !== 'search') applyFilters(); };",
    code
)
code = re.sub(
    r"selectAllLbl\.querySelector\('input'\)\.addEventListener\('change', \(e\) => \{\n\s*const isChecked = e\.target\.checked;\n\s*document\.querySelectorAll\('\.year-checkbox'\)\.forEach\(cb => \{ cb\.checked = isChecked; \}\);\n\s*applyFilters\(\);\n\s*\}\);",
    r"selectAllLbl.querySelector('input').addEventListener('change', (e) => {\n            const isChecked = e.target.checked;\n            document.querySelectorAll('.year-checkbox').forEach(cb => { cb.checked = isChecked; });\n            if (currentMode !== 'search') applyFilters();\n        });",
    code
)
code = re.sub(
    r"lbl\.querySelector\('input'\)\.addEventListener\('change', \(\) => \{\n\s*const allChecked = Array\.from\(document\.querySelectorAll\('\.year-checkbox'\)\)\.every\(cb => cb\.checked\);\n\s*document\.getElementById\('year-select-all'\)\.checked = allChecked;\n\s*applyFilters\(\);\n\s*\}\);",
    r"lbl.querySelector('input').addEventListener('change', () => {\n                const allChecked = Array.from(document.querySelectorAll('.year-checkbox')).every(cb => cb.checked);\n                document.getElementById('year-select-all').checked = allChecked;\n                if (currentMode !== 'search') applyFilters();\n            });",
    code
)
code = re.sub(
    r"const selectAllCb = selectAllLbl\.querySelector\('input'\);\n\s*selectAllCb\.addEventListener\('change', \(e\) => \{\n\s*const isChecked = e\.target\.checked;\n\s*document\.querySelectorAll\('\.multi-subject-cb'\)\.forEach\(cb => cb\.checked = isChecked\);\n\s*applyFilters\(\);\n\s*\}\);",
    r"const selectAllCb = selectAllLbl.querySelector('input');\n        selectAllCb.addEventListener('change', (e) => {\n            const isChecked = e.target.checked;\n            document.querySelectorAll('.multi-subject-cb').forEach(cb => cb.checked = isChecked);\n            if (currentMode !== 'search') applyFilters();\n        });",
    code
)
code = re.sub(
    r"lbl\.querySelector\('input'\)\.addEventListener\('change', \(\) => \{\n\s*const allChecked = Array\.from\(document\.querySelectorAll\('\.multi-subject-cb'\)\)\.every\(cb => cb\.checked\);\n\s*document\.getElementById\('multi-subject-select-all'\)\.checked = allChecked;\n\s*applyFilters\(\);\n\s*\}\);",
    r"lbl.querySelector('input').addEventListener('change', () => {\n                const allChecked = Array.from(document.querySelectorAll('.multi-subject-cb')).every(cb => cb.checked);\n                document.getElementById('multi-subject-select-all').checked = allChecked;\n                if (currentMode !== 'search') applyFilters();\n            });",
    code
)

# And add event listener for btn-search-execute
btn_init = """
const btnSearchExecute = document.getElementById('btn-search-execute');
if (btnSearchExecute) {
    btnSearchExecute.addEventListener('click', () => {
        const val = regexInput ? regexInput.value.trim() : '';
        if (val) {
            const history = JSON.parse(localStorage.getItem('regexHistory') || '[]');
            if (!history.includes(val)) {
                history.unshift(val);
                if (history.length > 20) history.pop();
                localStorage.setItem('regexHistory', JSON.stringify(history));
            }
        }
        applyFilters();
    });
}
"""

# inject at the end where we have event listeners
code = re.sub(r'(if \(btnBatchTag\) \{)', btn_init + r'\n\1', code)

with open('app/public/app.js', 'w', encoding='utf-8') as f:
    f.write(code)

print("Updated app.js")

