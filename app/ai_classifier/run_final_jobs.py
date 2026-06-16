import os
import subprocess
import sys

print("Starting final jobs...")
env = os.environ.copy()
env['PYTHONUTF8'] = "1"

uv_path = r"C:\Users\star0\.local\bin\uv.exe"

try:
    print("Re-summarizing microbiology...")
    subprocess.run([uv_path, "run", "--with", "google-generativeai", "python", "cluster_summarize.py", "微生物學與臨床微生物學"], env=env, check=True)

    print("Running pipeline for molecular/microscopy...")
    subprocess.run([uv_path, "run", "--with", "google-generativeai", "python", "run_subject.py", "醫學分子檢驗學與臨床鏡檢學"], env=env, check=True)

    print("All tasks completed successfully!")
except Exception as e:
    print(f"Error occurred: {e}")
    sys.exit(1)

