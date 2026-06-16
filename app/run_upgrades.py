import subprocess
import sys

SUBJECTS = [
    '臨床血液學與血庫學',
    '醫學分子檢驗學與臨床鏡檢學',
    '微生物學與臨床微生物學',
    '臨床血清免疫學與臨床病毒學'
]

for sub in SUBJECTS:
    print(f"Running upgrade for {sub}...")
    subprocess.run(["C:\\Users\\star0\\.local\\bin\\uv.exe", "run", "--with", "google-genai", "--with", "pydantic", "python", "-u", "app\\upgrade_db_keys.py", sub])
    print(f"Finished upgrade for {sub}.")

