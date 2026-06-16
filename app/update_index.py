import re

filepath = 'public/index.html'
with open(filepath, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Remove header practice actions
html = re.sub(r'<div style="display:flex; gap:8px; align-items:center;" id="header-practice-actions">.*?</div>', '', html, flags=re.DOTALL)

# 2. Remove advanced search button
html = re.sub(r'<button class="btn btn-secondary" onclick="openAdvancedSearchModal\(\)" id="btn-advanced-search".*?</button>', '', html, flags=re.DOTALL)

# 3. Remove advanced-search-modal
html = re.sub(r'<div class="modal" id="advanced-search-modal">.*?</div>\s*</div>', '', html, flags=re.DOTALL) # Need to be careful here
# A safer way to remove the modal is to find `<div class="modal" id="advanced-search-modal">` and remove until the next modal or the end of the <body>.
# Let's use a more precise regex for the modal.
modal_pattern = re.compile(r'<div class="modal" id="advanced-search-modal">.*?(?:<div class="modal"|</body>)', re.DOTALL)
match = modal_pattern.search(html)
if match:
    # We matched too much if it hit another modal. Let's just find the closing tag for the modal.
    # We know the modal structure has a few divs.
    # Alternatively, just let BeautifulSoup do it if bs4 is available, but we can't guarantee bs4.
    pass

# Let's do it manually via python string methods
start_idx = html.find('<div class="modal" id="advanced-search-modal">')
if start_idx != -1:
    end_idx = html.find('</div>\n    </div>', start_idx) # End of modal content
    if end_idx != -1:
        # also remove the final </div> for the modal
        end_idx = html.find('</div>', end_idx + 10)
        if end_idx != -1:
            html = html[:start_idx] + html[end_idx+6:]

# 4. We need to inject the batch tag UI into `#search-mode-tools`
search_mode_tools_html = """
                    <div id="search-mode-tools" style="display:none; flex-direction:column; gap:8px;">
                        <!-- Custom Tag Checkboxes -->
                        <div id="custom-tags-container" style="padding: 8px; background:var(--bg-lighter); border-radius:4px;">
                            <div style="font-size:12px; color:var(--text-muted); margin-bottom:8px;">自訂標籤 (可複選)</div>
                            <div id="custom-tags-checkboxes" style="display:flex; flex-direction:column; gap:4px; max-height:100px; overflow-y:auto;"></div>
                        </div>
                        
                        <!-- Regex Search with History -->
                        <div style="position:relative;">
                            <input type="text" id="regex-search-input" class="search-input" placeholder="Regex 搜尋..." style="width:100%; padding-right:24px;">
                            <span id="regex-history-toggle" style="position:absolute; right:8px; top:50%; transform:translateY(-50%); cursor:pointer; color:var(--text-muted);">▼</span>
                            <div id="regex-history-menu" class="dropdown-menu" style="display:none;"></div>
                        </div>
                        
                        <!-- Batch Tagging -->
                        <div style="display:flex; gap:4px; margin-top:4px;">
                            <input type="text" id="batch-tag-input" class="search-input" placeholder="批次標籤命名..." style="flex:1;">
                            <button class="btn btn-secondary btn-small" id="btn-batch-tag">套用</button>
                        </div>
                    </div>
"""

# Replace the existing `<div id="search-mode-tools"...</div>` with our new one
html = re.sub(r'<div id="search-mode-tools".*?(?=</div>\s*</aside>)', search_mode_tools_html, html, flags=re.DOTALL)
# Wait, the regex above is risky if it matches too much.
# Let's find <div id="search-mode-tools" and replace until it closes.
start_sm = html.find('<div id="search-mode-tools"')
if start_sm != -1:
    end_sm = html.find('</div>\n                </div>', start_sm) # End of filters
    if end_sm != -1:
        # Since it's inside <div class="filters">, the end of filters is '</div>\n            </aside>'
        pass

# Let's be safer and just replace the whole `.filters` block
filters_start = html.find('<div class="filters"')
filters_end = html.find('</aside>')
if filters_start != -1 and filters_end != -1:
    old_filters = html[filters_start:filters_end]
    new_filters = """<div class="filters" style="margin-top:16px; display: flex; flex-direction: column; gap: 8px;">
                    <!-- General Mode: Single Select -->
                    <select id="filter-subject" class="search-input">
                        <option value="">-- 請選擇科目 --</option>
                    </select>
                    
                    <!-- Other Modes: Multiple Select for Subjects -->
                    <div id="filter-subject-multi" class="search-input" style="display:none; height:auto; max-height:120px; overflow-y:auto; padding:8px; font-size:14px; background:var(--bg-lighter);">
                        <!-- Checkboxes injected here -->
                    </div>
                    
                    <!-- Year Checkboxes -->
                    <div id="filter-year-container" class="search-input" style="height: auto; max-height: 120px; overflow-y: auto; padding: 8px; font-size: 14px; display: none;">
                        <div style="color:var(--text-muted); font-size:12px;">請先選擇科目...</div>
                    </div>

                    <!-- Search/Tag Mode Specific Tools -->
                    <div id="search-mode-tools" style="display:none; flex-direction:column; gap:8px;">
                        <div id="custom-tags-container" style="padding: 8px; background:var(--bg-lighter); border-radius:4px;">
                            <div style="font-size:12px; color:var(--text-muted); margin-bottom:8px;">自訂標籤 (聯集)</div>
                            <div id="custom-tags-checkboxes" style="display:flex; flex-direction:column; gap:4px; max-height:100px; overflow-y:auto;"></div>
                        </div>
                        
                        <div style="position:relative;">
                            <input type="text" id="regex-search-input" class="search-input" placeholder="Regex / 關鍵字搜尋..." style="width:100%; padding-right:24px;">
                            <span id="regex-history-toggle" style="position:absolute; right:8px; top:50%; transform:translateY(-50%); cursor:pointer; color:var(--text-muted);">▼</span>
                            <div id="regex-history-menu" class="dropdown-menu" style="display:none; position:absolute; top:100%; left:0; right:0; background:var(--bg-panel); border:1px solid var(--glass-border); border-radius:4px; z-index:10; max-height:150px; overflow-y:auto;"></div>
                        </div>
                        
                        <div style="display:flex; gap:4px; margin-top:4px;">
                            <input type="text" id="batch-tag-input" class="search-input" placeholder="批次標籤命名..." style="flex:1; padding:4px 8px; font-size:13px;">
                            <button class="btn btn-secondary btn-small" id="btn-batch-tag">標記當前清單</button>
                        </div>
                    </div>
                </div>
            """
    html = html[:filters_start] + new_filters + "\n        " + html[filters_end:]

# 5. Remove original search input in the sidebar
html = re.sub(r'<input type="text" id="search-input".*?>', '', html)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated index.html")

