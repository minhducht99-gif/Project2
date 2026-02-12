import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Đọc dữ liệu
df = pd.read_csv("Users_data.csv")

# Chuyển các cột số về dạng numeric
cols_to_numeric = ["current_age", "retirement_age", "birth_year", "birth_month",
                   "per_capita_income", "yearly_income", "total_debt",
                   "credit_score", "num_credit_cards"]

for col in cols_to_numeric:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# ============================
# 1. Phân tích theo giới tính
# ============================
gender_group = df.groupby("gender")["num_credit_cards"].mean().sort_values(ascending=False)
print("\nSố thẻ tín dụng trung bình theo giới tính:")
print(gender_group)

plt.figure(figsize=(6,4))
ax = sns.barplot(x=gender_group.index, y=gender_group.values)
plt.title("Số thẻ tín dụng trung bình theo giới tính")
plt.xlabel("Giới tính")
plt.ylabel("Số thẻ trung bình")

# Thêm chỉ số lên cột
for p in ax.patches:
    height = p.get_height()
    ax.annotate(f"{height:.2f}",
                (p.get_x() + p.get_width()/2, height),
                ha='center', va='bottom')

plt.show()

# ============================
# 2. Phân tích theo nhóm tuổi
# ============================
df["age_group"] = pd.cut(df["current_age"],
                         bins=[0, 25, 35, 50, 65, 100],
                         labels=["<25", "25-35", "35-50", "50-65", "65+"])

age_group = df.groupby("age_group")["num_credit_cards"].mean().sort_values(ascending=False)
print("\nSố thẻ tín dụng trung bình theo nhóm tuổi:")
print(age_group)

plt.figure(figsize=(7,4))
ax = sns.barplot(x=age_group.index, y=age_group.values)
plt.title("Số thẻ tín dụng trung bình theo nhóm tuổi")
plt.xlabel("Nhóm tuổi")
plt.ylabel("Số thẻ trung bình")

# Thêm chỉ số lên cột
for p in ax.patches:
    height = p.get_height()
    ax.annotate(f"{height:.2f}",
                (p.get_x() + p.get_width()/2, height),
                ha='center', va='bottom')

plt.show()

# ============================
# 3. Phân tích theo năm sinh
# ============================
birth_group = df.groupby("birth_year")["num_credit_cards"].mean().sort_values(ascending=False)

plt.figure(figsize=(10,4))
ax = sns.lineplot(x=birth_group.index, y=birth_group.values)
plt.title("Số thẻ tín dụng trung bình theo năm sinh")
plt.xlabel("Năm sinh")
plt.ylabel("Số thẻ trung bình")
plt.show()

print("\nNăm sinh có số thẻ tín dụng trung bình cao nhất:")
print(birth_group.head(5))
