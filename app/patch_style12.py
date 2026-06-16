css_append = """
/* Phase 12 Additions */
.btn {
    white-space: nowrap;
}

.tags-container {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 8px;
    margin-bottom: 8px;
}

.modal-content {
    display: flex;
    flex-direction: column;
    gap: 16px;
}

/* Two-column layout for advanced modal */
.adv-search-layout {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;
}

.adv-search-left {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.adv-search-right {
    background: var(--bg-lighter);
    padding: 12px;
    border-radius: 8px;
    border: 1px solid var(--glass-border);
    max-height: 250px;
    overflow-y: auto;
}

.star-icon {
    display: inline-block;
    transition: transform 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275), color 0.2s;
}
.star-icon.active {
    color: #facc15;
    text-shadow: 0 0 5px rgba(250, 204, 21, 0.5);
    transform: scale(1.15);
}
"""
with open("public/style.css", "a", encoding="utf-8") as f:
    f.write(css_append)
print("style.css patched.")

