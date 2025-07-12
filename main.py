import streamlit as st
from GTN import main as gtn_main
from HM import main as hm_main
from RPS import main as rps_main
from dashboard import main as dashboard_main
from leaderboard import main as leaderboard_main

# Page configuration
st.set_page_config(
    page_title="Game Center",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
    <style>
        .sidebar .sidebar-content {
            background-image: linear-gradient(to bottom, #2c3e50, #4ca1af);
            color: white;
        }
        .sidebar .sidebar-content .block-container {
            padding-top: 2rem;
        }
        .sidebar .sidebar-content .stRadio > div {
            flex-direction: column;
            gap: 0.5rem;
        }
        .sidebar .sidebar-content .stRadio > label {
            font-size: 1rem;
            color: white !important;
        }
        .sidebar .sidebar-content .stRadio [role="radiogroup"] {
            gap: 0.5rem;
        }
        .sidebar .sidebar-content .stRadio [data-baseweb="radio"] {
            margin-bottom: 0.5rem;
        }
        .sidebar .sidebar-content .stRadio [data-baseweb="radio"] label {
            cursor: pointer;
            padding: 0.75rem 1rem;
            border-radius: 10px;
            transition: all 0.3s ease;
            background-color: rgba(255,255,255,0.1);
            border: 1px solid rgba(255,255,255,0.2);
        }
        .sidebar .sidebar-content .stRadio [data-baseweb="radio"] label:hover {
            background-color: rgba(255,255,255,0.2);
            transform: translateX(5px);
        }
        .sidebar .sidebar-content .stRadio [data-baseweb="radio"] input:checked + label {
            background-color: #f39c12;
            color: white !important;
            font-weight: bold;
            border: 1px solid #f39c12;
            box-shadow: 0 0 10px rgba(243, 156, 18, 0.5);
        }
        .sidebar-title {
            font-size: 1.8rem !important;
            text-align: center;
            margin-bottom: 2rem;
            color: white;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
        }
        .welcome-container {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            border-radius: 15px;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        .game-card {
            background: white;
            border-radius: 10px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }
        .game-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        }
        .dev-info {
        background: linear-gradient(135deg, #2c3e50 0%, #4ca1af 100%);
        color: white;
        border-radius: 15px;
        padding: 2rem;
        margin-top: 2rem;
        text-align: center;
        }
        .dev-info h2 {
            margin-bottom: 1rem;
        }
        .dev-description {
            margin-bottom: 1.5rem;
            font-size: 1.1rem;
        }
        .dev-info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 1rem;
            max-width: 800px;
            margin: 0 auto;
        }
        .dev-label {
            color: #f39c12;
            font-size: 0.9rem;
            margin-bottom: 0.3rem;
        }
        .dev-value {
            font-size: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar navigation with emoji icons
with st.sidebar:
    st.markdown('<p class="sidebar-title">🎮 GAME CENTER</p>', unsafe_allow_html=True)
    
    # Main navigation options
    main_options = ["📊 Dashboard", "🎮 Games", "🏆 Leaderboard"]
    main_choice = st.radio(
        "MENU UTAMA",
        main_options,
        index=0,
        key="main_nav"
    )
    
    # Sub-menu for Games
    if main_choice == "🎮 Games":
        app_mode = st.radio(
            "PILIH PERMAINAN",
            [
                "🔢 Tebak Angka", 
                "💬 Tebak Kata", 
                "✂️ Gunting-Batu-Kertas"
            ],
            index=0,
            key="game_nav"
        )
    else:
        app_mode = main_choice

# Show welcome and info only on Dashboard
if "Dashboard" in app_mode:
    # Welcome section
    with st.container():
        st.markdown("""
        <div class="welcome-container">
            <h1 style="color: #2c3e50; text-align: center;">🎉 SELAMAT DATANG DI GAME CENTER! 🎉</h1>
            <p style="text-align: center; font-size: 1.1rem;">
                Temukan berbagai permainan seru yang siap menghibur Anda! Pilih game favorit Anda dari menu sidebar dan mulai bermain!
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="game-card">
            <h3>🔢 Tebak Angka</h3>
            <p>Uji kemampuan menebak Anda dalam permainan tebak angka! Komputer akan memilih angka acak antara 1-100 dan Anda harus menebaknya dalam jumlah tebakan sesedikit mungkin.</p>
            <p>🎯 <strong>Tingkat Kesulitan:</strong> Mudah</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="game-card">
            <h3>✂️ Gunting-Batu-Kertas</h3>
            <p>Permainan klasik melawan komputer! Pilih antara gunting, batu, atau kertas dan lihat siapa yang menang dalam pertarungan seru ini.</p>
            <p>🎯 <strong>Tingkat Kesulitan:</strong> Sedang</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="game-card">
            <h3>💬 Tebak Kata</h3>
            <p>Tebak kata misteri sebelum kesempatan Anda habis! Setiap kesalahan akan menggambar bagian tubuh manusia di tiang gantungan.</p>
            <p>🎯 <strong>Tingkat Kesulitan:</strong> Sulit</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="game-card">
            <h3>🏆 Leaderboard</h3>
            <p>Lihat peringkat pemain terbaik di semua game! Siapa yang akan menjadi juara dengan skor tertinggi?</p>
            <p>🏅 <strong>Fitur:</strong> Rekor skor tertinggi</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Developer information
    st.markdown("""
    <div class="dev-info">
        <h2>👨‍💻 TENTANG PENGEMBANG</h2>
        <p class="dev-description">
            Aplikasi Game Center dikembangkan untuk memberikan pengalaman bermain game yang menyenangkan dan interaktif.
        </p>
        <p class="dev-label">VERSI APLIKASI</p>
        <p class="dev-value">1.0.0</p>
        <p class="dev-label">TEKNOLOGI</p>
        <p class="dev-value">Python<br>Streamlit</p>
        <p class="dev-label">KONTAK</p>
        <p class="dev-value">gamecenter@example.com</p>
        <p class="dev-label">PENGEMBANG</p>
        <p class="dev-value">Tim Game Center</p>
    </div>
    """, unsafe_allow_html=True)

# Routing aplikasi
if "Dashboard" in app_mode:
    dashboard_main()
elif "Tebak Angka" in app_mode:
    gtn_main()
elif "Tebak Kata" in app_mode:
    hm_main()
elif "Gunting-Batu-Kertas" in app_mode:
    rps_main()
elif "Leaderboard" in app_mode:
    leaderboard_main()