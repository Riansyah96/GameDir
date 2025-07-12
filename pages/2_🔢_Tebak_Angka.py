from games.GTN import *

# Update leaderboard global
if 'leaderboard' in st.session_state and st.session_state.leaderboard:
    st.session_state.global_leaderboard['Tebak Angka'] = st.session_state.leaderboard
    st.session_state.total_global_games = st.session_state.total_games
    st.session_state.total_global_wins = st.session_state.total_wins

# Tambahkan judul khusus halaman
st.title("🔢 Game Tebak Angka")
st.markdown("""
    **Petunjuk:** 
    - Pilih level kesulitan dan jumlah hint
    - Klik "Mulai Game Baru" untuk memulai
    - Masukkan nama Anda dan mulai menebak!
""")