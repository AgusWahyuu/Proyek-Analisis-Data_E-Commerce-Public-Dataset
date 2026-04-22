import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

st.set_page_config(page_title="E-Commerce Performance Dashboard", layout="wide")

state_mapping = {
    'AC': 'Acre', 'AL': 'Alagoas', 'AM': 'Amazonas', 'AP': 'Amapá', 'BA': 'Bahia',
    'CE': 'Ceará', 'DF': 'Distrito Federal', 'ES': 'Espírito Santo', 'GO': 'Goiás',
    'MA': 'Maranhão', 'MG': 'Minas Gerais', 'MS': 'Mato Grosso do Sul', 'MT': 'Mato Grosso',
    'PA': 'Pará', 'PB': 'Paraíba', 'PE': 'Pernambuco', 'PI': 'Piauí', 'PR': 'Paraná',
    'RJ': 'Rio de Janeiro', 'RN': 'Rio Grande do Norte', 'RO': 'Rondônia', 'RR': 'Roraima',
    'RS': 'Rio Grande do Sul', 'SC': 'Santa Catarina', 'SE': 'Sergipe', 'SP': 'São Paulo', 'TO': 'Tocantins'
}

@st.cache_data
def load_data():
    df = pd.read_csv("dashboard/main_data.csv")
    datetime_columns = ["order_purchase_timestamp", "order_delivered_customer_date"]
    for column in datetime_columns:
        df[column] = pd.to_datetime(df[column])
    df['customer_state_full'] = df['customer_state'].map(state_mapping)
    return df

all_df = load_data()

# SIDEBAR
with st.sidebar:
    st.title("Filter Transaksi")
    min_date = all_df["order_purchase_timestamp"].min()
    max_date = all_df["order_purchase_timestamp"].max()

    try:
        start_date, end_date = st.date_input(
            label='Rentang Waktu',
            min_value=min_date,
            max_value=max_date,
            value=[min_date, max_date]
        )
    except ValueError:
        st.error("Silakan pilih rentang tanggal (Mulai & Selesai)")
        st.stop()

# Filter data utama
main_df = all_df[(all_df["order_purchase_timestamp"] >= pd.to_datetime(start_date)) & 
                (all_df["order_purchase_timestamp"] <= pd.to_datetime(end_date))].copy()

# MAIN PAGE
st.title('E-Commerce Performance Dashboard 📊')
st.markdown(f"Periode Analisis: **{start_date}** hingga **{end_date}**")
st.markdown("---")

# KORELASI PENGIRIMAN & REVIEW
st.subheader("1. Hubungan Durasi Pengiriman terhadap Kepuasan")
col1, col2 = st.columns([2, 1])

with col1:
    main_df['delivery_time'] = (main_df['order_delivered_customer_date'] - main_df['order_purchase_timestamp']).dt.days
    valid_delivery = main_df[main_df['delivery_time'] >= 0].copy()
    
    bins = [0, 7, 14, 21, 30, 60, 200]
    valid_delivery['delivery_bin'] = pd.cut(valid_delivery['delivery_time'], bins=bins)
    delivery_review = valid_delivery.groupby('delivery_bin', observed=True)['review_score'].mean().reset_index()
    
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    colors = ["#72BCD4" if x >= 4 else "#D3D3D3" for x in delivery_review['review_score']]
    
    sns.barplot(data=delivery_review, x='delivery_bin', y='review_score', palette=colors, hue='delivery_bin', legend=False, ax=ax1)
    ax1.axhline(y=4, color='red', linestyle='--', alpha=0.6)
    ax1.set_ylabel("Rata-rata Skor Review")
    ax1.set_xlabel("Rentang Hari Pengiriman")
    ax1.set_ylim(0, 5)
    st.pyplot(fig1)

with col2:
    avg_review = main_df['review_score'].mean()
    st.metric("Rata-rata Skor Review", round(avg_review, 2))

    safe_bins = delivery_review[delivery_review['review_score'] >= 4]
    if not safe_bins.empty:
        max_safe_bin = safe_bins.iloc[-1]['delivery_bin']
        st.info(f"**Insight:** Kepuasan tetap terjaga (skor ≥ 4.0) untuk pengiriman hingga rentang **{max_safe_bin}** hari. Melebihi durasi ini, skor kepuasan cenderung turun di bawah target.")
    else:
        st.warning(f"**Insight:** Tidak ada durasi pengiriman yang mencapai target skor 4.0 pada periode ini.")

# TOP PRODUK PER STATE
st.subheader("2. Kontribusi Pendapatan per Wilayah")
top_states_full = main_df['customer_state_full'].value_counts().head(5).index
selected_state_full = st.selectbox("Pilih Negara Bagian (Nama Lengkap):", top_states_full)

state_data = main_df[main_df['customer_state_full'] == selected_state_full]
top_category = state_data.groupby('product_category_name')['price'].sum().sort_values(ascending=False).head(5).reset_index()

fig2, ax2 = plt.subplots(figsize=(10, 5))
sns.barplot(data=top_category, x='price', y='product_category_name', color="#2E86C1", ax=ax2)
ax2.set_xlabel("Total Revenue (BRL)")
ax2.set_ylabel(None)
st.pyplot(fig2)

top_cat = top_category.iloc[0]
st.write(f"💡 **Insight:** Di wilayah **{selected_state_full}**, kategori produk **'{top_cat['product_category_name']}'** menjadi kontributor pendapatan terbesar dengan total **{top_cat['price']:,.2f} BRL**. Strategi pemasaran lokal di wilayah ini sebaiknya difokuskan pada kategori tersebut untuk memaksimalkan ROI.")

# PERFORMA PELANGGAN (RFM)
st.subheader("3. Performa Pelanggan (Metrik RFM)")

latest_date = main_df["order_purchase_timestamp"].max()
rfm_data = main_df.groupby("customer_unique_id").agg({
    "order_purchase_timestamp": lambda x: (latest_date - x.max()).days,
    "order_id": "nunique",
    "price": "sum"
}).reset_index()
rfm_data.columns = ["id", "recency", "frequency", "monetary"]

c1, c2, c3 = st.columns(3)
with c1: st.metric("Rata-rata Recency", f"{round(rfm_data['recency'].mean(), 1)} Hari")
with c2: st.metric("Rata-rata Frekuensi", f"{round(rfm_data['frequency'].mean(), 2)} Transaksi")
with c3: st.metric("Rata-rata Monetary", f"{round(rfm_data['monetary'].mean(), 2)} BRL")

fig3, ax3 = plt.subplots(nrows=1, ncols=3, figsize=(20, 6))

# Recency
sns.histplot(rfm_data['recency'], kde=True, ax=ax3[0], color="#72BCD4", edgecolor='white')
ax3[0].set_title("Recency Distribution", fontsize=14, weight='bold')
ax3[0].set_xlim(left=0)

# Frequency
sns.histplot(rfm_data['frequency'], bins=10, discrete=True, ax=ax3[1], color="#2E86C1")
ax3[1].set_title("Frequency Distribution", fontsize=14, weight='bold')
ax3[1].set_yscale('log')
ax3[1].set_xlim(left=0)
ax3[1].set_xticks(range(0, int(rfm_data['frequency'].max()) + 1))

# Monetary
sns.histplot(rfm_data['monetary'], kde=True, ax=ax3[2], color="#1F4E79", edgecolor='white')
ax3[2].set_title("Monetary Distribution", fontsize=14, weight='bold')
ax3[2].set_xlim(left=0, right=rfm_data['monetary'].quantile(0.95))

for ax in ax3:
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(False)

plt.tight_layout()
st.pyplot(fig3)

total_revenue = rfm_data['monetary'].sum()
one_time_buyers = (rfm_data['frequency'] == 1).sum()
percent_one_time = (one_time_buyers / len(rfm_data)) * 100

st.success(f"**Insight Strategis RFM:** Total pendapatan yang dihasilkan pada periode ini adalah **{total_revenue:,.2f} BRL**. Data menunjukkan bahwa **{percent_one_time:.1f}%** pelanggan hanya melakukan satu kali transaksi. Hal ini mengindikasikan perlunya program loyalitas atau kampanye re-engagement untuk meningkatkan retensi pelanggan yang sudah lama tidak bertransaksi (Recency tinggi).")