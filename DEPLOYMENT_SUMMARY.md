# 📦 TÓM TẮT DEPLOYMENT - QWEN 3.5 27B MoE

## ✅ ĐÃ HOÀN THÀNH

### 1. Code đã push lên GitHub
- **Repository:** https://github.com/20227991-AnBDQ/Qwen3.5-27B
- **Branch:** main
- **Commit:** Initial commit với 25 files

### 2. Cấu trúc project

```
Qwen3.5-27B/
├── api_gateway.py              # FastAPI server
├── normalize_cv.py             # Chuẩn hóa CV
├── score_all_cvs.py            # Chấm điểm 7 tiêu chí
├── process_mixed_cvs.py        # Xử lý PDF/DOCX/URL
├── test_api.py                 # Test API
├── test_cv.py                  # Test CV processing
├── demo.py                     # Demo script
├── download_from_gdrive.py     # Tải CV từ Google Drive
├── download_from_topcv.py      # Tải CV từ TopCV
├── extract_zip.py              # Giải nén ZIP
├── normalize_cv_regex.py       # Chuẩn hóa bằng regex
├── requirements.txt            # Dependencies
├── .gitignore                  # Git ignore rules
├── .env.example                # Environment template
├── README.md                   # Hướng dẫn chính
├── SETUP_SERVER.md             # Hướng dẫn setup server
└── docs/                       # Tài liệu
    ├── real_task.md            # Yêu cầu chi tiết
    ├── 3_PLAN.md               # Kế hoạch 8 tuần
    ├── 5_Remaining.md          # Công việc còn lại
    ├── 5_Remaining_Updated.md  # Cập nhật công việc
    ├── EXECUTIVE_SUMMARY.md    # Tổng hợp dự án
    ├── 1_CORE.md               # Core concepts
    ├── 2_PRESENTATION.md       # Presentation
    ├── 4_HostLocal.md          # Host local guide
    ├── tasks.md                # Tasks list
    └── task2.md                # Task 2 details
```

### 3. File dữ liệu (KHÔNG có trên GitHub)

**File:** `data_cvs_full.zip` (0.52 MB)

**Nội dung:**
- `data/cvs_extracted.jsonl` - 486 CV đã trích text từ PDF/DOCX

**Kích thước:** 0.52 MB (nén từ ~2MB text)

**Cách upload lên server:**
```bash
# Option 1: SCP (từ máy Windows)
scp data_cvs_full.zip user@server:/path/to/Qwen3.5-27B/

# Option 2: Upload lên Google Drive
# 1. Upload data_cvs_full.zip lên Google Drive
# 2. Share link public
# 3. Trên server: gdown https://drive.google.com/uc?id=FILE_ID -O data_cvs_full.zip

# Option 3: SFTP (dùng WinSCP hoặc FileZilla)
```

---

## 🚀 HƯỚNG DẪN TRIỂN KHAI TRÊN SERVER RTX 5090

### Bước 1: Clone code

```bash
git clone https://github.com/20227991-AnBDQ/Qwen3.5-27B.git
cd Qwen3.5-27B
```

### Bước 2: Setup Python

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Bước 3: Cài Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull qwen:4b  # hoặc model lớn hơn
```

### Bước 4: Upload dữ liệu

```bash
# Upload data_cvs.zip lên server
# Giải nén
unzip data_cvs.zip -d data/
```

### Bước 5: Chạy hệ thống

```bash
# Terminal 1: Ollama
ollama serve

# Terminal 2: API
python api_gateway.py

# Terminal 3: Test
python test_api.py
```

### Bước 6: Xử lý CV

```bash
python normalize_cv.py    # ~10-15 phút
python score_all_cvs.py   # ~5 phút
```

---

## 📊 KẾT QUẢ MONG ĐỢI

Sau khi chạy xong, bạn sẽ có:

1. **data/cvs_normalized.csv** - CV đã chuẩn hóa
2. **data/cvs_scored.csv** - CV đã chấm điểm
3. **Top 5 ứng viên** - In ra console

---

## 🔗 LINKS QUAN TRỌNG

- **GitHub Repo:** https://github.com/20227991-AnBDQ/Qwen3.5-27B
- **README:** https://github.com/20227991-AnBDQ/Qwen3.5-27B/blob/main/README.md
- **Setup Guide:** https://github.com/20227991-AnBDQ/Qwen3.5-27B/blob/main/SETUP_SERVER.md
- **Ollama:** https://ollama.com
- **Qwen Model:** https://huggingface.co/Qwen

---

## ⚠️ LƯU Ý QUAN TRỌNG

### 1. File KHÔNG có trên GitHub (cần upload riêng):
- ❌ `data/cvs_extracted.jsonl` (trong data_cvs.zip)
- ❌ `data/raw_cvs/` (PDF/DOCX gốc - không cần thiết)
- ❌ Model files (tải trực tiếp trên server)

### 2. Yêu cầu phần cứng:
- **GPU:** RTX 5090 (24GB VRAM) ✅
- **RAM:** >= 16GB
- **Disk:** >= 50GB free

### 3. Model options:
- **Qwen 4B:** ~4GB VRAM (test)
- **Qwen 27B:** ~16GB VRAM (production)
- **RTX 5090 24GB:** Đủ chạy Qwen 27B ✅

### 4. Thời gian xử lý:
- Setup: ~30-60 phút
- Normalize 500 CV: ~10-15 phút
- Score 500 CV: ~5 phút
- **Tổng:** ~1-1.5 giờ

---

## 📞 TROUBLESHOOTING

### Vấn đề 1: Ollama không chạy
```bash
sudo systemctl status ollama
sudo systemctl restart ollama
```

### Vấn đề 2: API không kết nối Ollama
```bash
curl http://localhost:11434
ollama list
```

### Vấn đề 3: Out of Memory
```bash
nvidia-smi
# Dùng model nhỏ hơn hoặc quantization
```

---

## ✅ CHECKLIST DEPLOYMENT

- [ ] Clone code từ GitHub
- [ ] Cài Python dependencies
- [ ] Cài Ollama
- [ ] Tải model Qwen
- [ ] Upload data_cvs.zip
- [ ] Giải nén dữ liệu
- [ ] Chạy Ollama server
- [ ] Chạy API Gateway
- [ ] Test API
- [ ] Chạy normalize_cv.py
- [ ] Chạy score_all_cvs.py
- [ ] Có top 5 ứng viên

---

## 🎯 BƯỚC TIẾP THEO (SAU KHI DEPLOY)

1. **Tối ưu hiệu năng** (Tuần 5-6)
   - Benchmark throughput
   - Latency optimization
   - Stress testing

2. **Fine-tune model** (Tuần 6-7 - tùy chọn)
   - Chuẩn bị training data
   - SFT/LoRA training

3. **Production deployment** (Tuần 7-8)
   - Docker containerization
   - Monitoring dashboard
   - Auto-restart, logging

---

**Ngày tạo:** 27/03/2026  
**Trạng thái:** Ready for deployment  
**Next action:** Clone code trên server RTX 5090
