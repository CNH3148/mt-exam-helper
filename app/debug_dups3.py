import json

def compare_exams():
    with open('data/微生物學與臨床微生物學.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    exam0 = [q for q in data if q['exam_id'] == 0]
    exam1 = [q for q in data if q['exam_id'] == 1]
    
    q0 = exam0[0]
    q1 = exam1[0]
    print("Exam 0 Q1:", q0['question'])
    print("Exam 1 Q1:", q1['question'])
    
    exam7 = [q for q in data if q['exam_id'] == 7]
    exam9 = [q for q in data if q['exam_id'] == 9]
    print("Exam 7 Q1:", exam7[0]['question'])
    print("Exam 9 Q1:", exam9[0]['question'])

compare_exams()

