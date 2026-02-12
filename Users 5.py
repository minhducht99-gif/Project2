import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Đọc dữ liệu
df = pd.read_csv("Users_data.csv")

# Chuẩn hóa tên cột
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# Làm sạch dữ liệu thu nhập và nợ
df["yearly_income"] = df["yearly_income"].replace('[\$,]', '', regex=True).astype(float)
df["total_debt"] = df["total_debt"].replace('[\$,]', '', regex=True).astype(float)

# ============================
# 1. CHIA 4 HƯỚNG ĐÔNG – TÂY – NAM – BẮC
# ============================

# Bắc – Nam theo latitude
def get_ns(lat):
    return "North" if lat >= 37.5 else "South"

# Đông – Tây theo longitude
def get_ew(lon):
    return "East" if lon >= -100 else "West"

df["NS"] = df["latitude"].apply(get_ns)
df["EW"] = df["longitude"].apply(get_ew)

# Ghép thành 4 hướng
df["direction"] = df["NS"] + "-" + df["EW"]

# ============================
# 2. HEATMAP THU NHẬP THEO 4 HƯỚNG
# ============================

income_pivot = df.pivot_table(
    values="yearly_income",
    index="NS",
    columns="EW",
    aggfunc="mean"
).round(1)

plt.figure(figsize=(8,6))
sns.heatmap(
    income_pivot,
    annot=True,
    fmt=".1f",
    cmap="YlGnBu"
)
plt.title("Heatmap Thu nhập trung bình theo 4 hướng Đông – Tây – Nam – Bắc")
plt.xlabel("Kinh độ (East / West)")
plt.ylabel("Vĩ độ (North / South)")
plt.show()

# ============================
# 3. HEATMAP NỢ THEO 4 HƯỚNG
# ============================

debt_pivot = df.pivot_table(
    values="total_debt",
    index="NS",
    columns="EW",
    aggfunc="mean"
).round(1)

plt.figure(figsize=(8,6))
sns.heatmap(
    debt_pivot,
    annot=True,
    fmt=".1f",
    cmap="OrRd"
)
plt.title("Heatmap Tổng nợ trung bình theo 4 hướng Đông – Tây – Nam – Bắc")
plt.xlabel("Kinh độ (East / West)")
plt.ylabel("Vĩ độ (North / South)")
plt.show()
