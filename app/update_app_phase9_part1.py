import re
import os

with open("public/app.js", "r", encoding="utf-8") as f:
    content = f.read()

# --- 1. State Variables & Migration ---
state_vars_old = """let currentSaveSlot = null;
let globalAnsweredState = {};"""

state_vars_new = """let currentSaveSlot = null;
let globalAnsweredState = {}; // { id: { first_answer: 'A', current_answer: 'B', is_fixed: false } }
let globalBookmarks = []; // [ "id1", "id2" ]
let globalCustomTags = {}; // { "tag_name": ["id1", "id2"] }
let globalExplanations = {}; // { "id1": "user explanation" }
let currentPracticeMode = 'normal'; // 'normal', 'wrong', 'bookmark'"""

content = content.replace(state_vars_old, state_vars_new)

# --- 2. selectSlot & saveProgress ---
select_slot_old = """window.selectSlot = function(slot) {
    currentSaveSlot = slot;
    const dataStr = localStorage.getItem('save_slot_' + slot);
    globalAnsweredState = dataStr ? JSON.parse(dataStr) : {};
    document.getElementById('slot-selection-modal').style.display = 'none';
    if (filterSubject.value) applyFilters(); // refresh dashboard if already loaded
};"""

select_slot_new = """window.selectSlot = function(slot) {
    currentSaveSlot = slot;
    const dataStr = localStorage.getItem('save_slot_' + slot);
    const data = dataStr ? JSON.parse(dataStr) : {};
    
    globalAnsweredState = data.answers || {};
    globalBookmarks = data.bookmarks || [];
    globalCustomTags = data.customTags || {};
    globalExplanations = data.explanations || {};
    
    // Migration logic for older string-based answers
    for (let k in globalAnsweredState) {
        if (typeof globalAnsweredState[k] === 'string') {
            globalAnsweredState[k] = {
                first_answer: globalAnsweredState[k],
                current_answer: globalAnsweredState[k],
                is_fixed: false
            };
        }
    }
    
    document.getElementById('slot-selection-modal').style.display = 'none';
    renderCustomTagsSidebar();
    if (filterSubject.value) applyFilters(); 
};"""

content = content.replace(select_slot_old, select_slot_new)

save_prog_old = """function saveProgress() {
    if (currentSaveSlot) {
        localStorage.setItem('save_slot_' + currentSaveSlot, JSON.stringify(globalAnsweredState));
    }
}"""

save_prog_new = """function saveProgress() {
    if (currentSaveSlot) {
        const payload = {
            answers: globalAnsweredState,
            bookmarks: globalBookmarks,
            customTags: globalCustomTags,
            explanations: globalExplanations
        };
        localStorage.setItem('save_slot_' + currentSaveSlot, JSON.stringify(payload));
    }
}"""
content = content.replace(save_prog_old, save_prog_new)

# resetSlot also needs to clear
reset_old = """if (currentSaveSlot === slot) {
            globalAnsweredState = {};
            if (filterSubject.value) applyFilters();
        }"""
reset_new = """if (currentSaveSlot === slot) {
            globalAnsweredState = {}; globalBookmarks = []; globalCustomTags = {}; globalExplanations = {};
            renderCustomTagsSidebar();
            if (filterSubject.value) applyFilters();
        }"""
content = content.replace(reset_old, reset_new)

# --- 3. Completion Meter & startPractice ---
meter_old = """        if (globalAnsweredState[id] === q.answer) {
            correctCount++;
        }"""
meter_new = """        const ans = globalAnsweredState[id];
        if (ans && ans.current_answer === q.answer) {
            correctCount++;
        }"""
content = content.replace(meter_old, meter_new)

start_prac_old = """answeredState = {};
    currentActiveTopicData.forEach((q, i) => {
        const id = q.exam_id + '_' + q.no;
        if (globalAnsweredState[id]) {
            answeredState[i] = globalAnsweredState[id];
        }
    });"""
start_prac_new = """answeredState = {};
    currentActiveTopicData.forEach((q, i) => {
        const id = q.exam_id + '_' + q.no;
        if (globalAnsweredState[id]) {
            // Keep the whole object so we can show first_answer in UI if needed
            answeredState[i] = globalAnsweredState[id];
        }
    });"""
content = content.replace(start_prac_old, start_prac_new)

# --- 4. Answer Logic ---
list_opt_old = """answeredState[idx] = selectedLetter;
    globalAnsweredState[currentActiveTopicData[idx].exam_id + '_' + currentActiveTopicData[idx].no] = selectedLetter;
    saveProgress();"""
list_opt_new = """
    const qid = currentActiveTopicData[idx].exam_id + '_' + currentActiveTopicData[idx].no;
    if (!globalAnsweredState[qid]) {
        globalAnsweredState[qid] = { first_answer: selectedLetter, current_answer: selectedLetter, is_fixed: false };
    } else {
        globalAnsweredState[qid].current_answer = selectedLetter;
    }
    
    if (currentPracticeMode === 'wrong' && selectedLetter === currentActiveTopicData[idx].answer) {
        globalAnsweredState[qid].is_fixed = true;
    }
    
    answeredState[idx] = globalAnsweredState[qid];
    saveProgress();"""
content = content.replace(list_opt_old, list_opt_new)

card_opt_old = """answeredState[currentIndex] = letter;
                globalAnsweredState[q.exam_id + '_' + q.no] = letter;
                saveProgress();"""
card_opt_new = """const qid = q.exam_id + '_' + q.no;
                if (!globalAnsweredState[qid]) {
                    globalAnsweredState[qid] = { first_answer: letter, current_answer: letter, is_fixed: false };
                } else {
                    globalAnsweredState[qid].current_answer = letter;
                }
                
                if (currentPracticeMode === 'wrong' && letter === q.answer) {
                    globalAnsweredState[qid].is_fixed = true;
                }
                
                answeredState[currentIndex] = globalAnsweredState[qid];
                saveProgress();"""
content = content.replace(card_opt_old, card_opt_new)

# update UI logic (card)
card_ui_old = """const userAns = answeredState[currentIndex];
        const isAnswered = !!userAns;
        
        let optionsHtml = '';
        q.choices.forEach(choice => {
            const letter = choice.substring(0, 1);
            let optionClass = 'option';
            
            if (isAnswered) {
                if (letter === q.answer) {
                    optionClass += ' correct';
                } else if (letter === userAns && userAns !== q.answer) {
                    optionClass += ' incorrect';
                } else {
                    optionClass += ' disabled';
                }
            }"""
card_ui_new = """const userAnsObj = answeredState[currentIndex];
        const isAnswered = !!userAnsObj;
        
        let optionsHtml = '';
        q.choices.forEach(choice => {
            const letter = choice.substring(0, 1);
            let optionClass = 'option';
            
            if (isAnswered) {
                if (letter === q.answer) {
                    optionClass += ' correct';
                } else if (letter === userAnsObj.first_answer && userAnsObj.first_answer !== q.answer) {
                    // Show their FIRST mistake if normal mode. If wrong mode, just show current.
                    // Wait, let's just show current_answer as red if wrong.
                    if (letter === userAnsObj.current_answer) optionClass += ' incorrect';
                    else optionClass += ' disabled';
                } else {
                    optionClass += ' disabled';
                }
            }"""
content = content.replace(card_ui_old, card_ui_new)

# update UI logic (list)
list_ui_old = """const isAnswered = !!answeredState[idx];
            let optionClass = 'list-option';
            if (isAnswered) {
                if (letter === q.answer) {
                    optionClass += ' correct';
                } else if (letter === answeredState[idx] && answeredState[idx] !== q.answer) {
                    optionClass += ' incorrect';
                }
            }"""
list_ui_new = """const userAnsObj = answeredState[idx];
            const isAnswered = !!userAnsObj;
            let optionClass = 'list-option';
            if (isAnswered) {
                if (letter === q.answer) {
                    optionClass += ' correct';
                } else if (letter === userAnsObj.current_answer && userAnsObj.current_answer !== q.answer) {
                    optionClass += ' incorrect';
                }
            }"""
content = content.replace(list_ui_old, list_ui_new)


with open("public/app.js", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated app.js part 1 successfully.")

