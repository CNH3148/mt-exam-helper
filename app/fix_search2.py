import re

with open('app/public/app.js', 'r', encoding='utf-8') as f:
    code = f.read()

# Fix currentMode -> globalPracticeMode
code = code.replace("if (currentMode !== 'search') applyFilters();", "if (globalPracticeMode !== 'search') applyFilters();")

# Also check for globalMode (if I had used it)
code = code.replace("if (globalMode !== 'search') applyFilters();", "if (globalPracticeMode !== 'search') applyFilters();")

# Modify switchGlobalMode
# Replace the end of switchGlobalMode
old_block = """    currentSubjectTitle.style.display = 'none';
    
    applyFilters();
}"""

new_block = """    currentSubjectTitle.style.display = 'none';
    
    if (mode === 'search') {
        filteredData = [];
        renderListView(); // Just render empty list, waiting for user to click Search
    } else {
        applyFilters();
    }
}"""

code = code.replace(old_block, new_block)

with open('app/public/app.js', 'w', encoding='utf-8') as f:
    f.write(code)

print("Fixed currentMode and switchGlobalMode in app.js")

