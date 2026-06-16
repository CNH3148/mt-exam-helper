import re

css_path = 'public/style.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

new_styles = """
/* Mode Buttons */
.mode-buttons .btn {
    opacity: 0.6;
    transition: all 0.2s;
    font-size: 13px;
}
.mode-buttons .btn.active {
    opacity: 1;
    background: var(--primary);
    color: white;
    border-color: var(--primary);
    font-weight: 600;
}

/* Dropdown Menu for Regex History */
.dropdown-menu {
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background: var(--bg-panel);
    border: 1px solid var(--glass-border);
    border-radius: 4px;
    z-index: 100;
    max-height: 150px;
    overflow-y: auto;
    box-shadow: 0 4px 6px rgba(0,0,0,0.3);
}
.dropdown-item {
    padding: 8px 12px;
    font-size: 13px;
    color: var(--text-main);
    cursor: pointer;
    transition: background 0.2s;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.dropdown-item:hover {
    background: rgba(255,255,255,0.1);
}
.dropdown-item .del-btn {
    color: var(--text-muted);
    font-size: 12px;
}
.dropdown-item .del-btn:hover {
    color: #ff4d4f;
}

/* Multi-select subject checkbox item */
.subject-multi-lbl {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 4px 0;
    cursor: pointer;
}
"""

if "/* Mode Buttons */" not in css:
    css += "\n" + new_styles
    with open(css_path, 'w', encoding='utf-8') as f:
        f.write(css)
print("CSS updated.")

