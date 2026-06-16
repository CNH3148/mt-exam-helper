import fitz
import re

pdf_path = r"C:\Users\star0\Desktop\刷題系統\歷屆考題\微生物學與臨床微生物學_merge.pdf"
doc = fitz.open(pdf_path)

# Page 0 is an answer key
page = doc.load_page(0)
text = page.get_text()

print("RAW TEXT:")
print(text[:500])

# Full-width to half-width translation for ABCD
trans = str.maketrans("ＡＢＣＤ", "ABCD")
text = text.translate(trans)

# Let's find all A, B, C, D that stand alone on a line or are attached to "答案"
lines = text.split('\n')
answers = []
for line in lines:
    line = line.strip()
    if line in ['A', 'B', 'C', 'D']:
        answers.append(line)
    elif line.startswith('答案'):
        ans = line.replace('答案', '').strip()
        if ans in ['A', 'B', 'C', 'D']:
            answers.append(ans)
            
print(f"\nExtracted {len(answers)} answers.")
print(answers)

