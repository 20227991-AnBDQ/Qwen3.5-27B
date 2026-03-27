# 🚀 HƯỚNG DẪN SETUP TRÊN SERVER RTX 5090

## 📦 File Cần Chuẩn Bị

1. **Code từ GitHub:** https://github.com/20227991-AnBDQ/Qwen3.5-27B
2. **Dữ liệu CV:** `data_cvs.zip` (tải riêng, không có trên GitHub)

---

## 🔧 BƯỚC 1: Clone Code Từ GitHub

```bash
# SSH vào server
ssh user@your-server-ip

# Clone repository
git clone https://github.com/20227991-AnBDQ/Qwen3.5-27B.git
cd Qwen3.5-27B

# Kiểm tra
ls -la
```

---

## 🔧 BƯỚC 2: Setup Python Environment

```bash
# Kiểm tra Python version (cần >= 3.8)
python3 --version

# Tạo virtual environment
python3 -m venv venv

# Activate
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Cài dependencies
pip install -r requirements.txt
```

---

## 🔧 BƯỚC 3: Cài Đặt Ollama

```bash
# Tải và cài Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Kiểm tra
ollama --version

# Khởi động Ollama service
sudo systemctl start ollama
sudo systemctl enable ollama

# Kiểm tra service
sudo systemctl status ollama
```

---

## 🔧 BƯỚC 4: Tải Model Qwen

### Option A: Model Nhỏ (Test) - Qwen 4B

```bash
# Tải model 4B (~2.5GB)
ollama pull qwen:4b

# Kiểm tra
ollama list

# Test model
ollama run qwen:4b "Xin chào"
```

### Option B: Model Lớn (Production) - Qwen 27B

```bash
# Nếu Ollama chưa hỗ trợ Qwen 27B MoE, dùng vLLM:

# Cài vLLM
pip install vllm

# Tải model từ HuggingFace
huggingface-cli download Qwen/Qwen2.5-27B-Instruct \
    --local-dir ./models/qwen2.5-27b \
    --resume-download

# Chạy vLLM server
python -m vllm.entrypoints.openai.api_server \
    --model ./models/qwen2.5-27b \
    --host 0.0.0.0 \
    --port 11434 \
    --tensor-parallel-size 1 \
    --max-model-len 8192 \
    --gpu-memory-utilization 0.90
```

---

## 🔧 BƯỚC 5: Upload Dữ Liệu CV

### Cách 1: SCP (Từ máy local)

```bash
# Trên máy local (Windows)
scp data_cvs.zip user@server-ip:/path/to/Qwen3.5-27B/

# Trên server
cd /path/to/Qwen3.5-27B
unzip data_cvs.zip -d data/
```

### Cách 2: Google Drive (Nếu file quá lớn)

```bash
# Trên server, cài gdown
pip install gdown

# Tải từ Google Drive (cần share link public)
gdown https://drive.google.com/uc?id=YOUR_FILE_ID -O data_cvs.zip

# Giải nén
unzip data_cvs.zip -d data/
```

### Kiểm Tra Dữ Liệu

```bash
# Kiểm tra file đã có chưa
ls -lh data/cvs_extracted.jsonl

# Đếm số CV
wc -l data/cvs_extracted.jsonl
```

---

## 🔧 BƯỚC 6: Cấu Hình Environment

```bash
# Copy file .env.example thành .env
cp .env.example .env

# Chỉnh sửa nếu cần
nano .env
```

Nội dung `.env`:
```bash
OLLAMA_URL=http://localhost:11434/api/generate
MODEL_NAME=qwen:4b
API_HOST=0.0.0.0
API_PORT=8000
```

---

## 🔧 BƯỚC 7: Chạy Hệ Thống

### Terminal 1: Ollama Server (nếu chưa chạy)

```bash
# Kiểm tra Ollama đã chạy chưa
curl http://localhost:11434

# Nếu chưa chạy:
ollama serve
```

### Terminal 2: API Gateway

```bash
cd /path/to/Qwen3.5-27B
source venv/bin/activate
python api_gateway.py
```

### Terminal 3: Test API

```bash
# Test health
curl http://localhost:8000/health

# Test chat
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Xin chào", "max_tokens": 100}'

# Hoặc dùng script
python test_api.py
```

---

## 🔧 BƯỚC 8: Chạy Pipeline Xử Lý CV

### 8.1. Chuẩn Hóa CV

```bash
# Đảm bảo Ollama + API đang chạy
python normalize_cv.py

# Kết quả: data/cvs_normalized.csv
```

**Thời gian:** ~10-15 phút cho 500 CV

### 8.2. Chấm Điểm CV

```bash
python score_all_cvs.py

# Kết quả: data/cvs_scored.csv
```

**Thời gian:** ~5 phút

### 8.3. Xem Top 5

```bash
# Top 5 sẽ in ra console
# Hoặc xem trong file CSV
head -6 data/cvs_scored.csv
```

---

## 🔧 BƯỚC 9: Chạy Nền (Background)

### Dùng tmux (Khuyến nghị)

```bash
# Cài tmux
sudo apt install tmux

# Tạo session cho Ollama
tmux new -s ollama
ollama serve
# Ctrl+B, D để detach

# Tạo session cho API
tmux new -s api
cd /path/to/Qwen3.5-27B
source venv/bin/activate
python api_gateway.py
# Ctrl+B, D để detach

# Xem danh sách sessions
tmux ls

# Attach lại session
tmux attach -t api
```

### Dùng systemd (Production)

Tạo file `/etc/systemd/system/hrm-api.service`:

```ini
[Unit]
Description=HRM LLM API Gateway
After=network.target ollama.service

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/Qwen3.5-27B
Environment="PATH=/path/to/Qwen3.5-27B/venv/bin"
ExecStart=/path/to/Qwen3.5-27B/venv/bin/python api_gateway.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Reload systemd
sudo systemctl daemon-reload

# Start service
sudo systemctl start hrm-api

# Enable auto-start
sudo systemctl enable hrm-api

# Check status
sudo systemctl status hrm-api
```

---

## 📊 BƯỚC 10: Monitoring

### GPU Usage

```bash
# Real-time GPU monitoring
nvidia-smi -l 1

# Hoặc dùng gpustat
pip install gpustat
gpustat -i 1
```

### API Logs

```bash
# Nếu dùng tmux
tmux attach -t api

# Nếu dùng systemd
sudo journalctl -u hrm-api -f
```

### Ollama Logs

```bash
sudo journalctl -u ollama -f
```

---

## ⚠️ Troubleshooting

### 1. Ollama không chạy

```bash
# Kiểm tra service
sudo systemctl status ollama

# Restart
sudo systemctl restart ollama

# Xem log
sudo journalctl -u ollama -n 50
```

### 2. API không kết nối được Ollama

```bash
# Kiểm tra Ollama có chạy không
curl http://localhost:11434

# Kiểm tra model đã tải chưa
ollama list

# Test model trực tiếp
ollama run qwen:4b "test"
```

### 3. Out of Memory (OOM)

```bash
# Kiểm tra VRAM
nvidia-smi

# Giảm batch size hoặc dùng model nhỏ hơn
# Hoặc dùng quantization (INT8/INT4)
```

### 4. normalize_cv.py chạy chậm

```bash
# Giảm số CV test trước
head -10 data/cvs_extracted.jsonl > data/cvs_test.jsonl

# Sửa script để đọc file test
# Hoặc tăng timeout trong normalize_cv.py
```

---

## 🎯 Checklist Hoàn Thành

- [ ] Clone code từ GitHub
- [ ] Cài Python dependencies
- [ ] Cài Ollama
- [ ] Tải model Qwen
- [ ] Upload dữ liệu CV
- [ ] Chạy Ollama server
- [ ] Chạy API Gateway
- [ ] Test API thành công
- [ ] Chạy normalize_cv.py
- [ ] Chạy score_all_cvs.py
- [ ] Có top 5 ứng viên

---

## 📞 Support

Nếu gặp vấn đề:
1. Kiểm tra logs
2. Kiểm tra GPU memory
3. Kiểm tra network connectivity
4. Xem file README.md

---

**Thời gian setup:** ~30-60 phút  
**Thời gian xử lý 500 CV:** ~15-20 phút  
**Tổng:** ~1-1.5 giờ
