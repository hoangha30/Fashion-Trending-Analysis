import glob
import pandas as pd

# Thay bằng thư mục chứa CSV của bạn
csv_folder = "/Users/hanguyen/Octoparse"

# Đọc tất cả file CSV
files = glob.glob(f"{csv_folder}/*.csv")

# Nạp và ghép
df = pd.concat((pd.read_csv(f) for f in files), ignore_index=True)

# Loại duplicate
df = df.drop_duplicates()

# Drop các dòng missing ở cột đầu tiên
df = df.dropna(subset=["product_img", "highlights"])

nan_count = df['highlights'].isna().sum()
print(f"Số dòng highlights = NaN: {nan_count}")

# Xuất ra file
df.to_csv("merged.csv", index=False)
print(f"Đã gộp {len(files)} file, còn {len(df)} dòng (chưa trùng).")
