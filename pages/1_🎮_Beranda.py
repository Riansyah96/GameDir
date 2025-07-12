import streamlit as st

st.title("Beranda Multi-Game")

st.markdown("""
    Selamat datang di dashboard game multipage! Berikut adalah daftar game yang tersedia:
    
    ### 🔢 Tebak Angka
    - Tebak angka yang dipilih komputer
    - Berbagai level kesulitan
    - Sistem hint yang membantu
    
    ### ✊ Gunting Batu Kertas
    - Game klasik dengan AI cerdas
    - Beberapa mode permainan
    - Tingkat kesulitan yang bisa disesuaikan
    
    ### 🏆 Leaderboard
    - Lihat peringkat pemain terbaik
    - Statistik permainan global
    
    Pilih game dari menu sidebar untuk mulai bermain!
""")

st.image("https://cdn.pixabay.com/photo/2016/11/14/03/06/game-1822680_1280.jpg", 
         caption="Selamat Bermain!", use_container_width=True)