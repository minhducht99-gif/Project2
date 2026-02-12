import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
df = pd.read_csv('cards_data.csv')

# Find the most popular card type
card_type_counts = df['card_type'].value_counts()
most_popular_card_type = card_type_counts.index[0]
most_popular_count = card_type_counts.iloc[0]

print("=== PHÂN TÍCH LOẠI THẺ PHỔ BIẾN NHẤT ===\n")
print("Số lượng thẻ theo loại:")
print(card_type_counts)
print(f"\nLoại thẻ phổ biến nhất: {most_popular_card_type}")
print(f"Số lượng: {most_popular_count} thẻ")
print(f"Tỷ lệ: {(most_popular_count / len(df) * 100):.2f}%")

# Visualization
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Bar chart
card_type_counts.plot(kind='bar', ax=axes[0], color='steelblue')
axes[0].set_title('Số lượng thẻ theo loại', fontsize=14, fontweight='bold')
axes[0].set_xlabel('Loại thẻ', fontsize=12)
axes[0].set_ylabel('Số lượng', fontsize=12)
axes[0].tick_params(axis='x', rotation=45)
axes[0].grid(axis='y', alpha=0.3)

# Pie chart
colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']
axes[1].pie(card_type_counts.values, labels=card_type_counts.index, autopct='%1.1f%%',
            colors=colors[:len(card_type_counts)], startangle=90)
axes[1].set_title('Tỷ lệ loại thẻ', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig('card_type_analysis.png', dpi=300, bbox_inches='tight')
plt.show()

print("\nBiểu đồ đã được lưu thành 'card_type_analysis.png'")
