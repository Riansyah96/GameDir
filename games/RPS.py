import random
import time
import streamlit as st

def inisialisasi_permainan():
    """Inisialisasi state permainan"""
    st.session_state.skor = {'pemain': 0, 'komputer': 0, 'seri': 0}
    st.session_state.permainan_selesai = False
    st.session_state.riwayat = []
    st.session_state.ronde = 1

def simpan_hasil(nama, mode, kesulitan):
    """Menyimpan hasil permainan ke leaderboard"""
    # Cek apakah sudah ada record dengan nama, mode, dan kesulitan yang sama
    ditemukan = False
    for record in st.session_state.leaderboard:
        if (record['nama'] == nama and 
            record['mode'] == mode and 
            record['kesulitan'] == kesulitan):
            # Update record yang sudah ada
            record['skor_pemain'] += st.session_state.skor['pemain']
            record['skor_komputer'] += st.session_state.skor['komputer']
            record['total_seri'] += st.session_state.skor['seri']
            record['total_ronde'] += st.session_state.ronde - 1
            record['terakhir_diperbarui'] = time.strftime("%Y-%m-%d %H:%M:%S")
            ditemukan = True
            break
    
    if not ditemukan:
        # Buat record baru
        st.session_state.leaderboard.append({
            'nama': nama,
            'mode': mode,
            'kesulitan': kesulitan,
            'skor_pemain': st.session_state.skor['pemain'],
            'skor_komputer': st.session_state.skor['komputer'],
            'total_seri': st.session_state.skor['seri'],
            'total_ronde': st.session_state.ronde - 1,
            'terakhir_diperbarui': time.strftime("%Y-%m-%d %H:%M:%S"),
            'waktu_dibuat': time.strftime("%Y-%m-%d %H:%M:%S")
        })
    
    st.session_state.nama_tersimpan = nama

# Inisialisasi data penyimpanan
if 'leaderboard' not in st.session_state:
    st.session_state.leaderboard = []
if 'total_permainan' not in st.session_state:
    st.session_state.total_permainan = 0
if 'total_kemenangan' not in st.session_state:
    st.session_state.total_kemenangan = 0

# =====================================
# BAGIAN PENGATURAN
# =====================================
st.title("Game GBK (Gunting-Batu-Kertas)")
with st.expander("⚙️ Pengaturan Game", expanded=True):
    kolom_set1, kolom_set2 = st.columns(2)
    
    with kolom_set1:
        mode_permainan = st.selectbox(
            "Mode Permainan:",
            ["Normal", "Best of 3", "Best of 5"],
            key="mode_permainan"
        )
    
    with kolom_set2:
        tingkat_kesulitan = st.selectbox(
            "Tingkat Kesulitan:",
            ["Normal", "Sulit", "Expert"],
            key="tingkat_kesulitan"
        )
    
    if st.button("🚀 Mulai Permainan Baru", 
                key="mulai_game", 
                use_container_width=True):
        inisialisasi_permainan()
        st.success(f"Permainan dimulai! Mode: {mode_permainan}")
        st.rerun()

st.markdown("---")

# =====================================
# BAGIAN UTAMA PERMAINAN
# =====================================
if 'skor' in st.session_state:
    nama_pemain = st.text_input(
        "Masukkan nama Anda:", 
        key="input_nama",
        max_chars=20,
        value=st.session_state.get("nama_tersimpan", "")
    )
    
    st.info(f"""
    🎮 **Mode:** {mode_permainan}  
    🏆 **Kesulitan:** {tingkat_kesulitan}  
    🔢 **Ronde:** {st.session_state.ronde}
    """)
    
    # Tampilan skor
    st.subheader("📊 Skor Permainan")
    skor1, skor2, skor3 = st.columns(3)
    with skor1:
        st.markdown("<div style='text-align: center;'><h3>Anda</h3><h1 style='color: #4CAF50;'>" + 
                   f"{st.session_state.skor['pemain']}</h1></div>", unsafe_allow_html=True)
    with skor2:
        st.markdown("<div style='text-align: center;'><h3>Seri</h3><h1 style='color: #FFC107;'>" + 
                   f"{st.session_state.skor['seri']}</h1></div>", unsafe_allow_html=True)
    with skor3:
        st.markdown("<div style='text-align: center;'><h3>Komputer</h3><h1 style='color: #F44336;'>" + 
                   f"{st.session_state.skor['komputer']}</h1></div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Pilihan pemain
    st.subheader("✊✌️✋ Pilihan Anda:")
    pil1, pil2, pil3 = st.columns(3)
    with pil1:
        batu = st.button("✊ **Batu**", key="batu", use_container_width=True, disabled=st.session_state.permainan_selesai)
    with pil2:
        gunting = st.button("✌️ **Gunting**", key="gunting", use_container_width=True, disabled=st.session_state.permainan_selesai)
    with pil3:
        kertas = st.button("✋ **Kertas**", key="kertas", use_container_width=True, disabled=st.session_state.permainan_selesai)
    
    # Logika permainan
    if batu or gunting or kertas:
        if not nama_pemain:
            st.warning("⚠️ Silakan masukkan nama Anda terlebih dahulu!")
        else:
            pilihan_pemain = 'Batu' if batu else 'Gunting' if gunting else 'Kertas'
            
            with st.spinner('Komputer sedang memilih...'):
                time.sleep(0.5)
            
            # AI komputer
            if tingkat_kesulitan == "Normal":
                pilihan_komputer = random.choice(['Batu', 'Gunting', 'Kertas'])
            elif tingkat_kesulitan == "Sulit":
                if st.session_state.riwayat and random.random() < 0.4:
                    pilihan_terakhir = st.session_state.riwayat[-1]['pemain']
                    pilihan_komputer = {'Batu': 'Kertas', 'Gunting': 'Batu', 'Kertas': 'Gunting'}[pilihan_terakhir]
                else:
                    pilihan_komputer = random.choice(['Batu', 'Gunting', 'Kertas'])
            else:  # Expert
                if len(st.session_state.riwayat) >= 2:
                    dua_terakhir = [x['pemain'] for x in st.session_state.riwayat[-2:]]
                    if dua_terakhir[0] == dua_terakhir[1]:
                        pilihan_komputer = {'Batu': 'Kertas', 'Gunting': 'Batu', 'Kertas': 'Gunting'}[dua_terakhir[0]]
                    else:
                        pilihan_komputer = random.choice(['Batu', 'Gunting', 'Kertas'])
                else:
                    pilihan_komputer = random.choice(['Batu', 'Gunting', 'Kertas'])
            
            # Tentukan pemenang
            if pilihan_pemain == pilihan_komputer:
                hasil = "Seri! 🤝"
                st.session_state.skor['seri'] += 1
            elif (pilihan_pemain == 'Batu' and pilihan_komputer == 'Gunting') or \
                 (pilihan_pemain == 'Gunting' and pilihan_komputer == 'Kertas') or \
                 (pilihan_pemain == 'Kertas' and pilihan_komputer == 'Batu'):
                hasil = f"{nama_pemain} Menang! 🎉" if nama_pemain else "Anda Menang! 🎉"
                st.session_state.skor['pemain'] += 1
                st.session_state.total_kemenangan += 1
            else:
                hasil = "Komputer Menang! 🤖"
                st.session_state.skor['komputer'] += 1
            
            # Simpan riwayat
            st.session_state.riwayat.append({
                'ronde': st.session_state.ronde,
                'pemain': pilihan_pemain,
                'komputer': pilihan_komputer,
                'hasil': hasil,
                'waktu': time.strftime("%Y-%m-%d %H:%M:%S")
            })
            
            st.session_state.total_permainan += 1
            st.session_state.ronde += 1
            
            # Tampilkan hasil
            st.success(f"**{hasil}**")
            
            # Tampilkan pilihan
            kol1, kol2 = st.columns(2)
            with kol1:
                st.subheader("Pilihan Anda:")
                st.markdown(f"<div style='text-align: center; font-size: 60px;'>" +
                           f"{'✊' if pilihan_pemain == 'Batu' else '✌️' if pilihan_pemain == 'Gunting' else '✋'}</div>", 
                           unsafe_allow_html=True)
            with kol2:
                st.subheader("Pilihan Komputer:")
                st.markdown(f"<div style='text-align: center; font-size: 60px;'>" +
                           f"{'✊' if pilihan_komputer == 'Batu' else '✌️' if pilihan_komputer == 'Gunting' else '✋'}</div>", 
                           unsafe_allow_html=True)
            
            # Cek jika permainan selesai
            if (mode_permainan == 'Best of 3' and max(st.session_state.skor['pemain'], st.session_state.skor['komputer']) >= 2) or \
               (mode_permainan == 'Best of 5' and max(st.session_state.skor['pemain'], st.session_state.skor['komputer']) >= 3):
                st.session_state.permainan_selesai = True
                pemenang = nama_pemain if st.session_state.skor['pemain'] > st.session_state.skor['komputer'] else "Komputer"
                st.balloons()
                st.success(f"🏆 **Permainan selesai!** {pemenang} memenangkan {mode_permainan}!")
                
                # Simpan hasil ke leaderboard
                if nama_pemain:
                    simpan_hasil(nama_pemain, mode_permainan, tingkat_kesulitan)

    # Tombol aksi
    st.markdown("---")
    st.subheader("🛠️ Aksi Permainan")
    aksi1, aksi2, aksi3, aksi4 = st.columns(4)
    
    with aksi1:
        if st.button("🔄 Main Lagi", 
                    key="ulangi",
                    use_container_width=True,
                    help="Mulai permainan baru dengan reset skor"):
            inisialisasi_permainan()
            st.rerun()
    
    with aksi2:
        if st.session_state.permainan_selesai and mode_permainan in ['Best of 3', 'Best of 5']:
            if st.button("🚀 Lanjutkan", 
                        key="lanjutkan",
                        use_container_width=True,
                        help="Lanjutkan dengan skor saat ini"):
                st.session_state.permainan_selesai = False
                st.rerun()
    
    with aksi3:
        if st.button("💾 Simpan & Lanjutkan", 
                    key="simpan",
                    use_container_width=True,
                    type="primary",
                    disabled=not nama_pemain,
                    help="Simpan hasil dan lanjutkan dengan pemain yang sama"):
            if nama_pemain:
                simpan_hasil(nama_pemain, mode_permainan, tingkat_kesulitan)
                st.success("Hasil permainan disimpan!")
                inisialisasi_permainan()
                st.rerun()
    
    with aksi4:
        if st.button("👤 Pemain Baru", 
                    key="pemain_baru",
                    use_container_width=True,
                    type="secondary",
                    disabled=not nama_pemain,
                    help="Simpan hasil dan mulai dengan pemain baru"):
            if nama_pemain:
                simpan_hasil(nama_pemain, mode_permainan, tingkat_kesulitan)
                if "nama_tersimpan" in st.session_state:
                    del st.session_state.nama_tersimpan
                st.success("Hasil permainan disimpan!")
                inisialisasi_permainan()
                st.rerun()

    # Riwayat permainan
    if st.session_state.riwayat:
        st.markdown("---")
        st.subheader("📋 Riwayat 5 Ronde Terakhir")
        riwayat_display = []
        for ronde in st.session_state.riwayat[-5:]:
            riwayat_display.append({
                "Ronde": ronde['ronde'],
                "Anda": ronde['pemain'],
                "Komputer": ronde['komputer'],
                "Hasil": ronde['hasil']
            })
        st.dataframe(riwayat_display, use_container_width=True, hide_index=True)

# =====================================
# BAGIAN STATISTIK
# =====================================
st.markdown("---")
st.subheader("📈 Statistik Permainan")

stat1, stat2, stat3 = st.columns(3)
with stat1:
    st.metric("Total Permainan", st.session_state.total_permainan)
with stat2:
    st.metric("Total Kemenangan", st.session_state.total_kemenangan)
with stat3:
    if st.session_state.total_permainan > 0:
        persen_menang = (st.session_state.total_kemenangan / st.session_state.total_permainan) * 100
        st.metric("Persentase Menang", f"{persen_menang:.1f}%")
    else:
        st.metric("Persentase Menang", "0%")

# =====================================
# BAGIAN LEADERBOARD
# =====================================
st.markdown("---")
st.subheader("🏆 Leaderboard")

if st.session_state.leaderboard:
    # Format data untuk ditampilkan
    leaderboard_display = []
    for record in st.session_state.leaderboard:
        leaderboard_display.append({
            "Pemain": record['nama'],
            "Mode": record['mode'],
            "Kesulitan": record['kesulitan'],
            "Menang": record['skor_pemain'],
            "Kalah": record['skor_komputer'],
            "Seri": record['total_seri'],
            "Total Ronde": record['total_ronde'],
            "Terakhir Diperbarui": record['terakhir_diperbarui']
        })
    
    # Urutkan berdasarkan jumlah kemenangan
    leaderboard_display.sort(key=lambda x: x['Menang'], reverse=True)
    
    st.dataframe(
        leaderboard_display,
        column_config={
            "Pemain": "Nama Pemain",
            "Mode": "Mode Permainan",
            "Kesulitan": "Tingkat Kesulitan",
            "Menang": st.column_config.NumberColumn("Total Menang"),
            "Kalah": st.column_config.NumberColumn("Total Kalah"),
            "Seri": st.column_config.NumberColumn("Total Seri"),
            "Total Ronde": st.column_config.NumberColumn("Jumlah Ronde"),
            "Terakhir Diperbarui": "Update Terakhir"
        },
        hide_index=True,
        use_container_width=True
    )
else:
    st.write("Belum ada data leaderboard")

# =====================================
# BAGIAN TIPS & STRATEGI
# =====================================
st.markdown("---")
with st.expander("💡 Tips & Strategi Bermain"):
    st.markdown("""
    ### 🎮 Cara Bermain:
    1. Pilih mode dan tingkat kesulitan
    2. Klik **Mulai Permainan Baru**
    3. Masukkan nama Anda
    4. Pilih tangan yang akan dimainkan
    
    ### 🧠 Strategi Menang:
    - **Level Normal**: Komputer acak
    - **Level Sulit**: Komputer 40% lebih mungkin melawan pilihan terakhir Anda
    - **Level Expert**: Komputer akan mendeteksi pola permainan Anda
    
    ### 💾 Penyimpanan Data:
    - Hasil permainan otomatis tersimpan di leaderboard
    - Data dikelompokkan berdasarkan pemain, mode, dan tingkat kesulitan
    - Statistik diupdate secara real-time
    """)