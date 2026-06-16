import re

filepath = 'public/app.js'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Define the observer at the end of the global variables / DOM declarations
# Let's insert it after `const viewTopicDetail = document.getElementById('view-topic-detail');`
observer_code = """
let breadcrumbObserver = null;
function initBreadcrumbObserver() {
    if (breadcrumbObserver) return;
    breadcrumbObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const sub = entry.target.getAttribute('data-subject');
                const topic = entry.target.getAttribute('data-topic');
                if (sub && topic) {
                    bcSubject.textContent = sub;
                    bcSubject.style.display = 'inline';
                    bcSepTopic.style.display = 'inline';
                    bcTopic.textContent = `🏷️ ${topic}`;
                    bcTopic.style.display = 'inline';
                }
            }
        });
    }, { root: null, rootMargin: '-20% 0px -70% 0px' });
}
"""
content = content.replace("const viewTopicDetail = document.getElementById('view-topic-detail');", "const viewTopicDetail = document.getElementById('view-topic-detail');\n" + observer_code)

# 2. Update renderListView
# Find `listContainer.innerHTML = '';`
# We need to add initBreadcrumbObserver(); breadcrumbObserver.disconnect();
content = content.replace("listContainer.innerHTML = '';\n    const letters = ['A', 'B', 'C', 'D'];", "listContainer.innerHTML = '';\n    const letters = ['A', 'B', 'C', 'D'];\n    initBreadcrumbObserver();\n    breadcrumbObserver.disconnect();")

# Add data-subject and data-topic to `card`
# card.className = 'list-card';
# card.id = 'list-card-' + idx;
card_injection = """        card.className = 'list-card';
        card.id = 'list-card-' + idx;
        card.setAttribute('data-subject', q.subject || currentActiveSubject);
        card.setAttribute('data-topic', q.topic || currentTopicName);"""
content = content.replace("        card.className = 'list-card';\n        card.id = 'list-card-' + idx;", card_injection)

# Observe the card at the end of the loop
# listContainer.appendChild(card);
content = content.replace("        listContainer.appendChild(card);\n    });", "        listContainer.appendChild(card);\n        breadcrumbObserver.observe(card);\n    });")

# 3. Update renderCardView
# In renderCardView, after `const q = currentActiveTopicData[currentIndex];`
# We set the breadcrumb directly.
old_card_q = "const q = currentActiveTopicData[currentIndex];\n    \n    currentCardId = q.exam_id + '_' + q.no;"
new_card_q = """const q = currentActiveTopicData[currentIndex];
    
    // Update breadcrumb for card mode
    const sub = q.subject || currentActiveSubject;
    const top = q.topic || currentTopicName;
    bcSubject.textContent = sub;
    bcSubject.style.display = 'inline';
    bcSepTopic.style.display = 'inline';
    bcTopic.textContent = `🏷️ ${top}`;
    bcTopic.style.display = 'inline';
    
    currentCardId = q.exam_id + '_' + q.no;"""
content = content.replace(old_card_q, new_card_q)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Breadcrumb observer injected.")

