import streamlit as st

st.set_page_config(
    page_title="Multi-Game Dashboard",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS kustom
st.markdown("""
    <style>
        .main {
            padding: 2rem;
        }
        .sidebar .sidebar-content {
            background-color: #f8f9fa;
        }
        h1 {
            color: #2c3e50;
        }
        .stButton>button {
            border-radius: 8px;
        }
        .game-card {
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            background-color: #98A1BC;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            transition: transform 0.3s;
        }
        .game-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("Multi-Game Dashboard")
st.sidebar.markdown("---")
st.sidebar.info("Pilih game dari menu navigasi")

# Inisialisasi session state untuk leaderboard global
if 'global_leaderboard' not in st.session_state:
    st.session_state.global_leaderboard = {
        'Tebak Angka': [],
        'Gunting Batu Kertas': []
    }

# Konten utama
st.title("Selamat Datang di Multi-Game Dashboard!")
st.markdown("""
    Dashboard ini menyediakan berbagai game seru yang bisa Anda mainkan. 
    Pilih game dari menu sidebar atau dari card di bawah ini.
""")

# Game cards
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="game-card">
        <h2>🔢 Tebak Angka</h2>
        <p>Tebak angka yang dipilih komputer dengan bantuan hint!</p>
        <p><strong>Fitur:</strong></p>
        <ul>
            <li>5 level kesulitan</li>
            <li>10 jenis hint berbeda</li>
            <li>Leaderboard</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="game-card">
        <h2>✊ Gunting Batu Kertas</h2>
        <p>Mainkan game klasik dengan AI yang menantang!</p>
        <p><strong>Fitur:</strong></p>
        <ul>
            <li>3 mode permainan</li>
            <li>3 tingkat kesulitan AI</li>
            <li>Statistik lengkap</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.subheader("📊 Statistik Global")
st.write("Total permainan yang dimainkan di semua game:")

if 'total_global_games' not in st.session_state:
    st.session_state.total_global_games = 0
if 'total_global_wins' not in st.session_state:
    st.session_state.total_global_wins = 0

stat1, stat2, stat3 = st.columns(3)
with stat1:
    st.metric("Total Permainan", st.session_state.total_global_games)
with stat2:
    st.metric("Total Kemenangan", st.session_state.total_global_wins)
with stat3:
    if st.session_state.total_global_games > 0:
        win_rate = (st.session_state.total_global_wins / st.session_state.total_global_games) * 100
        st.metric("Persentase Menang", f"{win_rate:.1f}%")
    else:
        st.metric("Persentase Menang", "0%")