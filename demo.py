import requests

# Demo 1: Chat đơn giản
print("=== DEMO 1: Chat ===")
response = requests.post(
    "http://localhost:8000/chat",
    json={"prompt": "Hãy giới thiệu về AI/Robotics"}
)
print(response.json()['response'])

# Demo 2: Tóm tắt CV
print("\n=== DEMO 2: Tóm tắt CV ===")
response = requests.post(
    "http://localhost:8000/process_cv",
    json={
        "cv_text": "Tôi là Nguyễn Văn A, học AI tại ĐH Bách Khoa, GPA 3.8. Kỹ năng: Python, TensorFlow, PyTorch. Project: Chatbot AI, Image Recognition. Internship tại VNG 6 tháng.",
        "task": "summarize_cv"
    }
)
print(response.json()['result'])

# Demo 3: Chấm điểm CV
print("\n=== DEMO 3: Chấm điểm CV ===")
response = requests.post(
    "http://localhost:8000/process_cv",
    json={
        "cv_text": "Trần Thị B, Robotics, GPA 3.6, C++, ROS, OpenCV. Project: Robot Navigation, SLAM. Lab tại ĐH Bách Khoa.",
        "task": "score_cv"
    }
)
print(response.json()['result'])
