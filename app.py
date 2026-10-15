import streamlit as st
import pandas as pd
import datetime
import gspread
import json

# --- KONFIGURASI GOOGLE SHEETS ---
# GANTI TULISAN DI BAWAH DENGAN LINK GOOGLE SHEETS ANDA SENDIRI:
URL_GOOGLE_SHEET = "https://docs.google.com/spreadsheets/d/1OPsXtDT_jcJhCdouScf7zXFW417G5QddAmWFzzMxmK8/edit?usp=sharing"

# 1. Daftar 16 Nama Guru (Sudah diurutkan)
daftar_guru = [
    "Pilih Guru...", "Ami Hasmi Utamasari, S.Pd.", "Anang, S.Pd., M.Pd.", "Arvin Pratama Apendi, S.Pd.", 
    "Budi Sukirman, S.Pd.", "Edgar Ismar Pratama, S.Pd.", "Enung Kusnayah, Hj. S.Ag., M.Pd.", 
    "Firman Maulana, S.Kom.", "Inggit Ciptaning Putri, S.Pd.", "Molin Setiawati, S.Pd.", 
    "Rizaq Nashrul Haq, S.Pd.", "Roby Firmansyah, S.Pd.", "Suci Hariang Kencana, S.Pd.", 
    "Susi Herdanti, S.Pd.", "Ujang Badrudin, S.Pd.", "Ujang Purnama Alamsyah", "Yani Mulayani, S.Pd."
]

# 2. Daftar 16 Mata Pelajaran
daftar_mapel = [
    "Pilih Mata Pelajaran...", "Fisika", "Bahasa Inggris", "PJOK", "Ekonomi", "Geografi", 
    "Pendidikan Agama", "Sosiologi", "Biologi", "Kimia", "TIK", "PKN", "Sejarah", 
    "Bahasa Indonesia", "PKWU", "KKA", "Matematika"
]

# 3. Daftar Status Kehadiran
daftar_status = ["Pilih Status...", "Hadir", "Tidak hadir (Tanpa alasan)", "Izin (Dengan alasan)", "Sakit"]

# CSS Warna Latar
st.markdown("""
<style>
.stApp { background-color: #D6EAF8; }
[data-testid="stForm"] { background-color: #FFFFFF; border: 2px solid #1E90FF; border-radius: 15px; padding: 20px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); }
</style>
""", unsafe_allow_html=True)

# HEADER
try:
    st.image("foto_kelas.jpg", use_container_width=True)
except FileNotFoundError:
    pass

st.markdown("""
<div style="border: 3px solid #1E90FF; padding: 15px; border-radius: 10px; text-align: center; background-color: #FFFFFF; margin-bottom: 20px;">
    <h1 style="margin: 0; color: #333333;">📋 Formulir Kehadiran Guru</h1>
</div>
""", unsafe_allow_html=True)

st.write("Silakan isi formulir di bawah ini untuk melaporkan kehadiran.")

# FORMULIR
with st.form("formulir_kehadiran"):
    tanggal = st.date_input("1. Tanggal", datetime.date.today())
    nama_guru = st.selectbox("2. Nama Guru", daftar_guru)
    index_guru = daftar_guru.index(nama_guru)
    mapel = st.selectbox("3. Mata Pelajaran", daftar_mapel, index=index_guru)
    status = st.selectbox("4. Status Kehadiran", daftar_status)
    tugas = st.text_area("5. Tugas yang diberikan (Kosongkan jika tidak ada)")
    tombol_simpan = st.form_submit_button("💾 Simpan Data")

# PROSES SIMPAN KE GOOGLE SHEETS
if tombol_simpan:
    if nama_guru == "Pilih Guru..." or mapel == "Pilih Mata Pelajaran..." or status == "Pilih Status...":
        st.error("⚠️ Gagal disimpan! Harap pastikan Nama Guru, Mata Pelajaran, dan Status sudah dipilih.")
    else:
        try:
            # Mengambil Kunci Rahasia dari brankas Streamlit
            kunci_dict = json.loads(st.secrets["gcp_service_account"])
            
            # Menghubungkan ke Google Sheets
            gc = gspread.service_account_from_dict(kunci_dict)
            sh = gc.open_by_url(URL_GOOGLE_SHEET)
            worksheet = sh.sheet1
            
            # Menyiapkan data
            data_baru = [
                tanggal.strftime("%d-%m-%Y"),
                nama_guru,
                mapel,
                status,
                tugas
            ]
            
            # Menambahkan data ke baris terbawah Google Sheets secara otomatis
            worksheet.append_row(data_baru)
            
            st.success(f"✅ Data kehadiran {nama_guru} berhasil masuk ke Google Sheets Anda secara Real-Time!")
        except Exception as e:
            st.error(f"❌ Terjadi kesalahan: {e}. Pastikan Kunci Rahasia dan Link Google Sheets sudah benar.")

st.markdown("---")
st.markdown("📊 **Data secara otomatis terekap ke Google Sheets.** Anda bisa melihatnya kapan saja di HP/Laptop.")