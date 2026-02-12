import pandas as pd
import numpy as np

# ===== TẢI DỮ LIỆU =====
print("=" * 60)
print("LOAD DỮ LIỆU TỪ FILE CSV")
print("=" * 60)

df = pd.read_csv('train_fraud_labels.csv')
print(f"\nKích thước dữ liệu: {df.shape}")
print(f"Số hàng: {df.shape[0]}, Số cột: {df.shape[1]}")
print("\nDữ liệu mẫu (5 hàng đầu):")
print(df.head())

# ===== 1. KIỂM TRA CÁC GIÁ TRỊ THIẾU BẰNG isnull() =====
print("\n" + "=" * 60)
print("1. KIỂM TRA CÁC GIÁ TRỊ THIẾU BẰNG isnull()")
print("=" * 60)

print("\nSố giá trị NULL theo từng cột:")
print(df.isnull().sum())

print("\nTổng số giá trị NULL trong toàn bộ dữ liệu:", df.isnull().sum().sum())

print("\nPercentage (%) các giá trị NULL theo từng cột:")
null_percentage = (df.isnull().sum() / len(df)) * 100
print(null_percentage[null_percentage > 0])

print("\nCác dòng có chứa giá trị NULL:")
print(df[df.isnull().any(axis=1)].head(10))

# ===== 2. KIỂM TRA CÁC GIÁ TRỊ KHÔNG BỊ THIẾU BẰNG notnull() =====
print("\n" + "=" * 60)
print("2. KIỂM TRA CÁC GIÁ TRỊ KHÔNG BỊ THIẾU BẰNG notnull()")
print("=" * 60)

print("\nSố giá trị NOT NULL theo từng cột:")
print(df.notnull().sum())

print("\nPercentage (%) các giá trị NOT NULL theo từng cột:")
notnull_percentage = (df.notnull().sum() / len(df)) * 100
print(notnull_percentage)

rows_complete = df[df.notnull().all(axis=1)]
print(f"\nSố dòng hoàn toàn không có giá trị NULL: {len(rows_complete)}")

# ===== 3. LOẠI BỎ GIÁ TRỊ THIẾU BẰNG dropna() =====
print("\n" + "=" * 60)
print("3. LOẠI BỎ GIÁ TRỊ THIẾU BẰNG dropna()")
print("=" * 60)

print(f"\nKích thước dữ liệu ban đầu: {df.shape}")

df_dropna_all = df.dropna()
print(f"Kích thước sau dropna() (loại bỏ dòng có ANY NULL): {df_dropna_all.shape}")
print(f"Số dòng đã bị loại bỏ: {df.shape[0] - df_dropna_all.shape[0]}")

df_dropna_cols = df.dropna(axis=1)
print(f"\nKích thước sau dropna(axis=1) (loại bỏ cột có NULL): {df_dropna_cols.shape}")
print(f"Các cột bị loại bỏ: {set(df.columns) - set(df_dropna_cols.columns)}")

df_dropna_all_null = df.dropna(how='all')
print(f"\nKích thước sau dropna(how='all') (loại bỏ dòng ALL NULL): {df_dropna_all_null.shape}")

# ===== 4. KIỂM TRA DỮ LIỆU TRÙNG LẶP =====
print("\n" + "=" * 60)
print("4. KIỂM TRA DỮ LIỆU TRÙNG LẶP")
print("=" * 60)

# Tổng số dòng trùng lặp hoàn toàn
num_duplicates = df.duplicated().sum()
print(f"\nSố dòng trùng lặp hoàn toàn: {num_duplicates}")

# Hiển thị các dòng trùng lặp (nếu có)
if num_duplicates > 0:
    print("\nCác dòng trùng lặp (hiển thị 10 dòng đầu):")
    print(df[df.duplicated()].head(10))
else:
    print("\nKhông có dòng trùng lặp hoàn toàn.")

# Kiểm tra trùng lặp theo cột 'index' (nếu đây là ID giao dịch)
if "index" in df.columns:
    dup_index = df["index"].duplicated().sum()
    print(f"\nSố giá trị trùng lặp trong cột 'index': {dup_index}")
    if dup_index > 0:
        print(df[df["index"].duplicated()].head(10))

# Loại bỏ dòng trùng lặp
df_no_duplicates = df.drop_duplicates()
print(f"\nKích thước sau khi loại bỏ dòng trùng lặp: {df_no_duplicates.shape}")
print(f"Số dòng đã bị loại bỏ do trùng lặp: {df.shape[0] - df_no_duplicates.shape[0]}")
