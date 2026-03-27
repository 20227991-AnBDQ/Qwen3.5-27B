   Báo cáo Chi tiết: Quy Trình Dựng LLM Engine, Dựng lại bằng Qwen 3.5 27B MoE 3B Opus 4.6 Drill

1. Giới thiệu chung

Dựng một LLM engine chạy được bằng Qwen3.5, ưu tiên nhánh 35B-A3B vì muốn có MoE 3B,Qwen chính thức có Qwen3.5-27B và Qwen3.5-35B-A3B, và có thể thêm lớp distill/phong cách reasoning kiểu Opus 4.6 ở mức MVP

Mục tiêu bài toán là HRM => LLM engine cho HRM để hỗ trợ lọc CV, tuyển dụng, đào tạo, đánh giá.


2. Bài toán này hướng đến đối tượng nào
Dự án này hướng đến bộ phận HR, tuyển dụng, đào tạo nội bộ và quản lý nhân sự trong doanh nghiệp. Mục tiêu là hỗ trợ đọc CV, sàng lọc ứng viên, tóm tắt thông tin và hỗ trợ đánh giá ban đầu, từ đó giảm việc thủ công, tiết kiệm thời gian và tăng hiệu quả quy trình HRM.

3. Các Bước Thực Hiện

3.1. Chốt model đúng, dựng môi trường, kéo model, serve được API đầu tiên

Bước 1 — Chốt mục tiêu và chọn model nền.
WHAT: xác định sản phẩm cần ra sau 3 ngày là một LLM engine MVP: có model chạy local/server, có API gọi được, có prompt system chuẩn, có test đầu ra, và có bản demo. 

HOW: chọn Qwen3.5-35B-A3B  bám đúng yêu cầu “MoE 3B”; chọn Qwen3.5-27B nếu muốn dễ vận hành hơn; còn bản “Opus 4.6 drill/distill” thì coi là lớp nâng cấp sau trên cùng nền Qwen. 

WHY: 3 ngày là đủ để dựng engine và post-train nhẹ, nhưng không thực tế để “train lại từ đầu” một frontier model cỡ này; may là Qwen đã phát hành sẵn weights và hỗ trợ nhiều framework serve.
 
Mục tiêu là dùng LLM engine để hỗ trợ tuyển, đào tạo , đánh giá tự động cho bài toán HRM 

Bước 2 — Dựng hạ tầng chạy model.
WHAT: chuẩn bị máy chủ, môi trường Python/CUDA, tải model, và kiểm tra model có thể generate được câu trả lời đầu tiên. 


HOW: dùng Linux/Ubuntu, Python, CUDA, Git, Hugging Face Hub; chạy thử bằng Transformers hoặc vào thẳng vLLM/SGLang vì Qwen3.5 được chính Qwen ghi nhận là tương thích với các framework này. 

WHY: phải có “base chạy ổn” trước rồi mới làm API, tối ưu, hay fine-tune; nếu hạ tầng chưa đứng vững thì các bước sau đều đổ.


Vấn đề là thứ nhất
: + chọn hạ tầng như thế nào mình cần phải biết phải tìm được một con đầu tiên là host trên máy đã để biết thao tác work như thế nào, tìm một số model có thể host tại máy và phải giải thích được tại sao sử dụng, chi phí này ra sao ?
Ollama / LM Studio = công cụ để host/chạy model
Qwen3.5 4B Q4_K_M = model cụ thể được đem đi host

Để học cách host model local, trước hết nên dùng một công cụ như Ollama hoặc LM Studio để chạy thử một model nhỏ trên máy cá nhân. Model phù hợp để bắt đầu là Qwen3.5 4B Q4_K_M, vì dung lượng nhỏ, dễ chạy và đủ để làm quen với quy trình tải model, mở API local và gửi request.


thứ nhất là môi trường học thao tác và proof-of-concept, tức là host một model đầu tiên để biết quy trình tải model, chạy server, gửi request và đọc log. Ở lớp này, ưu tiên sự ổn định và dễ thao tác.


Bước 2B — Làm rõ vấn đề thứ hai: tương tác với LLM thông qua cái gì, và gateway nào cần có
WHAT: Vấn đề thực chất ở đây là phải xác định được LLM không đứng một mình, mà phải có một lớp trung gian để hệ thống khác gọi vào. Lớp này chính là nơi tiếp nhận request, kiểm soát truy cập, chuẩn hóa input/output và kết nối với model.   


HOW:  Trong thiết kế này, nên coi FastAPI là API gateway chính, còn vLLM là model serving layer. Hệ thống HR, chatbot, hệ thống lưu CV hoặc các service khác sẽ không gọi trực tiếp model, mà gọi vào API. API sau đó mới chuyển request sang model server, nhận kết quả và trả về theo format chuẩn.
Các gateway hoặc lớp tích hợp nên liệt kê rõ gồm:

API Gateway: nhận request từ frontend hoặc hệ thống khác,
Model Gateway: lớp serve model OpenAI-compatible,
Auth Gateway: API key, JWT hoặc phân quyền nội bộ,
Data Gateway: kết nối PostgreSQL, object storage hoặc nơi lưu CV,
Retrieval Gateway: nếu cần tìm CV, JD hoặc tài liệu liên quan bằng semantic search,
Tool Gateway: nếu sau này muốn cho agent gọi tool như chấm CV, lọc hồ sơ, tạo shortlist.


Công nghệ sử dụng:
 FastAPI, Uvicorn, Pydantic, vLLM, PostgreSQL hoặc object storage, Redis, Docker.
WHY:
 Thiết kế theo gateway giúp hệ thống dễ tích hợp, dễ bảo trì và dễ mở rộng. vLLM có server OpenAI-compatible, nên các app khác có thể gọi theo chuẩn quen thuộc /v1/chat/completions thay vì phải viết một giao thức riêng. 
Bước 2C — Làm rõ vấn đề thứ ba: data lấy ở đâu, dùng như thế nào, và tiêu chí chọn ra 5 CV tốt nhất cho AI/Robotics được hình thành ra sao
WHAT: Mục tiêu của bước này là thu thập và chuẩn hóa dữ liệu CV để hệ thống có thể xếp hạng và chọn ra 5 ứng viên thực tập sinh phù hợp nhất cho mảng AI và Robotics. Vấn đề cốt lõi không chỉ là có bao nhiêu CV, mà là phải biến CV thành dữ liệu có cấu trúc, có tiêu chí rõ ràng, và có thể chấm điểm tương đối công bằng.


HOW: 
 Bước 1 — Chuẩn hóa dữ liệu CV, toàn bộ CV đầu vào (PDF, DOCX hoặc ảnh) sẽ được thu thập và trích xuất thành text. Sau đó, hệ thống tiến hành tách các thông tin quan trọng thành dữ liệu có cấu trúc như: tên, trường, chuyên ngành, GPA, kỹ năng, project, kinh nghiệm, giải thưởng và ngoại ngữ. Các thông tin này được lưu lại dưới dạng JSON hoặc CSV, giúp dễ dàng xử lý ở các bước sau. Quá trình này sử dụng Python, thư viện đọc PDF/DOCX, regex và LLM để trích xuất các field phức tạp, đảm bảo dữ liệu đầu vào được chuẩn hóa và nhất quán.


 Bước 2 — Xây bộ tiêu chí chấm điểm, hệ thống xác định một rubric cố định cho vị trí AI/Robotics, bao gồm các nhóm tiêu chí như: học thuật, kỹ năng kỹ thuật, project liên quan, kinh nghiệm, thành tích và mức độ phù hợp với vị trí. Mỗi nhóm tiêu chí được gán trọng số cụ thể (ví dụ: kỹ năng và project chiếm tỷ trọng cao hơn), đồng thời định nghĩa rõ cách chấm điểm (ví dụ: GPA > 3.6 được điểm cao hơn). Bộ tiêu chí này được lưu dưới dạng config (JSON/YAML) và áp dụng đồng loạt bằng Python và Pandas, đảm bảo tất cả CV được đánh giá theo cùng một chuẩn.


 Bước 3 — Gán nhãn tự động theo score, hệ thống sẽ chấm điểm từng CV theo từng tiêu chí, sau đó tính tổng điểm và ánh xạ sang các nhãn như shortlist, borderline, reject hoặc phân tầng theo phần trăm. Việc này được thực hiện hoàn toàn tự động bằng các hàm scoring trong Python, giúp quá trình đánh giá nhanh, nhất quán và không phụ thuộc vào con người.


 Bước 4 — Dùng LLM để hỗ trợ scoring và giải thích, mô hình ngôn ngữ được sử dụng để bổ trợ phần hiểu ngữ nghĩa, không thay thế logic chấm điểm. Cụ thể, LLM sẽ giúp map thông tin từ CV vào đúng tiêu chí (ví dụ: project có liên quan AI/Robotics hay không) và sinh ra phần giải thích ngắn gọn cho kết quả chấm điểm. Điều này giúp output không chỉ có số điểm mà còn có lý do rõ ràng, dễ hiểu cho HR hoặc người ra quyết định. LLM được sử dụng thông qua API hoặc local model, kết hợp với prompt engineering và structured output (JSON) để đảm bảo đầu ra ổn định.

LLM được dùng để hiểu nội dung CV, map vào các tiêu chí và sinh giải thích, nhưng không thay thế logic chấm điểm, giúp kết quả vừa có điểm vừa có lý do rõ ràng.


Dùng LLM qua API (như GPT/Qwen/Mistral) hoặc model local, với prompt + output JSON để map CV vào tiêu chí và sinh giải thích ngắn gọn.


 Bước 5 — Chọn top 5 ứng viên, toàn bộ CV sẽ được sắp xếp theo tổng điểm giảm dần, sau đó lọc theo một số điều kiện tối thiểu (ví dụ: phải có project AI/Robotics, có kỹ năng Python). Hệ thống sẽ chọn ra 5 CV có điểm cao nhất, đồng thời xuất kèm ranking, điểm số và lý do chọn. Việc này được thực hiện bằng Pandas và Python script, và có thể xuất ra Excel hoặc report để review.


WHY: không dùng HR gán nhãn thủ công vì tốn thời gian, khó mở rộng và dễ chủ quan; thay vào đó, kết hợp rule-based, rubric và LLM giúp đánh giá nhanh hơn, nhất quán hơn, dễ giải thích và dễ điều chỉnh khi tiêu chí thay đổi.


Công nghệ sử dụng: OCR/parser CV, Python, Pandas, JSON/CSV, LLM, Google Sheets, Excel.


Tiêu chí chấm điểm: 
1. Thông tin nền tảng:
Họ tên, năm sinh
Trường đại học, chuyên ngành
Năm học hiện tại
GPA
		Mục đích: đánh giá nền tảng học tập và mức độ phù hợp ngành
2. Kỹ năng kỹ thuật
Ngôn ngữ: Python, C++, C, Java
AI/ML: PyTorch, TensorFlow, Scikit-learn
Robotics: ROS/ROS2, OpenCV, SLAM, Gazebo
Kiến thức: ML, DL, CV, NLP, Control
Công cụ: Git, Linux, Docker
		Mục đích: đánh giá năng lực kỹ thuật và khả năng triển khai

3. Project / đồ án
Project AI/Robotics
Capstone / đồ án
Có GitHub/demo
Vai trò cá nhân rõ ràng
Kết quả cụ thể
		Mục đích: kiểm chứng khả năng làm thực tế
4. Kinh nghiệm
Internship
Lab / research
RA/TA
CLB kỹ thuật / startup
Làm việc nhóm
		Mục đích: đánh giá trải nghiệm thực tế và khả năng làm việc
5. Thành tích
Giải thưởng
Hackathon
Olympic / học thuật
Publication
Học bổng / chứng chỉ
		Mục đích: đánh giá năng lực nổi bật và động lực
6. Mức độ phù hợp AI/Robotics
Hướng AI / Robotics
Có giao thoa AI + Robotics
Match với JD
Đúng định hướng vị trí
		Mục đích: đảm bảo đúng domain tuyển dụng
7. Tiềm năng phát triển
Khả năng tự học
Chủ động
Tư duy kỹ thuật
Khả năng đào tạo tiếp
Mức độ nghiêm túc với AI/Robotics
		Mục đích: đánh giá khả năng phát triển dài hạn





Bước 3 — Biến model thành LLM engine có API.
WHAT: tạo một server API để chatbot, agent hoặc ứng dụng khác có thể gửi câu hỏi đến model và nhận câu trả lời.


Dùng vLLM để serve model thành API kiểu OpenAI-compatible; bên ngoài dùng FastAPI để thêm route nghiệp vụ như /chat, /rank_cv, /screen_candidate, /summarize_cv, cùng với auth, log, timeout và validate request/response. Khi cần test nhanh, có thể dùng Postman, cURL hoặc Python script. vLLM hiện có tài liệu chính thức cho HTTP server tương thích với OpenAI API, cho phép các ứng dụng bên ngoài gọi model theo chuẩn quen thuộc


Công nghệ sử dụng: vLLM, FastAPI, Uvicorn, Pydantic, Docker, Postman, cURL.


WHY: dùng chuẩn API phổ biến giúp dễ kết nối với UI, backend, agent hoặc tool khác sau này.

3.2. Thêm lớp engine logic, prompt chuẩn, lịch sử chat, và làm nhánh SFT/LoRA hoặc thử checkpoint distilled

Bước 4 — Thêm phần logic để model dùng được như một sản phẩm thật.
WHAT: thêm các phần như prompt hệ thống, ghi nhớ hội thoại gần đây, giới hạn độ dài câu trả lời, định dạng đầu ra, và mẫu prompt cho từng việc như hỏi đáp, tóm tắt, viết code, suy luận.


HOW: Dùng FastAPI và Python để viết lớp xử lý trung gian. Tạo các prompt template cho từng nghiệp vụ như: đánh giá CV, tóm tắt hồ sơ, so khớp CV với JD, tạo shortlist hoặc giải thích lý do loại. Lưu lịch sử chat ngắn bằng Redis hoặc SQLite nếu cần giữ ngữ cảnh. Ở mức prompt, nên dùng format rõ ràng, tách riêng phần instruction, context, examples và output format để model ít lẫn lộn hơn. Tài liệu prompt engineering của Anthropic cũng khuyến nghị dùng examples và XML tags để tách các phần trong prompt khi cần output có cấu trúc và độ ổn định cao. 


Công nghệ sử dụng: FastAPI, Python, Pydantic, Uvicorn, Redis hoặc SQLite, Jinja2 hoặc prompt templates.


WHY: vì chỉ chạy được model thôi thì chưa đủ; muốn gọi là engine thì nó phải trả lời ổn định, đúng kiểu mong muốn và dùng được trong ứng dụng thật.

Bước 5 —  Tinh chỉnh thêm để model trả lời theo phong cách mong muốn.
WHAT:  Mục tiêu của bước này là không train lại model từ đầu, mà tạo một bộ dữ liệu mẫu chất lượng cao từ bài toán HRM thật, sau đó dùng bộ dữ liệu đó để fine-tune Qwen.


Về bản chất, đây là bài toán teacher-generated dataset + supervised fine-tuning. Trong docs nên viết an toàn là dùng một teacher model mạnh của Claude để sinh dữ liệu mẫu, vì tài liệu public hiện Anthropic đang công bố Sonnet 4.6 và nhắc Opus 4.5; do đó phần “Opus 4.6 drill” nên hiểu là mục tiêu phong cách reasoning, không phải một checkpoint public riêng. .


HOW: dùng các công cụ như SFT/LoRA để dạy thêm cho model bằng dữ liệu mẫu, giúp nó trả lời gần với phong cách reasoning mình muốn, mà không tốn quá nhiều thời gian và tài nguyên máy. Công nghệ dùng Transformers + TRL + PEFT/LoRA + Unsloth để tinh chỉnh nhẹ model Qwen bằng dữ liệu mẫu; nếu máy yếu thì dùng thêm QLoRA/bitsandbytes để giảm VRAM và tăng khả năng train trên GPU nhỏ hơn.
Quy trình sinh dữ liệu mẫu và fine-tune gồm 6 bước:
1. Lấy dữ liệu gốc từ nghiệp vụ thật
 Nguồn dữ liệu đầu vào là:
CV thật


JD thật


tiêu chí tuyển dụng / rubric chấm điểm


một số case đã có quyết định hoặc nhận xét nội bộ


Đây là phần raw data để tạo dataset.
2. Chuẩn hóa mỗi case thành một input thống nhất
 Mỗi mẫu dữ liệu sẽ được đóng gói thành một case gồm:
cv_text


job_description


criteria


task


Ví dụ task có thể là:
tóm tắt CV


chấm mức độ phù hợp với JD


giải thích điểm mạnh / điểm thiếu


xếp hạng shortlist


3. Dùng teacher model để sinh output mẫu
 Cho từng input ở trên, dùng teacher model mạnh để sinh ra một output chuẩn có cấu trúc, ví dụ:
summary


matched_criteria


missing_criteria


score


recommendation


brief_reason


Tức là bộ dữ liệu mẫu được sinh ra từ case HRM thật + output tốt do teacher tạo ra.
4. Lọc và sửa bộ dữ liệu mẫu
 Sau khi teacher sinh output, cần:
loại các mẫu trả lời kém chất lượng


sửa các mẫu chưa đúng tiêu chí tuyển dụng


giữ format nhất quán giữa các case


Bước này giúp dataset sạch hơn trước khi train.
5. Chia bộ dữ liệu thành train / eval / holdout
 Sau khi làm sạch, chia dataset thành:
train set để fine-tune


eval set để so sánh trước–sau


holdout set để kiểm tra model trên case mới chưa thấy trước đó


6. Đưa dataset vào pipeline fine-tune
 Bộ dữ liệu cuối cùng sẽ được lưu dưới dạng JSONL / JSON / Hugging Face Dataset theo kiểu:
prompt–completion, hoặc


conversational/messages format


Sau đó đưa trực tiếp vào train_dataset của TRL SFTTrainer để fine-tune Qwen. Tài liệu TRL xác nhận SFTTrainer hỗ trợ cả prompt-completion dataset lẫn conversational dataset; còn PEFT/LoRA và QLoRA được dùng để giảm chi phí bộ nhớ khi fine-tune model lớn. 



WHY: vì đây là cách nhanh nhất và khả thi nhất để model “học thêm phong cách trả lời” mà vẫn làm xong trong thời gian ngắn.


Công nghệ sử dụng: Claude Opus 4.6 làm teacher, prompt templates, XML tags hoặc JSON schema cho structured output, TRL SFTTrainer, PEFT/LoRA, bitsandbytes/QLoRA, Transformers, Unsloth nếu cần tối ưu thêm.

3.3. Eval, sửa lỗi, tối ưu, docker hóa, và chuẩn bị demo cuối

Bước 6 — Đánh giá chất lượng và độ ổn định.
WHAT:  Kiểm tra model có trả lời đúng định dạng hay không, có reasoning tốt hơn chưa, có bị lặp, ảo giác, timeout hoặc fail khi gặp case khó không.


HOW:  
Chia bộ test thành các nhóm: 
Câu hỏi nghiệp vụ HRM thường gặp,
Bài toán đọc và chấm CV,
Bài toán nhiều bước như so sánh nhiều ứng viên,
Case gây lỗi hoặc dữ liệu khó.


Đo cả hai mặt:
Chất lượng đầu ra như đúng format, đúng lý do, đúng shortlist,
Hiệu năng vận hành như latency, token/s, fail rate, timeout.
 Các chỉ số này có thể lấy từ log của FastAPI/vLLM và phân tích bằng Python, Pandas hoặc notebook.

	
WHY: không có eval thì  không chứng minh được engine tốt hơn model gốc ở điểm nào. 
Công nghệ sử dụng: Python, Pandas, Jupyter, log từ FastAPI, log từ vLLM.
Bước 7 — Đóng gói để demo và bàn giao.
WHAT: chốt một bản chạy được, dễ demo, dễ bàn giao cho team. 


HOW: dùng Docker/Docker Compose, đóng gói các service gồm llm-server, api, ui-test và file .env.example; viết README rất ngắn: cách chạy, cách gọi API, cấu hình model, prompt mẫu, rủi ro và giới hạn.


 WHY: khách hàng không cần thấy đã thử bao nhiêu thứ; họ cần một bản “bật lên là chạy”.
Công nghệ sử dụng: Docker, Docker Compose, README, .env.example.
4. Tại sao cần phải làm dự án này mà ko dùng cái có sẵn

Không chỉ chạy model, mà là dựng LLM engine để dùng thật.
 Model chỉ là lõi xử lý; còn engine là toàn bộ hệ thống xung quanh như deploy, gọi model, quản lý prompt, tích hợp tool, theo dõi log, đo chất lượng và kiểm soát chi phí để đưa vào công việc thực tế.


Dự án này giúp công ty chủ động hơn.
 Thứ hai, dự án này giúp công ty chủ động hơn về dữ liệu, quy trình và tích hợp. Bài toán HRM liên quan trực tiếp đến CV, JD, dữ liệu ứng viên và quy trình nội bộ. Khi tự dựng engine, công ty có thể quyết định dữ liệu nào được dùng, output phải theo format nào, tích hợp với hệ thống nào, và ai có quyền sử dụng.


Không dùng open source nguyên xi vì nó chỉ là điểm khởi đầu.
 Code mẫu giúp chạy thử nhanh, nhưng chưa đủ cho môi trường thật. Khi đưa vào công ty, vẫn cần thêm bảo mật, phân quyền, logging, fallback, giám sát hiệu năng, đánh giá chất lượng và quy trình vận hành rõ ràng.


Dự án này giúp tối ưu chi phí và hiệu năng.
 Các model Qwen MoE có lợi thế về hiệu quả suy luận, nhưng muốn tận dụng tốt thì phải tự thiết kế cách serving và vận hành. Tự dựng engine giúp công ty dùng đúng tài nguyên, đúng hiệu năng, không bị lệ thuộc cấu hình mặc định.







