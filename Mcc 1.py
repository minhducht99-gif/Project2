import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the MCC data
df = pd.read_csv('mcc_codes.csv')

# Display basic information
print("=" * 80)
print("THÔNG TIN CƠ BẢN VỀ DỮ LIỆU")
print("=" * 80)
print(f"\nKích thước dữ liệu: {df.shape[0]} dòng, {df.shape[1]} cột\n")

print("Các cột trong dữ liệu:")
print(df.dtypes)

print("\n5 dòng đầu tiên:")
print(df.head())

print("\n5 dòng cuối cùng:")
print(df.tail())

print("\nThông tin chi tiết:")
print(df.info())

print("\nCác thống kê mô tả:")
print(df.describe())

# Tính toán từ khóa phổ biến
import re
from collections import Counter

# Tạo danh sách tất cả các từ
all_words = []
stop_words = {'and', 'or', 'the', 'a', 'an', 'in', 'on', 'at', 'to', 'by'}  # Loại bỏ từ không có ý nghĩa

for category in df['merchant_category']:
    words = re.findall(r'\b[A-Za-z]+\b', category.lower())
    all_words.extend([w for w in words if w not in stop_words])

# Đếm từ khóa
word_counts = Counter(all_words)

# 7.2 - Biểu đồ từ khóa phổ biến
fig, ax = plt.subplots(figsize=(14, 8))

top_20_words = dict(word_counts.most_common(20))
words = list(top_20_words.keys())
counts = list(top_20_words.values())

# Tạo barplot
bars = ax.barh(words, counts, color='teal', alpha=0.7, edgecolor='navy')

# Thêm giá trị trên mỗi cột
for i, bar in enumerate(bars):
    width = bar.get_width()
    ax.text(width + 0.2, bar.get_y() + bar.get_height()/2, 
            str(int(width)), ha='left', va='center', fontweight='bold')

ax.set_xlabel('Tần suất', fontsize=12, fontweight='bold')
ax.set_ylabel('Từ khóa', fontsize=12, fontweight='bold')
ax.set_title('Top 20 Từ Khóa Phổ Biến trong Mô tả Merchant Category', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3, axis='x')
ax.invert_yaxis()

plt.tight_layout()
plt.savefig('mcc_keywords.png', dpi=300, bbox_inches='tight')
plt.show()

print("Biểu đồ từ khóa đã được lưu!")