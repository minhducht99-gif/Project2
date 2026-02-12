# 1. Import thư viện
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style='whitegrid')
plt.rcParams['figure.figsize'] = (10, 5)

# Cài đặt font mặc định lớn hơn cho toàn bộ biểu đồ
plt.rcParams.update({
    'axes.titlesize': 18,       # Cỡ chữ tiêu đề biểu đồ
    'axes.labelsize': 16,       # Cỡ chữ nhãn trục
    'xtick.labelsize': 14,      # Cỡ chữ nhãn trục X
    'ytick.labelsize': 14,      # Cỡ chữ nhãn trục Y
    'legend.fontsize': 14,      # Cỡ chữ chú thích
    'figure.titlesize': 20      # Cỡ chữ tiêu đề toàn biểu đồ (nếu dùng plt.suptitle)
})


# 2. Đọc dữ liệu
df_trans = pd.read_csv('transactions_data_10pc.csv')
df_card = pd.read_csv('cards_data.csv')
df_user = pd.read_csv('users_data.csv')
df_merchant = pd.read_csv('mcc_codes.csv')
df_fraud = pd.read_csv('train_fraud_labels.csv')

# 3. Làm sạch tên cột
for df in [df_trans, df_card, df_user, df_merchant, df_fraud]:
    df.columns = df.columns.str.strip()

# 4. Chuyển đổi dữ liệu nếu cần
df_trans['amount'] = df_trans['amount'].replace('[\$,]', '', regex=True).astype(float)
df_user['yearly_income'] = df_user['yearly_income'].replace('[\$,]', '', regex=True).astype(float)
df_card['credit_limit'] = df_card['credit_limit'].replace('[\$,]', '', regex=True).astype(float)
df_fraud['target'] = df_fraud['label'].map({'Yes': 1, 'No': 0})

# 5. JOIN dữ liệu
df_tx_user = df_trans.merge(df_user, left_on='client_id', right_on='id', how='left', suffixes=('', '_user'))
df_tx_card = df_trans.merge(df_card, left_on='card_id', right_on='id', how='left', suffixes=('', '_card'))
df_tx_merchant = df_trans.merge(df_merchant, left_on='mcc', right_on='mcc_code', how='left')
df_tx_fraud = df_trans.merge(df_fraud[['id', 'target']], on='id', how='left')
df_card_user = df_card.merge(df_user, left_on='client_id', right_on='id', how='left')


# 6A. Chi tiêu theo tuổi, thu nhập

plt.figure()
sns.scatterplot(data=df_tx_user, x='current_age', y='amount', hue='gender', alpha=0.5)
plt.title('Chi tiêu theo độ tuổi')
plt.show()

plt.figure()
sns.scatterplot(data=df_tx_user, x='yearly_income', y='amount', alpha=0.5)
plt.title('Chi tiêu theo thu nhập')
plt.show()

# 6B. Hạn mức, loại thẻ
plt.figure()
sns.boxplot(data=df_tx_card, x='card_type', y='amount')
plt.title('Chi tiêu theo loại thẻ')
plt.show()

plt.figure()
sns.scatterplot(data=df_tx_card, x='credit_limit', y='amount', hue='card_type', alpha=0.5)
plt.title('Chi tiêu theo hạn mức thẻ')
plt.show()

# 6C. Phân khúc hành vi theo nhóm merchant
top_categories = df_tx_merchant['merchant_category'].value_counts().nlargest(10).index
df_top_merchants = df_tx_merchant[df_tx_merchant['merchant_category'].isin(top_categories)]

plt.figure()
sns.boxplot(data=df_top_merchants, x='merchant_category', y='amount')
plt.xticks(rotation=45)
plt.title('Chi tiêu theo nhóm merchant phổ biến')
plt.show()

# 6D. Rủi ro gian lận theo loại giao dịch, MCC
df_tx_fraud['target'] = df_tx_fraud['target'].fillna(0)

top_mcc_fraud = df_tx_fraud.groupby('mcc')['target'].mean().sort_values(ascending=False).head(10)

plt.figure()
sns.barplot(x=top_mcc_fraud.index.astype(str), y=top_mcc_fraud.values)
plt.title('Top 10 MCC có tỷ lệ gian lận cao nhất')
plt.ylabel('Tỷ lệ gian lận')
plt.xlabel('MCC')
plt.show()

# 6E. Hạn mức theo thu nhập, số thẻ theo tuổi
plt.figure()
sns.scatterplot(data=df_card_user, x='yearly_income', y='credit_limit', alpha=0.5)
plt.title('Hạn mức thẻ theo thu nhập')
plt.show()
