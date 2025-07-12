import streamlit as st
import pandas as pd
from datetime import datetime

def main():
    st.title("📊 Dashboard Game Center")
    
    # Ambil data dari session state (asumsi sudah ada)
    data_game = {
        "Game": ["Tebak Angka", "Hangman", "Gunting-Batu-Kertas"],
        "Total Permainan": [
            st.session_state.get("total_games", 0),
            st.session_state.get("hangman_total_permainan", 0),
            st.session_state.get("total_permainan", 0)
        ],
        "Total Kemenangan": [
            st.session_state.get("total_wins", 0),
            st.session_state.get("hangman_total_kemenangan", 0),
            st.session_state.get("total_kemenangan", 0)
        ],
        "Terakhir Dimainkan": [
            st.session_state.get("last_played_gtn", "-"),
            st.session_state.get("last_played_hm", "-"),
            st.session_state.get("last_played_rps", "-")
        ]
    }
    
    # Tampilkan metrik utama
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Game Dimainkan", sum(data_game["Total Permainan"]))
    with col2:
        st.metric("Total Kemenangan", sum(data_game["Total Kemenangan"]))
    with col3:
        win_rate = (sum(data_game["Total Kemenangan"]) / sum(data_game["Total Permainan"])) * 100 if sum(data_game["Total Permainan"]) > 0 else 0
        st.metric("Win Rate", f"{win_rate:.1f}%")
    
    st.markdown("---")
    
    # Tampilkan data game
    st.subheader("📈 Statistik per Game")
    df = pd.DataFrame(data_game)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Grafik performa
    st.subheader("📊 Grafik Performa")
    tab1, tab2 = st.tabs(["Total Permainan", "Win Rate"])
    
    with tab1:
        st.bar_chart(df.set_index("Game")["Total Permainan"])
    
    with tab2:
        df["Win Rate"] = (df["Total Kemenangan"] / df["Total Permainan"]) * 100
        st.bar_chart(df.set_index("Game")["Win Rate"])
    
    # Aktivitas terakhir
    st.markdown("---")
    st.subheader("⏱ Aktivitas Terakhir")
    
    # Asumsikan kita menyimpan riwayat aktivitas
    if "activity_log" not in st.session_state:
        st.session_state.activity_log = []
    
    if st.session_state.activity_log:
        st.table(pd.DataFrame(st.session_state.activity_log[-5:]))
    else:
        st.info("Belum ada aktivitas yang tercatat")

def log_activity(game, action):
    """Fungsi untuk mencatat aktivitas"""
    if "activity_log" not in st.session_state:
        st.session_state.activity_log = []
    
    st.session_state.activity_log.append({
        "Waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Game": game,
        "Aksi": action
    })