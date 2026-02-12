import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv('cards_data.csv')

# Check for missing values in key columns
print("Missing values:")
print(df[['expires', 'acct_open_date']].isnull().sum())

# Convert 'expires' column to datetime format
df['expires'] = pd.to_datetime(df['expires'], errors='coerce')

# Convert 'acct_open_date' column to datetime format
df['acct_open_date'] = pd.to_datetime(df['acct_open_date'], errors='coerce')

# Extract year and month from expires
df['expires_year'] = df['expires'].dt.year
df['expires_month'] = df['expires'].dt.month
df['expires_year_month'] = df['expires'].dt.to_period('M')

# Extract year and month from acct_open_date
df['open_year'] = df['acct_open_date'].dt.year
df['open_month'] = df['acct_open_date'].dt.month
df['open_year_month'] = df['acct_open_date'].dt.to_period('M')

print("\nDữ liệu sau xử lý:")
print(df[['expires', 'expires_year_month', 'acct_open_date', 'open_year_month']].head(10))

# Analyze expiration trends
print("=== XU HƯỚNG TRẺ HẾT HẠN ===\n")

# Grouping by expiration year and month
expiration_by_period = df.groupby('expires_year_month').size()
print("Số lượng thẻ hết hạn theo tháng/năm:")
print(expiration_by_period)

# Grouping by expiration year
expiration_by_year = df.groupby('expires_year').size()
print("\nSố lượng thẻ hết hạn theo năm:")
print(expiration_by_year)

# Grouping by expiration month (to see seasonal patterns)
expiration_by_month = df.groupby('expires_month').size()
print("\nSố lượng thẻ hết hạn theo tháng trong năm:")
print(expiration_by_month)

# Summary statistics
print(f"\nNăm hết hạn sớm nhất: {df['expires_year'].min()}")
print(f"Năm hết hạn muộn nhất: {df['expires_year'].max()}")
print(f"Ngày hết hạn sớm nhất: {df['expires'].min()}")
print(f"Ngày hết hạn muộn nhất: {df['expires'].max()}")


# Analyze account opening trends
print("\n=== XU HƯỚNG THỜI GIAN MỞ THẺ ===\n")

# Grouping by opening year and month
opening_by_period = df.groupby('open_year_month').size()
print("Số lượng thẻ được mở theo tháng/năm:")
print(opening_by_period)

# Grouping by opening year
opening_by_year = df.groupby('open_year').size()
print("\nSố lượng thẻ được mở theo năm:")
print(opening_by_year)

# Grouping by opening month (to see seasonal patterns)
opening_by_month = df.groupby('open_month').size()
print("\nSố lượng thẻ được mở theo tháng trong năm:")
print(opening_by_month)

# Summary statistics
print(f"\nNăm mở thẻ sớm nhất: {df['open_year'].min()}")
print(f"Năm mở thẻ muộn nhất: {df['open_year'].max()}")
print(f"Ngày mở thẻ sớm nhất: {df['acct_open_date'].min()}")
print(f"Ngày mở thẻ muộn nhất: {df['acct_open_date'].max()}")


# Visualization 1: Card Expiration Trends by Year
fig, axes = plt.subplots(2, 2, figsize=(16, 10))

# Plot 1: Expiration by Year
expiration_by_year.plot(kind='bar', ax=axes[0, 0], color='skyblue', edgecolor='black')
axes[0, 0].set_title('Số Lượng Thẻ Hết Hạn Theo Năm', fontsize=12, fontweight='bold')
axes[0, 0].set_xlabel('Năm', fontsize=10)
axes[0, 0].set_ylabel('Số Lượng Thẻ', fontsize=10)
axes[0, 0].tick_params(axis='x', rotation=45)

# Plot 2: Expiration by Month (seasonal pattern)
expiration_by_month.plot(kind='bar', ax=axes[0, 1], color='lightcoral', edgecolor='black')
axes[0, 1].set_title('Xu Hướng Hết Hạn Theo Tháng Trong Năm', fontsize=12, fontweight='bold')
axes[0, 1].set_xlabel('Tháng', fontsize=10)
axes[0, 1].set_ylabel('Số Lượng Thẻ', fontsize=10)
axes[0, 1].set_xticklabels(range(1, 13), rotation=45)

# Plot 3: Account Opening by Year
opening_by_year.plot(kind='bar', ax=axes[1, 0], color='lightgreen', edgecolor='black')
axes[1, 0].set_title('Số Lượng Thẻ Được Mở Theo Năm', fontsize=12, fontweight='bold')
axes[1, 0].set_xlabel('Năm', fontsize=10)
axes[1, 0].set_ylabel('Số Lượng Thẻ', fontsize=10)
axes[1, 0].tick_params(axis='x', rotation=45)

# Plot 4: Account Opening by Month (seasonal pattern)
opening_by_month.plot(kind='bar', ax=axes[1, 1], color='lightyellow', edgecolor='black')
axes[1, 1].set_title('Xu Hướng Mở Thẻ Theo Tháng Trong Năm', fontsize=12, fontweight='bold')
axes[1, 1].set_xlabel('Tháng', fontsize=10)
axes[1, 1].set_ylabel('Số Lượng Thẻ', fontsize=10)
axes[1, 1].set_xticklabels(range(1, 13), rotation=45)

plt.tight_layout()
plt.show()



print("=" * 70)
print("TÓM TẮT VÀ NHỮNG THÔNG TIN CÓ GIÁ TRỊ")
print("=" * 70)

print("\n### 1. XU HƯỚNG TRẺ HẾT HẠN ###\n")

# Find peak expiration period
peak_exp_period = expiration_by_period.idxmax()
peak_exp_count = expiration_by_period.max()
print(f"• Kỳ hạn hết hạn cao nhất: {peak_exp_period} với {peak_exp_count} thẻ")

# Find peak year
peak_exp_year = expiration_by_year.idxmax()
peak_exp_year_count = expiration_by_year.max()
print(f"• Năm hết hạn nhiều nhất: {peak_exp_year} với {peak_exp_year_count} thẻ")

# Peak month
peak_exp_month = expiration_by_month.idxmax()
peak_exp_month_name = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][peak_exp_month - 1]
peak_exp_month_count = expiration_by_month.max()
print(f"• Tháng hết hạn nhiều nhất: Tháng {peak_exp_month} ({peak_exp_month_name}) với {peak_exp_month_count} thẻ")

# Distribution percentage
print(f"\n• Phân bố thẻ hết hạn theo năm:")
for year in sorted(df['expires_year'].dropna().unique()):
    count = expiration_by_year[year]
    pct = (count / expiration_by_year.sum()) * 100
    print(f"  - {int(year)}: {count} thẻ ({pct:.2f}%)")

print("\n### 2. XU HƯỚNG THỜI GIAN MỞ THẺ ###\n")

# Find peak opening period
peak_open_period = opening_by_period.idxmax()
peak_open_count = opening_by_period.max()
print(f"• Kỳ mở thẻ cao nhất: {peak_open_period} với {peak_open_count} thẻ")

# Find peak year
peak_open_year = opening_by_year.idxmax()
peak_open_year_count = opening_by_year.max()
print(f"• Năm mở thẻ nhiều nhất: {peak_open_year} với {peak_open_year_count} thẻ")

# Peak month
peak_open_month = opening_by_month.idxmax()
peak_open_month_name = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][peak_open_month - 1]
peak_open_month_count = opening_by_month.max()
print(f"• Tháng mở thẻ nhiều nhất: Tháng {peak_open_month} ({peak_open_month_name}) với {peak_open_month_count} thẻ")

# Distribution percentage
print(f"\n• Phân bố thẻ mở theo năm:")
for year in sorted(df['open_year'].dropna().unique()):
    count = opening_by_year[year]
    pct = (count / opening_by_year.sum()) * 100
    print(f"  - {int(year)}: {count} thẻ ({pct:.2f}%)")

print("\n### 3. PHÂN TÍCH SO SÁNH ###\n")
print(f"• Tổng số thẻ: {len(df):,}")
print(f"• Số thẻ có dữ liệu hết hạn hợp lệ: {df['expires'].notna().sum():,}")
print(f"• Số thẻ có dữ liệu mở hợp lệ: {df['acct_open_date'].notna().sum():,}")
print(f"• Tuổi trung bình của thẻ (từ ngày mở): {(df['expires'] - df['acct_open_date']).dt.days.mean():.0f} ngày ({(df['expires'] - df['acct_open_date']).dt.days.mean()/365:.2f} năm)")

# Growth trend
print(f"\n• Xu hướng tăng trưởng:")
first_year_open = opening_by_year.iloc[0]
last_year_open = opening_by_year.iloc[-1]
growth = ((last_year_open - first_year_open) / first_year_open * 100) if first_year_open > 0 else 0
print(f"  - Từ {int(opening_by_year.index[0])} đến {int(opening_by_year.index[-1])}: {growth:+.2f}%")

print("\n" + "=" * 70)