import os
import sys
import subprocess
import json
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI()

# Prevent browser caching of static assets so updates are always served fresh
from fastapi import Request
from fastapi.responses import Response

@app.middleware("http")
async def add_no_cache_headers(request: Request, call_next):
    response = await call_next(request)
    path = request.url.path
    if path.endswith(('.js', '.css', '.html')) or path == '/':
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
    return response


# Serve data files
app.mount("/data", StaticFiles(directory="data"), name="data")

@app.post("/api/save_progress/{slot}")
def save_progress(slot: int, data: dict):
    os.makedirs("saves", exist_ok=True)
    save_path = os.path.join("saves", f"save_slot_{slot}.json")
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return {"status": "success"}

@app.post("/api/open_saves_folder")
def open_saves_folder():
    saves_dir = os.path.abspath("saves")
    os.makedirs(saves_dir, exist_ok=True)
    try:
        if sys.platform == 'win32':
            os.startfile(saves_dir)
        elif sys.platform == 'darwin':
            subprocess.Popen(['open', saves_dir])
        else:
            subprocess.Popen(['xdg-open', saves_dir])
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/load_progress/{slot}")
def load_progress(slot: int):
    save_path = os.path.join("saves", f"save_slot_{slot}.json")
    if os.path.exists(save_path):
        with open(save_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

@app.delete("/api/delete_progress/{slot}")
def delete_progress(slot: int):
    save_path = os.path.join("saves", f"save_slot_{slot}.json")
    if os.path.exists(save_path):
        os.remove(save_path)
    return {"status": "success"}

@app.get("/api/slot_names")
def get_slot_names():
    names = {}
    for i in range(1, 4):
        save_path = os.path.join("saves", f"save_slot_{i}.json")
        if os.path.exists(save_path):
            try:
                with open(save_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if "_meta" in data and "slotName" in data["_meta"]:
                        names[str(i)] = data["_meta"]["slotName"]
            except Exception:
                pass
    return names

class RenameSlotRequest(BaseModel):
    name: str

@app.post("/api/rename_slot/{slot}")
def rename_slot(slot: int, req: RenameSlotRequest):
    os.makedirs("saves", exist_ok=True)
    save_path = os.path.join("saves", f"save_slot_{slot}.json")
    data = {}
    if os.path.exists(save_path):
        with open(save_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except Exception:
                data = {}
                
    if "_meta" not in data:
        data["_meta"] = {}
    data["_meta"]["slotName"] = req.name
    
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    return {"status": "success"}


class TagUpdate(BaseModel):
    subject: str
    question_no: int
    exam_id: int
    year: str = None
    tag: str



@app.post("/api/add_tag")
def add_tag(update: TagUpdate):
    json_path = os.path.join("data", f"{update.subject}.json")
    if not os.path.exists(json_path):
        raise HTTPException(status_code=404, detail="Subject data not found")
        
    with open(json_path, "r", encoding="utf-8") as f:
        questions = json.load(f)
        
    updated = False
    for q in questions:
        if q["no"] == update.question_no and q["exam_id"] == update.exam_id and (update.year is None or q.get("year") == update.year):
            if "tags" not in q:
                q["tags"] = []
            if update.tag not in q["tags"]:
                q["tags"].append(update.tag)
            updated = True
            break
            
    if updated:
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(questions, f, ensure_ascii=False, indent=2)
        return {"status": "success", "tag": update.tag}
        
    raise HTTPException(status_code=404, detail="Question not found")

class TagBatchUpdate(BaseModel):
    subject: str
    questions: list[dict] # [{"exam_id": 1, "no": 2, "year": "115-1"}]
    tag: str

class SearchRule(BaseModel):
    name: str
    query: str

@app.post("/api/add_tag_batch")
def add_tag_batch(update: TagBatchUpdate):
    json_path = os.path.join("data", f"{update.subject}.json")
    if not os.path.exists(json_path):
        raise HTTPException(status_code=404, detail="Subject data not found")
        
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    updated_count = 0
    target_qs = {(q.get("year"), q["exam_id"], q["no"]) for q in update.questions}
    
    for q in data:
        if (q.get("year"), q["exam_id"], q["no"]) in target_qs or (None, q["exam_id"], q["no"]) in target_qs:
            if "tags" not in q:
                q["tags"] = []
            if update.tag not in q["tags"]:
                q["tags"].append(update.tag)
                updated_count += 1
                
    if updated_count > 0:
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
    return {"status": "success", "updated_count": updated_count}

@app.post("/api/save_search_rule")
def save_search_rule(rule: SearchRule):
    rules_path = os.path.join("data", "saved_searches.json")
    rules = []
    if os.path.exists(rules_path):
        with open(rules_path, "r", encoding="utf-8") as f:
            rules = json.load(f)
            
    # Update if exists, else append
    for r in rules:
        if r["name"] == rule.name:
            r["query"] = rule.query
            break
    else:
        rules.append({"name": rule.name, "query": rule.query})
        
    with open(rules_path, "w", encoding="utf-8") as f:
        json.dump(rules, f, ensure_ascii=False, indent=2)
    return {"status": "success"}

@app.get("/api/get_search_rules")
def get_search_rules():
    rules_path = os.path.join("data", "saved_searches.json")
    if os.path.exists(rules_path):
        with open(rules_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

@app.delete("/api/delete_search_rule/{rule_name}")
def delete_search_rule(rule_name: str):
    rules_path = os.path.join("data", "saved_searches.json")
    if os.path.exists(rules_path):
        with open(rules_path, "r", encoding="utf-8") as f:
            rules = json.load(f)
        rules = [r for r in rules if r['name'] != rule_name]
        with open(rules_path, "w", encoding="utf-8") as f:
            json.dump(rules, f, ensure_ascii=False, indent=2)
    return {"status": "success"}

from fastapi import UploadFile, File, Form
import shutil
import uuid

@app.post("/api/upload_image")
async def upload_image(
    subject: str = Form(...),
    exam_id: int = Form(...),
    year: str = Form(None),
    no: int = Form(...),
    file: UploadFile = File(...)
):
    os.makedirs("public/images", exist_ok=True)
    ext = os.path.splitext(file.filename)[1]
    filename = f"{uuid.uuid4().hex}{ext}"
    file_path = os.path.join("public", "images", filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    json_path = os.path.join("data", f"{subject}.json")
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        updated = False
        for q in data:
            if q["exam_id"] == exam_id and q["no"] == no and (year is None or q.get("year") == year):
                if "images" in q and "original_images" not in q:
                    q["original_images"] = q["images"].copy()
                q["images"] = [f"images/{filename}"]
                updated = True
                break
                
        if updated:
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
    return {"status": "success", "image_url": f"images/{filename}"}

class ResetImageRequest(BaseModel):
    subject: str
    exam_id: int
    year: str = None
    no: int

@app.post("/api/reset_image")
def reset_image(req: ResetImageRequest):
    json_path = os.path.join("data", f"{req.subject}.json")
    if not os.path.exists(json_path):
        raise HTTPException(status_code=404, detail="Subject data not found")
        
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    updated = False
    restored_images = []
    for q in data:
        if q["exam_id"] == req.exam_id and q["no"] == req.no and (req.year is None or q.get("year") == req.year):
            if "original_images" in q:
                q["images"] = q["original_images"].copy()
                restored_images = q["images"]
                updated = True
            break
            
    if updated:
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return {"status": "success", "images": restored_images}
    return {"status": "error", "message": "No original images to restore or question not found"}

class AnswerUpdate(BaseModel):
    subject: str
    year: str = None
    exam_id: int
    no: int
    new_answer: str

@app.post("/api/update_correct_answer")
def update_correct_answer(update: AnswerUpdate):
    json_path = os.path.join("data", f"{update.subject}.json")
    if not os.path.exists(json_path):
        raise HTTPException(status_code=404, detail="Subject data not found")
        
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    updated = False
    for q in data:
        if q["exam_id"] == update.exam_id and q["no"] == update.no and (update.year is None or q.get("year") == update.year):
            q["answer"] = update.new_answer
            updated = True
            break
            
    if updated:
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return {"status": "success"}
    return {"status": "error", "message": "Question not found"}


app.mount("/", StaticFiles(directory="public", html=True), name="public")

import threading
import webbrowser

if __name__ == "__main__":
    import uvicorn
    # Open browser slightly after server starts
    threading.Timer(1.5, lambda: webbrowser.open("http://127.0.0.1:8080/")).start()
    uvicorn.run(app, host="127.0.0.1", port=8080)

