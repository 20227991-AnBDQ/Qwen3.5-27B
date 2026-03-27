# 📊 BẢN TRÌNH BÀY: Kế hoạch Dựng LLM Engine — Qwen 3.5 27B MoE3B

> **Người trình bày:** [Tên bạn] — Thực tập sinh  
> **Ngày trình bày:** 13/03/2026 (Thứ Sáu)  
> **Thời lượng dự kiến:** 15-20 phút  
> **Cấu trúc trình bày:** 3W1H (What - Why - When - How)

---

## 📋 Agenda *(= Nội dung trình bày, "chương trình" của buổi họp)*

| # | Phần | Nội dung |
|---|------|---------|
| 1 | **WHAT** | Mục tiêu dự án — Dựng cái gì? |
| 2 | **WHY** | Tại sao phải làm? Lợi ích gì? |
| 3 | **WHEN** | Timeline cụ thể — Từng task nhỏ, mốc thời gian |
| 4 | **HOW** | Làm bằng cách nào? Công nghệ gì? |
| 5 | | Thách thức & giải pháp |
| 6 | | Kết luận |

---

# PHẦN 1: WHAT — Dự án là gì?

## 1.1. Mục tiêu tổng quan

> **Mục tiêu:** Xây dựng một **LLM Engine** *(= hệ thống phần mềm để chạy AI, nhận câu hỏi → trả lời thông minh)* hoàn chỉnh, triển khai mô hình **Qwen 3.5 27B MoE3B** *(= model AI mã nguồn mở, 27 tỷ tham số, kiến trúc Mixture of Experts chỉ kích hoạt 3 tỷ mỗi lần)*, có khả năng phục vụ inference *(= suy luận, tức quá trình AI xử lý câu hỏi → sinh câu trả lời)* cho nội bộ công ty.

## 1.2. Giải thích từng thuật ngữ trong đề bài

| Thuật ngữ | Giải thích ngắn gọn — đọc phát hiểu |
|-----------|--------------------------------------|
| **LLM Engine** | Hệ thống phần mềm chạy mô hình AI ngôn ngữ lớn. Giống như "máy chạy" cho AI — nó nhận câu hỏi, đưa vào model, rồi trả lời. |
| **Qwen 3.5** | Tên model AI mã nguồn mở *(= ai cũng xem/tải code được, miễn phí)* của Alibaba (công ty Trung Quốc), phiên bản 3.5 (mới nhất). |
| **27B** | 27 Billion = 27 tỷ tham số *(parameters)*. Tham số = các con số model đã "học" từ dữ liệu. Càng nhiều tham số → AI càng "thông minh", nhưng cũng cần máy mạnh hơn. |
| **MoE 3B** | MoE = Mixture of Experts = "Hỗn hợp Chuyên gia". Tổng model có 27B tham số nhưng mỗi lần xử lý chỉ **kích hoạt 3B** → nhanh như model nhỏ, thông minh như model lớn. |
| **Opus 4.6** | Claude Opus 4.6 — AI của công ty Anthropic. Trong dự án này, dùng nó như **trợ lý hỗ trợ** viết code, debug, lập kế hoạch. Không phải model ta triển khai. |
| **Drill** | Quá trình đào sâu: chạy thử → đánh giá kỹ → tối ưu → fine-tune *(= huấn luyện thêm cho domain riêng)* → lặp lại cho đến khi ổn. |

## 1.3. Mục tiêu cụ thể (SMART)

> 📝 **SMART** = phương pháp đặt mục tiêu: **S**pecific (cụ thể), **M**easurable (đo được), **A**chievable (khả thi), **R**elevant (phù hợp), **T**ime-bound (có deadline). Sếp rất thích khi bạn trình bày mục tiêu theo SMART vì nó cho thấy bạn đã suy nghĩ kỹ.

| Tiêu chí | Chi tiết |
|----------|---------|
| **Specific** *(Cụ thể)* | Triển khai Qwen 3.5 27B MoE3B trên LLM Engine (vLLM), expose API *(= mở cổng kết nối)* tương thích OpenAI *(= dùng được giống hệt cách gọi ChatGPT API)* |
| **Measurable** *(Đo được)* | TTFT < 500ms *(TTFT = Time To First Token, thời gian từ lúc gửi câu hỏi đến lúc nhận chữ đầu tiên — target dưới 0.5 giây)*, throughput *(= thông lượng, số câu trả lời xử lý được mỗi giây)* > 30 tokens/s, uptime *(= thời gian hệ thống chạy ổn định, không bị sập)* > 99% |
| **Achievable** *(Khả thi)* | Dùng framework có sẵn (vLLM), model open-source *(= mã nguồn mở, miễn phí tải)*, hardware phù hợp |
| **Relevant** *(Phù hợp)* | Phục vụ nhu cầu AI nội bộ: chatbot *(= trợ lý chat tự động)*, xử lý tài liệu, code assistant *(= AI hỗ trợ viết code)* |
| **Time-bound** *(Có deadline)* | MVP *(= Minimum Viable Product, "sản phẩm tối thiểu chạy được" — chưa hoàn hảo nhưng dùng được)* trong 4 tuần, production-ready *(= sẵn sàng chạy thật)* trong 8 tuần |

## 1.4. Deliverables *(= Sản phẩm bàn giao — những thứ cuối cùng bạn "nộp" cho sếp)*

1. ✅ LLM Engine chạy ổn định với Qwen 3.5 27B MoE3B
2. ✅ API endpoint *(= địa chỉ URL mà ứng dụng khác gọi vào để dùng AI)* tương thích OpenAI format
3. ✅ Benchmark report *(= báo cáo đo hiệu năng: nhanh chậm ra sao, chất lượng thế nào)*
4. ✅ Documentation *(= tài liệu hướng dẫn)* : hướng dẫn deploy *(= triển khai hệ thống)*, troubleshoot *(= khắc phục lỗi)*
5. ✅ Monitoring dashboard *(= bảng điều khiển giám sát)*: theo dõi real-time *(= theo dõi trực tiếp, ngay lập tức)*

---

# PHẦN 2: WHY — Tại sao cần làm?

## 2.1. Vấn đề hiện tại

```
Hiện tại (AS-IS):
┌────────────────────────────────────┐
│  Đang dùng API bên ngoài          │
│  (gọi ChatGPT/Google qua mạng)    │
│                                    │
│  ❌ Chi phí cao & khó kiểm soát    │
│  ❌ Dữ liệu công ty gửi ra ngoài  │
│  ❌ Phụ thuộc bên thứ 3            │
│  ❌ Không tùy chỉnh được           │
│  ❌ Rate limit & downtime          │
└────────────────────────────────────┘
```

> 📝 **Rate limit** = giới hạn số lần gọi API mỗi phút/giờ. Ví dụ OpenAI chỉ cho gọi 60 request/phút → đông user là nghẽn.  
> 📝 **Downtime** = thời gian hệ thống bị sập, không dùng được. Nếu OpenAI sập → cả công ty ta bị ảnh hưởng.

## 2.2. Giải pháp đề xuất

```
Tương lai (TO-BE):
┌────────────────────────────────────┐
│  Self-hosted LLM Engine            │
│  (tự chạy AI trên server của mình) │
│                                    │
│  ✅ Chi phí cố định, dự đoán được  │
│  ✅ Dữ liệu 100% nội bộ           │
│  ✅ Không phụ thuộc ai              │
│  ✅ Fine-tune cho domain riêng     │
│  ✅ Toàn quyền kiểm soát           │
└────────────────────────────────────┘
```

> 📝 **Self-hosted** = tự mình "host" (chạy, lưu trữ) trên server của công ty, không phải trả tiền thuê bên ngoài từng lần dùng.  
> 📝 **Fine-tune** = "tinh chỉnh" — lấy model có sẵn rồi huấn luyện thêm trên dữ liệu riêng của công ty (ví dụ: dữ liệu pháp luật, y tế, tài chính) để AI giỏi hơn trong lĩnh vực đó.

## 2.3. Tại sao chọn Qwen 3.5 27B MoE3B mà không chọn model khác?

| Tiêu chí | Qwen 3.5 27B MoE3B | Llama 3 70B | GPT-4 API |
|----------|-------------------|-------------|-----------|
| **Chi phí vận hành** | Thấp (1 GPU) | Cao (2-4 GPU) | Rất cao (trả tiền theo lần dùng) |
| **Tốc độ inference** | Nhanh (chỉ 3B active) | Chậm (70B active) | Phụ thuộc mạng + API |
| **Chất lượng** | Tốt (kiến thức 27B) | Rất tốt | Xuất sắc |
| **Bảo mật dữ liệu** | ✅ On-premise | ✅ On-premise | ❌ Cloud |
| **Customization** | ✅ Fine-tune được | ✅ Fine-tune được | ❌ Giới hạn |
| **License** | Apache 2.0 | Llama License | Proprietary |
| **GPU cần** | 1x A100 80GB | 2x A100 80GB | Không cần GPU |

> 📝 **On-premise** = chạy trên máy chủ đặt tại công ty mình, dữ liệu không ra ngoài internet.  
> 📝 **Cloud** = chạy trên server của bên khác (Amazon, Google, Microsoft), dữ liệu phải gửi ra ngoài.  
> 📝 **Apache 2.0** = loại giấy phép mã nguồn mở cho phép dùng thương mại, miễn phí. Thoải mái dùng cho sản phẩm kiếm tiền.  
> 📝 **Llama License** = giấy phép của Meta (Facebook), cũng miễn phí nhưng có điều kiện (ví dụ: doanh nghiệp trên 700 triệu user phải xin phép riêng).  
> 📝 **Proprietary** = "sở hữu riêng", bạn không có quyền xem code, phải trả tiền để dùng, và phải tuân theo luật của họ.  
> 📝 **A100 80GB** = card GPU (card đồ họa chuyên cho AI) của NVIDIA, có 80GB bộ nhớ riêng (VRAM). Đây là dòng cao cấp cho AI, giá ~$10,000-15,000/cái.

**Điểm đặc biệt của MoE — Tại sao nó vượt trội?**

> Qwen 3.5 27B MoE3B có **kiến thức tương đương model 27B** tham số, nhưng tốc độ inference **gần bằng model 3B** tham số. Đây là sự kết hợp tốt nhất giữa **chất lượng** và **chi phí**.

**Đào sâu — MoE hoạt động như thế nào?**

Trong kiến trúc MoE (Mixture of Experts), mô hình được thiết kế với nhiều "chuyên gia" (expert networks) song song nhau. Mỗi expert *(= chuyên gia, thực chất là một mạng neural nhỏ chuyên xử lý một loại thông tin)* là một **Feed-Forward Network (FFN)** *(= mạng truyền thẳng — lớp xử lý dữ liệu cơ bản nhất trong AI, nhận input → biến đổi → ra output)* riêng biệt.

Khi một token *(= đơn vị nhỏ nhất của text mà AI xử lý, có thể là 1 từ hoặc 1 phần từ, ví dụ "xin chào" có thể là 2 tokens)* đầu vào cần xử lý:

1. **Router Network** *(= "bộ định tuyến", một mạng neural rất nhỏ chuyên phân loại)* tính điểm cho mỗi expert
2. Chọn **top-K experts** *(= K chuyên gia có điểm cao nhất, thường K=2)* 
3. Chỉ có K experts đó thực hiện tính toán → tiết kiệm cực lớn
4. Output = **weighted sum** *(= tổng có trọng số — expert nào điểm cao hơn thì đóng góp nhiều hơn)* của các experts được chọn

```
Ví dụ cụ thể dễ hiểu:
- Model có 8 experts, mỗi expert ~3B params (tham số)
- Tổng: 8 × 3B + shared params (phần dùng chung) ≈ 27B params
- Mỗi token chỉ đi qua 1-2 experts → active params (tham số thực sự chạy) ≈ 3B
- Kết quả: FLOPs (số phép tính) giảm 8x nhưng kiến thức giữ nguyên 27B
```

> 📝 **FLOPs** = Floating Point Operations = số phép tính dấu chấm động. Càng ít FLOPs → chạy càng nhanh, tốn ít điện hơn. MoE giảm FLOPs 8x = nhanh hơn 8 lần so với model thông thường cùng kích thước.  
> 📝 **Shared params** = các tham số dùng chung cho tất cả experts (ví dụ: lớp Attention, lớp Embedding). Không phải toàn bộ 27B đều chia cho experts — có phần nào expert nào cũng cần.

**Ví dụ đời thường:** Bệnh viện có 8 bác sĩ chuyên khoa (= 8 experts). Bệnh nhân đến (= input), lễ tân (= router) chuyển đến 1-2 bác sĩ phù hợp nhất thay vì phải khám tất cả 8 bác sĩ → nhanh hơn, vẫn chính xác.

## 2.4. ROI *(= Return on Investment, "tỷ lệ hoàn vốn" — bỏ bao nhiêu tiền ra, thu lại bao nhiêu)* dự kiến

| Khoản mục | API bên ngoài (hiện tại) | Self-hosted (đề xuất) |
|-----------|------------------------|---------------------|
| Chi phí/tháng | ~$3,000-5,000 (tùy usage) | ~$1,500-2,000 (thuê GPU cloud) |
| Setup cost *(chi phí cài đặt ban đầu)* | $0 | ~$2,000-3,000 (một lần) |
| Break-even *(= điểm hòa vốn, lúc tiết kiệm đủ bù chi phí setup)* | — | ~2-3 tháng |
| Năm đầu tiên | ~$36,000-60,000 | ~$20,000-27,000 |

> **Kết luận phần WHY:** Tiết kiệm **40-55% chi phí** sau khi hòa vốn, đồng thời tăng **bảo mật** (dữ liệu ở nội bộ) và **tính độc lập** (không phụ thuộc ai).

---

# PHẦN 3: WHEN — Mốc thời gian cụ thể

## 3.1. Tổng quan timeline *(= dòng thời gian, lịch trình)* — 8 tuần

```
Tuần 1-2: Research & Setup          ████████░░░░░░░░░░░░░░░░  25%
Tuần 3-4: Core Engine Development   ████████████████░░░░░░░░  50%
Tuần 5-6: Optimization & Benchmark  ██████████████████████░░  75%
Tuần 7-8: Production & Handover     ████████████████████████  100%
```

## 3.2. Chi tiết từng giai đoạn — TỪNG TASK NHỎ CỤ THỂ

---

### 📅 TUẦN 1-2: Research & Setup *(Nghiên cứu & Chuẩn bị)*

**WHAT — Giai đoạn này làm gì?**
> Tìm hiểu, so sánh các công nghệ, chuẩn bị server và môi trường, tải model về, chạy thử lần đầu.

**WHY — Tại sao phải làm giai đoạn này?**
> Không thể xây nhà mà không có nền móng. Giai đoạn này giống "đi chợ mua nguyên liệu + đọc công thức" trước khi nấu ăn. Nếu chọn sai framework hoặc server yếu → phải làm lại từ đầu.

**WHEN — Các task cụ thể:**

| # | Task | Ngày bắt đầu | Ngày kết thúc | Output *(= kết quả bàn giao)* |
|---|------|-------------|---------------|------|
| 1.1 | Khảo sát framework *(= so sánh các "bộ khung" phần mềm để chạy AI)* | Ngày 1 | Ngày 3 | Bảng so sánh vLLM vs SGLang vs TGI |
| 1.2 | Xin access GPU server + setup môi trường dev *(= cài đặt máy phát triển)* | Ngày 1 | Ngày 5 | Server sẵn sàng, CUDA + Python chạy OK |
| 1.3 | Download model Qwen 3.5 27B MoE3B từ HuggingFace *(= kho model AI lớn nhất thế giới, giống GitHub cho AI)* | Ngày 4 | Ngày 6 | File model ~54GB trên server |
| 1.4 | Chạy thử "Hello World" — gửi câu hỏi đơn giản qua model | Ngày 6 | Ngày 8 | Screenshot model trả lời thành công |
| 1.5 | Nghiên cứu kiến trúc MoE — hiểu router, expert, load balancing *(= cân bằng tải, đảm bảo các expert được dùng đều)* | Ngày 5 | Ngày 10 | Technical notes |

> 📝 **Framework** = "bộ khung" phần mềm có sẵn mà bạn dùng làm nền để xây ứng dụng, thay vì viết từ số 0. Ví dụ: vLLM, SGLang là framework cho LLM Engine.  
> 📝 **HuggingFace** = website/nền tảng lớn nhất để chia sẻ model AI. Giống "App Store cho AI models". Bạn lên đó tải model miễn phí, giống tải app trên điện thoại.  
> 📝 **CUDA** = phần mềm của NVIDIA cho phép lập trình GPU. Giống "hệ điều hành" cho card đồ họa. Không có CUDA → GPU không chạy được AI.

**HOW — Làm cụ thể thế nào?**

```bash
# Bước 1: Kiểm tra GPU server có sẵn sàng chưa
nvidia-smi
# → Xác nhận: GPU model (A100), VRAM (80GB), CUDA version (12.1+)

# Bước 2: Tạo môi trường ảo Python (tách biệt, không ảnh hưởng hệ thống)
conda create -n qwen-engine python=3.11 -y
conda activate qwen-engine
# 📝 conda = trình quản lý thư viện/môi trường Python
# 📝 "môi trường ảo" = sandbox riêng, cài gì vào đây không ảnh hưởng máy chính

# Bước 3: Cài đặt PyTorch (thư viện AI nền tảng) + CUDA
pip install torch==2.4.0 --index-url https://download.pytorch.org/whl/cu121
# 📝 PyTorch = thư viện AI phổ biến nhất, giống "nền móng" để chạy model

# Bước 4: Cài đặt vLLM (engine chạy model)
pip install vllm>=0.6.0

# Bước 5: Cài thư viện hỗ trợ
pip install transformers accelerate safetensors huggingface_hub
# 📝 transformers = thư viện của HuggingFace để load model
# 📝 accelerate = hỗ trợ chạy trên nhiều GPU
# 📝 safetensors = format an toàn để lưu model weights (các con số "bộ não" AI)

# Bước 6: Tải model về (nặng ~54GB, cần internet nhanh)
huggingface-cli download Qwen/Qwen3-27B-MoE3B \
    --local-dir /models/qwen3-27b-moe3b

# Bước 7: Test nhanh — load tokenizer (bộ tách từ) xem model có OK không
python -c "
from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained('/models/qwen3-27b-moe3b')
print('Tokenizer loaded:', tokenizer.vocab_size, 'tokens')
"
# 📝 Tokenizer = bộ tách từ, chuyển text thành số để model hiểu.
#    Ví dụ: "Xin chào" → [23451, 8923]
```

**🏁 Milestone M1 *(= mốc quan trọng thứ 1)*:** Cuối tuần 2 → **Demo chạy model cơ bản** cho sếp.

---

### 📅 TUẦN 3-4: Core Engine Development *(Phát triển Engine)*

**WHAT — Giai đoạn này làm gì?**
> Dựng vLLM server chính thức, mở API, thử quantization (nén model), bắt đầu monitoring.

**WHY — Tại sao phải làm giai đoạn này?**
> Tuần 1-2 mới chỉ "chạy thử" trên máy. Giờ phải biến nó thành "dịch vụ" mà người khác gọi được qua API, giống như biến từ "nấu ăn ở nhà" thành "mở nhà hàng phục vụ khách".

**WHEN — Các task cụ thể:**

| # | Task | Ngày bắt đầu | Ngày kết thúc | Output |
|---|------|-------------|---------------|--------|
| 2.1 | Triển khai vLLM server — config *(= cấu hình)*, launch *(= khởi chạy)*, API endpoint *(= địa chỉ URL để gọi AI)* | Ngày 11 | Ngày 15 | Server running, gọi API được |
| 2.2 | Tạo API layer — OpenAI-compatible *(= tương thích OpenAI, gọi giống ChatGPT API)*,  authentication *(= xác thực, chỉ người có quyền mới gọi được)* | Ngày 13 | Ngày 17 | API docs |
| 2.3 | Test Quantization *(= lượng tử hóa, nén model nhỏ lại)*: thử INT8, INT4, so sánh chất lượng | Ngày 15 | Ngày 20 | Quantization report |
| 2.4 | Setup basic monitoring *(= giám sát cơ bản)*: Prometheus metrics *(= thu thập số liệu)*, health check *(= kiểm tra "sức khỏe" server)* | Ngày 18 | Ngày 22 | Monitoring dashboard |
| 2.5 | Integration testing *(= test tích hợp, test toàn bộ hệ thống từ đầu đến cuối)* | Ngày 20 | Ngày 24 | Test suite *(= bộ test)* |

> 📝 **Quantization (Lượng tử hóa)** = kỹ thuật "nén" model, giảm dung lượng bộ nhớ cần thiết. Giống như nén ảnh: ảnh gốc PNG 10MB → JPEG 2MB, nhìn gần giống nhau.
> - **FP16** = Float 16-bit (2 bytes/param) → model 27B cần ~54GB VRAM
> - **INT8** = Integer 8-bit (1 byte/param) → giảm còn ~27GB, chất lượng giảm ~1%
> - **INT4** = Integer 4-bit (0.5 byte/param) → giảm còn ~14GB, chất lượng giảm ~3-5%
> 
> 📝 **Prometheus** = phần mềm miễn phí thu thập số liệu (CPU, GPU, RAM, request/giây, lỗi...). Giống "camera giám sát" nhưng cho server.  
> 📝 **Health check** = endpoint đặc biệt (ví dụ gọi vào `/health`) để kiểm tra server còn sống không. Giống hỏi "bạn ơi bạn có OK không?", server trả lời "OK" hoặc im lặng (= chết).

**HOW — Cấu hình vLLM Server cụ thể:**

```python
# config.py — Cấu hình chi tiết cho vLLM

ENGINE_CONFIG = {
    # Model
    "model": "/models/qwen3-27b-moe3b",     # Đường dẫn đến model đã tải
    "tokenizer": "/models/qwen3-27b-moe3b",  # Dùng tokenizer đi kèm model
    "trust_remote_code": True,                # Cho phép chạy code custom của model
    
    # Performance (Hiệu năng)
    "tensor_parallel_size": 1,     # Số GPU sử dụng. 1 = dùng 1 card GPU
    "max_model_len": 8192,         # Context window tối đa (= model "nhớ" được bao nhiêu chữ)
    "gpu_memory_utilization": 0.90, # Dùng 90% VRAM (bộ nhớ GPU). Giữ 10% dự phòng
    "dtype": "auto",               # Tự chọn kiểu số (FP16 hoặc BF16, tùy GPU)
    
    # Batching (Gom request)
    "max_num_batched_tokens": 32768, # Max tokens xử lý cùng lúc trong 1 batch
    "max_num_seqs": 256,             # Max số request đồng thời
    # 📝 Batching = gom nhiều request lại xử lý 1 lần trên GPU
    #    Giống xe buýt: chở 50 người 1 chuyến nhanh hơn chạy 50 chuyến xe ôm
    
    # Optimization (Tối ưu)
    "enable_prefix_caching": True,   # Cache phần prompt giống nhau giữa các request
    "enforce_eager": False,          # Dùng CUDA graphs (tối ưu tốc độ GPU)
}
```

```bash
# Lệnh khởi chạy server
python -m vllm.entrypoints.openai.api_server \
    --model /models/qwen3-27b-moe3b \
    --host 0.0.0.0 \     # 📝 0.0.0.0 = cho phép truy cập từ mọi IP, không chỉ localhost
    --port 8000 \         # 📝 Port = "cổng" mạng. Server lắng nghe ở cổng 8000
    --tensor-parallel-size 1 \
    --max-model-len 8192
```

**HOW — Gọi API sau khi deploy:**

```python
# Gọi API giống hệt cách gọi ChatGPT!
import openai  # 📝 Thư viện chính thức của OpenAI, dùng luôn cho self-hosted

client = openai.OpenAI(
    base_url="http://localhost:8000/v1",  # 📝 Trỏ vào server của MÌNH thay vì OpenAI
    api_key="not-needed"  # Self-hosted không cần API key thật
)

response = client.chat.completions.create(
    model="qwen3-27b-moe3b",
    messages=[
        {"role": "system", "content": "Bạn là trợ lý AI thông minh."},
        {"role": "user", "content": "Giải thích blockchain đơn giản."}
    ],
    temperature=0.7,  # 📝 temperature = mức "sáng tạo". 0 = luôn trả lời giống nhau.
                      #    1 = rất ngẫu nhiên, sáng tạo. 0.7 = cân bằng
    max_tokens=1024,  # 📝 Số token max trong câu trả lời (~750 từ)
    stream=True       # 📝 stream = trả về từng chữ một (giống ChatGPT gõ từng chữ)
                      #    thay vì đợi xong hết mới hiện
)

for chunk in response:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

**🏁 Milestone M2:** Cuối tuần 4 → **Demo gọi API live** cho sếp. Gọi 1 câu hỏi → nhận câu trả lời → xong.

---

### 📅 TUẦN 5-6: Optimization & Benchmark *(Tối ưu & Đánh giá)*

**WHAT — Giai đoạn này làm gì?**
> "Tuning" hệ thống cho nhanh, ổn, tốt nhất có thể. Rồi chạy benchmark đo kết quả bằng số liệu cụ thể.

**WHY — Tại sao phải làm giai đoạn này?**
> Tuần 3-4 engine đã chạy nhưng có thể chưa tối ưu (chậm, tốn RAM, 1 lúc đông user là lag). Giai đoạn này giống "sửa xe, canh chỉnh máy, rồi đem đi đua thử" — cần có **số liệu cụ thể** để chứng minh với sếp "hệ thống tốt đến đâu".

**WHEN — Các task cụ thể:**

| # | Task | Ngày bắt đầu | Ngày kết thúc | Output |
|---|------|-------------|---------------|--------|
| 3.1 | Benchmark throughput *(= đo thông lượng)*: load test *(= bơm thật nhiều request)* với 10, 50, 100 concurrent users *(= người dùng cùng lúc)* | Ngày 25 | Ngày 29 | Performance report |
| 3.2 | Optimize latency *(= giảm độ trễ)*: tối ưu TTFT, tuning batching | Ngày 27 | Ngày 31 | Optimized config |
| 3.3 | Quality evaluation *(= đánh giá chất lượng)*: test QA, summary, code, tiếng Việt | Ngày 29 | Ngày 33 | Quality report |
| 3.4 | Chọn quantization level tối ưu — FP16 vs INT8 vs INT4 | Ngày 30 | Ngày 35 | Final quant config |
| 3.5 | Stress testing *(= test "tra tấn" hệ thống)*: chạy 24h liên tục, edge cases *(= trường hợp cực đoan)* | Ngày 33 | Ngày 38 | Stability report |

> 📝 **Load test** = gửi rất nhiều request cùng lúc vào server để xem nó "chịu" được bao nhiêu trước khi chậm/sập. Giống thử xem cầu chịu được bao nhiêu xe chạy qua.  
> 📝 **Concurrent users** = số người dùng cùng một lúc. 100 concurrent users = 100 người đang gọi API đồng thời.  
> 📝 **Latency** = độ trễ, thời gian từ lúc gửi câu hỏi đến lúc nhận được câu trả lời đầy đủ.

**HOW — Benchmark sẽ đo gì?**

```
Benchmark gồm 4 phần:

1. THROUGHPUT TEST (đo thông lượng):
   - 10 → 50 → 100 → 200 concurrent requests
   - Đo: tokens/s (token mỗi giây), requests/s (request mỗi giây)
   - Input: 128 tokens | Output: 256 tokens

2. LATENCY TEST (đo độ trễ):
   - TTFT (Time to First Token): Target < 500ms
     📝 = thời gian từ gửi câu hỏi đến nhận chữ ĐẦU TIÊN. Dưới 0.5 giây là tốt.
   - TPOT (Time per Output Token): Target < 50ms  
     📝 = thời gian sinh MỖI TOKEN tiếp theo. Dưới 50ms = trên 20 token/giây.
   - End-to-end latency P50, P95, P99
     📝 P99 = 99% request xong trong thời gian này. 
     Ví dụ: P99 = 3 giây → 99/100 request xong dưới 3 giây, chỉ 1/100 chậm hơn.

3. QUALITY TEST (đo chất lượng AI):
   - MMLU benchmark (kiến thức tổng hợp: toán, sử, khoa học...)
     📝 MMLU = bộ câu hỏi trắc nghiệm 57 môn, dùng đo "thông minh" của AI
   - HumanEval (code generation — AI viết code có đúng không)
   - MT-Bench (multi-turn conversation — hội thoại nhiều lượt)
   - Vietnamese QA dataset (test riêng cho tiếng Việt)

4. STABILITY TEST (đo ổn định):
   - Chạy liên tục 24 giờ → xem có bị memory leak không
     📝 Memory leak = "rò rỉ bộ nhớ", server dùng ngày càng nhiều RAM 
     mà không giải phóng → cuối cùng sập
   - GPU temperature monitoring (nhiệt độ GPU, target < 85°C)
   - Error rate tracking (tỷ lệ lỗi, target < 0.1%)
```

**🏁 Milestone M3:** Cuối tuần 6 → **Nộp Benchmark Report** chi tiết cho sếp.

---

### 📅 TUẦN 7-8: Production & Handover *(Triển khai chính thức & Bàn giao)*

**WHAT — Giai đoạn này làm gì?**
> Đóng gói hệ thống bằng Docker, deploy lên server production, setup monitoring đầy đủ, viết docs, bàn giao.

**WHY — Tại sao phải làm giai đoạn này?**
> Chạy trên máy dev ≠ chạy production. Production cần: ổn định 24/7, tự restart khi lỗi, có monitoring, có docs để người khác vận hành khi bạn vắng mặt.

**WHEN — Các task cụ thể:**

| # | Task | Ngày bắt đầu | Ngày kết thúc | Output |
|---|------|-------------|---------------|--------|
| 4.1 | Docker containerization *(= đóng gói hệ thống vào "container" — xem giải thích bên dưới)* | Ngày 39 | Ngày 42 | Dockerfile, docker-compose |
| 4.2 | Production deployment *(= triển khai chính thức lên server thật)* | Ngày 41 | Ngày 45 | Running production server |
| 4.3 | Monitoring dashboard — Grafana *(= phần mềm vẽ biểu đồ đẹp từ số liệu Prometheus)* | Ngày 43 | Ngày 48 | Dashboard URL |
| 4.4 | Documentation *(= viết tài liệu)*: User guide, API docs, ops runbook *(= sổ tay vận hành, "nếu lỗi X thì làm Y")* | Ngày 45 | Ngày 50 | Doc package |
| 4.5 | Knowledge transfer *(= chuyển giao kiến thức)* — training cho team | Ngày 48 | Ngày 52 | Recorded session |

> 📝 **Docker** = phần mềm đóng gói toàn bộ engine + thư viện + config vào 1 "hộp" (container). Ai nhận hộp đó đều chạy được giống nhau, không cần cài đặt lại gì. Giống gửi cho bạn cả cái máy tính đã cài sẵn mọi thứ, thay vì gửi hướng dẫn cài 50 bước.  
> 📝 **Grafana** = phần mềm miễn phí hiển thị biểu đồ real-time (GPU usage, latency, request/giây...) trên web. Giống "bảng đồng hồ" trong buồng lái máy bay — nhìn phát biết tình trạng toàn bộ hệ thống.  
> 📝 **docker-compose** = file cấu hình cho Docker, định nghĩa "cần chạy gì, cần bao nhiêu tài nguyên, mở cổng nào". Giống bản vẽ kiến trúc nhà vậy.

**HOW — Docker Deployment cụ thể:**

```dockerfile
# Dockerfile — "công thức" để đóng gói engine vào container
FROM nvidia/cuda:12.1.0-runtime-ubuntu22.04
# 📝 FROM = bắt đầu từ "hộp" có sẵn CUDA (GPU driver) trên Ubuntu Linux

# Cài Python
RUN apt-get update && apt-get install -y python3.11 python3-pip

# Cài vLLM + transformers
RUN pip install vllm transformers

# Health check — tự động kiểm tra server có sống không, mỗi 30 giây hỏi 1 lần
HEALTHCHECK --interval=30s --timeout=10s \
  CMD curl -f http://localhost:8000/health || exit 1

# Lệnh khởi động khi container start
ENTRYPOINT ["python3", "-m", "vllm.entrypoints.openai.api_server"]
CMD ["--model", "/models/qwen3-27b-moe3b", \
     "--host", "0.0.0.0", "--port", "8000", \
     "--tensor-parallel-size", "1", \
     "--max-model-len", "8192"]
```

**🏁 Milestone M4:** Cuối tuần 8 → **Production URL + Full Docs** bàn giao cho sếp.

---

## 3.3. Tổng hợp Milestones *(= các mốc quan trọng)*

| Mốc | Thời gian | Báo cáo | Demo gì? |
|-----|-----------|---------|----------|
| **M1** | Cuối tuần 2 | Weekly report | Chạy model, gửi câu hỏi → nhận trả lời |
| **M2** | Cuối tuần 4 | Weekly report | Gọi API live, demo OpenAI-compatible |
| **M3** | Cuối tuần 6 | Benchmark report | Số liệu: tốc độ, chất lượng, so sánh |
| **M4** | Cuối tuần 8 | Final report + docs | Production URL, monitoring dashboard |

> **Báo cáo hàng tuần:** Thứ 6 hàng tuần, trình bày tiến độ và blocker *(= vấn đề đang chặn tiến độ, không tự giải quyết được)* nếu có.

---

# PHẦN 4: HOW — Công nghệ sử dụng

## 4.1. Kiến trúc hệ thống tổng quan

```
┌──────────────────────────────────────────────────────────────────┐
│                    PRODUCTION ARCHITECTURE                        │
│                                                                  │
│  ┌──────────┐     ┌─────────────────┐     ┌─────────────────┐   │
│  │ Client   │────▶│ Load Balancer   │────▶│ LLM Engine      │   │
│  │ (App/Web)│     │ (Nginx)         │     │ (vLLM Server)   │   │
│  └──────────┘     └─────────────────┘     └───────┬─────────┘   │
│                                                    │             │
│                   ┌─────────────────┐     ┌───────▼─────────┐   │
│                   │ Monitoring      │◀────│ GPU Server      │   │
│                   │ (Grafana)       │     │ (A100 80GB)     │   │
│                   └─────────────────┘     └─────────────────┘   │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │              Model Storage (NVMe SSD)                    │    │
│  │      Qwen 3.5 27B MoE3B weights (~54GB)                 │    │
│  └──────────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────────┘
```

> 📝 **Load Balancer (Nginx)** = "bộ cân bằng tải". Khi có nhiều user gọi cùng lúc, Nginx phân chia request đều ra các server. Giống lễ tân hướng dẫn khách vào đúng phòng, không để 1 phòng đông quá.  
> 📝 **Nginx** *(đọc là "engine-x")* = phần mềm miễn phí, rất phổ biến, dùng làm web server hoặc load balancer.  
> 📝 **NVMe SSD** = loại ổ cứng nhanh nhất hiện tại (đọc/ghi 3-7 GB/giây). Cần thiết vì khi khởi động engine phải đọc file model 54GB từ ổ cứng vào RAM → ổ càng nhanh, khởi động càng nhanh.

## 4.2. Technology Stack *(= "chồng" công nghệ, danh sách tất cả công nghệ dùng trong dự án)*

| Layer *(= tầng)* | Công nghệ | Lý do chọn | 📝 Giải thích nhanh |
|-------|-----------|-----------|---------------------|
| **Model** | Qwen 3.5 27B MoE3B | MoE hiệu quả, open-source, license thương mại | Model AI chính mà ta triển khai |
| **Engine** | vLLM 0.6+ | Phổ biến nhất, community *(= cộng đồng)* lớn | Phần mềm "chạy" model, giống động cơ cho xe |
| **Quantization** | AWQ / GPTQ | Giảm VRAM 50-75%, ít mất chất lượng | Kỹ thuật nén model. **AWQ** = Activation-aware Weight Quantization, **GPTQ** = GPT-Quantization. Cả 2 đều nén FP16 → INT4 nhưng bằng cách thông minh hơn nén thô |
| **API Format** | OpenAI-compatible | Dễ tích hợp, ecosystem *(= hệ sinh thái, nhiều tool/app hỗ trợ)* lớn | Gọi giống ChatGPT API → app cũ chuyển sang dễ dàng |
| **Container** | Docker + NVIDIA Container Toolkit | Reproducible *(= ai chạy cũng ra kết quả giống nhau)*, dễ deploy | Đóng gói toàn bộ hệ thống vào 1 "hộp" |
| **Infrastructure** | Linux Ubuntu 22.04, CUDA 12.1 | Ổn định, hỗ trợ rộng | Hệ điều hành + driver GPU |
| **Monitoring** | Prometheus + Grafana | Miễn phí, tiêu chuẩn ngành | Prometheus thu data, Grafana vẽ biểu đồ |
| **GPU** | NVIDIA A100 80GB (hoặc H100) | Tier-1 *(= hạng cao nhất)* cho LLM | Card GPU chuyên AI |
| **AI Assistant** | Claude Opus 4.6 | Hỗ trợ code, debug, planning | Dùng như "mentor AI" hỗ trợ mình |

**Đào sâu — Tại sao chọn vLLM mà không chọn engine khác?**

vLLM là engine phổ biến nhất hiện nay nhờ các tính năng:

1. **PagedAttention** *(= quản lý bộ nhớ GPU theo "trang", giống cách máy tính quản lý RAM ảo)*
   - Giảm lãng phí bộ nhớ GPU 60-80%
   - Cho phép phục vụ nhiều người cùng lúc hơn (more concurrent requests)
   
2. **Continuous Batching** *(= gom request liên tục, không chờ)*
   - Request mới được thêm vào batch *(= nhóm xử lý)* ngay khi có request cũ hoàn thành
   - Không cần đợi cả batch xong mới bắt đầu batch mới — tiết kiệm thời gian chờ
   
3. **Tensor Parallelism** *(= chia model ra nhiều GPU chạy song song)*
   - Hỗ trợ TP *(= Tensor Parallel)* = 1, 2, 4, 8 GPU
   - Model quá lớn cho 1 GPU? Chia đôi ra 2 GPU chạy cùng lúc
   
4. **OpenAI-compatible API** *(= Drop-in replacement, "thay thế trực tiếp" OpenAI)*
   - Chỉ cần đổi `base_url` trong code, app cũ dùng ChatGPT API chạy luôn không cần sửa gì
   
5. **MoE Support** *(= hỗ trợ tốt kiến trúc MoE)*
   - Expert parallelism *(= chia experts ra nhiều GPU)*
   - Optimized router *(= bộ định tuyến đã tối ưu)*

---

# PHẦN 5: Thách thức và Giải pháp

## 5.1. Thách thức kỹ thuật

| # | Thách thức | Mức độ | Giải pháp dự kiến |
|---|-----------|--------|-------------------|
| 1 | **VRAM không đủ** cho FP16 (cần ~54GB) | 🔴 Cao | Dùng quantization INT8/INT4 (giảm còn 27/14GB) |
| 2 | **Latency cao** *(= trả lời chậm)* khi context *(= đoạn hội thoại)* dài | 🟡 TB | Tối ưu KV Cache *(= bộ nhớ đệm)*, Flash Attention *(= kỹ thuật tính attention nhanh + ít bộ nhớ)*, giới hạn max_len |
| 3 | **MoE routing không đều** *(= có expert bận quá, expert khác rảnh)* | 🟡 TB | Monitoring expert utilization *(= theo dõi mức dùng từng expert)*, tuning router |
| 4 | **Throughput thấp** khi nhiều user | 🟡 TB | Continuous batching, horizontal scaling *(= thêm máy chủ)* |
| 5 | **Model quality cho tiếng Việt** chưa chắc tốt | 🟡 TB | Benchmark sớm (tuần 2), fine-tune nếu cần |
| 6 | **Chi phí GPU server** | 🟡 TB | Quantization giảm yêu cầu GPU, spot instances *(= thuê GPU giá rẻ vào giờ thấp điểm)* |

> 📝 **Flash Attention** = kỹ thuật tính attention (bộ phận quan trọng nhất trong AI) nhanh gấp 2-4 lần và tiết kiệm bộ nhớ hơn. Hầu hết engine mới đều có sẵn.  
> 📝 **KV Cache** = Key-Value Cache. Lưu lại kết quả attention đã tính → lần sau không tính lại. Giống ghi nhớ đáp án bài toán đã giải, không cần giải lại. Nếu không có KV Cache, cứ mỗi token mới sinh ra, AI phải tính lại TẤT CẢ token trước → cực chậm.  
> 📝 **Horizontal scaling** = "scale ngang" = thêm máy chủ mới thay vì nâng cấp máy cũ. Giống mở thêm quầy thu ngân khi siêu thị đông, thay vì bắt 1 nhân viên làm nhanh hơn.  
> 📝 **Spot instances** = thuê GPU trên cloud với giá rẻ hơn 60-90% bình thường, nhưng có thể bị thu hồi bất cứ lúc nào. Phù hợp cho thử nghiệm, không phù hợp cho production.

## 5.2. Thách thức vận hành

| # | Thách thức | Giải pháp | 📝 Giải thích |
|---|-----------|----------|---------------|
| 1 | GPU failure/crash *(= GPU hỏng/sập)* | Auto-restart *(= tự khởi động lại)*, health monitoring, fallback *(= phương án dự phòng)* | Docker tự restart container khi lỗi |
| 2 | Model updates *(= Qwen ra version mới)* | Blue-green deployment, rollback plan | **Blue-green** = chạy 2 server (xanh = cũ, lục = mới), chuyển traffic dần sang mới, nếu lỗi → quay lại cũ ngay |
| 3 | Security *(= bảo mật)*: prompt injection *(= user cố "hack" AI bằng câu hỏi đặc biệt)* | Input sanitization *(= lọc input xấu)*, rate limiting *(= giới hạn số request/phút)*, auth *(= xác thực)* | Chặn từ đầu vào |
| 4 | Scale *(= mở rộng)* khi user tăng | Horizontal scaling, load balancing | Thêm server mới, Nginx chia tải đều |

## 5.3. Thách thức cá nhân (thực tập sinh)

| Thách thức | Giải pháp |
|-----------|----------|
| Kiến thức LLM còn non | Học song song với làm, dùng Opus 4.6 hỗ trợ bất cứ lúc nào |
| Chưa quen GPU programming | Sử dụng framework có sẵn (vLLM), không cần tự viết CUDA |
| Khối lượng công việc lớn | Chia nhỏ tasks, ưu tiên MVP *(= sản phẩm tối thiểu)* trước, báo blockers sớm |

## 5.4. Risk Mitigation *(= Giảm thiểu rủi ro — "nếu xảy ra A thì làm B")*

| Risk *(= rủi ro)* | Probability *(= xác suất)* | Impact *(= tác động)* | Mitigation *(= cách giảm thiểu)* |
|------|------------|--------|-----------|
| GPU không đủ VRAM | Trung bình | Cao | Dùng AWQ/GPTQ quantization → giảm xuống INT4 (14GB VRAM) |
| Model kém cho tiếng Việt | Thấp | Cao | Benchmark sớm (tuần 2), nếu kém → dùng bản Qwen đã fine-tune tiếng Việt |
| vLLM không hỗ trợ tốt MoE | Thấp | Cao | Backup plan: chuyển sang SGLang hoặc TensorRT-LLM |
| Deadline trễ | Trung bình | Trung bình | Buffer *(= dự phòng)* 1 tuần, báo sớm nếu có rủi ro |
| Server downtime *(= sập)* | Thấp | Trung bình | Auto-restart, monitoring tự gửi alert *(= cảnh báo)* |

---

# PHẦN 6: Kết luận

## 6.1. Tóm tắt dự án

```
╔═══════════════════════════════════════════════════════════╗
║                    TÓM TẮT DỰ ÁN                        ║
║                                                           ║
║  🎯 WHAT:  Dựng LLM Engine chạy Qwen 3.5 27B MoE3B      ║
║            → Self-hosted, API-ready                       ║
║                                                           ║
║  💡 WHY:   Bảo mật dữ liệu nội bộ                        ║
║            Tiết kiệm 40-55% chi phí                       ║
║            Tùy chỉnh, không phụ thuộc ai                  ║
║                                                           ║
║  📅 WHEN:  8 tuần                                         ║
║            MVP tuần 4 — Production tuần 8                 ║
║            Báo cáo thứ 6 hàng tuần                        ║
║                                                           ║
║  🔧 HOW:   vLLM + Docker + Monitoring                    ║
║            GPU: A100 80GB                                 ║
║            Quantization nếu cần                           ║
║                                                           ║
║  ⚡ HIỆU NĂNG: Tốc độ model 3B, trí tuệ model 27B       ║
║                (nhờ kiến trúc MoE)                        ║
╚═══════════════════════════════════════════════════════════╝
```

## 6.2. Next Steps *(= Bước tiếp theo)* — nếu được sếp approve *(= phê duyệt)*

1. **Tuần này:** Xin approval từ sếp, confirm *(= xác nhận)* budget *(= ngân sách)* GPU server
2. **Tuần tới:** Setup dev environment, download model, first inference
3. **Ongoing *(= liên tục)*:** Báo cáo hàng tuần vào thứ 6

## 6.3. Yêu cầu hỗ trợ từ sếp & team

| Yêu cầu | Từ ai | Deadline |
|----------|-------|---------|
| Approve GPU budget (~$1,500-2,000/tháng) | Sếp | Tuần này |
| Access GPU server | IT/DevOps *(= đội vận hành hạ tầng)* | Tuần tới |
| Danh sách use case *(= bài toán cụ thể)* muốn AI giải quyết | Team/Sếp | Tuần 2 |
| Review & feedback benchmark report | Sếp/Senior *(= anh/chị kỹ sư cấp cao)* | Tuần 6 |

## 6.4. Cam kết

- ✅ Báo cáo tiến độ **hàng tuần vào thứ 6**
- ✅ Escalate *(= báo cáo lên cấp cao hơn)* blocker **trong vòng 24h**
- ✅ Demo tại mỗi milestone
- ✅ Document đầy đủ để team có thể handover *(= bàn giao, tiếp quản)*

---

## 📎 Phụ lục

### A. Tài liệu tham khảo

| Tài liệu | Mô tả |
|-----------|-------|
| vLLM Documentation | https://docs.vllm.ai — Hướng dẫn sử dụng vLLM |
| Qwen 3 Model Card | HuggingFace: Qwen/Qwen3-27B-MoE3B — Thông tin model |
| MoE Paper | "Switch Transformers" (Google, 2021) — Paper gốc về MoE |
| PagedAttention Paper | "Efficient Memory Management for LLM Serving" (UC Berkeley, 2023) |
| Flash Attention Paper | "FlashAttention: Fast and Memory-Efficient Exact Attention" (Stanford, 2022) |

### B. Bảng tổng hợp thuật ngữ — Tra cứu nhanh

| Thuật ngữ | Tiếng Việt | Giải thích 1 câu |
|-----------|-----------|-------------------|
| Inference | Suy luận | AI xử lý câu hỏi → sinh câu trả lời |
| Throughput | Thông lượng | Số request/token xử lý được mỗi giây |
| Latency | Độ trễ | Thời gian chờ từ gửi request đến nhận response |
| TTFT | Thời gian đến token đầu | Từ gửi câu hỏi đến nhận chữ đầu tiên |
| TPOT | Thời gian mỗi token | Thời gian sinh mỗi token tiếp theo |
| Token | Đơn vị text | Phần nhỏ nhất AI xử lý (~0.75 từ/token tiếng Anh) |
| Quantization | Lượng tử hóa | Nén model: FP16→INT8→INT4. Nhỏ hơn, nhanh hơn |
| VRAM | Bộ nhớ GPU | RAM riêng trên card đồ họa. Cần đủ để load model |
| FP16 | Số thực 16-bit | 2 bytes/tham số. Tiêu chuẩn hiện tại |
| INT8 | Số nguyên 8-bit | 1 byte/tham số. Nén 2x, giảm chất lượng ~1% |
| INT4 | Số nguyên 4-bit | 0.5 byte/tham số. Nén 4x, giảm chất lượng ~3-5% |
| KV Cache | Bộ nhớ Key-Value | Cache attention đã tính → không tính lại |
| PagedAttention | Quản lý bộ nhớ theo trang | Tiết kiệm 60-80% VRAM cho KV Cache |
| Flash Attention | Attention nhanh | Tính attention nhanh 2-4x, tiết kiệm VRAM |
| Tensor Parallelism | Song song tensor | Chia model ra nhiều GPU chạy cùng lúc |
| Batch / Batching | Gom request | Xử lý nhiều request 1 lần → nhanh hơn |
| Fine-tuning | Tinh chỉnh | Huấn luyện thêm model trên dữ liệu riêng |
| Distillation | Chưng cất | Dạy model nhỏ học từ model lớn |
| MoE | Hỗn hợp chuyên gia | Nhiều expert, chỉ kích hoạt 1-2 mỗi lần |
| Docker | Đóng gói container | Gói toàn bộ hệ thống vào 1 "hộp" chạy được |
| Kubernetes (K8s) | Quản lý container | Ông quản lý nhiều Docker containers |
| Prometheus | Thu thập metrics | Camera giám sát cho server |
| Grafana | Vẽ biểu đồ | Bảng điều khiển đẹp từ dữ liệu Prometheus |
| API | Giao diện lập trình | Cổng kết nối để app khác gọi vào dùng AI |
| Endpoint | Địa chỉ API | URL cụ thể (ví dụ: /v1/chat/completions) |
| MVP | Sản phẩm tối thiểu | Bản đầu tiên "chạy được", chưa hoàn hảo |
| Deploy | Triển khai | Đưa hệ thống lên server chạy thật |
| Production | Môi trường thật | Server phục vụ user thật, không phải test |
| Blocker | Vấn đề chặn | Thứ gì đó ngăn bạn tiếp tục, cần hỗ trợ |

---

> **💡 Lưu ý cho người trình bày:**  
> - Phần **WHAT + WHY**: 5-7 phút — Nói mục tiêu, lý do, lợi ích. Sếp quan tâm nhất phần này.  
> - Phần **WHEN**: 3-4 phút — Timeline + milestones. Sếp muốn biết bao giờ xong.  
> - Phần **HOW**: 5-7 phút — Công nghệ, kiến trúc. Đồng nghiệp kỹ thuật quan tâm phần này.  
> - **Thách thức + Kết luận**: 2-3 phút — Cho thấy bạn đã lường trước vấn đề.  
> - Nếu sếp hỏi chi tiết kỹ thuật → dùng các phần "Đào sâu" và bảng thuật ngữ để trả lời.  
> - **Tự tin lên** — bạn đã chuẩn bị rất kỹ rồi! 💪
