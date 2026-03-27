from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import json

app = FastAPI(title="HRM LLM Engine")

# Cấu hình
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen:4b"

# Prompt templates cho từng task
PROMPTS = {
    "summarize_cv": """Tóm tắt CV sau đây thành 3-4 dòng, bao gồm: tên, chuyên ngành, kỹ năng chính, kinh nghiệm.

CV:
{cv_text}

Tóm tắt:""",
    
    "score_cv": """Chấm điểm CV dưới đây theo tiêu chí AI/Robotics (0-10).
Trả lời dạng JSON: {{"score": X, "reason": "..."}}

CV:
{cv_text}

Tiêu chí:
- Có kỹ năng Python/C++
- Có project AI/Robotics
- Có kinh nghiệm thực tập

Kết quả:""",
    
    "match_jd": """So khớp CV với JD. Trả lời JSON: {{"match_score": 0-10, "matched_skills": [...], "missing_skills": [...]}}

CV:
{cv_text}

JD:
{jd_text}

Kết quả:"""
}

# Định nghĩa request/response
class ChatRequest(BaseModel):
    prompt: str
    max_tokens: int = 500

class ChatResponse(BaseModel):
    response: str
    model: str


# Prompt templates cho từng task
PROMPTS = {
    "summarize_cv": """Tóm tắt CV sau đây thành 3-4 dòng, bao gồm: tên, chuyên ngành, kỹ năng chính, kinh nghiệm.

CV:
{cv_text}

Tóm tắt:""",
    
    "score_cv": """Chấm điểm CV dưới đây theo tiêu chí AI/Robotics (0-10).
Trả lời dạng JSON: {{"score": X, "reason": "..."}}

CV:
{cv_text}

Tiêu chí:
- Có kỹ năng Python/C++
- Có project AI/Robotics
- Có kinh nghiệm thực tập

Kết quả:""",
    
    "match_jd": """So khớp CV với JD. Trả lời JSON: {{"match_score": 0-10, "matched_skills": [...], "missing_skills": [...]}}

CV:
{cv_text}

JD:
{jd_text}

Kết quả:"""
}

# Route 1: Chat đơn giản
@app.post("/chat")
async def chat(request: ChatRequest):
    """Gọi model để trả lời câu hỏi"""
    try:
        payload = {
            "model": MODEL_NAME,
            "prompt": request.prompt,
            "stream": False
        }
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        result = response.json()
        
        return ChatResponse(
            response=result.get("response", ""),
            model=MODEL_NAME
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Route 2: Health check
@app.get("/health")
async def health():
    """Kiểm tra server có chạy không"""
    return {"status": "ok", "model": MODEL_NAME}

# Route 3: Xử lý CV
class CVRequest(BaseModel):
    cv_text: str
    task: str  # "summarize_cv", "score_cv", "match_jd"
    jd_text: str = None  # Dùng cho task "match_jd"

@app.post("/process_cv")
async def process_cv(request: CVRequest):
    """Xử lý CV theo task"""
    try:
        # Lấy prompt template
        template = PROMPTS.get(request.task)
        if not template:
            raise HTTPException(status_code=400, detail="Task không hợp lệ")
        
        # Điền dữ liệu vào template
        if request.task == "match_jd":
            prompt = template.format(cv_text=request.cv_text, jd_text=request.jd_text)
        else:
            prompt = template.format(cv_text=request.cv_text)
        
        # Gọi model
        payload = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        result = response.json()
        
        return {
            "task": request.task,
            "result": result.get("response", ""),
            "model": MODEL_NAME
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
