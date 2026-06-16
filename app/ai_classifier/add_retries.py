import os

helper_code = """
import random
import time
def generate_with_retry(model, prompt, max_retries=10, initial_delay=5):
    delay = initial_delay
    for i in range(max_retries):
        try:
            return model.generate_content(prompt)
        except Exception as e:
            err_msg = str(e)
            if "429" in err_msg or "ResourceExhausted" in err_msg or "Quota" in err_msg:
                if i == max_retries - 1:
                    raise e
                sleep_time = delay + random.uniform(0, 2)
                print(f"API Rate limit hit. Retrying in {sleep_time:.2f} seconds... (Attempt {i+1}/{max_retries})")
                time.sleep(sleep_time)
                delay *= 1.5  # Exponential backoff
            else:
                raise e
"""

files_to_patch = [
    r"C:\Users\star0\Desktop\刷題系統\app\ai_classifier\cluster_classify.py",
    r"C:\Users\star0\Desktop\刷題系統\app\ai_classifier\cluster_summarize.py",
    r"C:\Users\star0\Desktop\刷題系統\app\ai_classifier\cluster_taxonomy.py"
]

for file_path in files_to_patch:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    if "def generate_with_retry" not in content:
        # Insert helper after imports
        content = content.replace("import google.generativeai as genai", "import google.generativeai as genai\n" + helper_code)
        
        # Replace the call
        content = content.replace("response = model.generate_content(prompt)", "response = generate_with_retry(model, prompt)")
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Patched {os.path.basename(file_path)}")
    else:
        print(f"Already patched {os.path.basename(file_path)}")

