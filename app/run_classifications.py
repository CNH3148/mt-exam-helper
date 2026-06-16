import subprocess
import os

subjects = [
    "臨床生理學與病理學",
    "臨床血液學與血庫學",
    "醫學分子檢驗學與臨床鏡檢學",
    "微生物學與臨床微生物學",
    "臨床血清免疫學與臨床病毒學"
]

uv_path = r"C:\Users\star0\.local\bin\uv.exe"

print("Starting batch classification for all remaining subjects...")
for subject in subjects:
    print(f"\n==========================================")
    print(f"Launching enhanced_classify for {subject}")
    print(f"==========================================")
    
    result = subprocess.run([
        uv_path, "run", "--with", "google-genai", "--with", "pydantic",
        "python", "-u", "app/enhanced_classify.py", subject
    ], capture_output=False)
    
    if result.returncode != 0:
        print(f"Error running classification for {subject}!")
    else:
        print(f"Finished classification for {subject}.")
        
print("\nAll classifications completed!")

