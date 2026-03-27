# ⚡ QUICK START - 5 PHÚT SETUP

## 📦 Chuẩn Bị

1. **File data_cvs.zip** (0.52 MB) - Tải lên server
2. **Server RTX 5090** - SSH access

---

## 🚀 5 LỆNH SETUP

```bash
# 1. Clone code
git clone https://github.com/20227991-AnBDQ/Qwen3.5-27B.git && cd Qwen3.5-27B

# 2. Setup Python
python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt

# 3. Cài Ollama + Model
curl -fsSL https://ollama.com/install.sh | sh && ollama pull qwen:4b

# 4. Upload & giải nén dữ liệu (upload data_cvs.zip trước)
unzip data_cvs.zip -d data/

# 5. Chạy hệ thống
# Terminal 1: ollama serve
# Terminal 2: python api_gateway.py
```

---

## ✅ Test Nhanh

```bash
# Test API
curl http://localhost:8000/health

# Test chat
python test_api.py

# Xử lý CV
python normalize_cv.py    # ~10 phút
python score_all_cvs.py   # ~5 phút
```

---

## 📊 Kết Quả

Sau khi chạy xong:
- `data/cvs_normalized.csv` - CV chuẩn hóa
- `data/cvs_scored.csv` - CV đã chấm điểm
- Top 5 ứng viên in ra console

---

## 🔗 Chi Tiết

- **Full Guide:** [SETUP_SERVER.md](SETUP_SERVER.md)
- **README:** [README.md](README.md)
- **Deployment:** [DEPLOYMENT_SUMMARY.md](DEPLOYMENT_SUMMARY.md)

---

**Thời gian:** ~30 phút setup + 15 phút xử lý = 45 phút tổng
