import os
import json
import time
import configparser
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# ============================================
# PHẦN 1: TRÍCH URL TỪ FILE .URL
# ============================================

def extract_url_from_url_file(url_file_path):
    """Trích URL từ file .url (Windows shortcut)"""
    try:
        config = configparser.ConfigParser()
        config.read(url_file_path)
        
        if 'InternetShortcut' in config:
            url = config['InternetShortcut'].get('URL')
            return url
    except Exception as e:
        print(f"  ❌ Lỗi trích URL: {str(e)}")
    
    return None

# ============================================
# PHẦN 2: DOWNLOAD CV TỪ TOPCV
# ============================================

def download_cv_from_topcv(url, output_path, timeout=60):
    """
    Tải CV từ TopCV URL bằng Selenium
    
    Quy trình:
    1. Mở URL bằng Chrome
    2. Chờ trang load
    3. Tìm nút download PDF
    4. Lưu file
    """
    
    driver = None
    try:
        # Cấu hình Chrome
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Chạy nền
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Cấu hình download
        prefs = {
            "download.default_directory": os.path.dirname(output_path),
            "download.prompt_for_download": False,
            "profile.default_content_settings.popups": 0
        }
        chrome_options.add_experimental_option("prefs", prefs)
        
        # Khởi tạo driver
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(timeout)
        
        print(f"  🌐 Mở URL...")
        driver.get(url)
        
        # Chờ trang load
        time.sleep(3)
        
        # Cách 1: Tìm nút download PDF
        print(f"  🔍 Tìm nút download...")
        
        try:
            # Tìm các nút có thể là download
            download_buttons = driver.find_elements(By.XPATH, 
                "//button[contains(text(), 'Download')] | "
                "//button[contains(text(), 'download')] | "
                "//a[contains(text(), 'Download')] | "
                "//a[contains(text(), 'PDF')]"
            )
            
            if download_buttons:
                print(f"  ✅ Tìm thấy {len(download_buttons)} nút download")
                download_buttons[0].click()
                time.sleep(2)
            else:
                print(f"  ⚠️  Không tìm thấy nút download")
        except Exception as e:
            print(f"  ⚠️  Lỗi tìm nút: {str(e)[:50]}")
        
        # Cách 2: Lấy PDF từ iframe hoặc embed
        try:
            iframes = driver.find_elements(By.TAG_NAME, "iframe")
            if iframes:
                print(f"  📄 Tìm thấy {len(iframes)} iframe")
                for iframe in iframes:
                    src = iframe.get_attribute("src")
                    if src and "pdf" in src.lower():
                        print(f"  ✅ Tìm thấy PDF iframe: {src[:60]}...")
                        # Tải PDF từ iframe src
                        import requests
                        response = requests.get(src, timeout=30)
                        if response.status_code == 200:
                            with open(output_path, 'wb') as f:
                                f.write(response.content)
                            return True
        except Exception as e:
            print(f"  ⚠️  Lỗi iframe: {str(e)[:50]}")
        
        # Cách 3: Lấy page source và tìm PDF link
        try:
            page_source = driver.page_source
            if "pdf" in page_source.lower():
                print(f"  📄 Tìm thấy PDF trong page source")
                # Tìm link PDF
                import re
                pdf_links = re.findall(r'https?://[^\s"\'<>]+\.pdf', page_source)
                if pdf_links:
                    print(f"  ✅ Tìm thấy {len(pdf_links)} PDF link")
                    import requests
                    response = requests.get(pdf_links[0], timeout=30)
                    if response.status_code == 200:
                        with open(output_path, 'wb') as f:
                            f.write(response.content)
                        return True
        except Exception as e:
            print(f"  ⚠️  Lỗi page source: {str(e)[:50]}")
        
        # Cách 4: Chụp screenshot (fallback)
        print(f"  📸 Chụp screenshot...")
        driver.save_screenshot(output_path.replace('.pdf', '.png'))
        
        return False
        
    except Exception as e:
        print(f"  ❌ Lỗi Selenium: {str(e)[:60]}")
        return False
    finally:
        if driver:
            driver.quit()

# ============================================
# PHẦN 3: PIPELINE CHÍNH
# ============================================

def download_all_urls(input_dir="data/raw_cvs", output_dir="data/raw_cvs"):
    """
    Tải tất cả CV từ file .url
    """
    
    os.makedirs(output_dir, exist_ok=True)
    
    print("="*60)
    print("📥 TẢI CV TỪ TOPCV URLs")
    print("="*60)
    
    # Tìm tất cả file .url
    url_files = list(Path(input_dir).rglob("*.url"))
    
    print(f"\n🔍 Tìm thấy {len(url_files)} file .url\n")
    
    success = 0
    failed = 0
    
    for i, url_file in enumerate(url_files, 1):
        print(f"[{i}/{len(url_files)}] {url_file.name}")
        
        # Trích URL
        url = extract_url_from_url_file(str(url_file))
        
        if not url:
            print(f"  ❌ Không trích được URL")
            failed += 1
            continue
        
        print(f"  🔗 URL: {url[:50]}...")
        
        # Tạo tên file output
        cv_filename = f"topcv_{i}_{url_file.stem}.pdf"
        cv_path = os.path.join(output_dir, cv_filename)
        
        # Tải CV
        print(f"  ⬇️  Tải xuống...")
        
        if download_cv_from_topcv(url, cv_path):
            print(f"  ✅ Tải thành công: {cv_filename}")
            success += 1
        else:
            print(f"  ⚠️  Tải thất bại hoặc không phải PDF")
            failed += 1
        
        # Delay để tránh quá tải
        time.sleep(2)
    
    # Thống kê
    print(f"\n" + "="*60)
    print(f"✅ HOÀN THÀNH")
    print(f"="*60)
    print(f"📊 Thống kê:")
    print(f"  - Tải thành công: {success}")
    print(f"  - Thất bại: {failed}")
    print(f"  - Tổng cộng: {len(url_files)}")

# ============================================
# CHẠY SCRIPT
# ============================================

if __name__ == "__main__":
    print("📦 Kiểm tra thư viện...")
    
    try:
        from selenium import webdriver
        print("✅ Selenium sẵn sàng\n")
    except ImportError:
        print("❌ Cần cài Selenium:")
        print("  pip install selenium")
        print("\n❌ Cần cài ChromeDriver:")
        print("  1. Tải từ: https://chromedriver.chromium.org/")
        print("  2. Hoặc: pip install webdriver-manager")
        exit(1)
    
    # Chạy download
    download_all_urls(
        input_dir="data/raw_cvs/drive-download-20260324T015930Z-3-001",
        output_dir="data/raw_cvs"
    )
    
    print("\n" + "="*60)
    print("🎯 Bước tiếp theo:")
    print("  python process_mixed_cvs.py")
    print("="*60)
