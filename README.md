# LLM Engine cho HRM - Qwen 3.5 27B MoE

Hệ thống tự động hóa lọc CV, chấm điểm, xếp hạng ứng viên cho vị trí AI/Robotics.

## 📋 Tổng Quan

- **Model:** Qwen 3.5 27B MoE (hoặc 4B cho testing)
- **Engine:** Ollama / vLLM
- **API:** FastAPI
- **Chức năng:** Xử lý CV, chấm điểm theo 7 tiêu chí, xếp hạng top 5

## 🚀 Setup Trên Server (RTX 5090)

### Bước 1: Clone Repository

```bash
git clone https://github.com/20227991-AnBDQ/Qwen3.5-27B.git
cd Qwen3.5-27B
```

### Bước 2: Cài Đặt Dependencies

```bash
# Tạo virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# hoặc: venv\Scripts\activate  # Windows

# Cài packages
pip install -r requirements.txt
```

### Bước 3: Cài Đặt Ollama

```bash
# Linux
curl -fsSL https://ollama.com/install.sh | sh

# Kiểm tra
ollama --version
```

### Bước 4: Tải Model Qwen

```bash
# Option 1: Model nhỏ để test (4B - ~2.5GB)
ollama pull qwen:4b

# Option 2: Model lớn cho production (27B - cần ~16GB VRAM)
# Chờ Ollama hỗ trợ hoặc dùng vLLM
```

### Bước 5: Giải Nén Dữ Liệu CV

**File cần tải:** `data_cvs_full.zip` (0.52 MB, chứa 486 CV đã trích text)

```bash
# Upload file data_cvs_full.zip lên server (SCP/SFTP/Google Drive)
# Sau đó giải nén:
unzip data_cvs_full.zip -d data/

# Kiểm tra file đã có:
ls -lh data/cvs_extracted.jsonl
wc -l data/cvs_extracted.jsonl  # Phải có 486 dòng

# Cấu trúc sau khi giải nén:
# data/
#   └── cvs_extracted.jsonl  (486 CV đã trích text, sẵn sàng xử lý)
```

**Lưu ý:** File `data_cvs_full.zip` KHÔNG có trên GitHub (quá lớn). Bạn cần:
1. Tải từ Google Drive / nơi lưu trữ riêng
2. Hoặc copy từ máy local lên server

### Bước 6: Chạy Ollama Server

```bash
# Terminal 1: Chạy Ollama
ollama serve
# Mặc định chạy ở http://localhost:11434
```

### Bước 7: Chạy API Gateway

```bash
# Terminal 2: Chạy FastAPI
python api_gateway.py
# API chạy ở http://localhost:8000
```

### Bước 8: Test API

```bash
# Terminal 3: Test
curl http://localhost:8000/health

# Test chat
python test_api.py
```

## 📊 Pipeline Xử Lý CV

### Bước 1: Chuẩn Hóa CV (Trích Thông Tin)

```bash
python normalize_cv.py
# Input:  data/cvs_extracted.jsonl
# Output: data/cvs_normalized.csv
```

### Bước 2: Chấm Điểm Theo 7 Tiêu Chí

```bash
python score_all_cvs.py
# Input:  data/cvs_normalized.csv
# Output: data/cvs_scored.csv
```

### Bước 3: Xem Top 5 Ứng Viên

Kết quả sẽ in ra console và lưu trong `data/cvs_scored.csv`.

## 🎯 7 Tiêu Chí Chấm Điểm

| # | Tiêu Chí | Trọng Số |
|---|----------|---------|
| 1 | Thông tin nền tảng (GPA, trường, chuyên ngành) | 15% |
| 2 | Kỹ năng kỹ thuật (Python, C++, TensorFlow, ROS) | 25% |
| 3 | Project / Đồ án (AI/Robotics, GitHub) | 25% |
| 4 | Kinh nghiệm (Internship, Lab, RA/TA) | 15% |
| 5 | Thành tích (Giải thưởng, Hackathon, Publication) | 10% |
| 6 | Mức độ phù hợp AI/Robotics | 5% |
| 7 | Tiềm năng phát triển | 5% |

## 📁 Cấu Trúc Project

```
Qwen3.5-27B/
├── api_gateway.py           # FastAPI server
├── normalize_cv.py          # Chuẩn hóa CV
├── score_all_cvs.py         # Chấm điểm 7 tiêu chí
├── process_mixed_cvs.py     # Xử lý PDF/DOCX/URL
├── test_api.py              # Test API
├── test_cv.py               # Test xử lý CV
├── requirements.txt         # Dependencies
├── README.md                # File này
├── data/
│   ├── cvs_extracted.jsonl  # CV đã trích text (từ zip)
│   ├── cvs_normalized.csv   # CV chuẩn hóa (sau normalize)
│   └── cvs_scored.csv       # CV đã chấm điểm (sau score)
└── docs/
    ├── real_task.md         # Yêu cầu chi tiết
    ├── 3_PLAN.md            # Kế hoạch 8 tuần
    ├── 5_Remaining_Updated.md  # Công việc còn lại
    └── EXECUTIVE_SUMMARY.md # Tổng hợp dự án
```

## 🔧 API Endpoints

### 1. Health Check
```bash
GET http://localhost:8000/health
```

### 2. Chat
```bash
POST http://localhost:8000/chat
{
  "prompt": "Xin chào",
  "max_tokens": 500
}
```

### 3. Xử Lý CV
```bash
POST http://localhost:8000/process_cv
{
  "cv_text": "Nguyễn Văn A, Python, TensorFlow...",
  "task": "summarize_cv"  # hoặc "score_cv", "match_jd"
}
```

## 🐳 Docker (Tùy Chọn)

```bash
# Build image
docker build -t hrm-llm-engine .

# Run container
docker run -p 8000:8000 --gpus all hrm-llm-engine
```

## 📈 Monitoring

- **Ollama logs:** `journalctl -u ollama -f`
- **API logs:** Console output từ `api_gateway.py`
- **GPU usage:** `nvidia-smi -l 1`

## ⚠️ Lưu Ý

1. **VRAM Requirements:**
   - Qwen 4B: ~4GB VRAM
   - Qwen 27B: ~16GB VRAM (FP16)
   - RTX 5090 (24GB) → đủ chạy 27B

2. **Thời gian xử lý:**
   - Normalize 500 CV: ~10-15 phút
   - Score 500 CV: ~5 phút

3. **Rate limiting:**
   - Script có `time.sleep(2)` để tránh quá tải model

## 🔗 Links

- **Repository:** https://github.com/20227991-AnBDQ/Qwen3.5-27B
- **Ollama:** https://ollama.com
- **Qwen Model:** https://huggingface.co/Qwen

## 📞 Support

Nếu gặp vấn đề, kiểm tra:
1. Ollama server có chạy không: `curl http://localhost:11434`
2. Model đã tải chưa: `ollama list`
3. API có chạy không: `curl http://localhost:8000/health`

---

**Ngày cập nhật:** 27/03/2026  
**Trạng thái:** Ready for deployment on RTX 5090
