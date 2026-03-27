# 5_Remaining.md - Các Nhiệm Vụ Còn Lại (CẬP NHẬT)

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

```bash
pip install fastapi uvicorn requests pydantic python-dotenv
```

#### Bước 2.2: Tạo File API

File `api_gateway.py` đã được tạo ✅

#### Bước 2.3: Chạy API Server

```bash
python api_gateway.py
```

#### Bước 2.4: Kiểm Tra API

```bash
python test_api.py
```

---

## BƯỚC 2B: Thêm Route Xử Lý CV

### Mục Đích
Thêm route `/process_cv` để xử lý CV (tóm tắt, chấm điểm, match JD)

### Các Bước Thực Hiện

File `api_gateway.py` đã được cập nhật với:
- ✅ Prompt templates cho 3 task
- ✅ Route `/process_cv`
- ✅ Xử lý CV text

Test:
```bash
python test_cv.py
```

---

## BƯỚC 2C: Chuẩn Bị Dữ Liệu CV (Từ Google Drive)

### Mục Đích
Thu thập 500 CV từ Google Drive, xử lý cả PDF + .URL files, chuẩn hóa dữ liệu.

### Các Bước Thực Hiện

#### Bước 2C.1: Tải 500 CV Từ Google Drive

**Option 1: Tải Thủ Công**
1. Mở Google Drive folder
2. Chọn tất cả: `Ctrl+A`
3. Chuột phải → "Tải xuống"
4. Giải nén vào: `data/raw_cvs/`

**Option 2: Dùng rclone**
```bash
rclone config
rclone copy gdrive:FOLDER_ID data/raw_cvs/ -P
```

#### Bước 2C.2: Giải Nén File ZIP

```bash
python extract_zip.py
```

#### Bước 2C.3: Xử Lý CV (PDF + .URL)

**Script:** `process_mixed_cvs.py` ✅

Xử lý:
- ✅ File `.url` → trích URL → tải CV
- ✅ File PDF/DOCX → trích text (bao gồm bảng, text boxes)
- ✅ Lưu vào `data/cvs_extracted.jsonl`

Chạy:
```bash
python process_mixed_cvs.py
```

**Thời gian:** ~20-30 phút

---

## BƯỚC 3: Chuẩn Hóa Dữ Liệu CV

### Mục Đích
Trích xuất thông tin CV (tên, chuyên ngành, GPA, kỹ năng, project, kinh nghiệm) thành CSV có cấu trúc.

### Các Bước Thực Hiện

**Script:** `normalize_cv.py` ✅

Dùng model Qwen để trích xuất:
- Tên
- Chuyên ngành
- GPA
- Kỹ năng
- Project
- Kinh nghiệm

Chạy:
```bash
python normalize_cv.py
```

**Kết quả:** `data/cvs_normalized.csv`

**Thời gian:** ~10-15 phút

---

## BƯỚC 4: Chấm Điểm & Xếp Hạng CV (7 TIÊU CHÍ)

### Mục Đích
Chấm điểm 500 CV theo 7 tiêu chí chi tiết từ `real_task.md`, xếp hạng và chọn top 5.

### 7 Tiêu Chí Chấm Điểm

| # | Tiêu Chí | Trọng Số | Nội Dung |
|---|----------|---------|---------|
| 1 | Thông tin nền tảng | 15% | GPA, trường, chuyên ngành |
| 2 | Kỹ năng kỹ thuật | 25% | Python, C++, TensorFlow, ROS, Git, Linux, Docker |
| 3 | Project / Đồ án | 25% | Project AI/Robotics, Capstone, GitHub, vai trò |
| 4 | Kinh nghiệm | 15% | Internship, Lab, RA/TA, CLB, Startup |
| 5 | Thành tích | 10% | Giải thưởng, Hackathon, Olympic, Publication, Học bổng |
| 6 | Phù hợp AI/Robotics | 5% | Hướng AI, Robotics, giao thoa |
| 7 | Tiềm năng phát triển | 5% | Tự học, chủ động, tư duy kỹ thuật |

### Các Bước Thực Hiện

**Script:** `score_all_cvs.py` ✅

Chấm điểm:
- ✅ 7 tiêu chí chi tiết
- ✅ Tính trọng số
- ✅ Xếp hạng: Shortlist / Borderline / Reject
- ✅ In top 5 shortlist với chi tiết

Chạy:
```bash
python score_all_cvs.py
```

**Kết quả:** `data/cvs_scored.csv`

**Thời gian:** ~5 phút

---

## BƯỚC 5: Lịch Sử Chat & Prompt Chuẩn

### Mục Đích
Giữ ngữ cảnh hội thoại, tránh model quên thông tin trước đó.

### Các Bước Thực Hiện

Thêm vào `api_gateway.py`:

```python
from collections import defaultdict
from datetime import datetime

chat_history = defaultdict(list)

class ChatWithHistoryRequest(BaseModel):
    user_id: str
    message: str
    max_history: int = 5

@app.post("/chat_with_history")
async def chat_with_history(request: ChatWithHistoryRequest):
    """Chat với lịch sử"""
    try:
        history = chat_history[request.user_id][-request.max_history:]
        
        context = "Lịch sử hội thoại:\n"
        for msg in history:
            context += f"User: {msg['user']}\nAssistant: {msg['assistant']}\n"
        
        full_prompt = f"{context}\nUser: {request.message}\nAssistant:"
        
        payload = {
            "model": MODEL_NAME,
            "prompt": full_prompt,
            "stream": False
        }
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        result = response.json()
        assistant_response = result.get("response", "")
        
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

Test:
```bash
curl -X POST http://localhost:8000/chat_with_history \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user1", "message": "Tôi là lập trình viên Python"}'
```

---

## BƯỚC 6: Fine-Tune Model (Tùy Chọn)

### Mục Đích
Dạy model trả lời theo phong cách mong muốn cho bài toán HRM.

### Các Bước Thực Hiện

#### Bước 6.1: Chuẩn Bị Dữ Liệu Training

Tạo file `training_data.jsonl`:

```jsonl
{"prompt": "Tóm tắt CV: Nguyễn Văn A, Python, TensorFlow, Internship VNG", "completion": "Nguyễn Văn A - Lập trình viên AI, kỹ năng Python & TensorFlow, có kinh nghiệm internship tại VNG."}
{"prompt": "Chấm điểm CV: Trần Thị B, GPA 3.8, C++, ROS, Lab ĐH", "completion": "Điểm: 8.5/10. Lý do: GPA cao, kỹ năng Robotics tốt, có kinh nghiệm lab."}
```

#### Bước 6.2: Cài Đặt Thư Viện

```bash
pip install transformers peft bitsandbytes torch
```

#### Bước 6.3: Script Fine-Tune

Tạo file `finetune.py` (nâng cao, cần GPU mạnh)

---

## BƯỚC 7: Đánh Giá & Test

### Mục Đích
Kiểm tra model trả lời đúng, không ảo giác, không timeout.

### Các Bước Thực Hiện

#### Bước 7.1: Tạo Test Suite

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

---

## BƯỚC 8: Docker Hóa & Demo

### Mục Đích
Đóng gói toàn bộ hệ thống để dễ deploy và demo.

### Các Bước Thực Hiện

#### Bước 8.1: Tạo Dockerfile

Tạo file `Dockerfile`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY api_gateway.py .
COPY rubric.json .
COPY data/ ./data/

EXPOSE 8000

CMD ["python", "api_gateway.py"]
```

#### Bước 8.2: Tạo Docker Compose

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

#### Bước 8.3: Chạy Với Docker

```bash
docker-compose up
```

---

## 📋 Tóm Tắt Quy Trình

| Bước | Công Việc | Lệnh | Thời Gian |
|------|-----------|------|----------|
| 1 | Tải CV từ Google Drive | `rclone copy ...` | 10-20 phút |
| 2 | Giải nén ZIP | `python extract_zip.py` | 2-5 phút |
| 3 | Xử lý PDF + .URL | `python process_mixed_cvs.py` | 20-30 phút |
| 4 | Chuẩn hóa CV | `python normalize_cv.py` | 10-15 phút |
| 5 | Chấm điểm (7 tiêu chí) | `python score_all_cvs.py` | 5 phút |
| 6 | Test API | `python test_suite.py` | 5 phút |

**Tổng cộng:** ~50-75 phút

---

## ⚠️ Lưu Ý Quan Trọng

1. **Giữ Ollama + API chạy** - Cần để normalize_cv.py hoạt động
2. **RAM** - Cần ~4GB trống
3. **Backup** - Lưu CSV trước khi xóa
4. **Thời gian** - Tổng ~1-1.5 giờ cho 500 CV

---

**Bạn sẵn sàng bắt đầu chưa?** 🚀
