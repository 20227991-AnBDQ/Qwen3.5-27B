import requests

# Test 1: Tóm tắt CV
print("=== Test 1: Tóm tắt CV ===")
response = requests.post(
    "http://localhost:8000/process_cv",
    json={
        "cv_text": "Tôi là Nguyễn Văn A, học Khoa Học Máy Tính tại ĐH Bách Khoa, GPA 3.8. Kỹ năng: Python, TensorFlow, PyTorch. Project: Chatbot AI, Image Recognition. Kinh nghiệm: Internship tại VNG 6 tháng.",
        "task": "summarize_cv"
    }
)
print("Status:", response.status_code)
print("Result:", response.json()['result'])

print("\n=== Test 2: Chấm điểm CV ===")
response = requests.post(
    "http://localhost:8000/process_cv",
    json={
        "cv_text": "Trần Thị B, Robotics, GPA 3.6, C++, ROS, OpenCV. Project: Robot Navigation, SLAM. Kinh nghiệm: Lab tại ĐH Bách Khoa.",
        "task": "score_cv"
    }
)
print("Status:", response.status_code)
print("Result:", response.json()['result'])

print("\n=== Test 3: Match CV với JD ===")
response = requests.post(
    "http://localhost:8000/process_cv",
    json={
        "cv_text": "Phạm Văn C, AI/Robotics, GPA 3.9, Python, C++, PyTorch, ROS. Project: Autonomous Robot, NLP. Startup AI.",
        "task": "match_jd",
        "jd_text": "Tuyển lập trình viên AI/Robotics. Yêu cầu: Python, C++, PyTorch, ROS, có project AI/Robotics."
    }
)
print("Status:", response.status_code)
print("Result:", response.json()['result'])
