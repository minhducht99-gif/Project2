import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Đọc dữ liệu
df = pd.read_csv("Users_data.csv")

# Chuẩn hóa tên cột
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# Chuyển credit_score về dạng số
df["credit_score"] = pd.to_numeric(df["credit_score"], errors="coerce")

# ============================
# 1. PHÂN BỐ ĐIỂM TÍN DỤNG
# ============================
plt.figure(figsize=(10,5))
ax = sns.histplot(df["credit_score"], bins=30, kde=True, color="steelblue")
plt.title("Phân bố điểm tín dụng của khách hàng")
plt.xlabel("Điểm tín dụng")
plt.ylabel("Số lượng khách hàng")

# Gắn nhãn số lên histogram
for p in ax.patches:
    height = p.get_height()
    if height > 0:
        ax.annotate(f"{int(height)}",
                    (p.get_x() + p.get_width()/2, height),
                    ha='center', va='bottom', fontsize=8)

plt.show()

# ============================
# 3. BOX PLOT THEO GIỚI TÍNH
# ============================
plt.figure(figsize=(8,5))
ax = sns.boxplot(data=df, x="gender", y="credit_score", palette="Set2")
plt.title("Phân bố điểm tín dụng theo giới tính")
plt.xlabel("Giới tính")
plt.ylabel("Điểm tín dụng")

# Gắn nhãn trung bình lên từng nhóm
means = df.groupby("gender")["credit_score"].mean().round(1)
for i, gender in enumerate(means.index):
    ax.annotate(f"Mean: {means[gender]}",
                (i, means[gender]),
                ha='center', va='bottom', fontsize=10, color="red")

plt.show()

# ============================
# 4. BOX PLOT THEO NHÓM TUỔI
# ============================
df["age_group"] = pd.cut(df["current_age"],
                         bins=[0,25,35,50,65,120],
                         labels=["<25","25-35","35-50","50-65","65+"])


plt.figure(figsize=(10,5))
ax = sns.boxplot(data=df, x="age_group", y="credit_score", palette="coolwarm")
plt.title("Phân bố điểm tín dụng theo nhóm tuổi")
plt.xlabel("Nhóm tuổi")
plt.ylabel("Điểm tín dụng")

# Gắn nhãn trung bình lên từng nhóm tuổi
means_age = df.groupby("age_group")["credit_score"].mean().round(1)
for i, age_group in enumerate(means_age.index):
    ax.annotate(f"{means_age[age_group]}",
                (i, means_age[age_group]),
                ha='center', va='bottom', fontsize=10, color="black")

plt.show()
