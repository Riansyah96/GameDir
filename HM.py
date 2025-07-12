import random
import time
import streamlit as st
from streamlit.components.v1 import html

def main():
    def init_game():
        """Inisialisasi state permainan Hangman"""
        st.session_state.hangman = {
            'kata': '',
            'kategori': '',
            'tebakan': [],
            'huruf_tebakan': [],
            'nyawa': 6,
            'game_over': False,
            'menang': False,
            'riwayat': [],
            'ronde': 1,
            'skor': {'menang': 0, 'kalah': 0}
        }

    def pilih_kata(kategori):
        """Memilih kata acak berdasarkan kategori"""
        kata_per_kategori = {
            'Hewan': [
                'gajah', 'harimau', 'kucing', 'anjing', 'burung', 'ular', 'kuda', 'zebra',
                'singa', 'jerapah', 'kanguru', 'koala', 'panda', 'beruang', 'rubah', 'serigala',
                'kancil', 'kelinci', 'tupai', 'kelelawar', 'lumba-lumba', 'paus', 'hiu',
                'buaya', 'kura-kura', 'komodo', 'badak', 'gurita', 'ubur-ubur', 'kupu-kupu',
                'laba-laba', 'capung', 'belalang', 'nyamuk', 'kumbang', 'kadal', 'tokek'
            ],
            'Buah': [
                'apel', 'jeruk', 'mangga', 'pisang', 'anggur', 'semangka', 'melon', 'nanas',
                'pepaya', 'alpukat', 'durian', 'rambutan', 'manggis', 'jambu', 'salak', 'sirsak',
                'markisa', 'kiwi', 'leci', 'kelengkeng', 'stroberi', 'blueberry', 'raspberry',
                'blackberry', 'cherry', 'persik', 'plum', 'aprikot', 'kurma', 'delima',
                'sukun', 'nangka', 'cempedak', 'duku', 'langsat', 'sawo', 'kesemek'
            ],
            'Negara': [
                'indonesia', 'jepang', 'amerika', 'brasil', 'kanada', 'australia', 'mesir', 'jerman',
                'inggris', 'perancis', 'italia', 'spanyol', 'portugal', 'belanda', 'rusia', 'china',
                'india', 'korea', 'thailand', 'malaysia', 'singapura', 'vietnam', 'filipina',
                'argentina', 'chili', 'meksiko', 'kolombia', 'venezuela', 'afrikaselatan', 'nigeria',
                'kenya', 'maroko', 'arabsaudi', 'turki', 'yunani', 'swedia', 'norwegia'
            ],
            'Olahraga': [
                'sepakbola', 'basket', 'tenis', 'renang', 'voli', 'badminton', 'golf', 'atletik',
                'bulutangkis', 'bersepeda', 'maraton', 'triathlon', 'gymnastik', 'senam', 'angkatbesi',
                'tinju', 'karate', 'judo', 'taekwondo', 'silat', 'panahan', 'menembak',
                'dayung', 'kayak', 'selancar', 'ski', 'seluncures', 'hoki', 'rugby',
                'baseball', 'softball', 'kriket', 'poloair', 'loncatindah', 'squash', 'tenismeja'
            ],
            'Profesi': [
                'dokter', 'guru', 'polisi', 'tentara', 'perawat', 'arsitek', 'insinyur', 'programmer',
                'akuntan', 'pengacara', 'hakim', 'jaksa', 'wartawan', 'penyiar', 'koki', 'pelayan',
                'supir', 'pilot', 'pramugari', 'nelayan', 'petani', 'peternak', 'penjahit',
                'tukangkayu', 'tukangbatu', 'tukanglas', 'tukanglistrik', 'penataRambut', 'makeupartist',
                'fotografer', 'desainer', 'musisi', 'penyanyi', 'aktor', 'penari', 'pelukis'
            ],
            'Kendaraan': [
                'mobil', 'motor', 'sepeda', 'bus', 'truk', 'kereta', 'pesawat', 'helikopter',
                'kapal', 'perahu', 'yacht', 'jetski', 'becak', 'bajaj', 'angkot', 'tram',
                'mobilbalap', 'mobilsport', 'suv', 'mpv', 'ambulans', 'pemadam', 'tank',
                'buldoser', 'eskavator', 'traktor', 'forklift', 'skuter', 'hoverboard', 'segway'
            ],
            'Makanan': [
                'nasi', 'mie', 'ayam', 'sapi', 'ikan', 'tempe', 'tahu', 'sosis',
                'bakso', 'sate', 'rendang', 'gudeg', 'soto', 'rawon', 'sop', 'gado-gado',
                'ketoprak', 'pecel', 'lontong', 'ketupat', 'lemper', 'risoles', 'pastel',
                'martabak', 'pizza', 'burger', 'hotdog', 'spaghetti', 'sushi', 'tempura'
            ],
            'Buah Tropis': [
                'manggis', 'durian', 'rambutan', 'salak', 'nangka', 'cempedak', 'duku', 'langsat',
                'sawo', 'kesemek', 'sukun', 'jambuair', 'jambubiji', 'belimbing', 'sirsak', 'markisa',
                'kelengkeng', 'leci', 'matoa', 'gandaria', 'kedondong', 'bacang', 'kemang', 'jamblang'
            ],
            'Elektronik': [
                'smartphone', 'laptop', 'tablet', 'televisi', 'radio', 'kulkas', 'mesincuci', 'komputer',
                'printer', 'scanner', 'kamera', 'drone', 'konsol', 'playstation', 'xbox', 'nintendo',
                'headphone', 'speaker', 'microphone', 'amplifier', 'proyektor', 'smartwatch', 'fitbit',
                'router', 'modem', 'harddisk', 'flashdisk', 'ssd', 'processor', 'motherboard'
            ],
            'Alat Musik': [
                'gitar', 'piano', 'drum', 'biola', 'suling', 'terompet', 'saxophone', 'clarinet',
                'harmonika', 'akordeon', 'harpa', 'ukulele', 'banjo', 'mandolin', 'cello', 'kontrabas',
                'flute', 'oboe', 'tuba', 'trombon', 'timpani', 'xylophone', 'marimba', 'gamelan',
                'angklung', 'kolintang', 'sasando', 'rebana', 'kendang', 'tamborin'
            ]
        }
        
        return random.choice(kata_per_kategori[kategori]), kategori

    def update_tebakan(huruf):
        """Memperbarui tebakan pemain"""
        if huruf.lower() in st.session_state.hangman['huruf_tebakan']:
            return False
        
        st.session_state.hangman['huruf_tebakan'].append(huruf.lower())
        
        if huruf.lower() not in st.session_state.hangman['kata']:
            st.session_state.hangman['nyawa'] -= 1
            return False
        return True

    def cek_game_over():
        """Memeriksa apakah permainan selesai"""
        kata = st.session_state.hangman['kata']
        tebakan = st.session_state.hangman['huruf_tebakan']
        
        # Cek jika semua huruf sudah ditebak
        menang = all(huruf in tebakan for huruf in kata)
        
        if menang:
            st.session_state.hangman['menang'] = True
            st.session_state.hangman['game_over'] = True
            st.session_state.hangman['skor']['menang'] += 1
            return True
        
        # Cek jika nyawa habis
        if st.session_state.hangman['nyawa'] <= 0:
            st.session_state.hangman['menang'] = False
            st.session_state.hangman['game_over'] = True
            st.session_state.hangman['skor']['kalah'] += 1
            return True
        
        return False

    def simpan_hasil(nama, kategori):
        """Menyimpan hasil permainan ke leaderboard"""
        ditemukan = False
        for record in st.session_state.hangman_leaderboard:
            if record['nama'] == nama and record['kategori'] == kategori:
                record['menang'] += 1 if st.session_state.hangman['menang'] else 0
                record['kalah'] += 0 if st.session_state.hangman['menang'] else 1
                record['total_ronde'] += 1
                record['terakhir_diperbarui'] = time.strftime("%Y-%m-%d %H:%M:%S")
                ditemukan = True
                break
        
        if not ditemukan:
            st.session_state.hangman_leaderboard.append({
                'nama': nama,
                'kategori': kategori,
                'menang': 1 if st.session_state.hangman['menang'] else 0,
                'kalah': 0 if st.session_state.hangman['menang'] else 1,
                'total_ronde': 1,
                'terakhir_diperbarui': time.strftime("%Y-%m-%d %H:%M:%S"),
                'waktu_dibuat': time.strftime("%Y-%m-%d %H:%M:%S")
            })
        
        st.session_state.hangman_nama_tersimpan = nama

    # Inisialisasi data penyimpanan
    if 'hangman_leaderboard' not in st.session_state:
        st.session_state.hangman_leaderboard = []
    if 'hangman_total_permainan' not in st.session_state:
        st.session_state.hangman_total_permainan = 0
    if 'hangman_total_kemenangan' not in st.session_state:
        st.session_state.hangman_total_kemenangan = 0
    if 'hangman_nama_tersimpan' not in st.session_state:
        st.session_state.hangman_nama_tersimpan = ""

    # =====================================
    # BAGIAN PENGATURAN
    # =====================================
    st.title("Tebak Kata (Hangman)")
    with st.expander("⚙️ Pengaturan Game", expanded=True):
        kolom_set1, kolom_set2 = st.columns(2)
        
        with kolom_set1:
            kategori_kata = st.selectbox(
                "Kategori Kata:",
                ["Hewan", "Buah", "Negara", "Olahraga","Profesi", "Kendaraan", "Makanan", "Buah Tropis", "Elektronik", "Alat Musik", "Hewan", "Buah", "Negara", "Olahraga","Profesi",],
                key="hangman_kategori"
            )
        
        with kolom_set2:
            tingkat_kesulitan = st.selectbox(
                "Tingkat Kesulitan:",
                ["Mudah (6 nyawa)", "Sedang (5 nyawa)", "Sulit (4 nyawa)"],
                key="hangman_kesulitan"
            )
        
        if st.button("🚀 Mulai Permainan Baru", 
                    key="hangman_mulai", 
                    use_container_width=True):
            init_game()
            kata, kategori = pilih_kata(kategori_kata)
            st.session_state.hangman['kata'] = kata
            st.session_state.hangman['kategori'] = kategori
            
            # Set nyawa berdasarkan tingkat kesulitan
            if tingkat_kesulitan == "Mudah (6 nyawa)":
                st.session_state.hangman['nyawa'] = 6
            elif tingkat_kesulitan == "Sedang (5 nyawa)":
                st.session_state.hangman['nyawa'] = 5
            else:
                st.session_state.hangman['nyawa'] = 4
                
            st.success(f"Permainan dimulai! Kategori: {kategori_kata}")
            st.rerun()

    st.markdown("---")

    # =====================================
    # BAGIAN UTAMA PERMAINAN
    # =====================================
    if 'hangman' in st.session_state and st.session_state.hangman['kata']:
        nama_pemain = st.text_input(
            "Masukkan nama Anda:", 
            key="hangman_input_nama",
            max_chars=20,
            value=st.session_state.hangman_nama_tersimpan
        )
        
        st.info(f"""
        🎮 **Kategori:** {st.session_state.hangman['kategori']}  
        🏆 **Kesulitan:** {tingkat_kesulitan}  
        ❤️ **Nyawa:** {st.session_state.hangman['nyawa']}
        🔢 **Ronde:** {st.session_state.hangman['ronde']}
        """)
        
        # Tampilan skor
        st.subheader("📊 Skor Permainan")
        skor1, skor2 = st.columns(2)
        with skor1:
            st.markdown("<div style='text-align: center;'><h3>Menang</h3><h1 style='color: #4CAF50;'>" + 
                    f"{st.session_state.hangman['skor']['menang']}</h1></div>", unsafe_allow_html=True)
        with skor2:
            st.markdown("<div style='text-align: center;'><h3>Kalah</h3><h1 style='color: #F44336;'>" + 
                    f"{st.session_state.hangman['skor']['kalah']}</h1></div>", unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Tampilan kata yang ditebak
        kata_display = []
        for huruf in st.session_state.hangman['kata']:
            if huruf in st.session_state.hangman['huruf_tebakan']:
                kata_display.append(huruf.upper())
            else:
                kata_display.append("_")
        
        st.markdown(f"<div style='text-align: center; font-size: 36px; letter-spacing: 10px; margin: 20px 0;'>" +
                f"{' '.join(kata_display)}</div>", unsafe_allow_html=True)
        
        # Tampilan hangman (visual)
        hangman_stages = [
            """
            _____
            |     |
            |
            |
            |
            |
            __|__
            """,
            """
            _____
            |     |
            |     O
            |
            |
            |
            __|__
            """,
            """
            _____
            |     |
            |     O
            |     |
            |
            |
            __|__
            """,
            """
            _____
            |     |
            |     O
            |    /|
            |
            |
            __|__
            """,
            """
            _____
            |     |
            |     O
            |    /|\\
            |
            |
            __|__
            """,
            """
            _____
            |     |
            |     O
            |    /|\\
            |    /
            |
            __|__
            """,
            """
            _____
            |     |
            |     O
            |    /|\\
            |    / \\
            |
            __|__
            """
        ]
        
        nyawa_tersisa = st.session_state.hangman['nyawa']
        max_nyawa = 6 if tingkat_kesulitan == "Mudah (6 nyawa)" else 5 if tingkat_kesulitan == "Sedang (5 nyawa)" else 4
        stage_index = min(6, (max_nyawa - nyawa_tersisa))
        
        st.code(hangman_stages[stage_index], language="text")
        
        # Pilihan huruf
        st.subheader("🔤 Tebak Huruf")
        abjad = 'abcdefghijklmnopqrstuvwxyz'
        cols_per_row = 7
        abjad_rows = [abjad[i:i+cols_per_row] for i in range(0, len(abjad), cols_per_row)]
        
        for row in abjad_rows:
            cols = st.columns(cols_per_row)
            for i, huruf in enumerate(row):
                with cols[i]:
                    disabled = (
                        st.session_state.hangman['game_over'] or 
                        huruf in st.session_state.hangman['huruf_tebakan']
                    )
                    if st.button(
                        huruf.upper(),
                        key=f"hangman_huruf_{huruf}",
                        disabled=disabled,
                        use_container_width=True
                    ):
                        st.session_state.hangman_total_permainan += 1
                        if update_tebakan(huruf):
                            if cek_game_over():
                                st.session_state.hangman_total_kemenangan += 1
                                st.balloons()
                        else:
                            cek_game_over()
                        st.rerun()
        
        # Tampilkan huruf yang sudah ditebak
        if st.session_state.hangman['huruf_tebakan']:
            st.write("Huruf yang sudah ditebak:", ", ".join(sorted(st.session_state.hangman['huruf_tebakan'])))
        
        # Tampilkan hasil jika game over
        if st.session_state.hangman['game_over']:
            if st.session_state.hangman['menang']:
                st.success(f"🎉 Selamat! Anda menebak kata: {st.session_state.hangman['kata'].upper()}")
            else:
                st.error(f"💀 Game Over! Kata yang benar: {st.session_state.hangman['kata'].upper()}")
            
            # Simpan riwayat
            st.session_state.hangman['riwayat'].append({
                'ronde': st.session_state.hangman['ronde'],
                'kata': st.session_state.hangman['kata'],
                'hasil': 'Menang' if st.session_state.hangman['menang'] else 'Kalah',
                'waktu': time.strftime("%Y-%m-%d %H:%M:%S")
            })
        
        # Tombol aksi
        st.markdown("---")
        st.subheader("🛠️ Aksi Permainan")
        aksi1, aksi2, aksi3, aksi4 = st.columns(4)
        
        with aksi1:
            if st.button("🔄 Main Lagi", 
                        key="hangman_ulangi",
                        use_container_width=True,
                        help="Mulai permainan baru dengan kata acak"):
                kata, kategori = pilih_kata(kategori_kata)
                st.session_state.hangman['kata'] = kata
                st.session_state.hangman['kategori'] = kategori
                st.session_state.hangman['tebakan'] = []
                st.session_state.hangman['huruf_tebakan'] = []
                st.session_state.hangman['nyawa'] = max_nyawa
                st.session_state.hangman['game_over'] = False
                st.session_state.hangman['menang'] = False
                st.session_state.hangman['ronde'] += 1
                st.rerun()
        
        with aksi2:
            if st.session_state.hangman['game_over']:
                if st.button("🚀 Kategori Baru", 
                            key="hangman_kategori_baru",
                            use_container_width=True,
                            help="Mulai dengan kategori yang berbeda"):
                    init_game()
                    st.rerun()
        
        with aksi3:
            if st.session_state.hangman['game_over'] and nama_pemain:
                if st.button("💾 Simpan & Lanjutkan", 
                            key="hangman_simpan",
                            use_container_width=True,
                            type="primary",
                            help="Simpan hasil dan lanjutkan dengan pemain yang sama"):
                    simpan_hasil(nama_pemain, st.session_state.hangman['kategori'])
                    st.success("Hasil permainan disimpan!")
                    init_game()
                    st.rerun()
        
        with aksi4:
            if st.session_state.hangman['game_over'] and nama_pemain:
                if st.button("👤 Pemain Baru", 
                            key="hangman_pemain_baru",
                            use_container_width=True,
                            type="secondary",
                            help="Simpan hasil dan mulai dengan pemain baru"):
                    simpan_hasil(nama_pemain, st.session_state.hangman['kategori'])
                    if "hangman_nama_tersimpan" in st.session_state:
                        del st.session_state.hangman_nama_tersimpan
                    st.success("Hasil permainan disimpan!")
                    init_game()
                    st.rerun()

        # Riwayat permainan
        if st.session_state.hangman['riwayat']:
            st.markdown("---")
            st.subheader("📋 Riwayat 5 Ronde Terakhir")
            riwayat_display = []
            for ronde in st.session_state.hangman['riwayat'][-5:]:
                riwayat_display.append({
                    "Ronde": ronde['ronde'],
                    "Kata": ronde['kata'].upper(),
                    "Hasil": ronde['hasil'],
                    "Waktu": ronde['waktu']
                })
            st.dataframe(riwayat_display, use_container_width=True, hide_index=True)

    # =====================================
    # BAGIAN STATISTIK
    # =====================================
    st.markdown("---")
    st.subheader("📈 Statistik Permainan")

    stat1, stat2, stat3 = st.columns(3)
    with stat1:
        st.metric("Total Permainan", st.session_state.hangman_total_permainan)
    with stat2:
        st.metric("Total Kemenangan", st.session_state.hangman_total_kemenangan)
    with stat3:
        if st.session_state.hangman_total_permainan > 0:
            persen_menang = (st.session_state.hangman_total_kemenangan / st.session_state.hangman_total_permainan) * 100
            st.metric("Persentase Menang", f"{persen_menang:.1f}%")
        else:
            st.metric("Persentase Menang", "0%")

    # =====================================
    # BAGIAN LEADERBOARD
    # =====================================
    st.markdown("---")
    st.subheader("🏆 Leaderboard")

    if st.session_state.hangman_leaderboard:
        # Format data untuk ditampilkan
        leaderboard_display = []
        for record in st.session_state.hangman_leaderboard:
            leaderboard_display.append({
                "Pemain": record['nama'],
                "Kategori": record['kategori'],
                "Menang": record['menang'],
                "Kalah": record['kalah'],
                "Total Ronde": record['total_ronde'],
                "Terakhir Diperbarui": record['terakhir_diperbarui']
            })
        
        # Urutkan berdasarkan jumlah kemenangan
        leaderboard_display.sort(key=lambda x: x['Menang'], reverse=True)
        
        st.dataframe(
            leaderboard_display,
            column_config={
                "Pemain": "Nama Pemain",
                "Kategori": "Kategori Kata",
                "Menang": st.column_config.NumberColumn("Total Menang"),
                "Kalah": st.column_config.NumberColumn("Total Kalah"),
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
        1. Pilih kategori dan tingkat kesulitan
        2. Klik **Mulai Permainan Baru**
        3. Masukkan nama Anda
        4. Tebak huruf-huruf dalam kata tersembunyi
        
        ### 🧠 Strategi Menang:
        - Mulailah dengan huruf vokal (A, E, I, O, U)
        - Tebak huruf yang paling umum muncul dalam bahasa Indonesia (E, A, N, I)
        - Perhatikan pola kata berdasarkan kategori
        
        ### ❤️ Sistem Nyawa:
        - **Mudah**: 6 nyawa
        - **Sedang**: 5 nyawa
        - **Sulit**: 4 nyawa
        
        ### 💾 Penyimpanan Data:
        - Hasil permainan otomatis tersimpan di leaderboard
        - Data dikelompokkan berdasarkan pemain dan kategori
        - Statistik diupdate secara real-time
        """)