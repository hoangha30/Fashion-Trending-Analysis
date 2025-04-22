import json
import os
import requests

# Đường dẫn đến file JSON đã crawl
JSON_PATH = 'dataset_instagram-post-scraper_2025-04-15_12-12-00-598.json'
# Thư mục lưu ảnh
OUTPUT_DIR = 'insta_img'

# Tạo thư mục gốc nếu chưa có
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Đọc dữ liệu
with open(JSON_PATH, 'r', encoding='utf-8') as f:
    posts = json.load(f)

for post in posts:
    post_id = post.get('id')
    post_type = post.get('type', '').lower()
    # Tạo thư mục riêng cho mỗi post (tùy chọn)
    post_dir = os.path.join(OUTPUT_DIR, post_id)
    os.makedirs(post_dir, exist_ok=True)
    
    # Chọn list URL tuỳ vào type
    if post_type == 'sidecar':
        urls = post.get('images', [])
    elif post_type in ('image', 'video'):
        # displayUrl chứa ảnh (video thì chỉ lấy thumbnail)
        url = post.get('displayUrl')
        urls = [url] if url else []
    else:
        urls = []
    
    # Tải từng URL
    for idx, url in enumerate(urls, start=1):
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
        except Exception as e:
            print(f"[!] Lỗi tải {url}: {e}")
            continue
        
        # Lấy phần đuôi tên file (jpg/png)
        ext = url.split('?')[0].split('.')[-1]
        filename = f"{idx}.{ext}"
        save_path = os.path.join(post_dir, filename)
        
        with open(save_path, 'wb') as imgf:
            imgf.write(resp.content)
        
        print(f"[+] Đã lưu {save_path}")
