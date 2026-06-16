import os
import json
import fitz
import glob
import re
import shutil

def fix_image_mapping(pdf_path, json_path, img_dir):
    with open(json_path, "r", encoding="utf-8") as f:
        questions = json.load(f)
        
    doc = fitz.open(pdf_path)
    subject_name = os.path.basename(pdf_path).replace(".pdf", "").replace("_merge", "")
    print(f"Fixing images for {subject_name}...")
    
    # Get exam boundaries by finding answer key pages
    exams = []
    current_ans_page = -1
    current_q_pages = []
    for i in range(len(doc)):
        text = doc.load_page(i).get_text()
        if "測驗式試題標準答案" in text:
            if current_ans_page != -1 and current_q_pages:
                exams.append(current_q_pages)
            current_ans_page = i
            current_q_pages = []
        else:
            if current_ans_page != -1:
                current_q_pages.append(i)
    if current_ans_page != -1 and current_q_pages:
        exams.append(current_q_pages)
        
    for exam_idx, q_pages in enumerate(exams, 1):
        global_q_positions = []
        global_images = []
        
        for pid in q_pages:
            page = doc.load_page(pid)
            blocks = page.get_text("blocks")
            for b in blocks:
                text = b[4].strip()
                match = re.match(r'^(\d{1,2})\.', text)
                if match:
                    q_num = int(match.group(1))
                    abs_y = pid * 2000 + b[1]
                    global_q_positions.append((q_num, abs_y))
                    
            for img in page.get_images():
                xref = img[0]
                width, height = img[2], img[3]
                if width < 50 or height < 50:
                    continue
                rects = page.get_image_rects(xref)
                if rects:
                    abs_y = pid * 2000 + rects[0].y0
                    global_images.append((xref, abs_y, img[1], img[2], img[3])) # xref, abs_y, ext...
                    
        global_q_positions.sort(key=lambda x: x[1])
        global_images.sort(key=lambda x: x[1])
        
        img_mappings = {}
        for img_idx, img_tuple in enumerate(global_images):
            xref, abs_y = img_tuple[0], img_tuple[1]
            
            assigned_q_num = None
            for q in reversed(global_q_positions):
                if q[1] <= abs_y + 30: # 30 pixels tolerance
                    assigned_q_num = q[0]
                    break
            if assigned_q_num is None and global_q_positions:
                assigned_q_num = global_q_positions[0][0]
                
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            ext = base_image["ext"]
            img_filename = f"{subject_name}_exam{exam_idx}_q{assigned_q_num}_{img_idx}.{ext}"
            img_filepath = os.path.join(img_dir, img_filename)
            
            with open(img_filepath, "wb") as f:
                f.write(image_bytes)
                
            if assigned_q_num not in img_mappings:
                img_mappings[assigned_q_num] = []
            img_mappings[assigned_q_num].append(f"images/{img_filename}")
            
        # Now update the JSON for this exam_id
        for q in questions:
            if q["exam_id"] == exam_idx:
                q["images"] = img_mappings.get(q["no"], [])

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)
    print(f"Done {subject_name}")

def main():
    pdf_dir = r"C:\Users\star0\Desktop\刷題系統\歷屆考題"
    json_dir = r"C:\Users\star0\Desktop\刷題系統\app\data"
    img_dir = r"C:\Users\star0\Desktop\刷題系統\app\public\images"
    
    # Clear old images to prevent orphans
    for f in glob.glob(os.path.join(img_dir, "*")):
        os.remove(f)
        
    for pdf_path in glob.glob(os.path.join(pdf_dir, "*.pdf")):
        subject_name = os.path.basename(pdf_path).replace(".pdf", "").replace("_merge", "")
        json_path = os.path.join(json_dir, f"{subject_name}.json")
        if os.path.exists(json_path):
            fix_image_mapping(pdf_path, json_path, img_dir)

if __name__ == "__main__":
    main()

