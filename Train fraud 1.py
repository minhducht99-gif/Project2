import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Đọc dữ liệu
df = pd.read_csv("train_fraud_labels.csv")

# Chuẩn hóa tên cột
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# Chuyển label Yes/No thành 1/0
df["fraud"] = df["label"].map({"Yes": 1, "No": 0})

# ============================
# 1. THỐNG KÊ CƠ BẢN
# ============================

print("Số lượng giao dịch:", len(df))
print(df["fraud"].value_counts())
print((df["fraud"].value_counts(normalize=True) * 100).round(2))

# ============================
# 2. BIỂU ĐỒ PHÂN BỐ LỪA ĐẢO
# ============================

plt.figure(figsize=(6,5))
ax = sns.countplot(data=df, x="fraud", palette="viridis")

plt.title("Phân bố giao dịch lừa đảo (0 = bình thường, 1 = lừa đảo)")
plt.xlabel("Loại giao dịch")
plt.ylabel("Số lượng")

# Gắn nhãn số lượng + %
counts = df["fraud"].value_counts()
percents = (counts / len(df) * 100).round(1)

for i, p in enumerate(ax.patches):
    height = p.get_height()
    ax.annotate(
        f"{height} giao dịch\n{percents.iloc[i]}%",
        (p.get_x() + p.get_width()/2, height),
        ha='center', va='bottom', fontsize=10
    )

plt.show()

