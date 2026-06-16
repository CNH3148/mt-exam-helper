import os
import json
import fitz
import glob
import re

def process_subject(pdf_path, json_path, output_img_dir):
    with open(json_path, "r", encoding="utf-8") as f:
        questions = json.load(f)
        
    doc = fitz.open(pdf_path)
    subject_name = os.path.basename(pdf_path).replace(".pdf", "").replace("_merge", "")
    
    print(f"Mapping images for {subject_name}...")
    
    q_index = 0 # Pointer to our questions array
    
    for i in range(len(doc)):
        page = doc.load_page(i)
        images = page.get_images()
        if not images:
            continue
            
        blocks = page.get_text("blocks")
        
        q_positions = []
        for b in blocks:
            text = b[4].strip()
            match = re.match(r'^(\d{1,2})\.', text)
            if match:
                q_num = int(match.group(1))
                q_positions.append((q_num, b[1]))
                
        if not q_positions:
            continue
            
        q_positions.sort(key=lambda x: x[1])
        
        for img_idx, img in enumerate(images):
            xref = img[0]
            rects = page.get_image_rects(xref)
            if not rects:
                continue
                
            img_y0 = rects[0].y0
            
            assigned_q_num = None
            for q in reversed(q_positions):
                if q[1] <= img_y0 + 10:
                    assigned_q_num = q[0]
                    break
                    
            if assigned_q_num is None:
                assigned_q_num = q_positions[0][0]
                
            # Extract and save image
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            ext = base_image["ext"]
            img_filename = f"{subject_name}_p{i}_q{assigned_q_num}_{img_idx}.{ext}"
            img_filepath = os.path.join(output_img_dir, img_filename)
            
            with open(img_filepath, "wb") as f:
                f.write(image_bytes)
                
            # Update the JSON
            # Find the exact question in the JSON. Because exams can have multiple page 10s, 
            # we look forward from q_index to find a question with `no == assigned_q_num` 
            # that is within a reasonable range (e.g. next 80 questions).
            found_idx = -1
            for search_idx in range(q_index, min(len(questions), q_index + 160)):
                if questions[search_idx]["no"] == assigned_q_num:
                    found_idx = search_idx
                    break
            
            if found_idx != -1:
                if "images" not in questions[found_idx]:
                    questions[found_idx]["images"] = []
                questions[found_idx]["images"].append(f"images/{img_filename}")
                # advance q_index slightly to prevent matching an old exam
                q_index = max(0, found_idx - 40) 

    # Save updated JSON
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)

def main():
    pdf_dir = r"C:\Users\star0\Desktop\刷題系統\歷屆考題"
    json_dir = r"C:\Users\star0\Desktop\刷題系統\app\data"
    output_img_dir = r"C:\Users\star0\Desktop\刷題系統\app\public\images"
    
    os.makedirs(output_img_dir, exist_ok=True)
    pdf_files = glob.glob(os.path.join(pdf_dir, "*.pdf"))
    
    for pdf_path in pdf_files:
        subject_name = os.path.basename(pdf_path).replace(".pdf", "").replace("_merge", "")
        json_path = os.path.join(json_dir, f"{subject_name}.json")
        if os.path.exists(json_path):
            process_subject(pdf_path, json_path, output_img_dir)
            
    print("Image mapping complete!")

if __name__ == "__main__":
    main()

