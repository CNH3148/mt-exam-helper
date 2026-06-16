import fitz
import os
import re

pdf_path = r"C:\Users\star0\Desktop\刷題系統\歷屆考題\微生物學與臨床微生物學_merge.pdf"
doc = fitz.open(pdf_path)

print("Scanning for images in the first exam...")
for page_num in range(1, 16): # exam questions page
    page = doc.load_page(page_num)
    images = page.get_images()
    if images:
        print(f"Page {page_num} has {len(images)} images.")
        for img_idx, img in enumerate(images):
            xref = img[0]
            # Try to get bbox
            rects = page.get_image_rects(xref)
            if rects:
                print(f"  Image {img_idx} (xref {xref}) is at {rects[0]}")
                
            # Extract image
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            ext = base_image["ext"]
            img_path = f"test_img_p{page_num}_{img_idx}.{ext}"
            with open(img_path, "wb") as f:
                f.write(image_bytes)
                
    # Also list text blocks
    blocks = page.get_text("blocks")
    for b in blocks:
        # b[4] is text, b[0]-b[3] is rect
        text = b[4].strip()
        if re.match(r'^\d{1,2}\.', text):
            # print(f"  Question at {b[:4]}: {text[:20]}")
            pass

print("Done scanning.")

