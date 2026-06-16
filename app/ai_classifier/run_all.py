import sys
import run_subject

subjects = [
    "生物化學與臨床生化學",
    "臨床生理學與病理學",
    "臨床血液學與血庫學",
    "臨床血清免疫學與臨床病毒學",
    "醫學分子檢驗學與臨床鏡檢學"
]

def main():
    print("Starting batch analysis for all 5 subjects...")
    for sub in subjects:
        try:
            run_subject.main(sub)
        except Exception as e:
            print(f"Error analyzing {sub}: {e}")

if __name__ == "__main__":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    main()

