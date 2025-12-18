# Data Strategy & Architecture Standards

Dokumen ini memetakan proyek **Anthropic Interview Analysis** terhadap 8 standar industri wajib untuk Data Analytics. Ini bertujuan untuk menunjukkan kematangan arsitektur dan kualitas penanganan data dalam proyek ini.

## 1. Data Architecture
*Stack teknis yang jelas dan scalable.*

*   **Penerapan**: Menggunakan arsitektur **ETL (Extract, Transform, Load)** modular berbasis Python.
    *   **Extract**: `data_loader.py` menangani pengambilan data dari Hugging Face.
    *   **Transform**: `preprocessor.py` menangani pembersihan dan segmentasi dialog (User vs Assistant).
    *   **Analyze**: `analysis.py` dan `semantic_analysis.py` menangani logika bisnis dan statistik.
    *   **Load**: Output disimpan dalam format Laporan Markdown (`.md`) dan Visualisasi (`.png`).
*   **Scalability**: Kode didesain modular. Jika data membesar, modul `pandas` bisa diganti dengan `dask` atau `spark` tanpa merusak logika analisis utama.

## 2. Data Modeling
*Model data yang rapi untuk insight yang akurat.*

*   **Penerapan**: Menggunakan **Flat Schema** (Denormalized) dalam bentuk DataFrame.
*   **Struktur Data**:
    *   `turn_id`: Primary key unik untuk setiap giliran bicara.
    *   `role`: Metadata kategorikal ('user' vs 'assistant').
    *   `content`: Data teks tidak terstruktur (Unstructured Data).
    *   `length`: Fitur turunan (derived feature) untuk analisis klaster.

## 3. Data Warehouse
*Satu sumber kebenaran (Single Source of Truth).*

*   **Penerapan**: Karena skala proyek ini lokal/portofolio, "Warehouse" disimulasikan sebagai penyimpanan file lokal yang terpusat.
*   **Source**: Dataset Hugging Face `Anthropic/anthropic-hh-rlhf` dianggap sebagai Raw Data Lake.
*   **Mart**: Output `analysis_report_generated.md` berfungsi sebagai Data Mart yang siap dikonsumsi oleh stakeholder (user).

## 4. Data Governance
*Pengelolaan akses, lineage, dan konsistensi.*

*   **Penerapan**:
    *   **Lineage**: Alur data jelas dari `Extract` -> `Preprocess` -> `Analyze` -> `Report`.
    *   **Consistency**: Penggunaan `STOPWORDS` standar di seluruh modul (didefinisikan di `analysis.py` dan `semantic_analysis.py`) memastikan integritas hasil analisis teks.

## 5. Data Quality
*Data buruk = keputusan buruk.*

*   **Penerapan**: Proyek ini memiliki **3 Layer Quality Control**:
    1.  **Filtering**: Menghapus kata sambung (stopwords) dan kata pendek (< 4 huruf) untuk mengurangi noise.
    2.  **Bias Removal**: Secara spesifik menghapus bias wawancara (seperti kata 'particularly', 'made') untuk memastikan kemurnian sentimen (Debiasing).
    3.  **Thresholding**: Hanya menghitung koneksi semantik dengan frekuensi > 6 untuk membuang anomali/kebetulan.

## 6. Data Observability
*Monitoring freshness dan kesehatan data.*

*   **Penerapan**: Sistem **Logging** konsol (`print`) yang mendetail di setiap step.
    *   User diberitahu berapa baris data yang berhasil di-load (`Successfully loaded 1000 rows`).
    *   Peringatan jika data null atau gagal load.
    *   Status eksekusi per modul ("Running Semantic Network...", "Analysis Complete").

## 7. Data Security & Privacy
*Perlindungan data sensitif (PII).*

*   **Penerapan**:
    *   **Public Data**: Dataset yang digunakan adalah data publik yang sudah dianonimisasi oleh penyedia (Anthropic).
    *   **Safety**: Script tidak mengirim data ke server eksternal (full local processing), sehingga aman dari kebocoran data.

## 8. Metadata Management
*Dokumentasi dan konteks data.*

*   **Penerapan**:
    *   `README.md`: Dokumentasi teknis cara kerja sistem.
    *   `CUSTOMIZATION.md`: Glossary parameter (apa itu `k`, apa itu `threshold`).
    *   `PANDUAN_PEMULA.md`: Dokumentasi bisnis/kontekstual untuk non-teknis.
    *   Code Comments: Penjelasan fungsi di setiap blok kode (misal: docstring pada `analyze_semantic_network`).

---

**Status Audit**: COMPLIANT (Skala Portofolio/Lokal)
Proyek ini telah memenuhi prinsip-prinsip dasar Data Engineering modern dalam skala yang sesuai.
