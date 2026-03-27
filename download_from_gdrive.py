import os
import io
from google.colab import auth
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import requests

# Cách 1: Nếu bạn có Google Colab (dễ nhất)
# Chỉ cần chạy trên Colab, nó tự authenticate

# Cách 2: Nếu chạy local, dùng link chia sẻ trực tiếp

def download_from_gdrive_link(folder_link, output_dir="data/raw_cvs"):
    """
    Tải CV từ Google Drive folder link
    
    folder_link: https://drive.google.com/drive/folders/FOLDER_ID
    """
    
    # Tạo thư mục
    os.makedirs(output_dir, exist_ok=True)
    
    # Trích FOLDER_ID từ link
    folder_id = folder_link.split('/folders/')[-1].split('?')[0]
    
    print(f"📥 Tải CV từ Google Drive...")
    print(f"Folder ID: {folder_id}")
    
    # Dùng API Google Drive
    try:
        from google.auth.transport.requests import Request
        from google.oauth2.service_account import Credentials
    except:
        print("⚠️ Cần authenticate. Dùng cách khác...")
        return
    
    # Nếu không có service account, dùng cách thủ công
    print("\n⚠️ Cách 1 (API) cần authentication phức tạp")
    print("Dùng Cách 2 (thủ công) dễ hơn:")
    print("\n" + "="*50)
    print("CÁCH 2: Tải Thủ Công (Đơn Giản)")
    print("="*50)

def download_manually():
    """
    Hướng dẫn tải thủ công từ Google Drive
    """
    print("""
1. Mở Google Drive folder
2. Chọn tất cả file (Ctrl+A)
3. Chuột phải → "Tải xuống"
4. Chờ tải file .zip
5. Giải nén vào thư mục: data/raw_cvs/

Hoặc dùng rclone (tự động):
    """)

def setup_rclone():
    """
    Hướng dẫn cài rclone để tải tự động
    """
    print("""
CÁCH 3: Dùng rclone (Tự Động)

Bước 1: Cài rclone
  Windows: https://rclone.org/downloads/
  hoặc: choco install rclone
  
Bước 2: Cấu hình Google Drive
  rclone config
  - Chọn "n" (new remote)
  - Tên: gdrive
  - Type: 15 (Google Drive)
  - Làm theo hướng dẫn
  
Bước 3: Tải CV
  rclone copy gdrive:FOLDER_ID data/raw_cvs/ -P
  
Bước 4: Kiểm tra
  ls data/raw_cvs/
    """)

if __name__ == "__main__":
    print("="*50)
    print("TẢI CV TỪ GOOGLE DRIVE")
    print("="*50)
    
    print("\n3 CÁCH TẢI:")
    print("1. Tải thủ công (dễ, nhanh)")
    print("2. Dùng rclone (tự động, nhanh)")
    print("3. Dùng API (phức tạp)")
    
    print("\n" + "="*50)
    print("KHUYẾN NGHỊ: CÁCH 2 (rclone)")
    print("="*50)
    
    setup_rclone()
