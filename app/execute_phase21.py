import re

with open("public/app.js", "r", encoding="utf-8") as f:
    app = f.read()

old_listener = """    searchInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            const q = searchInput.value.toLowerCase().trim();
            if (q) {
                let matched = [];
                currentData.forEach(question => {
                    const text = question.question + " " + question.choices.join(" ");
                    if (text.toLowerCase().includes(q)) matched.push(question);
                });
                if (matched.length > 0) {
                    currentActiveTopicData = matched;
                    currentPracticeMode = 'normal';
                    switchView('practice');
                    switchMode('list');
                    startPractice();
                }
            }
        }
    });"""

new_listener = """    searchInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            // Delay slightly to allow the 'input' event (e.g. from IME commit) to finish
            // processing applyFilters() which incorrectly resets the view to topic-list.
            setTimeout(() => {
                const q = searchInput.value.toLowerCase().trim();
                if (q) {
                    let matched = [];
                    currentData.forEach(question => {
                        const text = question.question + " " + question.choices.join(" ");
                        if (text.toLowerCase().includes(q)) matched.push(question);
                    });
                    if (matched.length > 0) {
                        currentActiveTopicData = matched;
                        currentPracticeMode = 'normal';
                        switchView('practice');
                        switchMode('list');
                        startPractice();
                    }
                }
            }, 50);
        }
    });"""

app = app.replace(old_listener, new_listener)

with open("public/app.js", "w", encoding="utf-8") as f:
    f.write(app)

print("Phase 21 executed.")

