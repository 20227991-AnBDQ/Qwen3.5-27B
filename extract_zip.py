import zipfile
import os
from pathlib import Path

def extract_zip(zip_file, extract_to):
    """Giải nén file .zip"""
    
    print(f"📦 Giải nén: {zip_file}")
    print(f"📁 Đến: {extract_to}")
    print("-" * 60)
    
    try:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            # Lấy danh sách file
            file_list = zip_ref.namelist()
            print(f"✅ Tìm thấy {len(file_list)} file\n")
            
            # Giải nén
            zip_ref.extractall(extract_to)
            
            print(f"✅ Giải nén thành công!")
            print(f"\n📊 Thống kê:")
            
            # Đếm loại file
            pdf_count = sum(1 for f in file_list if f.lower().endswith('.pdf'))
            docx_count = sum(1 for f in file_list if f.lower().endswith('.docx'))
            url_count = sum(1 for f in file_list if f.lower().endswith('.url'))
            
            print(f"  - PDF: {pdf_count}")
            print(f"  - DOCX: {docx_count}")
            print(f"  - .URL: {url_count}")
            print(f"  - Khác: {len(file_list) - pdf_count - docx_count - url_count}")
            
    except Exception as e:
        print(f"❌ Lỗi: {str(e)}")

if __name__ == "__main__":
    # Đường dẫn file zip
    zip_file = "data/raw_cvs/drive-download-20260324T015930Z-3-001.zip"
    extract_to = "data/raw_cvs/"
    
    # Kiểm tra file tồn tại
    if not os.path.exists(zip_file):
        print(f"❌ Không tìm thấy file: {zip_file}")
        print(f"\n💡 Kiểm tra đường dẫn:")
        print(f"  - File phải ở: {os.path.abspath(zip_file)}")
        exit(1)
    
    # Giải nén
    extract_zip(zip_file, extract_to)
    
    print("\n" + "="*60)
    print("🎯 Bước tiếp theo:")
    print("  python process_mixed_cvs.py")
    print("="*60)
