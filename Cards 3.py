import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Cài đặt style cho Seaborn
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 5)
print("Libraries imported successfully!")

# Load the dataset
df = pd.read_csv('cards_data.csv')

# Convert YES/NO columns to binary (1/0)
df['has_chip'] = (df['has_chip'] == 'YES').astype(int)
df['card_on_dark_web'] = (df['card_on_dark_web'] == 'Yes').astype(int)

# Check for missing values
print("Missing Values per Column:")
print("="*80)
missing_values = df.isnull().sum()
print(missing_values[missing_values > 0] if missing_values.sum() > 0 else "No missing values!")

print("\n" + "="*80)
print("Data Types Summary:")
print("="*80)
print(df.dtypes)

# Display statistics about has_chip and card_on_dark_web
print("\n" + "="*80)
print("Unique values in key columns:")
print("="*80)
print(f"has_chip unique values: {df['has_chip'].unique()}")
print(f"card_on_dark_web unique values: {df['card_on_dark_web'].unique()}")

# Analyze chip distribution
chip_counts = df['has_chip'].value_counts()
chip_percentages = df['has_chip'].value_counts(normalize=True) * 100

print("Phân Tích Phân Bố Chip Trên Thẻ")
print("="*80)
print("\nSố lượng thẻ:")
print(chip_counts)

print("\nPhần trăm:")
print(chip_percentages.round(2))

# Create a summary table
chip_summary = pd.DataFrame({
    'Chip Status': ['Có Chip', 'Không Có Chip'],
    'Số Lượng': [chip_counts.get(1, 0), chip_counts.get(0, 0)],
    'Phần Trăm': [f"{chip_percentages.get(1, 0):.2f}%", f"{chip_percentages.get(0, 0):.2f}%"]
})

print("\n" + "="*80)
print("Bảng Tóm Tắt:")
print("="*80)
print(chip_summary)

# Calculate ratio
total = len(df)
with_chip = chip_counts.get(1, 0)
without_chip = chip_counts.get(0, 0)

if with_chip > 0 and without_chip > 0:
    ratio = with_chip / without_chip
    print(f"\nTỷ Lệ (Có Chip : Không Có Chip) = {with_chip} : {without_chip} = {ratio:.2f}:1")
else:
    print(f"\nTổng số thẻ: {total}")
    print(f"Thẻ có chip: {with_chip}")
    print(f"Thẻ không có chip: {without_chip}")

# Analyze dark web presence
darkweb_counts = df['card_on_dark_web'].value_counts()
darkweb_percentages = df['card_on_dark_web'].value_counts(normalize=True) * 100

print("Phân Tích Thẻ Xuất Hiện Trên Dark Web")
print("="*80)
print("\nSố lượng thẻ:")
print(darkweb_counts)

print("\nPhần trăm:")
print(darkweb_percentages.round(2))

# Create a summary table
darkweb_summary = pd.DataFrame({
    'Dark Web Status': ['Xuất Hiện Trên Dark Web', 'Không Xuất Hiện Trên Dark Web'],
    'Số Lượng': [darkweb_counts.get(1, 0), darkweb_counts.get(0, 0)],
    'Phần Trăm': [f"{darkweb_percentages.get(1, 0):.2f}%", f"{darkweb_percentages.get(0, 0):.2f}%"]
})

print("\n" + "="*80)
print("Bảng Tóm Tắt:")
print("="*80)
print(darkweb_summary)

# Calculate ratio
on_darkweb = darkweb_counts.get(1, 0)
not_on_darkweb = darkweb_counts.get(0, 0)

if on_darkweb > 0 and not_on_darkweb > 0:
    ratio = on_darkweb / not_on_darkweb
    print(f"\nTỷ Lệ (Xuất Hiện : Không Xuất Hiện) = {on_darkweb} : {not_on_darkweb} = {ratio:.4f}:1")
else:
    print(f"\nTổng số thẻ: {total}")
    print(f"Thẻ xuất hiện trên dark web: {on_darkweb}")
    print(f"Thẻ không xuất hiện trên dark web: {not_on_darkweb}")

# Create visualizations
fig, axes = plt.subplots(2, 2, figsize=(12, 8))

# 1. Pie chart for Chip Distribution
chip_labels = ['Có Chip', 'Không Có Chip']
chip_values = [chip_counts.get(1, 0), chip_counts.get(0, 0)]
colors_chip = ['#2ecc71', '#e74c3c']

axes[0, 0].pie(chip_values, labels=chip_labels, autopct='%1.1f%%', colors=colors_chip, startangle=90)
axes[0, 0].set_title('Tỷ Lệ Phân Phối Chip Trên Thẻ', fontsize=12, fontweight='bold')

# Bar chart for Chip Distribution
axes[0, 1].bar(chip_labels, chip_values, color=colors_chip, edgecolor='black', linewidth=1.5)
axes[0, 1].set_title('Số Lượng Thẻ Theo Chip', fontsize=12, fontweight='bold')
axes[0, 1].set_ylabel('Số Lượng', fontweight='bold')
for i, v in enumerate(chip_values):
    axes[0, 1].text(i, v + 50, str(v), ha='center', va='bottom', fontweight='bold')

# 2. Pie chart for Dark Web Presence
darkweb_labels = ['Xuất Hiện trên Dark Web', 'Không Xuất Hiện']
darkweb_values = [darkweb_counts.get(1, 0), darkweb_counts.get(0, 0)]
colors_darkweb = ['#e74c3c', '#2ecc71']

axes[1, 0].pie(darkweb_values, labels=darkweb_labels, autopct='%1.1f%%', colors=colors_darkweb, startangle=90)
axes[1, 0].set_title('Tỷ Lệ Thẻ Xuất Hiện Trên Dark Web', fontsize=12, fontweight='bold')

# Bar chart for Dark Web Presence
axes[1, 1].bar(darkweb_labels, darkweb_values, color=colors_darkweb, edgecolor='black', linewidth=1.5)
axes[1, 1].set_title('Số Lượng Thẻ Trên Dark Web', fontsize=12, fontweight='bold')
axes[1, 1].set_ylabel('Số Lượng', fontweight='bold')
for i, v in enumerate(darkweb_values):
    axes[1, 1].text(i, v + 50, str(v), ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig('cards_analysis_visualization.png', dpi=150, bbox_inches='tight')
plt.show()

print("✓ Biểu đồ đã được lưu thành công!")
print("✓ Tên file: cards_analysis_visualization.png")