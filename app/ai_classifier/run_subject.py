import sys
import subprocess
import os

def run_script(script_name, subject_name):
    print(f"--- Starting {script_name} for {subject_name} ---")
    
    env = os.environ.copy()
    env["SUBJECT_NAME"] = subject_name
    env["PYTHONIOENCODING"] = "utf-8"
    
    # Do not capture output, let it flow to stdout/stderr directly
    result = subprocess.run([
        "C:\\Users\\star0\\.local\\bin\\uv.exe", "run", "--with", "google-generativeai", "python", script_name
    ], env=env)
        
    if result.returncode != 0:
        print(f"FAILED {script_name}")
        raise RuntimeError(f"FAILED {script_name}")

def main(subject_name):
    run_script("cluster_taxonomy.py", subject_name)
    run_script("cluster_classify.py", subject_name)
    run_script("cluster_summarize.py", subject_name)
    print(f"=== ALL DONE for {subject_name} ===")

if __name__ == "__main__":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sub = os.environ.get("SUBJECT_NAME")
    if len(sys.argv) > 1 and sys.argv[1].strip():
        sub = sys.argv[1]
    if sub:
        main(sub)
    else:
        print("Subject name required.")

