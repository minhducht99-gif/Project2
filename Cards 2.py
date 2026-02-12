import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import argparse


# ============================================================
# HÀM LOAD DỮ LIỆU
# - Đọc file CSV
# - Làm sạch cột credit_limit (loại ký tự $, dấu phẩy...)
# - Chuyển về dạng số để phân tích
# ============================================================
def load_data(path):
    df = pd.read_csv(path)

    # Loại bỏ ký tự không phải số trong credit_limit (ví dụ: "$5,000")
    s = df['credit_limit'].astype(str).str.replace(r"[^0-9.-]", "", regex=True)

    # Chuyển sang dạng số, lỗi -> NaN
    df['credit_limit_clean'] = pd.to_numeric(s, errors='coerce')
    return df


# ============================================================
# HÀM TÓM TẮT THỐNG KÊ credit_limit
# - Đếm giá trị thiếu
# - Thống kê mô tả
# - Tính quantile
# - Skewness & Kurtosis
# - Thống kê theo card_type
# - Lấy top 10 hạn mức cao nhất
# ============================================================
def summarize_credit(df):
    credit = df['credit_limit_clean']

    # Số lượng giá trị thiếu
    missing = credit.isna().sum()

    # Thống kê mô tả cơ bản
    desc = credit.describe()

    # Các quantile quan trọng
    qs = credit.quantile([0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 0.9, 0.95, 0.99])

    # Độ lệch (skew) và độ nhọn (kurtosis)
    skew = credit.skew()
    kurt = credit.kurt()

    # Thống kê theo loại thẻ
    by_type = df.groupby('card_type')['credit_limit_clean'].agg(
        ['count', 'mean', 'median', 'std']
    ).sort_values('count', ascending=False)

    # Top 10 hạn mức cao nhất
    top10 = df.nlargest(10, 'credit_limit_clean')[['id', 'client_id', 'card_brand', 'card_type', 'credit_limit_clean']]

    return {
        'missing': missing,
        'desc': desc,
        'quantiles': qs,
        'skew': skew,
        'kurt': kurt,
        'by_type': by_type,
        'top10': top10,
        'rows_cols': df.shape,
    }


# ============================================================
# HÀM VẼ BIỂU ĐỒ
# - Histogram dạng tuyến tính
# - Histogram dạng log10
# - Boxplot để xem outlier
# ============================================================
def make_plots(df, out_dir='.'):
    os.makedirs(out_dir, exist_ok=True)

    # Loại bỏ NaN để vẽ biểu đồ
    credit = df['credit_limit_clean'].dropna()

    # -----------------------------
    # Histogram dạng tuyến tính
    # -----------------------------
    plt.figure(figsize=(8, 5))
    sns.histplot(credit, bins=60, kde=True)
    plt.title('Credit limit distribution (linear)')
    plt.xlabel('credit_limit')
    plt.tight_layout()
    p1 = os.path.join(out_dir, 'credit_limit_hist.png')
    plt.savefig(p1, dpi=150)
    plt.close()

    # -----------------------------
    # Histogram dạng log10
    # - Giúp nhìn rõ phân bố khi dữ liệu lệch phải
    # -----------------------------
    plt.figure(figsize=(8, 5))
    sns.histplot(np.log10(credit + 1), bins=60, kde=True)
    plt.title('Log10 Credit limit distribution')
    plt.xlabel('log10(credit_limit + 1)')
    plt.tight_layout()
    p2 = os.path.join(out_dir, 'credit_limit_hist_log.png')
    plt.savefig(p2, dpi=150)
    plt.close()

    # -----------------------------
    # Boxplot để phát hiện outlier
    # -----------------------------
    plt.figure(figsize=(8, 2))
    sns.boxplot(x=credit, orient='h')
    plt.title('Credit limit boxplot')
    plt.tight_layout()
    p3 = os.path.join(out_dir, 'credit_limit_box.png')
    plt.savefig(p3, dpi=150)
    plt.close()

    return p1, p2, p3


# ============================================================
# HÀM IN BÁO CÁO PHÂN TÍCH
# - In thống kê mô tả
# - In quantile
# - In skew, kurtosis
# - In top 10 hạn mức cao nhất
# - In thống kê theo card_type
# ============================================================
def print_report(rep, paths):
    print('rows,cols:', rep['rows_cols'])

    print('\nmissing credit_limit:', rep['missing'])

    print('\nDescriptive stats:')
    print(rep['desc'])

    print('\nSelected quantiles:')
    print(rep['quantiles'])

    print('\nSkewness, kurtosis:', rep['skew'], rep['kurt'])

    print('\nTop 10 largest credit limits:')
    print(rep['top10'].to_string(index=False))

    print('\nBy card_type (count, mean, median, std):')
    print(rep['by_type'].to_string())

    print('\nSaved plots:')
    for p in paths:
        print(' -', p)


# ============================================================
# HÀM MAIN
# - Nhận input file & output folder từ command line
# - Chạy toàn bộ pipeline phân tích
# ============================================================
def main():
    parser = argparse.ArgumentParser(description='Analyze credit_limit in cards_data.csv')

    # Tham số input file
    parser.add_argument('--input', '-i', default='cards_data.csv')

    # Tham số thư mục lưu biểu đồ
    parser.add_argument('--outdir', '-o', default='.')

    args = parser.parse_args()

    # Load dữ liệu
    df = load_data(args.input)

    # Tóm tắt thống kê
    rep = summarize_credit(df)

    # Vẽ biểu đồ
    paths = make_plots(df, args.outdir)

    # In báo cáo
    print_report(rep, paths)


# ============================================================
# CHẠY CHƯƠNG TRÌNH
# ============================================================
if __name__ == '__main__':
    main()
