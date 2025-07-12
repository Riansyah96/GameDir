from games.RPS import *

# Update leaderboard global
if 'leaderboard' in st.session_state and st.session_state.leaderboard:
    st.session_state.global_leaderboard['Gunting Batu Kertas'] = st.session_state.leaderboard
    st.session_state.total_global_games = st.session_state.total_permainan
    st.session_state.total_global_wins = st.session_state.total_kemenangan

# Tambahkan judul khusus halaman
st.title("✊ Gunting Batu Kertas")
st.markdown("""
    **Petunjuk:**
    - Pilih mode dan tingkat kesulitan
    - Klik "Mulai Permainan Baru" untuk memulai
    - Pilih tangan yang akan dimainkan
""")