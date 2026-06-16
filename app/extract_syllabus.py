import pypdf

pdf_path = r"C:\Users\star0\.gemini\antigravity\brain\67ba8e5b-436e-4a35-a02e-6ba03074e5f2\.tempmediaStorage\aa2f23506665eda3.pdf"
out_path = r"C:\Users\star0\Desktop\刷題系統\app\data\syllabus.txt"

text = ""
with open(pdf_path, "rb") as f:
    reader = pypdf.PdfReader(f)
    for page in reader.pages:
        text += page.extract_text() + "\n"

with open(out_path, "w", encoding="utf-8") as f:
    f.write(text)

print(f"Extracted syllabus text to {out_path}")

