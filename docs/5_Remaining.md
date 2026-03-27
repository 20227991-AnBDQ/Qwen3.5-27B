# 5_Remaining.md - Các Nhiệm Vụ Còn Lại

## Tóm Tắt Công Việc

Bạn đã hoàn thành: **Bước 1 - Host Model Qwen 3.5 4B trên Ollama** ✅

Còn lại: **Bước 2 → Bước 7** (xây dựng LLM Engine hoàn chỉnh)

---

## BƯỚC 2: Xây Dựng API Gateway Với FastAPI

### Mục Đích
Tạo một API server để các ứng dụng khác có thể gọi model Qwen thay vì gọi trực tiếp Ollama.

### Tại Sao Cần?
- Kiểm soát truy cập (auth, rate limit)
- Thêm logic nghiệp vụ (prompt chuẩn, xử lý input/output)
- Dễ tích hợp với frontend, backend khác

### Các Bước Thực Hiện

#### Bước 2.1: Cài Đặt Thư Viện

Mở Terminal, gõ:

```bash
pip install fastapi uvicorn requests pydantic python-dotenv
```

**Giải thích:**
- `fastapi` = framework tạo API
- `uvicorn` = server chạy FastAPI
- `requests` = gọi Ollama từ Python
- `pydantic` = validate dữ liệu input/output
- `python-dotenv` = quản lý biến môi trường

#### Bước 2.2: Tạo File API

Tạo file `api_gateway.py`:

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import json

app = FastAPI(title="HRM LLM Engine")

# Cấu hình
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen:4b"

# Định nghĩa request/response
class ChatRequest(BaseModel):
    prompt: str
    max_tokens: int = 500

class ChatResponse(BaseModel):
    response: str
    model: str

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

#### Bước 2.3: Chạy API Server

Mở Terminal mới (giữ Ollama chạy), gõ:

```bash
python api_gateway.py
```

Bạn sẽ thấy:

```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

#### Bước 2.4: Kiểm Tra API

Mở Terminal thứ 3, gõ:

```bash
curl.exe -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d "{\"prompt\": \"Xin chào\"}"
```

Kết quả:

```json
{"response":"Xin chào! Tôi là Qwen...","model":"qwen:4b"}
```

✅ API hoạt động!

---

## BƯỚC 2B: Thêm Lớp Xử Lý Nghiệp Vụ HRM

### Mục Đích
Thêm các route riêng cho bài toán tuyển dụng (tóm tắt CV, chấm điểm, etc.)

### Các Bước Thực Hiện

#### Bước 2B.1: Tạo Prompt Template

Thêm vào `api_gateway.py`:

```python
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
```

#### Bước 2B.2: Thêm Route Mới

Thêm vào `api_gateway.py`:

```python
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
```

#### Bước 2B.3: Test Route Mới

```bash
curl -X POST http://localhost:8000/process_cv \
  -H "Content-Type: application/json" \
  -d "{\"cv_text\": \"Tôi là Nguyễn Văn A, học Khoa Học Máy Tính, có kỹ năng Python, TensorFlow\", \"task\": \"summarize_cv\"}"
```

---

## BƯỚC 2C: Chuẩn Bị Dữ Liệu CV

### Mục Đích
Thu thập và chuẩn hóa dữ liệu CV để hệ thống có thể xử lý.

### Các Bước Thực Hiện

#### Bước 2C.1: Tạo Thư Mục Dữ Liệu

```bash
mkdir data
mkdir data/cvs
mkdir data/output
```

#### Bước 2C.2: Tạo File CSV Mẫu

Tạo file `data/cvs_sample.csv`:

```csv
id,name,major,gpa,skills,projects,experience
1,Nguyễn Văn A,AI,3.8,"Python, TensorFlow, PyTorch","Chatbot AI, Image Recognition","Internship tại VNG"
2,Trần Thị B,Robotics,3.6,"C++, ROS, OpenCV","Robot Navigation, SLAM","Lab tại ĐH Bách Khoa"
3,Phạm Văn C,AI/Robotics,3.9,"Python, C++, PyTorch, ROS","Autonomous Robot, NLP","Startup AI"
```

#### Bước 2C.3: Tạo Script Đọc CSV

Tạo file `load_cvs.py`:

```python
import pandas as pd
import json

# Đọc CSV
df = pd.read_csv('data/cvs_sample.csv')

# Chuyển thành JSON
cvs_data = df.to_dict('records')

# Lưu JSON
with open('data/cvs_data.json', 'w', encoding='utf-8') as f:
    json.dump(cvs_data, f, ensure_ascii=False, indent=2)

print(f"Đã tải {len(cvs_data)} CV")
```

Chạy:

```bash
python load_cvs.py
```

---

## BƯỚC 3: Xây Dựng Hệ Thống Chấm Điểm CV

### Mục Đích
Tạo rubric (tiêu chí chấm điểm) và tự động chấm điểm CV.

### Các Bước Thực Hiện

#### Bước 3.1: Định Nghĩa Rubric

Tạo file `rubric.json`:

```json
{
  "criteria": {
    "academic": {
      "weight": 0.15,
      "description": "Nền tảng học tập",
      "rules": [
        {"gpa_min": 3.8, "score": 10},
        {"gpa_min": 3.6, "score": 8},
        {"gpa_min": 3.4, "score": 6},
        {"gpa_min": 0, "score": 4}
      ]
    },
    "technical_skills": {
      "weight": 0.25,
      "description": "Kỹ năng kỹ thuật",
      "required": ["Python", "C++"],
      "bonus": ["TensorFlow", "PyTorch", "ROS"]
    },
    "projects": {
      "weight": 0.30,
      "description": "Project AI/Robotics",
      "min_projects": 1,
      "keywords": ["AI", "Robotics", "ML", "CV", "NLP"]
    },
    "experience": {
      "weight": 0.20,
      "description": "Kinh nghiệm thực tập",
      "types": ["Internship", "Lab", "Startup"]
    },
    "achievements": {
      "weight": 0.10,
      "description": "Thành tích",
      "keywords": ["Giải thưởng", "Hackathon", "Học bổng"]
    }
  }
}
```

#### Bước 3.2: Tạo Script Chấm Điểm

Tạo file `scoring.py`:

```python
import json
import pandas as pd

# Tải rubric
with open('rubric.json', 'r', encoding='utf-8') as f:
    rubric = json.load(f)

def score_cv(cv_data):
    """Chấm điểm một CV"""
    scores = {}
    total_score = 0
    
    # 1. Chấm điểm học tập
    gpa = float(cv_data.get('gpa', 0))
    for rule in rubric['criteria']['academic']['rules']:
        if gpa >= rule['gpa_min']:
            scores['academic'] = rule['score']
            break
    
    # 2. Chấm điểm kỹ năng
    skills = cv_data.get('skills', '').split(',')
    skills_score = 0
    for skill in rubric['criteria']['technical_skills']['required']:
        if any(skill.lower() in s.lower() for s in skills):
            skills_score += 3
    for skill in rubric['criteria']['technical_skills']['bonus']:
        if any(skill.lower() in s.lower() for s in skills):
            skills_score += 2
    scores['technical_skills'] = min(skills_score, 10)
    
    # 3. Chấm điểm project
    projects = cv_data.get('projects', '')
    projects_score = 0
    for keyword in rubric['criteria']['projects']['keywords']:
        if keyword.lower() in projects.lower():
            projects_score += 2
    scores['projects'] = min(projects_score, 10)
    
    # 4. Chấm điểm kinh nghiệm
    experience = cv_data.get('experience', '')
    exp_score = 0
    for exp_type in rubric['criteria']['experience']['types']:
        if exp_type.lower() in experience.lower():
            exp_score += 3
    scores['experience'] = min(exp_score, 10)
    
    # 5. Tính tổng điểm
    for criterion, score in scores.items():
        weight = rubric['criteria'][criterion]['weight']
        total_score += score * weight
    
    return {
        'scores': scores,
        'total_score': round(total_score, 2),
        'rank': 'Shortlist' if total_score >= 7 else 'Borderline' if total_score >= 5 else 'Reject'
    }

# Chấm điểm tất cả CV
df = pd.read_csv('data/cvs_sample.csv')
results = []

for idx, row in df.iterrows():
    result = score_cv(row.to_dict())
    result['id'] = row['id']
    result['name'] = row['name']
    results.append(result)

# Sắp xếp theo điểm
results = sorted(results, key=lambda x: x['total_score'], reverse=True)

# Lưu kết quả
with open('data/scoring_results.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

# In top 5
print("Top 5 ứng viên:")
for i, r in enumerate(results[:5], 1):
    print(f"{i}. {r['name']} - Điểm: {r['total_score']} - {r['rank']}")
```

Chạy:

```bash
python scoring.py
```

---

## BƯỚC 4: Thêm Lịch Sử Chat & Prompt Chuẩn

### Mục Đích
Giữ ngữ cảnh hội thoại, tránh model quên thông tin trước đó.

### Các Bước Thực Hiện

#### Bước 4.1: Thêm Memory Vào API

Thêm vào `api_gateway.py`:

```python
from collections import defaultdict
from datetime import datetime

# Lưu lịch sử chat (dùng dict, sau có thể dùng Redis)
chat_history = defaultdict(list)

class ChatWithHistoryRequest(BaseModel):
    user_id: str
    message: str
    max_history: int = 5

@app.post("/chat_with_history")
async def chat_with_history(request: ChatWithHistoryRequest):
    """Chat với lịch sử"""
    try:
        # Lấy lịch sử gần đây
        history = chat_history[request.user_id][-request.max_history:]
        
        # Xây dựng context
        context = "Lịch sử hội thoại:\n"
        for msg in history:
            context += f"User: {msg['user']}\nAssistant: {msg['assistant']}\n"
        
        # Tạo prompt
        full_prompt = f"{context}\nUser: {request.message}\nAssistant:"
        
        # Gọi model
        payload = {
            "model": MODEL_NAME,
            "prompt": full_prompt,
            "stream": False
        }
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        result = response.json()
        assistant_response = result.get("response", "")
        
        # Lưu vào lịch sử
        chat_history[request.user_id].append({
            "user": request.message,
            "assistant": assistant_response,
            "timestamp": datetime.now().isoformat()
        })
        
        return {
            "response": assistant_response,
            "history_length": len(chat_history[request.user_id])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

#### Bước 4.2: Test

```bash
curl -X POST http://localhost:8000/chat_with_history \
  -H "Content-Type: application/json" \
  -d "{\"user_id\": \"user1\", \"message\": \"Tôi là lập trình viên Python\"}"
```

---

## BƯỚC 5: Fine-Tune Model (Tùy Chọn)

### Mục Đích
Dạy model trả lời theo phong cách mong muốn cho bài toán HRM.

### Các Bước Thực Hiện

#### Bước 5.1: Chuẩn Bị Dữ Liệu Training

Tạo file `training_data.jsonl`:

```jsonl
{"prompt": "Tóm tắt CV: Nguyễn Văn A, Python, TensorFlow, Internship VNG", "completion": "Nguyễn Văn A - Lập trình viên AI, kỹ năng Python & TensorFlow, có kinh nghiệm internship tại VNG."}
{"prompt": "Chấm điểm CV: Trần Thị B, GPA 3.8, C++, ROS, Lab ĐH", "completion": "Điểm: 8.5/10. Lý do: GPA cao, kỹ năng Robotics tốt, có kinh nghiệm lab."}
```

#### Bước 5.2: Cài Đặt Thư Viện Fine-Tune

```bash
pip install transformers peft bitsandbytes torch
```

#### Bước 5.3: Script Fine-Tune (Nâng Cao)

Tạo file `finetune.py`:

```python
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer
from peft import LoraConfig, get_peft_model
import torch

# Tải model
model_name = "Qwen/Qwen-4B"  # Hoặc từ Hugging Face
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16)

# Cấu hình LoRA
lora_config = LoraConfig(
    r=8,
    lora_alpha=16,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

model = get_peft_model(model, lora_config)

# Training arguments
training_args = TrainingArguments(
    output_dir="./qwen-finetuned",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    save_steps=10,
    save_total_limit=2,
)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=None,  # Load từ training_data.jsonl
)

# Fine-tune
trainer.train()
```

**Lưu ý:** Fine-tune cần GPU mạnh. Nếu máy yếu, bỏ qua bước này.

---

## BƯỚC 6: Đánh Giá & Kiểm Tra Chất Lượng

### Mục Đích
Kiểm tra model trả lời đúng, không ảo giác, không timeout.

### Các Bước Thực Hiện

#### Bước 6.1: Tạo Test Suite

Tạo file `test_suite.py`:

```python
import requests
import json
import time

API_URL = "http://localhost:8000"

test_cases = [
    {
        "name": "Tóm tắt CV đơn giản",
        "endpoint": "/process_cv",
        "data": {
            "cv_text": "Tôi là Nguyễn Văn A, học AI, GPA 3.8, kỹ năng Python, TensorFlow",
            "task": "summarize_cv"
        }
    },
    {
        "name": "Chấm điểm CV",
        "endpoint": "/process_cv",
        "data": {
            "cv_text": "Trần Thị B, Robotics, GPA 3.6, C++, ROS, Lab ĐH",
            "task": "score_cv"
        }
    },
    {
        "name": "Chat đơn giản",
        "endpoint": "/chat",
        "data": {
            "prompt": "Kỹ năng nào quan trọng cho vị trí AI?"
        }
    }
]

def run_tests():
    """Chạy test suite"""
    results = []
    
    for test in test_cases:
        print(f"\n🧪 Test: {test['name']}")
        
        try:
            start = time.time()
            response = requests.post(
                f"{API_URL}{test['endpoint']}",
                json=test['data'],
                timeout=60
            )
            elapsed = time.time() - start
            
            if response.status_code == 200:
                print(f"✅ PASS ({elapsed:.2f}s)")
                results.append({
                    "test": test['name'],
                    "status": "PASS",
                    "time": elapsed
                })
            else:
                print(f"❌ FAIL - Status {response.status_code}")
                results.append({
                    "test": test['name'],
                    "status": "FAIL",
                    "error": response.text
                })
        except Exception as e:
            print(f"❌ ERROR - {str(e)}")
            results.append({
                "test": test['name'],
                "status": "ERROR",
                "error": str(e)
            })
    
    # Tóm tắt
    print("\n" + "="*50)
    passed = sum(1 for r in results if r['status'] == 'PASS')
    print(f"Kết quả: {passed}/{len(results)} test passed")
    
    return results

if __name__ == "__main__":
    run_tests()
```

Chạy:

```bash
python test_suite.py
```

#### Bước 6.2: Đo Hiệu Năng

Thêm vào `test_suite.py`:

```python
def benchmark():
    """Đo tốc độ"""
    print("\n📊 Benchmark:")
    
    for i in range(5):
        start = time.time()
        response = requests.post(
            f"{API_URL}/chat",
            json={"prompt": "Xin chào"},
            timeout=60
        )
        elapsed = time.time() - start
        print(f"Request {i+1}: {elapsed:.2f}s")
```

---

## BƯỚC 7: Docker Hóa & Chuẩn Bị Demo

### Mục Đích
Đóng gói toàn bộ hệ thống để dễ deploy và demo.

### Các Bước Thực Hiện

#### Bước 7.1: Tạo Dockerfile

Tạo file `Dockerfile`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Cài đặt dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy code
COPY api_gateway.py .
COPY rubric.json .
COPY data/ ./data/

# Expose port
EXPOSE 8000

# Run
CMD ["python", "api_gateway.py"]
```

#### Bước 7.2: Tạo requirements.txt

```bash
pip freeze > requirements.txt
```

#### Bước 7.3: Tạo Docker Compose

Tạo file `docker-compose.yml`:

```yaml
version: '3.8'

services:
  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    command: serve

  api:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - ollama
    environment:
      - OLLAMA_URL=http://ollama:11434/api/generate

volumes:
  ollama_data:
```

#### Bước 7.4: Chạy Với Docker

```bash
docker-compose up
```

#### Bước 7.5: Tạo README Demo

Tạo file `README_DEMO.md`:

```markdown
# HRM LLM Engine - Demo

## Cách Chạy

### Option 1: Local (Không Docker)
1. Chạy Ollama: `ollama serve`
2. Chạy API: `python api_gateway.py`
3. Test: `curl http://localhost:8000/health`

### Option 2: Docker
```bash
docker-compose up
```

## API Endpoints

### 1. Chat Đơn Giản
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Xin chào"}'
```

### 2. Xử Lý CV
```bash
curl -X POST http://localhost:8000/process_cv \
  -H "Content-Type: application/json" \
  -d '{
    "cv_text": "Tôi là Nguyễn Văn A, Python, TensorFlow",
    "task": "summarize_cv"
  }'
```

### 3. Chat Với Lịch Sử
```bash
curl -X POST http://localhost:8000/chat_with_history \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user1",
    "message": "Tôi là lập trình viên"
  }'
```

## Giới Hạn & Rủi Ro

- **Latency:** 5-10s/request (tùy CPU)
- **Ảo giác:** Model có thể sinh dữ liệu không chính xác
- **Không có GPU:** Chậm hơn 5x
- **RAM:** Cần tối thiểu 8GB

## Bước Tiếp Theo

1. Thêm database (PostgreSQL) để lưu CV
2. Thêm authentication (JWT)
3. Thêm semantic search (Elasticsearch)
4. Fine-tune model với dữ liệu thật
```

---

## Tóm Tắt Công Việc Còn Lại

| Bước | Công Việc | Thời Gian | Độ Khó |
|------|-----------|----------|--------|
| 2 | Xây API Gateway FastAPI | 1-2h | ⭐⭐ |
| 2B | Thêm Logic HRM | 1-2h | ⭐⭐ |
| 2C | Chuẩn Bị Dữ Liệu CV | 1h | ⭐ |
| 3 | Hệ Thống Chấm Điểm | 2-3h | ⭐⭐⭐ |
| 4 | Lịch Sử Chat & Prompt | 1-2h | ⭐⭐ |
| 5 | Fine-Tune (Tùy Chọn) | 3-5h | ⭐⭐⭐⭐ |
| 6 | Đánh Giá & Test | 1-2h | ⭐⭐ |
| 7 | Docker & Demo | 1-2h | ⭐⭐ |

**Tổng cộng:** ~12-20 giờ (tùy kinh nghiệm)

---

## Lưu Ý Quan Trọng

1. **Giữ Ollama chạy** - Mở Terminal riêng, không đóng
2. **Test từng bước** - Không chạy hết một lúc
3. **Dùng Python 3.8+** - Kiểm tra: `python --version`
4. **Lưu ý RAM** - Nếu máy chậm, đóng ứng dụng khác
5. **Backup dữ liệu** - Lưu CSV, JSON trước khi xóa

---

**Chúc bạn thành công! 🚀**

Nếu gặp vấn đề, hãy kiểm tra lại các bước hoặc hỏi tôi.
