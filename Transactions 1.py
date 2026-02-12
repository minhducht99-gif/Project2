import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")

# ============================
# 0. ĐỌC & TIỀN XỬ LÝ DỮ LIỆU
# ============================

df = pd.read_csv("transactions_data_10pc.csv")

# Chuẩn hóa tên cột
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# Làm sạch amount
df["amount"] = df["amount"].replace('[\$,()]', '', regex=True).astype(float)

# Chuyển date sang datetime
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["date_only"] = df["date"].dt.date
df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month
df["month_period"] = df["date"].dt.to_period("M")
df["weekday"] = df["date"].dt.day_name()
df["hour"] = df["date"].dt.hour

# ============================
# 1. KHÁCH HÀNG CHI TIÊU BAO NHIÊU?
# ============================

client_summary = df.groupby("client_id").agg(
    total_amount=("amount", "sum"),
    n_transactions=("id", "count"),
    avg_amount=("amount", "mean")
).reset_index()

# Phân phối tổng chi tiêu
plt.figure(figsize=(8,5))
sns.histplot(client_summary["total_amount"], bins=50, kde=True, color="steelblue")
plt.title("Phân phối tổng chi tiêu theo khách hàng")
plt.xlabel("Tổng chi tiêu ($)")
plt.ylabel("Số khách hàng")
plt.tight_layout()
plt.show()

# Phân phối số lượng giao dịch
plt.figure(figsize=(8,5))
sns.histplot(client_summary["n_transactions"], bins=50, kde=True, color="darkorange")
plt.title("Phân phối số lượng giao dịch theo khách hàng")
plt.xlabel("Số giao dịch")
plt.ylabel("Số khách hàng")
plt.tight_layout()
plt.show()

# Phân phối giá trị giao dịch
plt.figure(figsize=(8,5))
sns.histplot(df["amount"], bins=50, kde=True, color="purple")
plt.title("Phân phối giá trị giao dịch")
plt.xlabel("Giá trị giao dịch ($)")
plt.ylabel("Số giao dịch")
plt.tight_layout()
plt.show()

# ============================
# 2. HÀNH VI CHI TIÊU THEO THỜI GIAN
# ============================

# --- 2.1 Chi tiêu theo 12 tháng ---
monthly_amount = df.groupby("month")["amount"].sum()
monthly_count = df.groupby("month")["id"].count()

plt.figure(figsize=(10,5))
sns.lineplot(x=monthly_amount.index, y=monthly_amount.values, marker="o")
plt.title("Tổng chi tiêu theo 12 tháng")
plt.xlabel("Tháng")
plt.ylabel("Tổng chi tiêu ($)")
plt.xticks(range(1,13))
plt.tight_layout()
plt.show()


# --- 2.2 Chi tiêu theo các năm ---
yearly_amount = df.groupby("year")["amount"].sum()
yearly_count = df.groupby("year")["id"].count()

plt.figure(figsize=(10,5))
sns.lineplot(x=yearly_amount.index, y=yearly_amount.values, marker="o")
plt.title("Tổng chi tiêu theo các năm")
plt.xlabel("Năm")
plt.ylabel("Tổng chi tiêu ($)")
plt.tight_layout()
plt.show()

# Tổng chi tiêu theo giờ giao dịch
hour_tx = df.groupby("hour")["amount"].sum()
plt.figure(figsize=(8,5))
sns.lineplot(x=hour_tx.index, y=hour_tx.values, marker="o")
plt.title("Tổng chi tiêu theo giờ giao dịch")
plt.xlabel("Giờ trong ngày")
plt.ylabel("Tổng chi tiêu ($)")
plt.xticks(range(0,24))
plt.tight_layout()
plt.show()

# ============================
# 3. PHƯƠNG THỨC THANH TOÁN
# ============================

plt.figure(figsize=(7,5))
order_methods = df["use_chip"].value_counts().index
ax = sns.countplot(data=df, x="use_chip", order=order_methods, palette="Set2")
plt.title("Phân bố phương thức thanh toán")
plt.xlabel("Phương thức")
plt.ylabel("Số lượng giao dịch")

counts = df["use_chip"].value_counts()
percents = (counts / len(df) * 100).round(1)

for i, p in enumerate(ax.patches):
    height = p.get_height()
    ax.annotate(f"{height}\n{percents.iloc[i]}%", 
                (p.get_x() + p.get_width()/2, height),
                ha='center', va='bottom')

plt.tight_layout()
plt.show()

# ============================
# 4. GIAO DỊCH BẤT THƯỜNG
# ============================

threshold_high = df["amount"].quantile(0.99)

suspicious_large = df[df["amount"] >= threshold_high]
suspicious_negative = df[df["amount"] < 0]
suspicious_online = df[df["merchant_city"].astype(str).str.upper() == "ONLINE"]
suspicious_error = df[df["errors"].notna() & (df["errors"].astype(str) != "")]

plt.figure(figsize=(8,5))
sns.histplot(df["amount"], bins=100, color="grey")
plt.axvline(threshold_high, color="red", linestyle="--", label=f"Ngưỡng top 1%: {threshold_high:.2f}")
plt.title("Phân phối giá trị giao dịch & ngưỡng giao dịch lớn bất thường")
plt.xlabel("Giá trị giao dịch ($)")
plt.ylabel("Số lượng")
plt.legend()
plt.tight_layout()
plt.show()

# ============================
# 5. PHÂN KHÚC KHÁCH HÀNG
# ============================

client_summary = df.groupby("client_id").agg(
    total_amount=("amount", "sum"),
    n_transactions=("id", "count"),
    avg_amount=("amount", "mean"),
    n_negative=("amount", lambda x: (x < 0).sum()),
    n_online=("merchant_city", lambda x: (x.astype(str).str.upper() == "ONLINE").sum()),
    n_error=("errors", lambda x: x.notna().sum())
).reset_index()

amount_70 = client_summary["total_amount"].quantile(0.7)
freq_70 = client_summary["n_transactions"].quantile(0.7)

def segment_client(row):
    risky = (row["n_negative"] > 0) or (row["n_error"] > 0)
    high_spender = row["total_amount"] >= amount_70
    high_freq = row["n_transactions"] >= freq_70

    if risky and (high_spender or high_freq):
        return "High Risk"
    elif high_spender and high_freq:
        return "High Value"
    elif high_spender or high_freq:
        return "Potential"
    else:
        return "Normal"

client_summary["segment"] = client_summary.apply(segment_client, axis=1)

plt.figure(figsize=(7,5))
order_seg = ["High Value", "High Risk", "Potential", "Normal"]
sns.countplot(data=client_summary, x="segment", order=order_seg, palette="viridis")
plt.title("Phân khúc khách hàng theo hành vi chi tiêu & rủi ro")
plt.xlabel("Phân khúc")
plt.ylabel("Số khách hàng")
plt.tight_layout()
plt.show()

plt.figure(figsize=(8,6))
sns.scatterplot(
    data=client_summary,
    x="n_transactions",
    y="total_amount",
    hue="segment",
    palette="viridis"
)
plt.title("Tổng chi tiêu vs số giao dịch theo phân khúc khách hàng")
plt.xlabel("Số giao dịch")
plt.ylabel("Tổng chi tiêu ($)")
plt.tight_layout()
plt.show()
