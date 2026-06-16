css_append = """
/* Phase 11 additions */
.tags-container {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 8px;
    margin-bottom: 8px;
}

.tags-container .badge {
    margin: 0;
}

.manual-tag-input {
    background: transparent;
    border: none;
    color: var(--text-main);
    outline: none;
    font-size: 13px;
    width: 100px;
    padding: 2px 4px;
    border-bottom: 1px dashed var(--glass-border);
    transition: all 0.2s;
}

.manual-tag-input:focus {
    border-bottom: 1px solid var(--primary);
    width: 150px;
}

.star-icon {
    display: inline-block;
    transition: transform 0.2s, color 0.2s;
}
.star-icon:active {
    transform: scale(1.5);
}
.star-icon.active {
    color: #facc15;
    text-shadow: 0 0 5px rgba(250, 204, 21, 0.5);
}
.star-icon.inactive {
    color: var(--text-muted);
}
"""

with open("public/style.css", "a", encoding="utf-8") as f:
    f.write(css_append)
print("CSS patched.")

