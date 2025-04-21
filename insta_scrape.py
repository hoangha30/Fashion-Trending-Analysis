import instaloader
from datetime import datetime
import time
import os

# Khởi tạo Instaloader và load session từ file
L = instaloader.Instaloader()
# L.load_session_from_file("session-jreef__")  # Đảm bảo file session-jreef__ nằm cùng thư mục với file script này
L.login("jreef__", ".ha3072003tanh.")

# Đặt thư mục chính nơi tất cả các ảnh sẽ được lưu
main_folder = "Instagram_Dataset"

# Kiểm tra nếu thư mục chính chưa tồn tại thì tạo mới
if not os.path.exists(main_folder):
    os.makedirs(main_folder)

# Danh sách profile
profiles = [
    "_dancarroll", "vine.fits", "willnordin", "dujiin", "okayhong",
    "leehk.k", "m.nchul", "nus_archive", "thvmxxs", "lhrim_",
    "mint__jun", "imnathgriff", "zaraman", "sonxoo_", "moyen_official",
    "hee_uun", "i.2.n.8", "wi__wi__wi", "actorleeminho", "imhyoseop",
    "eunwo.o_c", "vaidoh.gun", "mr_h.w.a.n", "leneeden_", "jinwoobaee"
]

# Giới hạn thời gian: chỉ lấy post đăng sau ngày 1/10/2024
DATE_LIMIT = datetime(2024, 10, 1)

# Duyệt qua từng profile
for name in profiles:
    try:
        print(f"→ Đang tải từ {name} …")
        profile = instaloader.Profile.from_username(L.context, name)
        count = 0
        # Tạo thư mục riêng cho mỗi profile trong thư mục chính
        profile_folder = os.path.join(main_folder, name)
        if not os.path.exists(profile_folder):
            os.makedirs(profile_folder)
        
        for post in profile.get_posts():
            if post.date_utc > DATE_LIMIT:
                # Tải ảnh vào thư mục profile riêng biệt
                L.download_post(post, target=profile_folder)
                count += 1
        
        print(f"✔️  Hoàn thành: {count} ảnh từ {name}\n")
        time.sleep(15)  # Tạm dừng giữa các profile để tránh bị chặn
    except Exception as e:
        print(f"❌ Lỗi khi xử lý {name}: {e}")
