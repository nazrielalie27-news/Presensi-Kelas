import streamlit as st
import pandas as pd
import datetime
import os
from openpyxl.styles import Border, Side

# Nama file Excel untuk menyimpan data
NAMA_FILE = "Data_Presensi_Guru.xlsx"

# 1. Daftar 16 Nama Guru (Sudah diurutkan sesuai Abjad A-Z)
daftar_guru = [
    "Pilih Guru...", 
    "Ami Hasmi Utamasari, S.Pd.", 
    "Anang, S.Pd., M.Pd.", 
    "Arvin Pratama Apendi, S.Pd.", 
    "Budi Sukirman, S.Pd.", 
    "Edgar Ismar Pratama, S.Pd.", 
    "Enung Kusnayah, Hj. S.Ag., M.Pd.", 
    "Firman Maulana, S.Kom.", 
    "Inggit Ciptaning Putri, S.Pd.", 
    "Molin Setiawati, S.Pd.", 
    "Rizaq Nashrul Haq, S.Pd.", 
    "Roby Firmansyah, S.Pd.", 
    "Suci Hariang Kencana, S.Pd.", 
    "Susi Herdanti, S.Pd.", 
    "Ujang Badrudin, S.Pd.", 
    "Ujang Purnama Alamsyah", 
    "Yani Mulayani, S.Pd."
]

# 2. Daftar 16 Mata Pelajaran
daftar_mapel = [
    "Pilih Mata Pelajaran...", 
    "Fisika",                
    "Bahasa Inggris",        
    "PJOK",                  
    "Ekonomi",               
    "Geografi",              
    "Pendidikan Agama",      
    "Sosiologi",             
    "Biologi",               
    "Kimia",                 
    "TIK",                   
    "PKN",                   
    "Sejarah",               
    "Bahasa Indonesia",      
    "PKWU",                  
    "KKA",                   
    "Matematika"             
]

# 3. Daftar Status Kehadiran
daftar_status = [
    "Pilih Status...", 
    "Hadir", 
    "Tidak hadir (Tanpa alasan)", 
    "Izin (Dengan alasan)", 
    "Sakit"
]

# === KODE CSS UNTUK WARNA LATAR SELURUH HALAMAN & FORMULIR ===
st.markdown("""
<style>
/* 1. Mengubah latar belakang seluruh halaman menjadi biru lembut */
.stApp {
    background-color: #D6EAF8; 
}

/* 2. Mengubah tampilan kotak form agar putih, menonjol, dan rapi */
[data-testid="stForm"] {
    background-color: #FFFFFF; 
    border: 2px solid #1E90FF; 
    border-radius: 15px;       
    padding: 20px;             
    box-shadow: 2px 2px 10px rgba(0,0,0,0.1); /* Tambahan bayangan halus */
}
</style>
""", unsafe_allow_html=True)

# === BAGIAN TAMPILAN WEBSITE (HEADER FOTO & JUDUL) ===

# Menampilkan Foto Kelas
try:
    st.image("foto_kelas.jpg", use_container_width=True)
except FileNotFoundError:
    st.info("🖼️ Foto kelas belum tersedia. (Simpan file gambar Anda dengan nama 'foto_kelas.jpg' di dalam folder Aplikasi Presensi).")

# Judul Utama dengan Bingkai
st.markdown("""
<div style="border: 3px solid #1E90FF; padding: 15px; border-radius: 10px; text-align: center; background-color: #FFFFFF; margin-bottom: 20px;">
    <h1 style="margin: 0; color: #333333;">📋 Formulir Kehadiran Guru</h1>
</div>
""", unsafe_allow_html=True)

st.write("Silakan isi formulir di bawah ini untuk melaporkan kehadiran.")

# === KOTAK FORMULIR ===
with st.form("formulir_kehadiran"):
    tanggal = st.date_input("1. Tanggal", datetime.date.today())
    
    nama_guru = st.selectbox("2. Nama Guru", daftar_guru)
    index_guru = daftar_guru.index(nama_guru)
    mapel = st.selectbox("3. Mata Pelajaran", daftar_mapel, index=index_guru)
    
    status = st.selectbox("4. Status Kehadiran", daftar_status)
    tugas = st.text_area("5. Tugas yang diberikan (Kosongkan jika tidak ada)")
    tombol_simpan = st.form_submit_button("💾 Simpan Data")

# === LOGIKA KETIKA TOMBOL SIMPAN DITEKAN ===
if tombol_simpan:
    if nama_guru == "Pilih Guru..." or mapel == "Pilih Mata Pelajaran..." or status == "Pilih Status...":
        st.error("⚠️ Gagal disimpan! Harap pastikan Nama Guru, Mata Pelajaran, dan Status sudah dipilih.")
    else:
        # Menyiapkan data
        data_baru = pd.DataFrame({
            "Tanggal": [tanggal.strftime("%d-%m-%Y")],
            "Nama Guru": [nama_guru],
            "Mata Pelajaran": [mapel],
            "Status Kehadiran": [status],
            "Tugas": [tugas]
        })

        # Cek apakah file sudah ada
        if os.path.exists(NAMA_FILE):
            df_lama = pd.read_excel(NAMA_FILE)
            df_gabung = pd.concat([df_lama, data_baru], ignore_index=True)
        else:
            df_gabung = data_baru

        # Menyimpan ke Excel
        with pd.ExcelWriter(NAMA_FILE, engine='openpyxl') as writer:
            df_gabung.to_excel(writer, index=False, sheet_name='Data Kehadiran')
            worksheet = writer.sheets['Data Kehadiran']
            
            garis_tipis = Border(
                left=Side(style='thin'), right=Side(style='thin'), 
                top=Side(style='thin'), bottom=Side(style='thin')
            )
            
            for col in worksheet.columns:
                max_length = 0
                column_letter = col[0].column_letter
                for cell in col:
                    cell.border = garis_tipis
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                worksheet.column_dimensions[column_letter].width = max_length + 2

        st.success(f"✅ Data kehadiran {nama_guru} berhasil dilaporkan ke Humas di Excel!")