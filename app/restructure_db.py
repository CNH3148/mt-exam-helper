import json
import glob
import os

CHUNKS_TO_YEAR = {
    0: "115-1", 1: "114-2", 2: "114-1", 3: "113-2", 4: "113-1",
    5: "112-2", 6: "112-1", 7: "111-2", 8: "111-1", 9: "110-2", 10: "110-1"
}

SUBJECT_TO_ID = {
    "臨床生理學與病理學": 1,
    "臨床血液學與血庫學": 2,
    "醫學分子檢驗學與臨床鏡檢學": 3,
    "微生物學與臨床微生物學": 4,
    "生物化學與臨床生化學": 5,
    "臨床血清免疫學與臨床病毒學": 6
}

def clean_and_restructure():
    files = glob.glob('app/data/*.json')
    
    for f in files:
        basename = os.path.basename(f)
        if basename.startswith('saved_') or basename.startswith('taxonomy_') or basename.startswith('topics_'):
            continue
            
        subject_name = basename.replace('.json', '')
        if subject_name not in SUBJECT_TO_ID:
            continue
            
        print(f"Processing {subject_name}...")
        
        with open(f, 'r', encoding='utf-8') as file:
            try:
                data = json.load(file)
            except Exception as e:
                print(f"Error loading {f}: {e}")
                continue
                
        # To verify chunks
        chunk_count = {}
        for q in data:
            chunk_idx = q.get('exam_id')
            if chunk_idx is not None and isinstance(chunk_idx, int) and chunk_idx <= 10:
                chunk_count[chunk_idx] = chunk_count.get(chunk_idx, 0) + 1
        
        # Now apply the restructure
        new_data = []
        unique_tags_check = set()
        duplicate_count = 0
        
        for q in data:
            # Determine chunk_idx (it might be in exam_id if we haven't overwritten it yet)
            chunk_idx = q.get('exam_id')
            if chunk_idx is None or chunk_idx > 10:
                # Fallback if already overwritten? Shouldn't happen on fresh DB
                print("Warning: unexpected exam_id", chunk_idx)
                continue
                
            true_year = CHUNKS_TO_YEAR[chunk_idx]
            q_no = q.get('no')
            
            # 1. Add year
            q['year'] = true_year
            
            # 2. Update exam_id to Subject ID
            q['exam_id'] = SUBJECT_TO_ID[subject_name]
            
            # 3. Clean and fix tags
            new_tags = []
            auto_tag = f"{true_year}-{subject_name}-{q_no}"
            
            for t in q.get('tags', []):
                # Remove any existing auto-tag (matches standard format roughly)
                # It usually starts with 11x-x and has the subject name
                if t.startswith('1') and '-' in t and subject_name in t:
                    pass # Drop it
                else:
                    new_tags.append(t)
                    
            # Insert the guaranteed correct auto-tag at the front
            new_tags.insert(0, auto_tag)
            q['tags'] = new_tags
            
            if auto_tag in unique_tags_check:
                duplicate_count += 1
            unique_tags_check.add(auto_tag)
            
            new_data.append(q)
            
        print(f"  Total processed: {len(new_data)}")
        print(f"  Unique strict tags: {len(unique_tags_check)}")
        print(f"  Duplicates found: {duplicate_count}")
        
        # Write back
        with open(f, 'w', encoding='utf-8') as out_file:
            json.dump(new_data, out_file, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    clean_and_restructure()

