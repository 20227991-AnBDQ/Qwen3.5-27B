# 📚 KIẾN THỨC CƠ BẢN VỀ LLM ENGINE — Từ Zero đến Hiểu

> **Mục đích:** Cung cấp nền tảng kiến thức cho một thực tập sinh mới bắt đầu tìm hiểu về LLM Engine, đặc biệt trong bối cảnh dự án triển khai **Qwen 3.5 27B MoE3B** với sự hỗ trợ của **Opus 4.6**.

---

## Mục lục

1. [Giải thích đề bài — Từng thuật ngữ một](#1-giải-thích-đề-bài--từng-thuật-ngữ-một)
2. [LLM Engine là gì?](#2-llm-engine-là-gì)
3. [Kiến trúc Transformer — Trái tim của LLM](#3-kiến-trúc-transformer--trái-tim-của-llm)
4. [Quy trình dựng một LLM Engine](#4-quy-trình-dựng-một-llm-engine)
5. [Các công nghệ và framework phổ biến](#5-các-công-nghệ-và-framework-phổ-biến)
6. [Inference Optimization — Tối ưu hóa suy luận](#6-inference-optimization--tối-ưu-hóa-suy-luận)
7. [Tại sao LLM Engine quan trọng?](#7-tại-sao-llm-engine-quan-trọng)
8. [Kết luận](#8-kết-luận)

---

## 1. Giải thích đề bài — Từng thuật ngữ một

Đề bài của bạn: **"Dựng LLM Engine qua Qwen 3.5 27B MoE3B, sử dụng Opus 4.6, drill"**

Hãy tách từng phần ra:

### 1.1. LLM Engine là gì?

**LLM** = **Large Language Model** (Mô hình Ngôn ngữ Lớn)

**LLM Engine** = Hệ thống phần mềm cho phép **chạy (inference)** một mô hình ngôn ngữ lớn, bao gồm:
- Nạp mô hình vào bộ nhớ (RAM/VRAM GPU) ← *VRAM = Video RAM, bộ nhớ riêng của card đồ họa (GPU), nơi model được nạp vào để chạy*
- Nhận input từ người dùng (prompt/câu hỏi)
- Xử lý qua mô hình để sinh ra output (câu trả lời)
- Tối ưu tốc độ, bộ nhớ, throughput ← *throughput = "thông lượng", tức số request/câu trả lời mà hệ thống xử lý được trong 1 giây. Giống như số xe chạy qua trạm thu phí mỗi phút vậy*

**Ví dụ đơn giản:** Hãy tưởng tượng LLM giống như một bộ não khổng lồ. LLM Engine giống như cơ thể chứa bộ não đó — nó cung cấp máu (dữ liệu), oxy (tài nguyên tính toán), và hệ thần kinh (pipeline xử lý) để bộ não có thể hoạt động.

**Các LLM Engine phổ biến:**
| Engine | Đặc điểm |
|--------|----------|
| **vLLM** | Tối ưu throughput cao, PagedAttention, phổ biến nhất |
| **TGI** (Text Generation Inference) | Của HuggingFace, dễ dùng |
| **SGLang** | Nhanh, hỗ trợ structured generation |
| **llama.cpp** | Chạy trên CPU, nhẹ, dùng GGUF format |
| **TensorRT-LLM** | Của NVIDIA, tối ưu cực mạnh trên GPU NVIDIA |
| **Ollama** | Dễ cài đặt, dành cho cá nhân |

> **📝 Giải thích nhanh các thuật ngữ trong bảng trên:**
> - **PagedAttention** = Kỹ thuật quản lý bộ nhớ GPU thông minh, chia nhỏ bộ nhớ thành "trang" (pages) giống cách máy tính quản lý RAM. Nhờ vậy GPU không bị lãng phí bộ nhớ → phục vụ được nhiều người cùng lúc hơn.
> - **TGI** = Text Generation Inference — tool của HuggingFace để chạy model AI, giống vLLM nhưng đơn giản hơn, dễ bắt đầu hơn.
> - **Structured generation** = Khả năng buộc AI trả lời theo đúng format cụ thể (ví dụ: bắt buộc trả JSON, bắt buộc trả đúng schema). Rất hữu ích khi tích hợp AI vào ứng dụng.
> - **GGUF format** = Một dạng file nén để lưu model AI. Giống như .mp4 là format cho video, GGUF là format cho model — được tối ưu để chạy trên CPU/laptop mà không cần GPU đắt tiền.

### 1.2. 27B là gì?

**27B = 27 Billion = 27 tỷ tham số (parameters)**

Tham số là gì? Là các con số (weights) bên trong mô hình mà nó đã "học" từ dữ liệu. Càng nhiều tham số → mô hình càng "thông minh" và có khả năng xử lý phức tạp hơn, NHƯNG cũng cần nhiều tài nguyên hơn.

**So sánh quy mô:**
> **📝 FP16 là gì?** FP16 = Float Point 16-bit, tức mỗi tham số được lưu bằng số thực 16-bit (2 bytes). Đây là độ chính xác tiêu chuẩn hiện tại. So sánh: FP32 (4 bytes/param, chính xác nhất), FP16 (2 bytes/param, đủ tốt), INT8 (1 byte/param, hơi giảm chất lượng), INT4 (0.5 byte/param). Mỗi tham số 27B × 2 bytes = ~54GB VRAM.

| Mô hình | Số tham số | VRAM cần (FP16) | Ví dụ |
|---------|-----------|-----------------|-------|
| Nhỏ | 1-3B | 2-6 GB | Qwen2.5-1.5B, Phi-3-mini |
| Trung bình | 7-14B | 14-28 GB | Llama 3 8B, Qwen2.5-7B |
| Lớn | 27-72B | 54-144 GB | Qwen 3.5 27B, Llama 3 70B |
| Rất lớn | 100B+ | 200+ GB | GPT-4, Llama 3.1 405B |

**Lưu ý quan trọng:** 27B ở đây là **tổng số tham số** của mô hình, nhưng nhờ MoE (xem bên dưới), không phải tất cả đều được kích hoạt cùng lúc.

### 1.3. MoE (Mixture of Experts) là gì?

**MoE = Mixture of Experts = Hỗn hợp các Chuyên gia**

Đây là một **kiến trúc mô hình** rất thông minh. Thay vì dùng toàn bộ 27B tham số cho mỗi token đầu vào, MoE chia mô hình thành nhiều "chuyên gia" (experts) nhỏ hơn và chỉ **kích hoạt một vài chuyên gia** cho mỗi input.

**Cách hoạt động:**

```
Input token → Router (Bộ định tuyến) → Chọn top-K experts → Chỉ tính toán qua K experts đó → Output
```

**Ví dụ cụ thể với Qwen 3.5 27B MoE3B:**
- **Tổng tham số:** 27 tỷ (27B) — bao gồm TẤT CẢ experts
- **Tham số kích hoạt (active):** 3 tỷ (3B) — chỉ số tham số THỰC SỰ chạy cho mỗi token
- Nghĩa là: Mô hình có "kiến thức" của 27B tham số, nhưng mỗi lần xử lý chỉ "nghĩ" bằng 3B tham số

**Tại sao MoE tuyệt vời?**
| Tiêu chí | Dense Model (thông thường) | MoE Model |
|----------|---------------------------|-----------|
| Tốc độ inference | Chậm (dùng tất cả params) | **Nhanh** (chỉ dùng subset) |
| Chất lượng | Tốt | **Rất tốt** (nhiều kiến thức hơn) |
| VRAM cần | Rất nhiều | Nhiều (phải load tất cả), nhưng tính toán ít |
| Chi phí tính toán | Cao | **Thấp hơn nhiều** |

**Ví dụ thực tế dễ hiểu:**
> Hãy tưởng tượng một bệnh viện có 9 bác sĩ chuyên khoa (= 9 experts). Khi bệnh nhân đến (= input token), lễ tân (= router) sẽ chuyển bệnh nhân đến 1-2 bác sĩ phù hợp nhất (= top-K experts), thay vì phải khám qua tất cả 9 bác sĩ. Kết quả: nhanh hơn, nhưng vẫn chính xác vì đúng chuyên khoa.

**Chi tiết kỹ thuật MoE trong Qwen 3.5 27B MoE3B:**
- Mỗi layer trong Transformer có nhiều Feed-Forward Network (FFN) experts
- Một **Router/Gate network** nhỏ quyết định expert nào xử lý token nào
- Thường chọn top-2 hoặc top-4 experts mỗi lần
- Load balancing loss được thêm vào training để đảm bảo các expert được sử dụng đều

### 1.4. Opus 4.6 là gì?

**Opus 4.6 = Claude Opus 4.6** — Là mô hình AI của công ty **Anthropic**.

Trong ngữ cảnh dự án của bạn, Opus 4.6 đóng vai trò là **công cụ hỗ trợ** (AI assistant) trong quá trình phát triển, KHÔNG phải là mô hình mà bạn triển khai. Cụ thể:

- **Hỗ trợ viết code:** Giúp viết script triển khai, config, debug
- **Hỗ trợ nghiên cứu:** Giải thích khái niệm, so sánh framework
- **Hỗ trợ lập kế hoạch:** Soạn plan, timeline, báo cáo
- **Pair programming:** Làm việc cùng bạn như một đồng nghiệp senior

**Nói đơn giản:** Bạn dùng Opus 4.6 (tôi) như một "mentor AI" để giúp bạn hoàn thành việc dựng LLM Engine chạy Qwen 3.5.

### 1.5. Drill là gì?

**Drill** trong ngữ cảnh LLM có thể hiểu theo các nghĩa sau:

**Nghĩa 1 — Knowledge Distillation (Chưng cất kiến thức):**
- Là quá trình "dạy" một mô hình nhỏ hơn (student) học từ mô hình lớn hơn (teacher)
- Ví dụ: Dùng output của Qwen 72B (teacher) để fine-tune Qwen 27B MoE (student)
- Mục đích: Mô hình nhỏ đạt chất lượng gần bằng mô hình lớn

**Nghĩa 2 — Drill-down / Deep-dive:**
- Quá trình đào sâu, thử nghiệm, benchmark kỹ lưỡng mô hình
- Đánh giá hiệu năng trên các task cụ thể
- Fine-tune và tối ưu cho use case riêng

**Nghĩa 3 — Iterative Refinement (Luyện tập lặp đi lặp lại):**
- Chạy thử → đánh giá → cải thiện → chạy lại
- Giống như "drill" trong quân đội: luyện tập cho đến khi thuần thục

**Trong dự án của bạn,** "drill" nhiều khả năng bao gồm cả 3 nghĩa: Bạn sẽ lấy mô hình Qwen 3.5 27B MoE3B → triển khai lên engine → benchmark/đánh giá kỹ → tối ưu → có thể fine-tune/distill cho use case cụ thể.

---

## 2. LLM Engine là gì? (Chi tiết hơn)

### 2.1. Định nghĩa chính thức

LLM Engine là một **hệ thống phần mềm end-to-end** *(end-to-end = "từ đầu đến cuối", tức hệ thống lo hết mọi thứ từ A→Z, từ nhận input cho đến trả output, bạn không cần ghép thêm tool nào khác)* cho phép:
1. **Load** model weights từ disk vào GPU memory
2. **Tokenize** input text thành token IDs
3. **Inference** — chạy forward pass qua model để sinh output
4. **Decode** token IDs thành text
5. **Serve** — phục vụ nhiều user đồng thời qua API

### 2.2. Kiến trúc tổng quan của một LLM Engine

```
┌─────────────────────────────────────────────────────────┐
│                    LLM ENGINE                           │
│                                                         │
│  ┌──────────┐   ┌──────────────┐   ┌────────────────┐  │
│  │ API      │──▶│ Request      │──▶│ Tokenizer      │  │
│  │ Server   │   │ Scheduler    │   │ (Text → Tokens)│  │
│  └──────────┘   └──────────────┘   └───────┬────────┘  │
│                                            │            │
│  ┌──────────┐   ┌──────────────┐   ┌───────▼────────┐  │
│  │ Response  │◀──│ Detokenizer  │◀──│ Model Engine   │  │
│  │ Streamer  │   │ (Tokens→Text)│   │ (GPU Compute)  │  │
│  └──────────┘   └──────────────┘   └────────────────┘  │
│                                                         │
│  ┌──────────────────────────────────────────────────┐   │
│  │          Memory Manager (KV Cache, Paging)       │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

**Giải thích từng thành phần:**

| Thành phần | Vai trò | Ví dụ |
|-----------|---------|-------|
| **API Server** | Nhận request từ client | FastAPI, gRPC endpoint |
| **Request Scheduler** | Xếp hàng, sắp xếp request, batching | Continuous batching |
| **Tokenizer** | Chuyển text thành số (token IDs) | BPE tokenizer |
| **Model Engine** | Chạy forward pass trên GPU | CUDA kernels |
| **Detokenizer** | Chuyển token IDs thành text | Decode tokens |
| **Memory Manager** | Quản lý VRAM, KV Cache | PagedAttention |
| **Response Streamer** | Trả kết quả dạng stream | SSE/WebSocket |

### 2.3. Quy trình xử lý một request

```
User gửi: "Xin chào, bạn là ai?"
    │
    ▼
1. Tokenize: [23451, 8923, 1234, 5678, 9012]
    │
    ▼
2. Prefill phase: Xử lý TẤT CẢ input tokens cùng lúc
   → Tạo KV Cache cho mỗi token
     (KV Cache = Key-Value Cache, "bộ nhớ tạm" lưu lại kết quả attention đã tính.
      Giống như bạn ghi chú lại đáp án bài tập đã giải, lần sau không cần giải lại.
      Nếu không có KV Cache, mỗi token mới phải tính lại attention cho TẤT CẢ token trước đó → cực chậm.)
   → Sinh ra token đầu tiên của response
    │
    ▼
3. Decode phase: Sinh từng token một (auto-regressive)
   → Token 1: "Tôi"
   → Token 2: "là"
   → Token 3: "một"
   → Token 4: "trợ"
   → Token 5: "lý"
   → Token 6: "AI"
   → Token 7: <EOS> (End of Sequence)
    │
    ▼
4. Detokenize & Stream: Trả về "Tôi là một trợ lý AI"
```

---

## 3. Kiến trúc Transformer — Trái tim của LLM

Tất cả các LLM hiện đại (GPT, Llama, Qwen) đều dựa trên kiến trúc **Transformer**. Bạn cần hiểu cơ bản về nó.

### 3.1. Cấu trúc cơ bản

```
Input Embedding
       │
       ▼
┌──────────────────┐
│  Transformer     │ ◀── Lặp lại N lần (N = số layers)
│  Block           │
│                  │
│  ┌────────────┐  │
│  │ Attention  │  │  ← Tìm mối quan hệ giữa các từ
│  └────────────┘  │
│       │          │
│  ┌────────────┐  │
│  │ FFN / MoE  │  │  ← Xử lý thông tin (đây là nơi MoE hoạt động)
│  └────────────┘  │
└──────────────────┘
       │
       ▼
Output (next token prediction)
```

### 3.2. Self-Attention (Cơ chế Tự chú ý)

Đây là phần quan trọng nhất của Transformer:

- **Ý tưởng:** Mỗi từ trong câu "nhìn" vào tất cả các từ khác để hiểu ngữ cảnh
- **Ví dụ:** Trong câu "Con mèo ngồi trên ghế, nó rất đáng yêu" → từ "nó" cần "nhìn" vào "con mèo" để biết "nó" đang nói về ai

**Công thức (đơn giản hóa):**
$$Attention(Q, K, V) = softmax\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$

Trong đó:
- **Q** (Query): "Tôi muốn tìm gì?"
- **K** (Key): "Tôi chứa thông tin gì?"
- **V** (Value): "Đây là thông tin thực sự của tôi"

### 3.3. Feed-Forward Network (FFN) vs MoE

**Trong Dense model (bình thường):**
- Mỗi layer có 1 FFN duy nhất
- TẤT CẢ tokens đều đi qua FFN này
- Ví dụ: FFN có 4096 → 11008 → 4096 neurons

**Trong MoE model (như Qwen 3.5 27B MoE3B):**
- Mỗi layer có NHIỀU FFN (gọi là experts)
- Mỗi token chỉ đi qua 1-2 experts được router chọn
- Ví dụ: 8 experts, mỗi cái 4096 → 1376 → 4096, chọn top-2

```
              Token
                │
                ▼
         ┌──────────┐
         │  Router   │  ← Quyết định expert nào xử lý
         └──────────┘
        ╱    │     ╲
       ╱     │      ╲
Expert 1  Expert 2  Expert 3  ...  Expert 8
  ✓(0.6)   ✓(0.3)    ✗         ...    ✗
       ╲     │
        ╲    │
         ▼   ▼
    Weighted Sum (0.6 * E1 + 0.3 * E2)
                │
                ▼
            Output
```

---

## 4. Quy trình dựng một LLM Engine

### 4.1. Tổng quan các bước

```
Bước 1: Chuẩn bị hạ tầng (Hardware & Environment)
    │
    ▼
Bước 2: Tải model weights (Download model)
    │
    ▼
Bước 3: Chọn và cài đặt Engine framework
    │
    ▼
Bước 4: Cấu hình và khởi chạy Engine
    │
    ▼
Bước 5: Tối ưu hóa (Quantization, Batching, etc.)
    │
    ▼
Bước 6: Đánh giá & Benchmark
    │
    ▼
Bước 7: Triển khai production (Deploy)
    │
    ▼
Bước 8: Monitoring & Maintenance
```

### 4.2. Chi tiết từng bước

#### Bước 1: Chuẩn bị hạ tầng

**Yêu cầu phần cứng cho Qwen 3.5 27B MoE3B:**

| Thông số | Tối thiểu | Khuyến nghị |
|----------|-----------|------------|
| **GPU** | 1x A100 40GB hoặc 2x RTX 4090 | 1x A100 80GB hoặc 1x H100 |
| **VRAM** | ~30GB (INT8 quantized) | ~54GB (FP16 full) |
| **RAM** | 64GB | 128GB |
| **Storage** | 100GB SSD | 200GB NVMe SSD |
| **CUDA** | 11.8+ | 12.1+ |

> **📝 Giải thích nhanh các thuật ngữ phần cứng:**
> - **1x, 2x** = Số lượng. 1x A100 = 1 cái card GPU A100. 2x RTX 4090 = 2 cái card GPU RTX 4090. Giống như bạn nói "1 cái laptop" hay "2 cái laptop" vậy thôi.
> - **A100, H100, RTX 4090** = Tên các loại card GPU (card đồ họa) của NVIDIA. A100/H100 là dòng chuyên cho AI (cực đắt, ~$10,000-30,000/cái). RTX 4090 là card gaming cao cấp cũng chạy AI được (~$1,600/cái).
> - **VRAM** = Video RAM — bộ nhớ riêng trên card GPU. Model AI cần được "nạp" vào VRAM mới chạy được. VRAM càng nhiều → chạy model càng lớn.
> - **INT8 quantized** = Nén model từ FP16 (2 bytes/param) xuống INT8 (1 byte/param = số nguyên 8-bit). Giống nén ảnh từ PNG sang JPEG: file nhỏ hơn 2x, chất lượng giảm không đáng kể (~1%). Nên VRAM cần chỉ còn ~30GB thay vì ~54GB.
> - **SSD** = Solid State Drive — ổ cứng thể rắn, nhanh hơn ổ HDD truyền thống rất nhiều. **NVMe SSD** = loại SSD nhanh nhất hiện tại (đọc/ghi ~3-7 GB/s), cần thiết vì khi khởi động engine phải đọc ~54GB model weights từ ổ cứng vào RAM → ổ càng nhanh, khởi động càng nhanh.
> - **CUDA** = Nền tảng phần mềm của NVIDIA để lập trình GPU. Giống như "hệ điều hành" cho GPU vậy. Phiên bản 11.8+ hoặc 12.1+ là yêu cầu tối thiểu.

> **Lưu ý:** Mặc dù MoE chỉ kích hoạt 3B params khi inference, bạn vẫn cần load TOÀN BỘ 27B params vào VRAM. MoE tiết kiệm **compute**, không tiết kiệm **memory** (trừ khi dùng expert offloading).

**Chuẩn bị môi trường:**
```bash
# Cài đặt Python environment
conda create -n llm-engine python=3.11
conda activate llm-engine

# Cài đặt PyTorch với CUDA
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121

# Cài đặt các thư viện cần thiết
pip install transformers accelerate safetensors
```

#### Bước 2: Tải model weights

```bash
# Cách 1: Dùng huggingface-cli
pip install huggingface_hub
huggingface-cli download Qwen/Qwen3-27B-MoE3B --local-dir ./models/qwen3-27b-moe3b

# Cách 2: Dùng Python
from huggingface_hub import snapshot_download
snapshot_download(
    repo_id="Qwen/Qwen3-27B-MoE3B",
    local_dir="./models/qwen3-27b-moe3b"
)

# Cách 3: Dùng Git LFS
git lfs install
git clone https://huggingface.co/Qwen/Qwen3-27B-MoE3B
```

> **Kích thước download:** ~50-55GB cho FP16 weights

#### Bước 3: Chọn Engine framework

Với Qwen 3.5 27B MoE3B, các engine phù hợp nhất:

**1. vLLM (Khuyến nghị cao nhất):**
```bash
pip install vllm

# Khởi chạy server
python -m vllm.entrypoints.openai.api_server \
    --model ./models/qwen3-27b-moe3b \
    --tensor-parallel-size 1 \
    --max-model-len 4096 \
    --trust-remote-code
```

**2. SGLang:**
```bash
pip install sglang[all]

# Khởi chạy server
python -m sglang.launch_server \
    --model-path ./models/qwen3-27b-moe3b \
    --tp 1
```

**3. Ollama (Đơn giản nhất, cho dev/test):**
```bash
ollama run qwen3:27b-moe3b
```

#### Bước 4: Cấu hình và khởi chạy

Ví dụ cấu hình vLLM chi tiết:

```python
from vllm import LLM, SamplingParams

# Khởi tạo engine
llm = LLM(
    model="./models/qwen3-27b-moe3b",
    tensor_parallel_size=1,        # Số GPU
    max_model_len=8192,            # Max context length
    gpu_memory_utilization=0.90,   # Sử dụng 90% VRAM
    dtype="auto",                  # Tự chọn precision
    trust_remote_code=True,
    enforce_eager=False,           # Dùng CUDA graphs
)

# Cấu hình sampling
sampling_params = SamplingParams(
    temperature=0.7,
    top_p=0.9,
    max_tokens=2048,
    repetition_penalty=1.1,
)

# Chạy inference
prompts = ["Xin chào, bạn có thể giới thiệu về mình không?"]
outputs = llm.generate(prompts, sampling_params)

for output in outputs:
    print(output.outputs[0].text)
```

#### Bước 5: Tối ưu hóa

**a. Quantization (Lượng tử hóa) — Giảm VRAM:**

| Phương pháp | VRAM | Chất lượng | Tốc độ |
|------------|------|-----------|--------|
| FP16 (gốc) | ~54GB | 100% | Baseline |
| INT8 (W8A8) | ~27GB | ~99% | Nhanh hơn |
| INT4 (GPTQ/AWQ) | ~14GB | ~95-97% | Nhanh hơn nữa |
| GGUF Q4_K_M | ~16GB | ~95% | Tùy backend |

```python
# Ví dụ dùng AWQ quantization
from vllm import LLM
llm = LLM(
    model="./models/qwen3-27b-moe3b-awq",  # AWQ quantized model
    quantization="awq",
    max_model_len=4096,
)
```

**b. Continuous Batching — Tăng throughput:**
- Thay vì xử lý từng request một, engine gom nhiều request lại xử lý cùng lúc
- vLLM tự động làm điều này

**c. KV Cache Optimization:**
- KV Cache lưu trữ kết quả attention đã tính rồi, không cần tính lại
- PagedAttention (của vLLM) quản lý KV Cache hiệu quả như bộ nhớ ảo trong OS

#### Bước 6: Đánh giá & Benchmark

```bash
# Benchmark throughput
python -m vllm.entrypoints.openai.api_server --model ./models/qwen3-27b-moe3b &

# Test với nhiều request song song
python benchmark_serving.py \
    --backend vllm \
    --model qwen3-27b-moe3b \
    --num-prompts 100 \
    --request-rate 10
```

**Các metric quan trọng:**
| Metric | Ý nghĩa | Target tốt |
|--------|---------|------------|
| **TTFT** (Time to First Token) | Thời gian từ gửi request đến nhận token đầu tiên | < 500ms |
| **TPS** (Tokens per Second) | Số token sinh ra mỗi giây | > 30 tokens/s |
| **Throughput** | Tổng tokens/s khi serve nhiều user | Tùy hardware |
| **Latency P99** | 99% request hoàn thành trong thời gian này | < 5s |

#### Bước 7: Triển khai production

```yaml
# docker-compose.yml
version: '3.8'
services:
  llm-engine:
    image: vllm/vllm-openai:latest
    runtime: nvidia
    ports:
      - "8000:8000"
    volumes:
      - ./models:/models
    environment:
      - NVIDIA_VISIBLE_DEVICES=all
    command: >
      --model /models/qwen3-27b-moe3b
      --tensor-parallel-size 1
      --max-model-len 8192
      --gpu-memory-utilization 0.9
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

#### Bước 8: Monitoring

- **Prometheus + Grafana:** Monitor GPU utilization, request latency, throughput
- **Logging:** Request/response logging cho debug
- **Health check:** Endpoint `/health` để monitor uptime

---

## 5. Các công nghệ và framework phổ biến

### 5.1. Framework cho Inference Engine

| Framework | Ưu điểm | Nhược điểm | Phù hợp cho |
|-----------|---------|------------|------------|
| **vLLM** | PagedAttention, throughput cao, community lớn | Cần GPU mạnh | Production serving |
| **SGLang** | Nhanh, structured generation | Mới, ít docs | Advanced use cases |
| **TensorRT-LLM** | Tối ưu cực mạnh cho NVIDIA | Phức tạp, chỉ NVIDIA | High-performance |
| **llama.cpp** | Chạy CPU/laptop, hỗ trợ nhiều mức quantization | Chậm hơn GPU | Edge deployment |
| **Ollama** | Cực dễ dùng | Ít tùy chỉnh | Dev/testing |
| **HF TGI** | Tích hợp HuggingFace | Chậm hơn vLLM | Simple deployment |

> **📝 "Nhiều quantization" nghĩa là gì?** Quantization (lượng tử hóa) là kỹ thuật nén model. "Nhiều quantization" nghĩa là llama.cpp hỗ trợ **nhiều mức nén khác nhau**: Q2, Q3, Q4, Q5, Q6, Q8... (con số càng nhỏ = nén mạnh hơn = nhẹ hơn nhưng kém chính xác hơn). Bạn được chọn mức phù hợp với máy của mình. Ví dụ: laptop 8GB RAM → dùng Q4; máy 32GB → dùng Q8 để chất lượng tốt hơn.

### 5.2. Thư viện hỗ trợ

| Thư viện | Vai trò |
|----------|---------|
| **transformers** | Load & chạy model, tokenizer |
| **accelerate** | Multi-GPU, mixed precision |
| **safetensors** | Format lưu model weights an toàn |
| **bitsandbytes** | Quantization (INT8, INT4) |
| **auto-gptq** | GPTQ quantization |
| **autoawq** | AWQ quantization |
| **flash-attention** | Attention tối ưu, tiết kiệm VRAM |

### 5.3. Infrastructure (Hạ tầng)

| Tool | Vai trò | 📝 Giải thích nhanh |
|------|--------|---------------------|
| **Docker** | Container hóa engine | Đóng gói toàn bộ engine + model + thư viện vào 1 "hộp" (container). Ai nhận hộp đó đều chạy được giống nhau, không cần cài đặt lại gì. Giống như gửi cho bạn cả cái máy tính đã cài sẵn mọi thứ, thay vì gửi hướng dẫn cài đặt 50 bước. |
| **Kubernetes** | Orchestration, scaling | Gọi tắt là **K8s**. Là "quản lý" cho nhiều Docker containers. Khi bạn có 10-100 server chạy AI, K8s tự động: khởi động lại nếu lỗi, thêm server khi đông user, giảm khi vắng. Giống một ông quản lý nhà máy, tự điều phối công nhân. |
| **NVIDIA Triton** | Multi-model serving | Server chuyên dụng của NVIDIA, cho phép chạy **nhiều model AI cùng lúc** trên 1 server. Ví dụ: vừa chạy model Qwen cho chatbot, vừa chạy model phân tích ảnh, vừa chạy model dịch thuật — tất cả trên 1 máy. |
| **Ray Serve** | Distributed serving | Framework giúp **chia tải** AI model ra nhiều máy tính. Khi 1 GPU không đủ hoặc quá nhiều user, Ray Serve tự động phân phối request ra nhiều máy. Giống mở thêm quầy thu ngân khi siêu thị đông. |
| **Prometheus/Grafana** | Monitoring | **Prometheus** = thu thập số liệu (GPU đang dùng bao nhiêu %, bao nhiêu request/giây, có lỗi không). **Grafana** = hiển thị số liệu đó thành biểu đồ đẹp trên web. Giống camera + màn hình giám sát trong phòng điều khiển vậy. |

---

## 6. Inference Optimization — Tối ưu hóa suy luận

### 6.1. Tại sao cần tối ưu?

Khi chạy Qwen 3.5 27B MoE3B:
- **Bộ nhớ:** Cần load ~54GB weights vào GPU
- **Tính toán:** Mỗi token cần hàng tỷ phép nhân ma trận
- **Chi phí:** GPU server rất đắt (A100 80GB ~ $2-3/giờ trên cloud)

→ Tối ưu = **giảm chi phí** + **tăng tốc** + **phục vụ nhiều user hơn**

### 6.2. Các kỹ thuật tối ưu chính

**1. Quantization (Lượng tử hóa):**
```
FP32 (32-bit) → FP16 (16-bit) → INT8 (8-bit) → INT4 (4-bit)
   Chính xác      Tiêu chuẩn     Hơi giảm        Giảm nhẹ
   nhất            hiện tại       chất lượng       chất lượng
```

Giống như ảnh JPEG: giảm chất lượng một chút nhưng kích thước nhỏ hơn rất nhiều.

**2. Flash Attention:**
- Giảm VRAM cho attention computation từ O(n²) xuống O(n)
- Tăng tốc computation 2-4x
- Hầu hết engine hiện đại đều tích hợp sẵn

**3. Continuous Batching:**
- Gom request → xử lý đồng thời trên GPU
- Tận dụng GPU parallelism
- Tăng throughput 2-10x so với naive batching

**4. KV Cache + PagedAttention:**
- Cache kết quả attention → không tính lại
- PagedAttention quản lý cache theo "trang" như virtual memory
- Tiết kiệm 60-80% VRAM cho KV cache

**5. Speculative Decoding:**
- Dùng model nhỏ dự đoán trước nhiều token
- Model lớn verify cùng lúc
- Tăng tốc 2-3x mà không giảm chất lượng

**6. Tensor Parallelism:**
- Chia model ra nhiều GPU
- Mỗi GPU xử lý một phần
- Cần cho model quá lớn so với 1 GPU

### 6.3. Đặc biệt cho MoE

MoE có những tối ưu riêng:
- **Expert Parallelism:** Chia experts ra nhiều GPU
- **Expert Offloading:** Chuyển expert không dùng sang CPU RAM
- **Expert Caching:** Cache expert weights thường dùng
- **Token Dropping:** Bỏ qua token ít quan trọng (khi training)

---

## 7. Tại sao LLM Engine quan trọng?

### 7.1. Trong lĩnh vực AI

1. **Democratization (Dân chủ hóa AI):** LLM Engine cho phép mọi tổ chức tự chạy AI, không phụ thuộc vào OpenAI/Google
2. **Data Privacy (Bảo mật dữ liệu):** Dữ liệu không ra khỏi server của bạn
3. **Customization (Tùy chỉnh):** Fine-tune cho domain riêng (y tế, pháp luật, tài chính)
4. **Cost Control (Kiểm soát chi phí):** Tự host rẻ hơn API khi scale lớn

### 7.2. Trong thực tế doanh nghiệp

- **Chatbot & Customer Service:** Hỗ trợ khách hàng 24/7
- **Code Assistant:** Hỗ trợ lập trình viên (như GitHub Copilot)
- **Document Processing:** Tóm tắt, phân tích tài liệu
- **Internal Search:** Tìm kiếm thông minh trong dữ liệu nội bộ
- **Content Generation:** Tạo nội dung marketing, report

### 7.3. Xu hướng hiện tại (2025-2026)

- **Open-source models ngày càng mạnh:** Qwen, Llama, Mistral cạnh tranh với closed-source
- **MoE trở thành mainstream:** Tiết kiệm chi phí, hiệu năng cao
- **Edge deployment:** Chạy model trên thiết bị cá nhân
- **Agentic AI:** LLM Engine làm "não" cho AI agents

---

## 8. Kết luận

### Tóm tắt những điểm chính:

| Thuật ngữ | Ý nghĩa |
|-----------|---------|
| **LLM Engine** | Hệ thống phần mềm để chạy và phục vụ mô hình ngôn ngữ lớn |
| **27B** | 27 tỷ tham số — kích thước tổng của mô hình |
| **MoE 3B** | Kiến trúc Mixture of Experts, chỉ kích hoạt 3B params mỗi lần |
| **Opus 4.6** | Claude Opus 4.6, AI assistant hỗ trợ bạn trong quá trình phát triển |
| **Drill** | Quá trình đào sâu, benchmark, fine-tune và distill mô hình |

### Quy trình tổng quan:

```
1. Chuẩn bị GPU server (A100/H100)
2. Download Qwen 3.5 27B MoE3B từ HuggingFace
3. Cài đặt vLLM (hoặc SGLang)
4. Cấu hình và khởi chạy engine
5. Quantize nếu cần (INT8/INT4)
6. Benchmark & đánh giá
7. Deploy production (Docker)
8. Monitor & maintain
```

### Lời khuyên cho bạn (thực tập sinh):

1. **Bắt đầu nhỏ:** Thử chạy model nhỏ trước (Qwen 0.6B, 1.5B) để hiểu flow
2. **Dùng Ollama:** Cách nhanh nhất để chạy thử model trên máy cá nhân
3. **Đọc docs:** vLLM docs (https://docs.vllm.ai) rất đầy đủ
4. **Hỏi nhiều:** Dùng Opus 4.6 (tôi) để hỏi bất cứ khi nào bạn không hiểu
5. **Hands-on:** Lý thuyết chỉ là 30%, 70% là tự tay làm và debug

---

> **Ghi nhớ:** Dựng LLM Engine không khó về mặt concept — nó khó ở việc tối ưu và xử lý các edge cases trong production. Hãy bắt đầu đơn giản, rồi tối ưu dần dần. Bạn luôn có thể quay lại file này để ôn lại kiến thức.
