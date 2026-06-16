import re
import sys

def main():
    filepath = 'public/app.js'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split to avoid modifying the helpers themselves
    # The helpers are defined right before `function loadSlotUI()`
    parts = content.split('function loadSlotUI() {')
    if len(parts) != 2:
        print("Error: Could not split at loadSlotUI")
        sys.exit(1)
        
    head = parts[0]
    tail = parts[1]

    # Replacements in tail
    
    # globalAnsweredState[q.exam_id + '_' + q.no] => getAnswerState(q)
    # Wait, the string is exactly `globalAnsweredState[q.exam_id + '_' + q.no]`
    tail = tail.replace("globalAnsweredState[q.exam_id + '_' + q.no]", "getAnswerState(q)")
    
    # globalAnsweredState[id] => (Wait, id is usually q.exam_id + '_' + q.no, but we need `q` to pass to getAnswerState)
    # In `updateAccuracy`, it is `const ans = globalAnsweredState[id];`
    # Let's use regex to replace specific patterns where `q` is available:
    tail = re.sub(r'const ans = globalAnsweredState\[id\];', r'const ans = getAnswerState(q);', tail)
    
    # In `startPractice`:
    # const id = q.exam_id + '_' + q.no;
    # if (globalAnsweredState[id]) {
    #     answeredState[i] = globalAnsweredState[id];
    # }
    tail = tail.replace("if (globalAnsweredState[id]) {\n                answeredState[i] = globalAnsweredState[id];", "if (getAnswerState(q)) {\n                answeredState[i] = getAnswerState(q);")
    
    # Card View Click Options:
    # if (!globalAnsweredState[qid]) {
    #     globalAnsweredState[qid] = { first_answer: letter, current_answer: letter, is_fixed: false };
    # } else {
    #     globalAnsweredState[qid].current_answer = letter;
    # }
    # if (currentPracticeMode === 'wrong' && letter === q.answer) {
    #     globalAnsweredState[qid].is_fixed = true;
    # }
    # answeredState[currentIndex] = globalAnsweredState[qid];
    #
    # We replace this block.
    old_card_ans = """if (!globalAnsweredState[qid]) {
                    globalAnsweredState[qid] = { first_answer: letter, current_answer: letter, is_fixed: false };
                } else {
                    globalAnsweredState[qid].current_answer = letter;
                }
                
                if (currentPracticeMode === 'wrong' && letter === q.answer) {
                    globalAnsweredState[qid].is_fixed = true;
                }
                
                answeredState[currentIndex] = globalAnsweredState[qid];"""
    
    new_card_ans = """let state = getAnswerState(q);
                if (!state) {
                    state = { first_answer: letter, current_answer: letter, is_fixed: false };
                } else {
                    state.current_answer = letter;
                }
                
                if (currentPracticeMode === 'wrong' && letter === q.answer) {
                    state.is_fixed = true;
                }
                
                setAnswerState(q, state);
                answeredState[currentIndex] = state;"""
    tail = tail.replace(old_card_ans, new_card_ans)
    
    # List View Click Options:
    # q is currentActiveTopicData[idx]
    old_list_ans = """if (!globalAnsweredState[qid]) {
        globalAnsweredState[qid] = { first_answer: selectedLetter, current_answer: selectedLetter, is_fixed: false };
    } else {
        globalAnsweredState[qid].current_answer = selectedLetter;
    }
    
    if (currentPracticeMode === 'wrong' && selectedLetter === currentActiveTopicData[idx].answer) {
        globalAnsweredState[qid].is_fixed = true;
    }
    
    answeredState[idx] = globalAnsweredState[qid];"""
    
    new_list_ans = """let q = currentActiveTopicData[idx];
    let state = getAnswerState(q);
    if (!state) {
        state = { first_answer: selectedLetter, current_answer: selectedLetter, is_fixed: false };
    } else {
        state.current_answer = selectedLetter;
    }
    
    if (currentPracticeMode === 'wrong' && selectedLetter === q.answer) {
        state.is_fixed = true;
    }
    
    setAnswerState(q, state);
    answeredState[idx] = state;"""
    tail = tail.replace(old_list_ans, new_list_ans)
    
    # Bookmarks
    tail = tail.replace("globalBookmarks.includes(q.exam_id + '_' + q.no)", "getBookmarkState(q)")
    
    # toggleBookmark
    old_toggle_bm = """window.toggleBookmark = function(e, exam_id, no) {
    e.stopPropagation();
    
    const id = exam_id + '_' + no;
    
    if (globalBookmarks.includes(id)) {
        globalBookmarks = globalBookmarks.filter(x => x !== id);
    } else {
        globalBookmarks.push(id);
    }
    saveProgress();"""
    
    new_toggle_bm = """window.toggleBookmark = function(e, exam_id, no) {
    e.stopPropagation();
    const q = currentData.find(x => x.exam_id == exam_id && x.no == no) || currentActiveTopicData.find(x => x.exam_id == exam_id && x.no == no);
    if (!q) return;
    
    const isBookmarked = getBookmarkState(q);
    setBookmarkState(q, !isBookmarked);
    saveProgress();"""
    tail = tail.replace(old_toggle_bm, new_toggle_bm)
    
    # wrongQs filter
    # const state = globalAnsweredState[id]; -> const state = getAnswerState(q);
    tail = tail.replace("const state = globalAnsweredState[id];\n        return state", "const state = getAnswerState(q);\n        return state")
    
    # bookmarkedQs filter
    tail = tail.replace("const bookmarkedQs = allQ.filter(q => globalBookmarks.includes(q.exam_id + '_' + q.no));", "const bookmarkedQs = allQ.filter(q => getBookmarkState(q));")
    
    # Custom tags rendering
    tail = tail.replace("globalCustomTags[t].includes(q.exam_id + '_' + q.no)", "getCustomTagIncludes(q, t)")
    
    # removeCustomTagFromQ
    old_remove_tag = """window.removeCustomTagFromQ = function(tag, exam_id, no) {
    const id = exam_id + '_' + no;
    if (globalCustomTags[tag]) {
        globalCustomTags[tag] = globalCustomTags[tag].filter(x => x !== id);
        if (globalCustomTags[tag].length === 0) delete globalCustomTags[tag];
        saveProgress();"""
    new_remove_tag = """window.removeCustomTagFromQ = function(tag, exam_id, no) {
    const q = currentData.find(x => x.exam_id == exam_id && x.no == no) || currentActiveTopicData.find(x => x.exam_id == exam_id && x.no == no);
    if (!q) return;
    removeCustomTagState(q, tag);
    saveProgress();"""
    tail = tail.replace(old_remove_tag, new_remove_tag)
    
    # saveUserExplanation
    old_save_exp = """window.saveUserExplanation = function(exam_id, no, val) {
    const id = exam_id + '_' + no;
    globalExplanations[id] = val;
    saveProgress();
};"""
    new_save_exp = """window.saveUserExplanation = function(exam_id, no, val) {
    const q = currentData.find(x => x.exam_id == exam_id && x.no == no) || currentActiveTopicData.find(x => x.exam_id == exam_id && x.no == no);
    if (!q) return;
    setExplanationState(q, val);
    saveProgress();
};"""
    tail = tail.replace(old_save_exp, new_save_exp)
    
    # addManualCustomTag
    old_add_tag_1 = """window.addManualCustomTag = function(exam_id, no, val) {
    if (!val) return;
    
    if (!globalCustomTags[val]) globalCustomTags[val] = [];
    const id = exam_id + '_' + no;
    if (!globalCustomTags[val].includes(id)) {
        globalCustomTags[val].push(id);
        saveProgress();"""
    new_add_tag_1 = """window.addManualCustomTag = function(exam_id, no, val) {
    if (!val) return;
    const q = currentData.find(x => x.exam_id == exam_id && x.no == no) || currentActiveTopicData.find(x => x.exam_id == exam_id && x.no == no);
    if (!q) return;
    addCustomTagState(q, val);
    saveProgress();"""
    tail = tail.replace(old_add_tag_1, new_add_tag_1)
    
    # addManualTag
    old_add_tag_2 = """window.addManualTag = function(exam_id, no) {
    const input = document.getElementById(`manual-tag-${exam_id}-${no}`);
    const tag = input.value.trim();
    if (!tag) return;
    
    if (!globalCustomTags[tag]) globalCustomTags[tag] = [];
    const id = exam_id + '_' + no;
    if (!globalCustomTags[tag].includes(id)) {
        globalCustomTags[tag].push(id);
        saveProgress();"""
    new_add_tag_2 = """window.addManualTag = function(exam_id, no) {
    const input = document.getElementById(`manual-tag-${exam_id}-${no}`);
    const tag = input.value.trim();
    if (!tag) return;
    const q = currentData.find(x => x.exam_id == exam_id && x.no == no) || currentActiveTopicData.find(x => x.exam_id == exam_id && x.no == no);
    if (!q) return;
    addCustomTagState(q, tag);
    saveProgress();"""
    tail = tail.replace(old_add_tag_2, new_add_tag_2)

    # globalExplanations[q.exam_id + '_' + q.no]
    tail = tail.replace("globalExplanations[q.exam_id + '_' + q.no]", "getExplanationState(q)")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(head + 'function loadSlotUI() {' + tail)

    print("Replacement complete.")

if __name__ == '__main__':
    main()

