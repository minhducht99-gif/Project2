import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Đọc dữ liệu
df = pd.read_csv("Users_data.csv")

# Chuyển các cột tài chính về dạng số
cols_to_numeric = ["per_capita_income", "yearly_income", "total_debt", "credit_score"]

for col in cols_to_numeric:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Tính tỷ lệ nợ trên thu nhập (Debt-to-Income Ratio)
df["debt_to_income"] = df["total_debt"] / df["yearly_income"]

# Xác định khách hàng rủi ro tài chính
df["is_risky"] = (df["debt_to_income"] > 0.4) | (df["credit_score"] < 580)

# Đếm số lượng khách hàng rủi ro
num_risky = df["is_risky"].sum()
print("Số lượng khách hàng thuộc nhóm rủi ro tài chính:", num_risky)

# ============================
# 1. Biểu đồ phân bố điểm tín dụng + chỉ số
# ============================
plt.figure(figsize=(8,4))
ax = sns.histplot(df["credit_score"], bins=30, kde=True)
plt.title("Phân bố điểm tín dụng")
plt.xlabel("Credit Score")
plt.ylabel("Số lượng")

# Thêm chỉ số lên histogram
for p in ax.patches:
    height = p.get_height()
    if height > 0:
        ax.annotate(f"{int(height)}",
                    (p.get_x() + p.get_width() / 2, height),
                    ha='center', va='bottom', fontsize=8)

plt.show()

# ============================
# 2. Biểu đồ phân bố Debt-to-Income Ratio + chỉ số
# ============================
plt.figure(figsize=(8,4))
ax = sns.histplot(df["debt_to_income"], bins=30, kde=True)
plt.title("Phân bố Debt-to-Income Ratio")
plt.xlabel("DTI")
plt.ylabel("Số lượng")

# Thêm chỉ số lên histogram
for p in ax.patches:
    height = p.get_height()
    if height > 0:
        ax.annotate(f"{int(height)}",
                    (p.get_x() + p.get_width() / 2, height),
                    ha='center', va='bottom', fontsize=8)

plt.show()

# ============================
# 3. Biểu đồ tỷ lệ khách hàng rủi ro + chỉ số
# ============================
plt.figure(figsize=(5,4))
ax = sns.countplot(x=df["is_risky"])
plt.title("Tỷ lệ khách hàng rủi ro tài chính")
plt.xlabel("Rủi ro (True = Có)")
plt.ylabel("Số lượng")

# Thêm chỉ số lên cột
for p in ax.patches:
    height = p.get_height()
    ax.annotate(f"{height}",
                (p.get_x() + p.get_width() / 2, height),
                ha='center', va='bottom', fontsize=10)

plt.show()
