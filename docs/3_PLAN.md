# 📋 KẾ HOẠCH THỰC HIỆN: Dựng LLM Engine — Qwen 3.5 27B MoE3B

> **Dự án:** Tự dựng LLM Engine qua Qwen 3.5 27B MoE3B, hỗ trợ bởi Opus 4.6, kết hợp Drill  
> **Phương pháp trình bày:** WHAT → WHY → WHEN → HOW cho từng giai đoạn

---

# 1. WHAT — Kế hoạch này là gì?

## 1.1. Tổng quan kế hoạch

Kế hoạch gồm **4 giai đoạn chính**, mỗi giai đoạn 2 tuần, tổng cộng **8 tuần**:

```
┌─────────────────────────────────────────────────────────────────┐
│                    KẾ HOẠCH TỔNG THỂ — 8 TUẦN                  │
│                                                                 │
│  GĐ1: Nghiên cứu & Chuẩn bị       [Tuần 1-2]  ████░░░░  25%  │
│  GĐ2: Dựng Engine & API            [Tuần 3-4]  ████████  50%  │
│  GĐ3: Tối ưu & Drill (đánh giá)   [Tuần 5-6]  ████████  75%  │
│  GĐ4: Production & Bàn giao        [Tuần 7-8]  ████████ 100%  │
└─────────────────────────────────────────────────────────────────┘
```

## 1.2. Mục tiêu cuối cùng

Sau 8 tuần, phải có:
1. ✅ LLM Engine chạy ổn định với Qwen 3.5 27B MoE3B
2. ✅ API endpoint *(= địa chỉ URL để gọi AI)* tương thích OpenAI format *(= gọi giống ChatGPT API)*
3. ✅ Benchmark report *(= báo cáo đo hiệu năng bằng số liệu cụ thể)*
4. ✅ Tài liệu hướng dẫn deploy + vận hành
5. ✅ Monitoring dashboard *(= bảng giám sát real-time trên web)*

---

# 2. CHI TIẾT TỪNG GIAI ĐOẠN: WHAT → WHY → WHEN → HOW

---

## ═══════════════════════════════════════════
## GIAI ĐOẠN 1: NGHIÊN CỨU & CHUẨN BỊ (Tuần 1-2)
## ═══════════════════════════════════════════

### WHAT — Làm gì?

> Tìm hiểu công nghệ, so sánh framework *(= bộ khung phần mềm có sẵn)*, chuẩn bị server *(= máy chủ)*, tải model về, chạy thử lần đầu tiên.

Nói đơn giản: Giai đoạn này giống **"đi chợ mua đồ + đọc công thức"** trước khi nấu ăn.

### WHY — Tại sao phải làm?

| Lý do | Giải thích |
|-------|-----------|
| **Chọn đúng framework** | Có nhiều engine (vLLM, SGLang, TGI...). Chọn sai → phải làm lại từ đầu, mất 2-3 tuần |
| **Hiểu kiến trúc MoE** | MoE *(= Mixture of Experts, "hỗn hợp chuyên gia")* khác model thường. Không hiểu → không tối ưu được, engine chạy chậm/lỗi |
| **Chuẩn bị server đúng** | Model 27B cần GPU mạnh *(A100 80GB VRAM)*. Nếu không kiểm tra trước → tải model về rồi mới biết GPU yếu quá → mất thời gian |
| **Tải model sớm** | File model ~54GB, download mất vài giờ đến 1 ngày. Nên làm sớm để không block *(= chặn)* các task sau |

### WHEN — Mốc thời gian cụ thể từng task nhỏ

| # | Task | Ngày | Thời gian | Output *(= kết quả)* |
|---|------|------|-----------|----------------------|
| 1.1 | **Khảo sát & so sánh framework** — tìm hiểu vLLM *(= engine phổ biến nhất, có PagedAttention)*, SGLang *(= engine mới, nhanh)*, TGI *(= Text Generation Inference, engine của HuggingFace)*, TensorRT-LLM *(= engine của NVIDIA, tối ưu cực mạnh nhưng phức tạp)* | Ngày 1→3 | 3 ngày | Bảng so sánh chi tiết |
| 1.2 | **Xin access + setup GPU server** — liên hệ IT, cài CUDA *(= phần mềm của NVIDIA để lập trình GPU)*, Python, conda *(= trình quản lý thư viện Python)* | Ngày 1→5 | 5 ngày | Server sẵn sàng |
| 1.3 | **Download model** từ HuggingFace *(= kho model AI lớn nhất, giống "App Store cho AI")* | Ngày 4→6 | 3 ngày | File model ~54GB trên server |
| 1.4 | **Chạy thử "Hello World"** — load model, gửi 1 câu hỏi đơn giản, xem có trả lời không | Ngày 6→8 | 2 ngày | Screenshot trả lời thành công |
| 1.5 | **Nghiên cứu kiến trúc MoE** — hiểu router *(= bộ định tuyến chọn expert)*, expert *(= "chuyên gia" — mạng neural nhỏ chuyên 1 loại thông tin)*, load balancing *(= đảm bảo các expert được dùng đều)* | Ngày 5→10 | 5 ngày | Ghi chú kỹ thuật |
| 1.6 | **Viết báo cáo tuần 1-2** | Ngày 10 | 1 ngày | Weekly report |

```
Timeline trực quan Tuần 1-2:

Ngày:  1   2   3   4   5   6   7   8   9   10
       ├───────────┤                              Task 1.1: Khảo sát framework
       ├───────────────────┤                      Task 1.2: Setup server
                   ├───────────┤                  Task 1.3: Download model
                               ├───────┤          Task 1.4: Hello World
                       ├───────────────────┤      Task 1.5: Nghiên cứu MoE
                                              ├┤  Task 1.6: Báo cáo
```

### HOW — Làm cụ thể thế nào?

**Task 1.1 — Khảo sát framework:**

Lập bảng so sánh theo tiêu chí:

| Tiêu chí | vLLM | SGLang | TGI | TensorRT-LLM |
|----------|------|--------|-----|---------------|
| Hỗ trợ MoE? *(= chạy được model Mixture of Experts không?)* | ✅ Tốt | ✅ Tốt | ✅ Cơ bản | ✅ Rất tốt |
| Throughput *(= thông lượng, số request xử lý/giây)* | Cao | Rất cao | Trung bình | Rất cao |
| Dễ cài đặt? | ✅ Rất dễ | ✅ Dễ | ✅ Dễ | ❌ Phức tạp |
| Community *(= cộng đồng hỗ trợ)* | Lớn nhất | Đang phát triển | Lớn | Trung bình |
| OpenAI-compatible API? *(= gọi giống ChatGPT?)* | ✅ Có sẵn | ✅ Có sẵn | ✅ Có sẵn | ❌ Phải tự viết |
| PagedAttention? *(= quản lý bộ nhớ GPU thông minh theo "trang")* | ✅ Có (họ phát minh ra) | ✅ Có | ❌ Không | ❌ Phương pháp riêng |

> **Kết luận dự kiến:** Chọn **vLLM** vì dễ cài, community lớn, hỗ trợ MoE tốt, có sẵn OpenAI API.

**Task 1.2 — Setup GPU server:**

```bash
# Bước 1: Kiểm tra GPU
nvidia-smi
# 📝 nvidia-smi = lệnh xem thông tin GPU: tên, VRAM bao nhiêu, CUDA version
# Kỳ vọng: A100 80GB, CUDA 12.1+

# Bước 2: Tạo môi trường Python ảo (sandbox riêng, cài gì vào đây không ảnh hưởng máy)
conda create -n qwen-engine python=3.11 -y
conda activate qwen-engine

# Bước 3: Cài PyTorch (thư viện AI nền tảng, giống "nền móng" cho mọi model)
pip install torch==2.4.0 --index-url https://download.pytorch.org/whl/cu121

# Bước 4: Cài vLLM (engine chạy model, giống "động cơ" cho AI)
pip install vllm>=0.6.0

# Bước 5: Cài thư viện phụ trợ
pip install transformers accelerate safetensors huggingface_hub
# 📝 transformers = thư viện load model AI từ HuggingFace
# 📝 accelerate = hỗ trợ chạy nhiều GPU
# 📝 safetensors = format an toàn lưu model weights (= các con số "bộ não" của AI)
# 📝 huggingface_hub = tool tải model từ HuggingFace
```

**Task 1.3 — Download model:**

```bash
# Tải model Qwen 3.5 27B MoE3B từ HuggingFace (~54GB, kiên nhẫn chờ)
huggingface-cli download Qwen/Qwen3-27B-MoE3B \
    --local-dir /models/qwen3-27b-moe3b \
    --resume-download
# 📝 --resume-download = nếu đứt mạng giữa chừng, chạy lại sẽ tiếp tục tải
#    chứ không tải lại từ đầu

# Kiểm tra model đã tải OK chưa
python -c "
from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained('/models/qwen3-27b-moe3b')
print('OK! Tokenizer vocab size:', tokenizer.vocab_size)
"
# 📝 Tokenizer = bộ tách từ, chuyển text → số để model hiểu
#    Nếu load tokenizer OK → file model không bị lỗi
```

**Task 1.4 — Hello World (chạy thử lần đầu):**

```python
# test_hello.py — Chạy thử model lần đầu tiên
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load model (sẽ mất 5-10 phút lần đầu)
model_path = "/models/qwen3-27b-moe3b"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    torch_dtype=torch.float16,   # 📝 float16 = dùng số 16-bit, tiết kiệm VRAM
    device_map="auto"            # 📝 tự phân bổ model vào GPU
)

# Hỏi 1 câu đơn giản
messages = [{"role": "user", "content": "Xin chào, bạn là ai?"}]
text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
inputs = tokenizer(text, return_tensors="pt").to(model.device)

# Sinh câu trả lời
outputs = model.generate(**inputs, max_new_tokens=200)
response = tokenizer.decode(outputs[0][inputs.input_ids.shape[-1]:], skip_special_tokens=True)
print("Trả lời:", response)

# Nếu in được câu trả lời → THÀNH CÔNG! 🎉
```

**🏁 Milestone M1 *(= mốc quan trọng thứ 1)*:** Cuối tuần 2 → **Demo model trả lời được câu hỏi đơn giản**.

---

## ═══════════════════════════════════════════
## GIAI ĐOẠN 2: DỰNG ENGINE & API (Tuần 3-4)
## ═══════════════════════════════════════════

### WHAT — Làm gì?

> Biến model từ "chạy thử trên máy" thành **"dịch vụ" mà người khác gọi được qua API** *(= Application Programming Interface, cổng kết nối để ứng dụng khác gọi vào dùng AI)*.

Nói đơn giản: Giai đoạn 1 giống nấu ăn thử ở nhà. Giai đoạn 2 giống **mở nhà hàng** — có quầy order (API), có bếp (engine), phục vụ được nhiều khách cùng lúc.

### WHY — Tại sao phải làm?

| Lý do | Giải thích |
|-------|-----------|
| **Model chạy trực tiếp rất chậm** | Code ở GĐ1 load model vào `transformers` → xử lý 1 request/lần → 10 user là nghẽn. Cần engine chuyên dụng (vLLM) xử lý **hàng trăm request đồng thời** |
| **Cần API chuẩn** | Các ứng dụng (chatbot, web app) cần gọi AI qua HTTP API *(= giao thức truyền dữ liệu web)*. Không ai gọi bằng Python script trực tiếp cả |
| **Quantization tiết kiệm tài nguyên** | FP16 *(= Float 16-bit, 2 bytes/tham số)* cần ~54GB VRAM. Quantize *(= nén)* xuống INT8 *(= Integer 8-bit, 1 byte/tham số)* chỉ cần ~27GB → GPU rẻ hơn vẫn chạy được |
| **Monitoring từ sớm** | Nếu đợi tuần 7 mới setup monitoring → không phát hiện được lỗi memory leak *(= rò rỉ bộ nhớ, RAM dùng ngày càng nhiều rồi sập)* hoặc GPU overheat *(= GPU quá nóng)* ở tuần 4-5 |

### WHEN — Mốc thời gian cụ thể từng task nhỏ

| # | Task | Ngày | Thời gian | Output |
|---|------|------|-----------|--------|
| 2.1 | **Triển khai vLLM server** — cài vLLM, config *(= cấu hình)*, chạy server, xác nhận API hoạt động | Ngày 11→15 | 5 ngày | Server running, gọi API được |
| 2.2 | **Xây dựng API layer** — thêm authentication *(= xác thực, chỉ người được phép mới gọi được)*, rate limiting *(= giới hạn số request/phút, chống spam)*, logging *(= ghi lại mọi request/response để debug)* | Ngày 13→17 | 4 ngày | API docs *(= tài liệu hướng dẫn gọi API)* |
| 2.3 | **Test Quantization** — thử nén model: FP16 vs INT8 vs INT4, đo chất lượng + tốc độ từng loại | Ngày 15→20 | 5 ngày | Bảng so sánh quantization |
| 2.4 | **Setup monitoring cơ bản** — cài Prometheus *(= phần mềm thu thập số liệu server)* + Grafana *(= phần mềm vẽ biểu đồ đẹp)*, thêm health check *(= endpoint kiểm tra "server còn sống không")* | Ngày 18→22 | 4 ngày | Dashboard URL |
| 2.5 | **Integration testing** *(= test tích hợp, test toàn bộ dây chuyền từ đầu đến cuối)* | Ngày 20→24 | 4 ngày | Bộ test cases |
| 2.6 | **Viết báo cáo tuần 3-4** | Ngày 24 | 1 ngày | Weekly report |

```
Timeline trực quan Tuần 3-4:

Ngày:  11  12  13  14  15  16  17  18  19  20  21  22  23  24
       ├───────────────────┤                                    Task 2.1: vLLM server
               ├───────────────────┤                            Task 2.2: API layer
                       ├───────────────────────┤                Task 2.3: Quantization
                                   ├───────────────────┤        Task 2.4: Monitoring
                                           ├───────────────────┤Task 2.5: Testing
                                                              ├┤Task 2.6: Báo cáo
```

### HOW — Làm cụ thể thế nào?

**Task 2.1 — Triển khai vLLM server:**

```bash
# Khởi chạy vLLM server — 1 lệnh duy nhất
python -m vllm.entrypoints.openai.api_server \
    --model /models/qwen3-27b-moe3b \
    --host 0.0.0.0 \
    --port 8000 \
    --tensor-parallel-size 1 \
    --max-model-len 8192 \
    --gpu-memory-utilization 0.90 \
    --trust-remote-code \
    --enable-prefix-caching

# 📝 Giải thích từng tham số:
# --model: đường dẫn đến thư mục model đã tải
# --host 0.0.0.0: cho phép truy cập từ mọi máy trong mạng (không chỉ localhost)
# --port 8000: server lắng nghe ở cổng 8000
# --tensor-parallel-size 1: dùng 1 GPU. Nếu có 2 GPU → đổi thành 2
# --max-model-len 8192: context window tối đa = 8192 tokens (~6000 từ)
#    📝 context window = "bộ nhớ ngắn hạn" của AI, nó nhớ được bao nhiêu chữ
#    trong 1 cuộc hội thoại
# --gpu-memory-utilization 0.90: dùng 90% VRAM, giữ 10% dự phòng
# --trust-remote-code: cho phép chạy code custom kèm theo model
# --enable-prefix-caching: cache phần prompt giống nhau giữa các request
#    📝 Ví dụ: 10 user cùng bắt đầu bằng "Bạn là AI thông minh..." → tính 1 lần, dùng lại 10 lần
```

```bash
# Kiểm tra server đã chạy OK chưa
curl http://localhost:8000/v1/models
# 📝 curl = lệnh gửi HTTP request. Nếu trả về tên model → server OK

# Test gửi câu hỏi
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen3-27b-moe3b",
    "messages": [{"role": "user", "content": "1 + 1 = ?"}],
    "max_tokens": 50
  }'
# Nếu trả về "2" → MỌI THỨ HOẠT ĐỘNG! 🎉
```

**Task 2.2 — API layer chi tiết:**

```python
# Sau khi vLLM server chạy, bất kỳ app nào cũng gọi được:

import openai  # 📝 Thư viện chính thức của OpenAI, dùng luôn cho self-hosted

client = openai.OpenAI(
    base_url="http://your-server:8000/v1",  # 📝 Trỏ vào server của MÌNH
    api_key="your-secret-key"               # 📝 API key tự đặt để xác thực
)

# Gọi chat — GIỐNG HỆT cách gọi ChatGPT!
response = client.chat.completions.create(
    model="qwen3-27b-moe3b",
    messages=[
        {"role": "system", "content": "Bạn là trợ lý AI công ty XYZ."},
        # 📝 "system" = lệnh thiết lập tính cách/vai trò cho AI
        {"role": "user", "content": "Tóm tắt email này: [nội dung email]"}
        # 📝 "user" = tin nhắn của người dùng
    ],
    temperature=0.7,    # 📝 Mức "sáng tạo": 0=luôn giống nhau, 1=rất ngẫu nhiên
    max_tokens=1024,    # 📝 Giới hạn độ dài câu trả lời (~750 từ)
    stream=True         # 📝 stream=True → AI trả lời từng chữ (giống ChatGPT gõ từng chữ)
)

# Đọc stream response
for chunk in response:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

**Task 2.3 — Quantization (nén model):**

So sánh các mức quantization:

| Phương pháp | VRAM cần | Chất lượng | Tốc độ | Khi nào dùng? |
|------------|---------|-----------|--------|-------------|
| **FP16** *(= Float 16-bit, 2 bytes/param, chuẩn gốc)* | ~54GB | 100% (gốc) | Baseline *(= mức chuẩn so sánh)* | Máy có A100 80GB |
| **INT8** *(= Integer 8-bit, 1 byte/param)* | ~27GB | ~99% | Nhanh hơn | Máy có A100 40GB hoặc RTX 4090 |
| **INT4 (AWQ)** *(= 4-bit, 0.5 byte/param, nén bằng AWQ)* | ~14GB | ~95-97% | Nhanh hơn nữa | Máy chỉ có RTX 3090 24GB |
| **INT4 (GPTQ)** *(= 4-bit, nén bằng GPTQ)* | ~14GB | ~95-97% | Nhanh hơn nữa | Tương tự AWQ, chọn cái nào model hỗ trợ |

> 📝 **AWQ** = Activation-aware Weight Quantization — nén thông minh, tìm ra weight nào quan trọng thì giữ chính xác hơn, weight nào ít quan trọng thì nén mạnh hơn.  
> 📝 **GPTQ** = GPT-Quantization — phương pháp nén khác, cũng hiệu quả tương đương AWQ.  
> 📝 Cả 2 đều tốt hơn nhiều so với nén "thô" (round-to-nearest = làm tròn đơn giản).

```python
# Cách chạy model đã quantize trên vLLM
# Bước 1: Tải model AWQ (đã nén sẵn, tải từ HuggingFace)
# Bước 2: Chạy vLLM với tham số quantization

# python -m vllm.entrypoints.openai.api_server \
#     --model /models/qwen3-27b-moe3b-awq \
#     --quantization awq \
#     --max-model-len 8192
# 📝 --quantization awq = báo cho vLLM biết đây là model đã nén AWQ
```

**Task 2.4 — Setup monitoring:**

```yaml
# docker-compose-monitoring.yml
# 📝 docker-compose = file cấu hình, 1 lệnh chạy nhiều service cùng lúc

version: '3.8'
services:
  prometheus:
    # 📝 Prometheus: thu thập metrics (số liệu) từ vLLM server mỗi 15 giây
    image: prom/prometheus
    ports:
      - "9090:9090"       # 📝 Truy cập Prometheus tại http://server:9090
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    # 📝 Grafana: vẽ biểu đồ đẹp từ dữ liệu Prometheus, xem trên web
    image: grafana/grafana
    ports:
      - "3000:3000"       # 📝 Truy cập Grafana tại http://server:3000
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin123  # 📝 Mật khẩu đăng nhập Grafana
```

Các metrics *(= số liệu)* cần giám sát:

| Metric | Ý nghĩa | 📝 Giải thích | Ngưỡng cảnh báo |
|--------|---------|--------------|-----------------|
| `gpu_utilization` | % GPU đang dùng | GPU bận bao nhiêu %. 0% = rảnh, 100% = full | > 95% liên tục → cần thêm GPU |
| `gpu_memory_used` | VRAM đang dùng (GB) | Bộ nhớ GPU đang chiếm bao nhiêu | > 95% VRAM → nguy cơ OOM *(= Out of Memory, hết bộ nhớ)* |
| `gpu_temperature` | Nhiệt độ GPU (°C) | GPU nóng quá sẽ tự giảm tốc hoặc hỏng | > 85°C → cần kiểm tra tản nhiệt |
| `request_throughput` | Request/giây | Bao nhiêu câu hỏi xử lý được mỗi giây | Giảm đột ngột → có vấn đề |
| `avg_ttft` | TTFT trung bình (ms) | Thời gian chờ chữ đầu tiên | > 1000ms → cần tối ưu |
| `error_rate` | Tỷ lệ lỗi (%) | Bao nhiêu % request bị lỗi | > 1% → cần fix |

**🏁 Milestone M2:** Cuối tuần 4 → **Demo gọi API live**, gửi câu hỏi qua API → nhận câu trả lời stream.

---

## ═══════════════════════════════════════════
## GIAI ĐOẠN 3: TỐI ƯU & DRILL (Tuần 5-6)
## ═══════════════════════════════════════════

### WHAT — Làm gì?

> **"Drill"** — Đào sâu, đánh giá kỹ, tối ưu hiệu năng, đo benchmark *(= chạy test có hệ thống để ra con số cụ thể)*.

Nói đơn giản: Xe đã chạy được (GĐ2), giờ **mang đi đua thử, canh chỉnh động cơ, đo tốc độ bằng số liệu**.

### WHY — Tại sao phải làm?

| Lý do | Giải thích |
|-------|-----------|
| **Engine chưa tối ưu** | Config mặc định chưa phải tốt nhất. Tuning *(= điều chỉnh tham số)* có thể tăng tốc 2-5x |
| **Cần số liệu cho sếp** | Sếp hỏi "nhanh cỡ nào? tốt cỡ nào?" → phải có **con số cụ thể**, không nói "nhanh lắm" được |
| **Phát hiện vấn đề sớm** | Stress test *(= bơm thật nhiều request để test giới hạn)* → phát hiện memory leak *(= rò rỉ bộ nhớ)*, crash *(= sập)*, bottleneck *(= nút thắt cổ chai, phần chậm nhất)* |
| **Chọn quantization tối ưu** | Từ bảng so sánh GĐ2, chọn mức nén tốt nhất: chất lượng/tốc độ/VRAM cân bằng |
| **Drill = lặp đi lặp lại** | Chạy → đo → phát hiện vấn đề → sửa → chạy lại → đo lại. Cho đến khi đạt target *(= mục tiêu)* |

### WHEN — Mốc thời gian cụ thể từng task nhỏ

| # | Task | Ngày | Thời gian | Output |
|---|------|------|-----------|--------|
| 3.1 | **Throughput benchmark** *(= đo thông lượng)* — load test *(= bơm nhiều request)* với 10, 50, 100, 200 concurrent users *(= người dùng cùng lúc)* | Ngày 25→29 | 5 ngày | Performance report |
| 3.2 | **Latency optimization** *(= tối ưu độ trễ)* — giảm TTFT *(= Time To First Token, thời gian đến chữ đầu tiên)*, tuning batch size *(= kích thước nhóm xử lý)* | Ngày 27→31 | 4 ngày | Optimized config |
| 3.3 | **Quality evaluation** *(= đánh giá chất lượng AI)* — test trên các task: hỏi đáp, tóm tắt, viết code, tiếng Việt | Ngày 29→33 | 4 ngày | Quality report |
| 3.4 | **Chọn quantization level tối ưu** — so sánh FP16/INT8/INT4, chọn mức cân bằng nhất | Ngày 30→35 | 5 ngày | Final config |
| 3.5 | **Stress testing** *(= test "tra tấn" hệ thống)* — chạy liên tục 24h, context dài, edge cases *(= trường hợp cực đoan)* | Ngày 33→38 | 5 ngày | Stability report |
| 3.6 | **Viết Benchmark Report** chi tiết | Ngày 38 | 1 ngày | Final benchmark report |

```
Timeline trực quan Tuần 5-6:

Ngày:  25  26  27  28  29  30  31  32  33  34  35  36  37  38
       ├───────────────────┤                                    Task 3.1: Throughput
               ├───────────────────┤                            Task 3.2: Latency
                       ├───────────────────┤                    Task 3.3: Quality
                           ├───────────────────────┤            Task 3.4: Quantization
                                       ├───────────────────────┤Task 3.5: Stress test
                                                              ├┤Task 3.6: Report
```

### HOW — Làm cụ thể thế nào?

**Task 3.1 — Throughput benchmark:**

```bash
# Dùng tool benchmark sẵn có của vLLM
python benchmark_serving.py \
    --backend vllm \
    --base-url http://localhost:8000 \
    --model qwen3-27b-moe3b \
    --num-prompts 100 \
    --request-rate 10
# 📝 --num-prompts 100 = gửi 100 câu hỏi
# 📝 --request-rate 10 = gửi 10 câu hỏi mỗi giây

# Chạy với nhiều mức concurrent users:
# request-rate 10  → ~10 users cùng lúc
# request-rate 50  → ~50 users cùng lúc
# request-rate 100 → ~100 users cùng lúc
```

**Bảng kết quả benchmark (template để điền):**

| Concurrent users | Throughput *(tokens/s)* | TTFT *(ms)* | TPOT *(ms)* | P99 Latency *(ms)* | Error rate |
|-----------------|----------------------|------------|------------|-------------------|-----------|
| 10 | ___ | ___ | ___ | ___ | ___% |
| 50 | ___ | ___ | ___ | ___ | ___% |
| 100 | ___ | ___ | ___ | ___ | ___% |
| 200 | ___ | ___ | ___ | ___ | ___% |

> 📝 **TPOT** = Time Per Output Token = thời gian sinh MỖI token tiếp theo. Target < 50ms.  
> 📝 **P99 Latency** = 99% request xong trong thời gian này. Ví dụ P99 = 3s → 99/100 request xong dưới 3 giây.

**Task 3.3 — Quality evaluation:**

```
Đánh giá chất lượng trên 4 loại task:

1. KIẾN THỨC TỔNG HỢP — MMLU benchmark
   📝 MMLU = bộ 14,000 câu hỏi trắc nghiệm 57 môn (toán, sử, luật, y khoa...)
   - Đo: % trả lời đúng
   - Target: > 70% (tốt cho model 27B MoE)

2. VIẾT CODE — HumanEval benchmark
   📝 HumanEval = 164 bài lập trình Python, AI viết code → chạy thử xem đúng không
   - Đo: pass@1 (% bài giải đúng ngay lần đầu)
   - Target: > 50%

3. HỘI THOẠI — MT-Bench
   📝 MT-Bench = 80 câu hội thoại nhiều lượt, GPT-4 chấm điểm 1-10
   - Đo: average score (điểm trung bình)
   - Target: > 7.5/10

4. TIẾNG VIỆT — Vietnamese QA
   - Test 100 câu hỏi tiếng Việt: kiến thức, tóm tắt, dịch thuật
   - Đo: human evaluation (người thật chấm)
   - Target: > 80% câu trả lời chấp nhận được
```

**Task 3.5 — Stress testing:**

```
Kịch bản stress test:

1. MARATHON TEST — Chạy liên tục 24 giờ:
   - Gửi 5 request/giây liên tục
   - Giám sát: VRAM, RAM, GPU temp, error rate
   - Target: không crash, không memory leak
   📝 Memory leak = RAM tăng dần theo thời gian mà không giảm → cuối cùng sập

2. LONG CONTEXT TEST — Đoạn hội thoại rất dài:
   - Input 4096 tokens (~3000 từ), output 2048 tokens
   - Kiểm tra: có bị OOM (Out of Memory) không?
   📝 OOM = hết bộ nhớ, server sập

3. EDGE CASES — Trường hợp cực đoan:
   - Input rỗng (gửi câu hỏi trống)
   - Input cực dài (vượt max_model_len)
   - Nhiều ngôn ngữ trộn lẫn
   - Request đồng thời cực cao (200+)
   - Target: xử lý gracefully (không crash, trả lỗi rõ ràng)
   📝 gracefully = "duyên dáng", tức hệ thống báo lỗi đàng hoàng thay vì sập
```

**Quy trình Drill (lặp lại):**
```
   ┌───────────────────────────────────────────────────┐
   │                  DRILL LOOP                        │
   │                                                    │
   │   Chạy benchmark ──▶ Phân tích kết quả            │
   │        ▲                    │                      │
   │        │                    ▼                      │
   │   Chạy lại          Tìm bottleneck                │
   │        ▲            (nút thắt cổ chai)             │
   │        │                    │                      │
   │        │                    ▼                      │
   │   Áp dụng fix ◀────── Tìm giải pháp              │
   │                                                    │
   │   Lặp lại cho đến khi đạt target!                 │
   └───────────────────────────────────────────────────┘
```

**🏁 Milestone M3:** Cuối tuần 6 → **Nộp Benchmark Report** đầy đủ số liệu cho sếp.

---

## ═══════════════════════════════════════════
## GIAI ĐOẠN 4: PRODUCTION & BÀN GIAO (Tuần 7-8)
## ═══════════════════════════════════════════

### WHAT — Làm gì?

> Đóng gói hệ thống bằng Docker *(= phần mềm đóng gói toàn bộ vào 1 "hộp", ai nhận cũng chạy được)*, deploy *(= triển khai)* lên server production *(= server chạy thật phục vụ user thật)*, setup monitoring đầy đủ, viết tài liệu, bàn giao.

Nói đơn giản: Nhà hàng đã thử nghiệm xong (GĐ2-3), giờ **khai trương chính thức** — có biển hiệu (docs), camera an ninh (monitoring), sổ tay vận hành (runbook).

### WHY — Tại sao phải làm?

| Lý do | Giải thích |
|-------|-----------|
| **Dev ≠ Production** | Trên máy dev crash *(= sập)* thì tự restart. Production sập → cả công ty mất AI. Cần auto-restart, monitoring |
| **Docker đảm bảo nhất quán** | "Trên máy tôi chạy được" — Docker giải quyết bằng cách đóng gói MỌI THỨ vào container *(= "hộp")* |
| **Tài liệu cho người khác** | Bạn nghỉ phép → ai vận hành? Cần docs + runbook *(= sổ tay "nếu lỗi X thì làm Y")* |
| **Monitoring production** | Cần dashboard real-time: sếp mở ra là thấy tình trạng hệ thống, không cần hỏi |

### WHEN — Mốc thời gian cụ thể từng task nhỏ

| # | Task | Ngày | Thời gian | Output |
|---|------|------|-----------|--------|
| 4.1 | **Docker containerization** *(= đóng gói vào container)* — viết Dockerfile, docker-compose | Ngày 39→42 | 4 ngày | Docker images |
| 4.2 | **Production deployment** *(= triển khai chính thức)* — deploy lên server thật, SSL *(= mã hóa kết nối, bảo mật)*, domain *(= tên miền, ví dụ: ai.company.com)* | Ngày 41→45 | 4 ngày | Production URL |
| 4.3 | **Monitoring dashboard** — setup Grafana đẹp, alert *(= cảnh báo tự động qua email/Slack khi lỗi)* | Ngày 43→47 | 4 ngày | Dashboard + alerts |
| 4.4 | **Viết Documentation** *(= tài liệu)* — User guide, API docs, ops runbook *(= sổ tay vận hành)* | Ngày 45→50 | 5 ngày | Doc package |
| 4.5 | **Knowledge transfer** *(= chuyển giao kiến thức)* — training cho team, record video | Ngày 48→52 | 4 ngày | Video training |
| 4.6 | **Final report** — tổng kết toàn dự án | Ngày 52 | 1 ngày | Final report |

```
Timeline trực quan Tuần 7-8:

Ngày:  39  40  41  42  43  44  45  46  47  48  49  50  51  52
       ├───────────────┤                                        Task 4.1: Docker
               ├───────────────────┤                            Task 4.2: Deploy
                       ├───────────────────┤                    Task 4.3: Monitoring
                               ├───────────────────────┤        Task 4.4: Docs
                                           ├───────────────────┤Task 4.5: KT
                                                              ├┤Task 4.6: Report
```

### HOW — Làm cụ thể thế nào?

**Task 4.1 — Docker containerization:**

```dockerfile
# Dockerfile — "công thức" đóng gói engine
FROM nvidia/cuda:12.1.0-runtime-ubuntu22.04
# 📝 FROM = bắt đầu từ image (hộp) có sẵn CUDA + Ubuntu

RUN apt-get update && apt-get install -y python3.11 python3-pip curl
RUN pip install vllm transformers

# Health check — mỗi 30 giây hỏi server "bạn có OK không?"
HEALTHCHECK --interval=30s --timeout=10s \
  CMD curl -f http://localhost:8000/health || exit 1
# 📝 Nếu /health không trả lời → Docker tự restart container

ENTRYPOINT ["python3", "-m", "vllm.entrypoints.openai.api_server"]
CMD ["--model", "/models/qwen3-27b-moe3b", \
     "--host", "0.0.0.0", "--port", "8000", \
     "--tensor-parallel-size", "1", \
     "--max-model-len", "8192"]
```

```yaml
# docker-compose.yml — Chạy tất cả bằng 1 lệnh: docker compose up
version: '3.8'
services:
  llm-engine:
    build: .
    runtime: nvidia        # 📝 Cho phép container dùng GPU
    ports:
      - "8000:8000"        # 📝 Map cổng 8000 trong container ra ngoài
    volumes:
      - /data/models:/models   # 📝 Mount thư mục model vào container
    restart: always        # 📝 Tự restart khi crash — quan trọng cho production!
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]

  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
```

```bash
# Chạy toàn bộ hệ thống bằng 1 lệnh:
docker compose up -d
# 📝 -d = "detached mode", chạy nền (background), không chiếm terminal

# Kiểm tra tất cả đang chạy:
docker compose ps
# 📝 Hiện danh sách tất cả container và trạng thái (running/stopped)

# Xem log (nhật ký):
docker compose logs -f llm-engine
# 📝 -f = "follow", xem log real-time
```

**Task 4.4 — Documentation (Tài liệu):**

Cần viết 3 loại tài liệu:

| Tài liệu | Dành cho ai | Nội dung |
|-----------|------------|---------|
| **User Guide** *(= hướng dẫn sử dụng)* | Developer *(= lập trình viên)* muốn gọi API | Cách gọi API, ví dụ code, parameters |
| **API Documentation** *(= tài liệu API)* | Developer tích hợp vào app | Danh sách endpoints *(= địa chỉ URL)*, request/response format |
| **Ops Runbook** *(= sổ tay vận hành)* | DevOps *(= đội vận hành)* | Cách deploy, restart, troubleshoot *(= khắc phục lỗi)*, "nếu lỗi X → làm Y" |

**🏁 Milestone M4:** Cuối tuần 8 → **Production URL + Full Docs + Monitoring Dashboard** bàn giao.

---

# 3. TỔNG HỢP: BẢNG KẾ HOẠCH TOÀN BỘ

## 3.1. Milestones tổng hợp

| Mốc | Khi nào | Demo/Output | Báo cáo cho ai |
|-----|---------|------------|----------------|
| **M1** | Cuối tuần 2 | Model trả lời được câu hỏi | Weekly report → Sếp |
| **M2** | Cuối tuần 4 | Gọi API live, stream response | Weekly report → Sếp |
| **M3** | Cuối tuần 6 | Benchmark report đầy đủ số liệu | Benchmark report → Sếp + Senior |
| **M4** | Cuối tuần 8 | Production URL + Docs + Dashboard | Final report → Sếp + Team |

## 3.2. Báo cáo hàng tuần

- **Thứ 6 hàng tuần**: Trình bày tiến độ
- Format báo cáo:
  1. Tuần này đã làm gì? (Done)
  2. Tuần sau sẽ làm gì? (Plan)
  3. Có blocker *(= vấn đề chặn tiến độ)* gì không? (Blocker)

## 3.3. Yêu cầu resources *(= tài nguyên)* từ công ty

| Yêu cầu | Từ ai | Khi nào cần | Budget *(= ngân sách)* |
|----------|-------|------------|----------------------|
| GPU server (A100 80GB) | IT/Sếp | Tuần 1 | ~$1,500-2,000/tháng (cloud) |
| HuggingFace access | IT | Tuần 1 | Miễn phí |
| Production server | IT/DevOps | Tuần 6 | Đã có từ GPU server |
| Domain + SSL | IT | Tuần 7 | ~$10-20/năm |

---

# 4. KẾT LUẬN

## Tóm tắt kế hoạch 1 trang

```
╔═══════════════════════════════════════════════════════════╗
║           KẾ HOẠCH DỰNG LLM ENGINE — TÓM TẮT            ║
║                                                           ║
║  🎯 WHAT: Dựng LLM Engine chạy Qwen 3.5 27B MoE3B       ║
║           Self-hosted, API-ready, production-grade        ║
║                                                           ║
║  💡 WHY:  Tiết kiệm 40-55% chi phí                       ║
║           Bảo mật dữ liệu 100% nội bộ                    ║
║           Tốc độ model 3B, trí tuệ model 27B (MoE)       ║
║                                                           ║
║  📅 WHEN: 8 tuần, 4 giai đoạn                            ║
║           Tuần 1-2: Nghiên cứu & Setup                   ║
║           Tuần 3-4: Dựng Engine & API                     ║
║           Tuần 5-6: Tối ưu & Drill                       ║
║           Tuần 7-8: Production & Bàn giao                 ║
║                                                           ║
║  🔧 HOW:  vLLM engine + Docker + Prometheus/Grafana       ║
║           Quantization (AWQ/GPTQ) nếu cần                ║
║           Drill: benchmark → tối ưu → lặp lại            ║
║           Opus 4.6 hỗ trợ code + debug + planning        ║
║                                                           ║
║  📊 TARGET:                                               ║
║     TTFT < 500ms | Throughput > 30 tokens/s               ║
║     Uptime > 99% | Error rate < 0.1%                      ║
╚═══════════════════════════════════════════════════════════╝
```

## Cam kết

- ✅ Báo cáo thứ 6 hàng tuần
- ✅ Demo tại mỗi milestone (M1, M2, M3, M4)
- ✅ Escalate *(= báo cáo lên cấp trên)* blocker trong 24h
- ✅ Tài liệu đầy đủ để bàn giao

---

> **Ghi chú cuối:** Kế hoạch này linh hoạt — nếu gặp vấn đề bất ngờ (GPU yếu hơn dự kiến, model lỗi...), sẽ điều chỉnh timeline và báo cáo ngay. Mục tiêu là **M2 (API chạy được) trong 4 tuần** — đây là mốc quan trọng nhất vì từ đó team đã có thể bắt đầu dùng thử.
