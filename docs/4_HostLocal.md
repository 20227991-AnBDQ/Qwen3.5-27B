# Hướng Dẫn Host Model Qwen 3.5 Q4_K_M Trên Ollama - Cho Người Mới

## Mục Đích Của Tài Liệu Này

Bạn sẽ học cách:
- Cài đặt Ollama (công cụ để chạy model AI trên máy cá nhân)
- Tải model Qwen 3.5 Q4_K_M (model nhỏ, dễ chạy)
- Khởi động server để gọi model qua API
- Kiểm tra model hoạt động đúng

**Thời gian:** ~30 phút (tùy tốc độ internet)

---

## Phần 1: Chuẩn Bị Máy Tính

### Yêu Cầu Tối Thiểu

| Yêu Cầu | Chi Tiết |
|---------|---------|
| **RAM** | Tối thiểu 8GB (16GB tốt hơn) |
| **Ổ cứng** | Tối thiểu 10GB trống |
| **GPU** (tùy chọn) | NVIDIA, AMD hoặc Mac M1/M2 (nhanh hơn, nhưng không bắt buộc) |
| **Hệ điều hành** | Windows, macOS, hoặc Linux |

### Kiểm Tra Máy Tính

**Trên Windows:**
1. Nhấn `Win + R`, gõ `msinfo32`, nhấn Enter
2. Tìm dòng "Installed RAM" để xem RAM
3. Mở File Explorer, chuột phải vào ổ C, chọn Properties để xem dung lượng trống

**Trên macOS:**
1. Nhấn `Apple Menu > About This Mac`
2. Xem mục "Memory" (RAM) và "Storage"

---

## Phần 2: Cài Đặt Ollama

### Bước 1: Tải Ollama

1. Truy cập: **https://ollama.ai**
2. Nhấn nút **Download** (màu xanh)
3. Chọn phiên bản phù hợp với máy bạn:
   - **Windows**: Chọn "Windows"
   - **macOS**: Chọn "macOS"
   - **Linux**: Chọn "Linux"

### Bước 2: Cài Đặt

**Trên Windows:**
1. Mở file `OllamaSetup.exe` vừa tải
2. Nhấn "Install" và chờ hoàn tất
3. Ollama sẽ tự khởi động

**Trên macOS:**
1. Mở file `Ollama.dmg`
2. Kéo icon Ollama vào thư mục Applications
3. Mở Applications, tìm Ollama, nhấn đôi để chạy

**Trên Linux:**
```bash
curl https://ollama.ai/install.sh | sh
```

### Bước 3: Kiểm Tra Cài Đặt

Mở Terminal (hoặc Command Prompt trên Windows) và gõ:

```bash
ollama --version
```

Nếu thấy số phiên bản (ví dụ: `ollama version 0.1.0`), cài đặt thành công ✓

---

## Phần 3: Tải Model Qwen 3.5 Q4_K_M

### Tại Sao Chọn Qwen 3.5 Q4_K_M?

| Đặc Điểm | Lợi Ích |
|----------|---------|
| **Q4_K_M** | Phiên bản nén, chỉ cần ~3GB RAM (thay vì 15GB) |
| **Qwen 3.5** | Model mới, chất lượng tốt, hỗ trợ tiếng Việt |
| **Nhỏ gọn** | Chạy nhanh trên máy cá nhân, không cần GPU mạnh |

### Bước 1: Mở Terminal

**Trên Windows:**
- Nhấn `Win + R`, gõ `cmd`, nhấn Enter

**Trên macOS/Linux:**
- Mở ứng dụng Terminal

### Bước 2: Tải Model

Gõ lệnh sau:

```bash
ollama pull qwen:4b
```

**Giải thích:**
- `ollama pull` = tải model
- `qwen:4b` = model Qwen 3.5 4B (phiên bản nhỏ, Q4_K_M)

**Chờ đợi:** Quá trình tải mất 5-10 phút (tùy tốc độ internet). Bạn sẽ thấy:

```
pulling manifest
pulling 8934d3bdaf3c
pulling 8c17c2ebe0f6
...
success
```

Khi thấy chữ `success`, tải xong ✓

---

## Phần 4: Khởi Động Server

### Bước 1: Chạy Model

Gõ lệnh:

```bash
ollama serve
```

Bạn sẽ thấy:

```
time=2024-01-15T10:30:00.000Z level=INFO msg="Listening on 127.0.0.1:11434"
```

**Điều này có nghĩa:** Server đang chạy trên địa chỉ `http://localhost:11434` ✓

**Lưu ý:** Giữ cửa sổ Terminal này mở. Đừng đóng nó, nếu không server sẽ dừng.

### Bước 2: Mở Terminal Mới (Để Gọi Model)

Mở một cửa sổ Terminal khác (không đóng cái cũ):

**Trên Windows:**
- Nhấn `Win + R`, gõ `cmd`, nhấn Enter

**Trên macOS/Linux:**
- Mở Terminal mới

---

## Phần 5: Kiểm Tra Model Hoạt Động

### Cách 1: Dùng Lệnh `ollama run` (Đơn Giản Nhất)

Trong Terminal mới, gõ:

```bash
ollama run qwen:4b
```

Bạn sẽ thấy:

```
>>> 
```

Đây là dấu nhắc để bạn nhập câu hỏi. Thử gõ:

```
Xin chào, bạn tên gì?
```

Nhấn Enter. Model sẽ trả lời:

```
Xin chào! Tôi là Qwen, một trợ lý AI được phát triển bởi Alibaba. Tôi có thể giúp bạn với...
```

Nếu thấy câu trả lời, model hoạt động đúng ✓

Để thoát, gõ `exit` hoặc nhấn `Ctrl + D`.

### Cách 2: Dùng cURL (Để Gọi API)

Nếu muốn gọi model qua API (để dùng trong ứng dụng), gõ:

```bash
curl http://localhost:11434/api/generate -d "{\"model\": \"qwen:4b\", \"prompt\": \"Xin chào\"}"
```

Bạn sẽ thấy kết quả dạng JSON:

```json
{"model":"qwen:4b","created_at":"2024-01-15T10:35:00.000Z","response":"Xin chào! ","done":false}
{"model":"qwen:4b","created_at":"2024-01-15T10:35:01.000Z","response":"Tôi là Qwen...","done":true}
```

Nếu thấy `"done":true`, API hoạt động đúng ✓

---

## Phần 6: Hiểu Rõ Cách Hoạt Động

### Sơ Đồ Kiến Trúc

```
┌─────────────────────────────────────────────────────────┐
│                    Máy Tính Của Bạn                     │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Ollama Server (chạy trên port 11434)           │  │
│  │  - Quản lý model                                │  │
│  │  - Nhận request từ client                       │  │
│  │  │                                              │  │
│  │  └─> Model Qwen 3.5 4B (3GB RAM)               │  │
│  │      - Xử lý câu hỏi                           │  │
│  │      - Sinh ra câu trả lời                     │  │
│  └──────────────────────────────────────────────────┘  │
│           ▲                                             │
│           │ (gửi câu hỏi)                              │
│           │                                             │
│  ┌────────┴────────────────────────────────────────┐   │
│  │  Client (Terminal, Python, JavaScript, etc.)   │   │
│  │  - Gõ câu hỏi                                  │   │
│  │  - Nhận câu trả lời                            │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Luồng Hoạt Động

1. **Bạn gõ câu hỏi** → Terminal gửi đến Ollama Server
2. **Ollama Server nhận** → Chuyển đến Model Qwen
3. **Model xử lý** → Sinh ra câu trả lời
4. **Ollama trả về** → Hiển thị trên Terminal

---

## Phần 7: Các Lệnh Hữu Ích

### Xem Danh Sách Model Đã Tải

```bash
ollama list
```

Kết quả:

```
NAME            ID              SIZE    MODIFIED
qwen:4b         abc123...       3.0GB   2 hours ago
```

### Xóa Model (Nếu Cần)

```bash
ollama rm qwen:4b
```

### Chạy Model Khác

Nếu muốn thử model khác (ví dụ: Llama):

```bash
ollama pull llama2
ollama run llama2
```

### Dừng Server

Trong cửa sổ Terminal chạy `ollama serve`, nhấn `Ctrl + C`.

---

## Phần 8: Gỡ Lỗi Thường Gặp

### Lỗi 1: "ollama: command not found"

**Nguyên nhân:** Ollama chưa được cài đặt hoặc PATH chưa được cập nhật.

**Cách sửa:**
- Cài đặt lại Ollama từ https://ollama.ai
- Khởi động lại máy tính
- Thử lại lệnh `ollama --version`

### Lỗi 2: "Connection refused" Khi Gọi API

**Nguyên nhân:** Server Ollama chưa chạy.

**Cách sửa:**
- Mở Terminal mới
- Gõ `ollama serve`
- Chờ thấy "Listening on 127.0.0.1:11434"
- Thử lại lệnh cURL

### Lỗi 3: "Out of memory" Hoặc Máy Chậm

**Nguyên nhân:** RAM không đủ hoặc model quá lớn.

**Cách sửa:**
- Đóng các ứng dụng khác (Chrome, Spotify, etc.)
- Dùng model nhỏ hơn: `ollama pull qwen:3b` (thay vì 4b)
- Nâng cấp RAM máy tính

### Lỗi 4: Tải Model Bị Dừng Giữa Chừng

**Nguyên nhân:** Mất kết nối internet hoặc timeout.

**Cách sửa:**
- Kiểm tra kết nối internet
- Thử lại: `ollama pull qwen:4b`
- Ollama sẽ tiếp tục từ nơi dừng

---

## Phần 9: Bước Tiếp Theo

Sau khi host thành công model trên Ollama, bạn có thể:

### 1. Tích Hợp Với Python

Tạo file `test_qwen.py`:

```python
import requests
import json

url = "http://localhost:11434/api/generate"
payload = {
    "model": "qwen:4b",
    "prompt": "Hãy tóm tắt CV của một lập trình viên Python",
    "stream": False
}

response = requests.post(url, json=payload)
result = response.json()
print(result['response'])
```

Chạy:

```bash
python test_qwen.py
```

### 2. Tích Hợp Với FastAPI (Để Tạo API Riêng)

Xem file `3_PLAN.md` hoặc `2_PRESENTATION.md` để biết cách tạo API gateway.

### 3. Thử Model Lớn Hơn

Khi máy bạn đủ mạnh, thử:

```bash
ollama pull qwen:7b
ollama run qwen:7b
```

---

## Phần 10: Tóm Tắt

| Bước | Lệnh | Kết Quả |
|------|------|---------|
| 1. Cài Ollama | Tải từ ollama.ai | Ollama sẵn sàng |
| 2. Tải Model | `ollama pull qwen:4b` | Model 3GB được tải |
| 3. Chạy Server | `ollama serve` | Server chạy trên port 11434 |
| 4. Kiểm Tra | `ollama run qwen:4b` | Model trả lời câu hỏi |
| 5. Gọi API | `curl http://localhost:11434/...` | Nhận kết quả JSON |

---

## Phần 11: Tài Liệu Tham Khảo

- **Ollama Docs:** https://github.com/ollama/ollama
- **Qwen Model:** https://huggingface.co/Qwen
- **API Reference:** https://github.com/ollama/ollama/blob/main/docs/api.md

---

## Câu Hỏi Thường Gặp (FAQ)

**Q: Tôi có thể chạy model mà không cần GPU không?**
A: Có, Ollama hỗ trợ CPU. Tốc độ sẽ chậm hơn (5-10 token/giây), nhưng vẫn chạy được.

**Q: Model Qwen 3.5 4B có tốt không?**
A: Có, nó đủ tốt cho bài toán HRM (tóm tắt CV, chấm điểm, etc.). Nếu cần chất lượng cao hơn, dùng 7B hoặc 14B.

**Q: Tôi có thể chạy nhiều model cùng lúc không?**
A: Có, nhưng cần RAM đủ. Ví dụ: 2 model 4B cần ~8GB RAM.

**Q: Dữ liệu của tôi có được gửi lên internet không?**
A: Không, mọi thứ chạy local trên máy bạn. Dữ liệu không rời khỏi máy.

**Q: Tôi có thể dùng model này cho sản phẩm thương mại không?**
A: Có, Qwen được phát hành dưới giấy phép Apache 2.0, cho phép sử dụng thương mại.

---

**Chúc bạn thành công! 🚀**

Nếu gặp vấn đề, hãy kiểm tra lại các bước hoặc tham khảo phần "Gỡ Lỗi Thường Gặp".
