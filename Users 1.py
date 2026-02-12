import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Tải dữ liệu từ file CSV
df = pd.read_csv('users_data.csv')

print("=" * 80)
print("THÔNG TIN CƠ BẢN VỀ DỮ LIỆU")
print("=" * 80)
print(f"\nKích thước dataset: {df.shape[0]} hàng, {df.shape[1]} cột")
print("\nCác cột trong dataset:")
print(df.columns.tolist())
print("\nKiểu dữ liệu:")
print(df.dtypes)
print("\nDữ liệu đầu tiên:")
print(df.head())



# Hàm chuyển đổi cột tiền tệ sang số
def convert_currency_to_numeric(value):
    if pd.isna(value):
        return np.nan
    if isinstance(value, (int, float)):
        return value
    # Loại bỏ ký tự '$' và dấu phẩy, sau đó chuyển đổi sang float
    value = str(value).replace('$', '').replace(',', '').strip()
    try:
        return float(value)
    except:
        return np.nan

# Áp dụng chuyển đổi cho các cột thu nhập
df['yearly_income_numeric'] = df['yearly_income'].apply(convert_currency_to_numeric)
df['per_capita_income_numeric'] = df['per_capita_income'].apply(convert_currency_to_numeric)
df['total_debt_numeric'] = df['total_debt'].apply(convert_currency_to_numeric)

print("=" * 80)
print("THÔNG TIN VỀ DỮ LIỆU SAU SỬ CHỮA")
print("=" * 80)
print("\nSố lượng giá trị null:")
print(f"yearly_income_numeric: {df['yearly_income_numeric'].isna().sum()}")
print(f"per_capita_income_numeric: {df['per_capita_income_numeric'].isna().sum()}")
print(f"total_debt_numeric: {df['total_debt_numeric'].isna().sum()}")

print("\nDữ liệu sau khi xử lý:")
print(df[['yearly_income_numeric', 'per_capita_income_numeric', 'total_debt_numeric']].head(10))


# Biểu đồ 1: Histogram cho Yearly Income và Per Capita Income
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Histogram - Yearly Income
axes[0].hist(df['yearly_income_numeric'], bins=50, edgecolor='black', color='steelblue', alpha=0.7)
axes[0].axvline(df['yearly_income_numeric'].mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: ${df["yearly_income_numeric"].mean():,.0f}')
axes[0].axvline(df['yearly_income_numeric'].median(), color='green', linestyle='--', linewidth=2, label=f'Median: ${df["yearly_income_numeric"].median():,.0f}')
axes[0].set_title('Phân Bố Thu Nhập Hằng Năm (Histogram)', fontsize=12, fontweight='bold')
axes[0].set_xlabel('Thu Nhập ($)')
axes[0].set_ylabel('Số Lượng Khách Hàng')
axes[0].legend()
axes[0].grid(alpha=0.3)

# Histogram - Per Capita Income
axes[1].hist(df['per_capita_income_numeric'], bins=50, edgecolor='black', color='coral', alpha=0.7)
axes[1].axvline(df['per_capita_income_numeric'].mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: ${df["per_capita_income_numeric"].mean():,.0f}')
axes[1].axvline(df['per_capita_income_numeric'].median(), color='green', linestyle='--', linewidth=2, label=f'Median: ${df["per_capita_income_numeric"].median():,.0f}')
axes[1].set_title('Phân Bố Thu Nhập Bình Quân Hộ (Histogram)', fontsize=12, fontweight='bold')
axes[1].set_xlabel('Thu Nhập Bình Quân ($)')
axes[1].set_ylabel('Số Lượng Khách Hàng')
axes[1].legend()
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.show()

print("Biểu đồ 1 được hiển thị")

# Biểu đồ 2: Box plots So sánh
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Box plot for Yearly Income
sns.boxplot(y=df['yearly_income_numeric'], ax=axes[0], color='lightblue')
axes[0].set_title('Box Plot: Thu Nhập Hằng Năm', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Thu Nhập ($)')
axes[0].grid(alpha=0.3, axis='y')

# Box plot for Per Capita Income
sns.boxplot(y=df['per_capita_income_numeric'], ax=axes[1], color='lightcoral')
axes[1].set_title('Box Plot: Thu Nhập Bình Quân Hộ', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Thu Nhập Bình Quân ($)')
axes[1].grid(alpha=0.3, axis='y')

plt.tight_layout()
plt.show()

print("Biểu đồ 2 được hiển thị")

# Biểu đồ 3: Violin plots
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Violin plot for Yearly Income
sns.violinplot(y=df['yearly_income_numeric'], ax=axes[0], color='skyblue')
axes[0].set_title('Violin Plot: Thu Nhập Hằng Năm', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Thu Nhập ($)')
axes[0].grid(alpha=0.3, axis='y')

# Violin plot for Per Capita Income
sns.violinplot(y=df['per_capita_income_numeric'], ax=axes[1], color='lightgreen')
axes[1].set_title('Violin Plot: Thu Nhập Bình Quân Hộ', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Thu Nhập Bình Quân ($)')
axes[1].grid(alpha=0.3, axis='y')

plt.tight_layout()
plt.show()

print("Biểu đồ 3 được hiển thị")


# Phân loại khách hàng theo khoảng thu nhập
income_brackets = [0, 30000, 60000, 100000, 150000, 250000, 500000]
income_labels = ['<30K', '30K-60K', '60K-100K', '100K-150K', '150K-250K', '>250K']

df['income_bracket'] = pd.cut(df['yearly_income_numeric'], bins=income_brackets, labels=income_labels, right=False)

print("=" * 80)
print("PHÂN LOẠI KHÁCH HÀNG THEO KHOẢNG THU NHẬP")
print("=" * 80)

income_dist = df['income_bracket'].value_counts().sort_index()
income_dist_pct = (df['income_bracket'].value_counts().sort_index() / len(df) * 100)

for bracket in income_labels:
    count = income_dist.get(bracket, 0)
    pct = income_dist_pct.get(bracket, 0)
    print(f"{bracket:15} : {count:5} khách hàng ({pct:5.2f}%)")

# Phát hiện outliers sử dụng IQR method
print("\n" + "=" * 80)
print("PHÁT HIỆN OUTLIERS (SỬ DỤNG IQR METHOD)")
print("=" * 80)

Q1 = df['yearly_income_numeric'].quantile(0.25)
Q3 = df['yearly_income_numeric'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers = df[(df['yearly_income_numeric'] < lower_bound) | (df['yearly_income_numeric'] > upper_bound)]
print(f"\nCận dưới: ${lower_bound:,.2f}")
print(f"Cận trên: ${upper_bound:,.2f}")
print(f"Số lượng outliers: {len(outliers)} ({len(outliers)/len(df)*100:.2f}%)")
print(f"\nOutlier - Thu nhập thấp: {(df['yearly_income_numeric'] < lower_bound).sum()} khách hàng")
print(f"Outlier - Thu nhập cao: {(df['yearly_income_numeric'] > upper_bound).sum()} khách hàng")

# Tính toán wealth categories
print("\n" + "=" * 80)
print("PHÂN LOẠI TÍNH CÁCH TÀI CHÍ DỰA TRÊN THU NHẬP")
print("=" * 80)

def categorize_wealth(income):
    if pd.isna(income):
        return 'Không xác định'
    elif income < 35000:
        return 'Thấp'
    elif income < 75000:
        return 'Trung bình'
    elif income < 150000:
        return 'Cao'
    else:
        return 'Rất cao'

df['wealth_category'] = df['yearly_income_numeric'].apply(categorize_wealth)
wealth_dist = df['wealth_category'].value_counts()

for category in ['Thấp', 'Trung bình', 'Cao', 'Rất cao', 'Không xác định']:
    count = wealth_dist.get(category, 0)
    pct = count / len(df) * 100
    if count > 0:
        print(f"{category:15} : {count:5} khách hàng ({pct:5.2f}%)")


# Phân tích thu nhập theo giới tính
print("=" * 80)
print("PHÂN TÍCH THU NHẬP THEO GIỚI TÍNH")
print("=" * 80)

gender_income = df.groupby('gender')['yearly_income_numeric'].agg(['count', 'mean', 'median', 'std', 'min', 'max'])
print(gender_income)

# Phân tích thu nhập theo nhóm tuổi
age_bins = [0, 25, 35, 45, 55, 65, 100]
age_labels = ['18-25', '25-35', '35-45', '45-55', '55-65', '65+']
df['age_group'] = pd.cut(df['current_age'], bins=age_bins, labels=age_labels, right=False)

print("\n" + "=" * 80)
print("PHÂN TÍCH THU NHẬP THEO NHÓM TUỔI")
print("=" * 80)

age_income = df.groupby('age_group')['yearly_income_numeric'].agg(['count', 'mean', 'median', 'std', 'min', 'max'])
print(age_income)

# Biểu đồ: So sánh thu nhập theo giới tính
print("\nTạo biểu đồ so sánh...")
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Box plot by Gender
sns.boxplot(data=df, x='gender', y='yearly_income_numeric', ax=axes[0, 0], palette='Set2')
axes[0, 0].set_title('Phân Bố Thu Nhập Theo Giới Tính (Box Plot)', fontsize=12, fontweight='bold')
axes[0, 0].set_ylabel('Thu Nhập ($)')
axes[0, 0].grid(alpha=0.3, axis='y')

# Violin plot by Gender
sns.violinplot(data=df, x='gender', y='yearly_income_numeric', ax=axes[0, 1], palette='Set2')
axes[0, 1].set_title('Phân Bố Thu Nhập Theo Giới Tính (Violin Plot)', fontsize=12, fontweight='bold')
axes[0, 1].set_ylabel('Thu Nhập ($)')
axes[0, 1].grid(alpha=0.3, axis='y')

# Box plot by Age Group
sns.boxplot(data=df, x='age_group', y='yearly_income_numeric', ax=axes[1, 0], palette='husl')
axes[1, 0].set_title('Phân Bố Thu Nhập Theo Nhóm Tuổi (Box Plot)', fontsize=12, fontweight='bold')
axes[1, 0].set_xlabel('Nhóm Tuổi')
axes[1, 0].set_ylabel('Thu Nhập ($)')
axes[1, 0].grid(alpha=0.3, axis='y')

# Violin plot by Age Group
sns.violinplot(data=df, x='age_group', y='yearly_income_numeric', ax=axes[1, 1], palette='husl')
axes[1, 1].set_title('Phân Bố Thu Nhập Theo Nhóm Tuổi (Violin Plot)', fontsize=12, fontweight='bold')
axes[1, 1].set_xlabel('Nhóm Tuổi')
axes[1, 1].set_ylabel('Thu Nhập ($)')
axes[1, 1].grid(alpha=0.3, axis='y')

plt.tight_layout()
plt.show()

print("Biểu đồ demographic được hiển thị")



print("=" * 80)
print("TÓM TẮT PHÂN TÍCH PHÂN BỐ THU NHẬP CỦA KHÁCH HÀNG")
print("=" * 80)

print(f"""
📊 NHỮNG PHÁT HIỆN CHÍNH:

1. THỐNG KÊ THU NHẬP HẰNG NĂM:
   - Trung bình: ${df['yearly_income_numeric'].mean():,.2f}
   - Trung vị: ${df['yearly_income_numeric'].median():,.2f}
   - Độ lệch chuẩn: ${df['yearly_income_numeric'].std():,.2f}
   - Khoảng từ: ${df['yearly_income_numeric'].min():,.2f} đến ${df['yearly_income_numeric'].max():,.2f}

2. HÌNH DẠNG PHÂN BỐ:
   - Skewness: {df['yearly_income_numeric'].skew():.3f}
   - Kurtosis: {df['yearly_income_numeric'].kurtosis():.3f}
   - Nhận xét: {'Phân bố lệch sang phải (right-skewed)' if df['yearly_income_numeric'].skew() > 0.5 else 'Phân bố tương đối cân bằng'}

3. PHÂN LOẠI KHÁCH HÀNG:
   - Số khách hàng thu nhập thấp (<30K): {(df['income_bracket'] == '<30K').sum()} ({(df['income_bracket'] == '<30K').sum()/len(df)*100:.1f}%)
   - Số khách hàng thu nhập trung bình (30K-100K): {((df['income_bracket'] == '30K-60K') | (df['income_bracket'] == '60K-100K')).sum()} ({((df['income_bracket'] == '30K-60K') | (df['income_bracket'] == '60K-100K')).sum()/len(df)*100:.1f}%)
   - Số khách hàng thu nhập cao (100K-250K): {((df['income_bracket'] == '100K-150K') | (df['income_bracket'] == '150K-250K')).sum()} ({((df['income_bracket'] == '100K-150K') | (df['income_bracket'] == '150K-250K')).sum()/len(df)*100:.1f}%)
   - Số khách hàng thu nhập rất cao (>250K): {(df['income_bracket'] == '>250K').sum()} ({(df['income_bracket'] == '>250K').sum()/len(df)*100:.1f}%)

4. PHÁT HIỆN NGOẠI LỆ:
   - Số lượng outliers: {len(outliers)} ({len(outliers)/len(df)*100:.2f}%)
   - Phần trăm outliers cao: {(df['yearly_income_numeric'] > upper_bound).sum()} khách hàng
   - Phần trăm outliers thấp: {(df['yearly_income_numeric'] < lower_bound).sum()} khách hàng

5. SO SÁNH GIỚI TÍNH:
""")

for gender in df['gender'].unique():
    gender_data = df[df['gender'] == gender]['yearly_income_numeric']
    print(f"   - {gender}: Trung bình = ${gender_data.mean():,.2f}, Trung vị = ${gender_data.median():,.2f}")

print(f"""
6. SO SÁNH THEO NHÓM TUỔI:
""")

for age_group in age_labels:
    age_data = df[df['age_group'] == age_group]['yearly_income_numeric']
    if len(age_data) > 0:
        print(f"   - {age_group}: Số lượng = {len(age_data)}, Trung bình = ${age_data.mean():,.2f}")

print(f"""
7. KỲ VỌNG:
   ✓ Phân bố thu nhập chứa mô hình tự nhiên với một số khách hàng có thu nhập rất cao
   ✓ Đa số khách hàng tập trung vào khoảng thu nhập từ $35K đến $75K
   ✓ Có sự khác biệt rõ rệt giữa các nhóm tuổi và giới tính về thu nhập
""")

print("=" * 80)