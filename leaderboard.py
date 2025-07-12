import streamlit as st
import pandas as pd

def main():
    st.title("🏆 Leaderboard Terintegrasi")
    
    # Gabungkan semua leaderboard dari berbagai game
    all_leaderboards = []
    
    # Leaderboard dari Tebak Angka (GTN)
    if "leaderboard" in st.session_state and hasattr(st.session_state, 'total_games'):
        for record in st.session_state.leaderboard:
            all_leaderboards.append({
                "Game": "Tebak Angka",
                "Pemain": record.get("name", "Anonim"),
                "Level": record.get("difficulty", "").split(" ")[0] if "difficulty" in record else "-",
                "Skor": record.get("guesses", 0),
                "Waktu": f"{record.get('time', 0):.1f}s" if 'time' in record else "-",
                "Tanggal": record.get("date", "-"),
                "Kategori": "Jumlah Tebakan"
            })
    
    # Leaderboard dari Hangman (HM)
    if "hangman_leaderboard" in st.session_state:
        for record in st.session_state.hangman_leaderboard:
            all_leaderboards.append({
                "Game": "Hangman",
                "Pemain": record.get("nama", "Anonim"),
                "Level": record.get("kategori", "-"),
                "Skor": record.get("menang", 0),
                "Waktu": "-",
                "Tanggal": record.get("terakhir_diperbarui", "-"),
                "Kategori": "Kemenangan"
            })
    
    # Leaderboard dari Gunting-Batu-Kertas (RPS)
    if "leaderboard" in st.session_state and hasattr(st.session_state, 'total_permainan'):
        for record in st.session_state.leaderboard:
            # Periksa apakah record memiliki kunci yang sesuai dengan game RPS
            if 'mode' in record and 'kesulitan' in record:
                all_leaderboards.append({
                    "Game": "Gunting-Batu-Kertas",
                    "Pemain": record.get("nama", "Anonim"),
                    "Level": f"{record.get('mode', '-')} ({record.get('kesulitan', '-')})",
                    "Skor": record.get("skor_pemain", 0),
                    "Waktu": "-",
                    "Tanggal": record.get("terakhir_diperbarui", "-"),
                    "Kategori": "Kemenangan"
                })
    
    if not all_leaderboards:
        st.info("Belum ada data leaderboard")
        return
    
    # Konversi ke DataFrame
    df = pd.DataFrame(all_leaderboards)
    
    # Filter
    st.subheader("🔍 Filter Leaderboard")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        game_filter = st.multiselect(
            "Pilih Game",
            options=df["Game"].unique(),
            default=df["Game"].unique()
        )
    
    with col2:
        kategori_filter = st.multiselect(
            "Pilih Kategori",
            options=df["Kategori"].unique(),
            default=df["Kategori"].unique()
        )
    
    with col3:
        sort_by = st.selectbox(
            "Urutkan Berdasarkan",
            ["Skor (Tertinggi)", "Waktu (Tercepat)", "Tanggal (Terbaru)"]
        )
    
    # Terapkan filter
    filtered_df = df[
        (df["Game"].isin(game_filter)) &
        (df["Kategori"].isin(kategori_filter))
    ].copy()
    
    # Konversi waktu ke numeric untuk sorting
    if not filtered_df.empty:
        filtered_df['Waktu_Numeric'] = filtered_df['Waktu'].str.replace('s', '').replace('-', '0').astype(float)
    
    # Urutkan
    if not filtered_df.empty:
        if sort_by == "Skor (Tertinggi)":
            filtered_df = filtered_df.sort_values("Skor", ascending=False)
        elif sort_by == "Waktu (Tercepat)":
            filtered_df = filtered_df.sort_values("Waktu_Numeric", ascending=True)
        else:
            filtered_df = filtered_df.sort_values("Tanggal", ascending=False)
    
    # Tampilkan leaderboard
    st.subheader("📊 Hasil Filter")
    
    if not filtered_df.empty:
        # Hapus kolom bantuan
        display_df = filtered_df.drop(columns=['Waktu_Numeric'], errors='ignore')
        
        st.dataframe(
            display_df,
            column_config={
                "Game": "Nama Game",
                "Pemain": "Nama Pemain",
                "Level": "Tingkat Kesulitan",
                "Skor": st.column_config.NumberColumn("Skor"),
                "Waktu": "Waktu Penyelesaian",
                "Tanggal": "Tanggal Pencapaian",
                "Kategori": "Jenis Skor"
            },
            hide_index=True,
            use_container_width=True
        )
    else:
        st.warning("Tidak ada data yang sesuai dengan filter")