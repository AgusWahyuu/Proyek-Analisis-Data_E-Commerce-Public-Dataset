# E-Commerce Data Analysis Dashboard 📊

Dashboard ini adalah proyek akhir analisis data yang menyajikan wawasan mendalam mengenai performa operasional dan perilaku pelanggan pada platform e-commerce di Brasil. Proyek ini mencakup seluruh siklus pengolahan data, mulai dari _Data Wrangling_, _Exploratory Data Analysis (EDA)_, hingga _Data Visualization_ dan _Deployment_.

---

## Fitur Utama

Proyek ini dirancang untuk menjawab pertanyaan bisnis strategis dengan fitur-fitur berikut:

### 1. Delivery & Satisfaction Analysis

- **Insight:** Secara otomatis mendeteksi ambang batas waktu pengiriman yang aman untuk menjaga skor ulasan tetap di atas target (Skor ≥ 4.0).
- **Logistik Bottleneck:** Visualisasi korelasi antara durasi pengiriman dengan tingkat kepuasan pelanggan.

### 2. Geographic Revenue Insight

- **Filter Wilayah:** Menampilkan 5 negara bagian (State) dengan pendapatan tertinggi di Brasil.
- **Top Product Kategori:** Mengetahui kategori produk yang paling mendominasi di setiap wilayah tertentu secara dinamis.

### 3. Customer Segmentation (RFM)

- **Recency Distribution:** Memantau seberapa baru pelanggan melakukan transaksi.
- **Frequency Distribution:** Menganalisis loyalitas pelanggan (dilengkapi dengan skala logaritmik).
- **Monetary Distribution:** Sebaran nilai transaksi pelanggan untuk mengidentifikasi kontribusi ekonomi.

---

## Struktur Direktori Proyek

| Berkas / Folder        | Keterangan                                                                        |
| :--------------------- | :-------------------------------------------------------------------------------- |
| **`dashboard/`**       | Berisi file aplikasi utama (`dashboard.py`) dan dataset bersih (`main_data.csv`). |
| **`data/`**            | Kumpulan dataset mentah dalam format CSV.                                         |
| **`notebook.ipynb`**   | File dokumentasi lengkap proses analisis (Gathering, Assessing, Cleaning, EDA).   |
| **`requirements.txt`** | Daftar pustaka (library) Python yang digunakan.                                   |
| **`url.txt`**          | Tautan dashboard yang sudah tayang di Streamlit Cloud.                            |

---

## Panduan Instalasi (Lokal)

Ikuti langkah-langkah berikut untuk menjalankan dashboard di komputer lokal Anda:

### 1. Clone Repository

Unduh proyek ini ke direktori lokal Anda:

```bash
git clone https://github.com/AgusWahyuu/Proyek-Analisis-Data_E-Commerce-Public-Dataset.git
cd Proyek-Analisis-Data_E-Commerce-Public-Dataset
```

### 2. Setup Virtual Environment (Opsional)

Gunakan environment terpisah agar tidak mengganggu library sistem:

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalasi Library

Instal semua dependensi yang dibutuhkan dengan perintah berikut:

```bash
pip install -r requirements.txt
```

### 4. Jalankan Dashboard

Setelah instalasi selesai, jalankan dashboard menggunakan Streamlit:

```bash
streamlit run dashboard/dashboard.py
```

Aplikasi akan otomatis terbuka di browser Anda, biasanya pada alamat `http://localhost:8501`.

---

## Deployment

Dashboard ini dapat diakses secara online melalui tautan berikut:

👉 [E-Commerce Performance Dashboard Live](https://e-commerce-dashboard--i-putu-agus-wahyu-wirakusuma-putra.streamlit.app/)
