import json
import csv
import requests
import time

def extract_cv_info(cv_text):
    """Dùng model để trích xuất thông tin CV"""
    
    prompt = f"""Trích xuất thông tin từ CV sau thành JSON (chỉ trả lời JSON, không giải thích):
{{
    "name": "Tên người",
    "major": "Chuyên ngành",
    "gpa": "GPA (nếu có, nếu không có ghi 0)",
    "skills": "Kỹ năng (cách nhau bằng dấu phẩy)",
    "projects": "Project (cách nhau bằng dấu phẩy)",
    "experience": "Kinh nghiệm"
}}

CV:
{cv_text[:800]}

JSON:"""
    
    try:
        response = requests.post(
            "http://localhost:8000/chat",
            json={"prompt": prompt},
            timeout=60  # Tăng từ 30 lên 60 giây
        )
        
        result = response.json()['response']
        
        # Trích JSON từ response
        import re
        json_match = re.search(r'\{.*\}', result, re.DOTALL)
        if json_match:
            json_str = json_match.group()
            return json.loads(json_str)
    except Exception as e:
        print(f"    ⚠️  Lỗi: {str(e)}")
    
    return None

def normalize_cvs():
    """Chuẩn hóa 500 CV"""
    
    input_file = "data/cvs_extracted.jsonl"
    output_file = "data/cvs_normalized.csv"
    
    print("="*60)
    print("🔄 CHUẨN HÓA DỮ LIỆU CV")
    print("="*60)
    
    results = []
    count = 0
    failed = 0
    
    print(f"\n📖 Đọc file: {input_file}")
    
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
                info = extract_cv_info(text)
                
                if info:
                    info['filename'] = filename
                    results.append(info)
                    count += 1
                    print(f"  ✅ {info.get('name', 'N/A')}")
                else:
                    print(f"  ❌ Không trích được")
                    failed += 1
                
                # Delay để tránh quá tải
                time.sleep(2)
                
            except Exception as e:
                print(f"  ❌ Lỗi: {str(e)}")
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
