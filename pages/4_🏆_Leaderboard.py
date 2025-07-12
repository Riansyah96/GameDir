import streamlit as st

st.title("🏆 Leaderboard Global")

st.markdown("""
    Berikut adalah leaderboard untuk semua game yang tersedia.
    Pilih tab di bawah untuk melihat leaderboard masing-masing game.
""")

tab1, tab2 = st.tabs(["🔢 Tebak Angka", "✊ Gunting Batu Kertas"])

with tab1:
    st.subheader("Leaderboard Tebak Angka")
    if st.session_state.global_leaderboard['Tebak Angka']:
        # Format data untuk ditampilkan
        leaderboard_display = []
        for record in st.session_state.global_leaderboard['Tebak Angka'][:10]:  # Batasi 10 teratas
            leaderboard_display.append({
                "Pemain": record['name'],
                "Level": record['difficulty'].split(' ')[0],
                "Tebakan": record['guesses'],
                "Waktu": f"{record['time']:.1f}s",
                "Hint": record['hints'],
                "Tanggal": record['date']
            })
        
        st.dataframe(
            leaderboard_display,
            column_config={
                "Pemain": "Nama Pemain",
                "Level": "Tingkat Kesulitan",
                "Tebakan": "Jumlah Tebakan",
                "Waktu": "Waktu Penyelesaian",
                "Hint": "Hint Digunakan",
                "Tanggal": "Waktu Pencapaian"
            },
            hide_index=True,
            use_container_width=True
        )
    else:
        st.info("Belum ada data leaderboard untuk game Tebak Angka")

with tab2:
    st.subheader("Leaderboard Gunting Batu Kertas")
    if st.session_state.global_leaderboard['Gunting Batu Kertas']:
        # Format data untuk ditampilkan
        leaderboard_display = []
        for record in st.session_state.global_leaderboard['Gunting Batu Kertas']:
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
            leaderboard_display[:10],  # Batasi 10 teratas
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
        st.info("Belum ada data leaderboard untuk game Gunting Batu Kertas")

st.markdown("---")
st.subheader("📊 Statistik Global")
col1, col2 = st.columns(2)

with col1:
    st.metric("Total Permainan Tebak Angka", 
              len(st.session_state.global_leaderboard['Tebak Angka']))

with col2:
    st.metric("Total Permainan GBK", 
              len(st.session_state.global_leaderboard['Gunting Batu Kertas']))