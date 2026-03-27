import json
import csv
import re
from pathlib import Path

def extract_info_from_cv(cv_text):
    """Trích thông tin CV bằng Regex (không cần API)"""
    
    info = {
        'name': '',
        'major': '',
        'gpa': '',
        'skills': '',
        'projects': '',
        'experience': ''
    }
    
    # 1. Trích tên (dòng đầu tiên hoặc sau "Name:")
    lines = cv_text.split('\n')
    for line in lines[:5]:
        line = line.strip()
        if line and len(line) < 50 and not any(c.isdigit() for c in line[:10]):
            info['name'] = line
            break
    
    # 2. Trích chuyên ngành (tìm từ khóa)
    major_keywords = ['AI', 'Machine Learning', 'Robotics', 'Data Science', 'Computer Science', 
                      'Software Engineering', 'Information Technology', 'Artificial Intelligence']
    for keyword in major_keywords:
        if keyword.lower() in cv_text.lower():
            info['major'] = keyword
            break
    
    # 3. Trích GPA (pattern: 3.8, 3.6, etc.)
    gpa_match = re.search(r'GPA[:\s]+(\d\.\d+)', cv_text, re.IGNORECASE)
    if gpa_match:
        info['gpa'] = gpa_match.group(1)
    else:
        gpa_match = re.search(r'(\d\.\d{1,2})\s*(?:/|out of)\s*4', cv_text)
        if gpa_match:
            info['gpa'] = gpa_match.group(1)
    
    # 4. Trích kỹ năng (tìm từ khóa công nghệ)
    skills_keywords = ['Python', 'C++', 'Java', 'JavaScript', 'TensorFlow', 'PyTorch', 
                       'Scikit-learn', 'ROS', 'ROS2', 'OpenCV', 'SLAM', 'Gazebo', 
                       'Git', 'Linux', 'Docker', 'SQL', 'React', 'Node.js']
    found_skills = []
    for skill in skills_keywords:
        if skill.lower() in cv_text.lower():
            found_skills.append(skill)
    info['skills'] = ', '.join(found_skills) if found_skills else 'N/A'
    
    # 5. Trích project (tìm từ khóa)
    project_keywords = ['project', 'capstone', 'thesis', 'github', 'demo', 'portfolio']
    projects = []
    for line in lines:
        line_lower = line.lower()
        if any(keyword in line_lower for keyword in project_keywords):
            projects.append(line.strip())
    info['projects'] = '; '.join(projects[:3]) if projects else 'N/A'
    
    # 6. Trích kinh nghiệm (tìm từ khóa)
    exp_keywords = ['internship', 'thực tập', 'lab', 'research', 'ra', 'ta', 'startup', 'company']
    experiences = []
    for line in lines:
        line_lower = line.lower()
        if any(keyword in line_lower for keyword in exp_keywords):
            experiences.append(line.strip())
    info['experience'] = '; '.join(experiences[:3]) if experiences else 'N/A'
    
    return info

def normalize_cvs():
    """Chuẩn hóa 500 CV bằng Regex"""
    
    input_file = "data/cvs_extracted.jsonl"
    output_file = "data/cvs_normalized.csv"
    
    print("="*60)
    print("🔄 CHUẨN HÓA DỮ LIỆU CV (REGEX - NHANH)")
    print("="*60)
    
    print(f"\n📖 Đọc file: {input_file}")
    
    results = []
    count = 0
    failed = 0
    
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        total = len(lines)
    
    print(f"Tổng cộng: {total} CV\n")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f, 1):
            try:
                cv = json.loads(line)
                filename = cv['filename']
                text = cv['text']
                
                print(f"[{i}/{total}] {filename[:40]}")
                
                # Trích thông tin
                info = extract_info_from_cv(text)
                info['filename'] = filename
                results.append(info)
                count += 1
                print(f"  ✅ {info.get('name', 'N/A')}")
                
            except Exception as e:
                print(f"  ❌ Lỗi: {str(e)[:50]}")
                failed += 1
    
    # Lưu CSV
    if results:
        print(f"\n💾 Lưu vào: {output_file}")
        
        keys = ['filename', 'name', 'major', 'gpa', 'skills', 'projects', 'experience']
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=keys, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(results)
        
        print(f"\n✅ HOÀN THÀNH")
        print(f"📊 Thống kê:")
        print(f"  - Chuẩn hóa thành công: {count}")
        print(f"  - Thất bại: {failed}")
        print(f"  - Tổng cộng: {len(results)} CV")
    else:
        print(f"\n❌ Không có dữ liệu để lưu")

if __name__ == "__main__":
    normalize_cvs()
