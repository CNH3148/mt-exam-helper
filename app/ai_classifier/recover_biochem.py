import json

data_path = r"C:\Users\star0\Desktop\刷題系統\app\data\生物化學與臨床生化學.json"
topics_path = r"C:\Users\star0\Desktop\刷題系統\app\data\topics_生物化學與臨床生化學.json"
tax_path = r"C:\Users\star0\Desktop\刷題系統\app\data\taxonomy_生物化學與臨床生化學.json"

# Load the completed summaries
with open(topics_path, "r", encoding="utf-8") as f:
    topics_data = json.load(f)

old_topic_names = list(topics_data.keys())

# Create a restored taxonomy
restored_tax = [{"topic": name, "definition": "Restored"} for name in old_topic_names]
with open(tax_path, "w", encoding="utf-8") as f:
    json.dump(restored_tax, f, ensure_ascii=False, indent=2)

print(f"Restored taxonomy with {len(old_topic_names)} topics.")

# Check the questions
with open(data_path, "r", encoding="utf-8") as f:
    qs = json.load(f)

invalid = [q for q in qs if q.get("topic") not in old_topic_names]
print(f"Questions needing classification: {len(invalid)}")

