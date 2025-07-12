import random
import time
import streamlit as st

def main():
    def initialize_game():
        """Initialize game state with current settings"""
        ranges = {
            "Pemula (1-50)": (1, 50),
            "Normal (1-100)": (1, 100),
            "Sulit (1-200)": (1, 200),
            "Expert (1-500)": (1, 500),
            "Master (1-1000)": (1, 1000)
        }
        min_val, max_val = ranges[st.session_state.difficulty]
        
        st.session_state.target_number = random.randint(min_val, max_val)
        st.session_state.guesses = []
        st.session_state.game_over = False
        st.session_state.start_time = time.time()
        st.session_state.hints_used = 0
        st.session_state.available_hints = st.session_state.max_hints_setting
        st.session_state.current_range = (min_val, max_val)

    def generate_hint(target, current_range, guesses):
        """Generate various types of hints"""
        hint_types = [
            "range", "even_odd", "multiple", "prime", 
            "digit_sum", "divisors", "distance", 
            "temperature", "math_clue", "binary"
        ]
        hint_type = random.choice(hint_types)
        
        if hint_type == "range":
            lower = max(current_range[0], target - random.randint(5,15))
            upper = min(current_range[1], target + random.randint(5,15))
            return f"🔍 **Range Hint:** Angka antara {lower} dan {upper}"
        
        elif hint_type == "even_odd":
            parity = "genap" if target % 2 == 0 else "ganjil"
            return f"🔍 **Paritas Hint:** Angka adalah bilangan {parity}"
        
        elif hint_type == "multiple":
            multiples = [i for i in range(2, 11) if target % i == 0]
            if multiples:
                return f"🔍 **Kelipatan Hint:** Angka bisa dibagi oleh {random.choice(multiples)}"
            else:
                return f"🔍 **Kelipatan Hint:** Angka tidak bisa dibagi oleh angka 2-10"
        
        elif hint_type == "prime":
            is_prime = all(target % i != 0 for i in range(2, int(target**0.5) + 1))
            return f"🔍 **Prima Hint:** Angka {'adalah' if is_prime else 'bukan'} bilangan prima"
        
        elif hint_type == "digit_sum":
            digit_sum = sum(int(d) for d in str(target))
            return f"🔍 **Jumlah Digit Hint:** Jumlah semua digit angka adalah {digit_sum}"
        
        elif hint_type == "divisors":
            divisors = [i for i in range(2, target) if target % i == 0]
            if divisors:
                return f"🔍 **Pembagi Hint:** Angka memiliki pembagi lain selain 1 dan dirinya sendiri (total {len(divisors)} pembagi)"
            else:
                return "🔍 **Pembagi Hint:** Angka hanya bisa dibagi oleh 1 dan dirinya sendiri"
        
        elif hint_type == "distance":
            if guesses:
                last_guess = guesses[-1]
                distance = abs(target - last_guess)
                direction = "lebih tinggi" if target > last_guess else "lebih rendah"
                return f"🔍 **Jarak Hint:** Target {direction} dari tebakan terakhir Anda ({last_guess}) dengan jarak {distance}"
            else:
                return generate_hint(target, current_range, guesses)  # Fallback to another hint
        
        elif hint_type == "temperature":
            if guesses:
                last_diff = abs(target - guesses[-1])
                max_diff = current_range[1] - current_range[0]
                ratio = last_diff / max_diff
                
                if ratio < 0.1:
                    return "🔥 **Suhu Hint:** Anda sangat dekat! Hampir menyentuh!"
                elif ratio < 0.3:
                    return "🌡️ **Suhu Hint:** Anda cukup dekat! Terasa hangat!"
                elif ratio < 0.6:
                    return "❄️ **Suhu Hint:** Masih cukup jauh, terasa dingin"
                else:
                    return "🧊 **Suhu Hint:** Masih sangat jauh! Beku!"
            else:
                return generate_hint(target, current_range, guesses)  # Fallback to another hint
        
        elif hint_type == "math_clue":
            operations = [
                f"angka ini ditambah {random.randint(5,20)} adalah {target + random.randint(5,20)}",
                f"angka ini dikali 2 adalah {target * 2}",
                f"angka ini dikurangi {random.randint(1,10)} adalah {target - random.randint(1,10)}",
                f"angka ini dibagi 2 (dibulatkan) adalah {round(target / 2)}"
            ]
            return f"🔍 **Petunjuk Matematika:** {random.choice(operations)}"
        
        elif hint_type == "binary":
            binary = bin(target)[2:]
            return f"🔍 **Binary Hint:** Angka dalam bentuk biner adalah {binary}"

    # Inisialisasi data
    if 'leaderboard' not in st.session_state:
        st.session_state.leaderboard = []
    if 'total_games' not in st.session_state:
        st.session_state.total_games = 0
    if 'total_wins' not in st.session_state:
        st.session_state.total_wins = 0

    # =====================================
    # BAGIAN PENGATURAN
    # =====================================
    st.title("🎮 Ultimate Number Guessing Challenge")
    with st.expander("⚙️ Pengaturan Game", expanded=True):
        col_set1, col_set2 = st.columns(2)
        
        with col_set1:
            difficulty = st.selectbox(
                "Level Kesulitan:",
                [
                    "Pemula (1-50)", 
                    "Normal (1-100)", 
                    "Sulit (1-200)", 
                    "Expert (1-500)",
                    "Master (1-1000)"
                ],
                key="difficulty"
            )
        
        with col_set2:
            max_hints = st.slider(
                "Maksimal Hint per Game:", 
                min_value=1, max_value=5, 
                value=3, key="max_hints_setting"
            )
        
        if st.button("🚀 Mulai Game Baru", 
                    key="start_game", 
                    use_container_width=True):
            initialize_game()
            st.success(f"Game dimulai! Level: {difficulty} | Maks Hint: {max_hints}")
            st.rerun()

    st.markdown("---")

    # =====================================
    # BAGIAN UTAMA PERMAINAN
    # =====================================
    if 'target_number' in st.session_state:
        player_name = st.text_input(
            "Masukkan nama Anda:", 
            key="player_name",
            max_chars=20,
            value=st.session_state.get("saved_name", "")
        )
        
        # Info game
        st.info(f"""
        🎮 **Level:** {difficulty.split(' ')[0]}  
        🔢 **Range:** {st.session_state.current_range[0]}-{st.session_state.current_range[1]}  
        💡 **Hint tersedia:** {st.session_state.available_hints - st.session_state.hints_used}/{st.session_state.available_hints}
        """)
        
        # Tampilan game status
        st.subheader("📊 Status Game")
        stat1, stat2, stat3 = st.columns(3)
        with stat1:
            st.markdown("<div style='text-align: center;'><h3>Tebakan</h3><h1 style='color: #4CAF50;'>" + 
                    f"{len(st.session_state.guesses)}</h1></div>", unsafe_allow_html=True)
        with stat2:
            time_spent = time.time() - st.session_state.start_time
            st.markdown("<div style='text-align: center;'><h3>Waktu</h3><h1 style='color: #2196F3;'>" + 
                    f"{time_spent:.1f}s</h1></div>", unsafe_allow_html=True)
        with stat3:
            st.markdown("<div style='text-align: center;'><h3>Hint Digunakan</h3><h1 style='color: #FF9800;'>" + 
                    f"{st.session_state.hints_used}</h1></div>", unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Input tebakan
        st.subheader("🔢 Masukkan Tebakan")
        guess = st.number_input(
            "Angka tebakan Anda:", 
            min_value=st.session_state.current_range[0], 
            max_value=st.session_state.current_range[1], 
            step=1,
            key="guess_input",
            disabled=st.session_state.game_over
        )
        
        # Tombol aksi
        col_act1, col_act2, col_act3, col_act4 = st.columns(4)
        
        with col_act1:
            if st.button("🎯 Tebak!", 
                        key="guess_button",
                        use_container_width=True, 
                        disabled=st.session_state.game_over):
                if not player_name:
                    st.warning("⚠️ Silakan masukkan nama Anda terlebih dahulu!")
                elif guess in st.session_state.guesses:
                    st.warning("Anda sudah menebak angka ini sebelumnya!")
                else:
                    st.session_state.guesses.append(guess)
                    
                    with st.spinner('Memeriksa tebakan...'):
                        time.sleep(0.5)
                        
                        if guess < st.session_state.target_number:
                            st.error(f"📉 {guess} terlalu rendah!")
                        elif guess > st.session_state.target_number:
                            st.error(f"📈 {guess} terlalu tinggi!")
                        else:
                            time_spent = time.time() - st.session_state.start_time
                            st.session_state.game_over = True
                            st.session_state.total_games += 1
                            st.session_state.total_wins += 1
                            
                            if player_name:
                                st.session_state.leaderboard.append({
                                    'name': player_name,
                                    'difficulty': difficulty,
                                    'guesses': len(st.session_state.guesses),
                                    'time': time_spent,
                                    'hints': st.session_state.hints_used,
                                    'date': time.strftime("%Y-%m-%d %H:%M:%S")
                                })
                                st.session_state.leaderboard.sort(key=lambda x: x['guesses'])
                            
                            st.success(f"""
                            🎉 **Selamat {player_name}!** Anda menebak dengan benar!
                            
                            🔢 **Angka:** {st.session_state.target_number}  
                            🎯 **Tebakan:** {len(st.session_state.guesses)}  
                            ⏱ **Waktu:** {time_spent:.1f} detik  
                            💡 **Hint digunakan:** {st.session_state.hints_used}
                            """)
                            st.balloons()
                            if len(st.session_state.guesses) <= 5:
                                st.snow()
        
        with col_act2:
            hint_disabled = (st.session_state.game_over or 
                            st.session_state.hints_used >= st.session_state.available_hints)
            
            if st.button("💡 Dapatkan Hint", 
                        key="hint_button",
                        use_container_width=True, 
                        disabled=hint_disabled):
                st.session_state.hints_used += 1
                hint = generate_hint(
                    st.session_state.target_number, 
                    st.session_state.current_range,
                    st.session_state.guesses
                )
                st.info(hint)
        
        with col_act3:
            if st.button("🔄 Ulangi Game", 
                        key="restart_button",
                        use_container_width=True,
                        help="Mulai game baru dengan pengaturan yang sama"):
                initialize_game()
                st.rerun()
        
        with col_act4:
            if st.button("💾 Simpan & Lanjutkan", 
                        key="save_button",
                        use_container_width=True,
                        type="primary",
                        disabled=not player_name or not st.session_state.game_over,
                        help="Simpan hasil dan lanjutkan dengan pemain baru"):
                if player_name:
                    st.session_state.saved_name = player_name
                    st.success("Hasil permainan tersimpan!")
                    initialize_game()
                    st.rerun()
        
        # Visualisasi tebakan
        if st.session_state.guesses:
            st.markdown("---")
            st.subheader("📋 Riwayat Tebakan")
            
            guess_data = []
            for i, g in enumerate(st.session_state.guesses, 1):
                diff = abs(g - st.session_state.target_number)
                direction = "⬇️ Rendah" if g < st.session_state.target_number else "⬆️ Tinggi" if g > st.session_state.target_number else "🎯 Tepat"
                
                if diff == 0:
                    feedback = "🔥 Tepat!"
                elif diff <= 5:
                    feedback = "♨️ Panas!"
                elif diff <= 15:
                    feedback = "🌤️ Hangat"
                elif diff <= 30:
                    feedback = "❄️ Dingin"
                else:
                    feedback = "🧊 Beku"
                
                guess_data.append({
                    "Percobaan": i,
                    "Tebakan": g,
                    "Keterangan": feedback,
                    "Arah": direction
                })
            
            st.dataframe(guess_data, use_container_width=True, hide_index=True)
        
        # Indikator panas-dingin
        if st.session_state.guesses and not st.session_state.game_over:
            last_guess = st.session_state.guesses[-1]
            difference = abs(last_guess - st.session_state.target_number)
            max_range = st.session_state.current_range[1] - st.session_state.current_range[0]
            progress_value = max(0, 1 - (difference/max_range))
            
            if difference == 0:
                temp_text = "🔥 TEPAT!"
            elif difference <= 0.1*max_range:
                temp_text = "♨️ Panas!"
            elif difference <= 0.3*max_range:
                temp_text = "🌤️ Hangat"
            else:
                temp_text = "❄️ Dingin"
            
            st.progress(progress_value, text=temp_text)
            st.caption(f"Jarak dari target: {difference} poin")

    # =====================================
    # BAGIAN STATISTIK
    # =====================================
    st.markdown("---")
    st.subheader("📈 Statistik Permainan")

    stat1, stat2, stat3 = st.columns(3)
    with stat1:
        st.metric("Total Permainan", st.session_state.total_games)
    with stat2:
        st.metric("Total Kemenangan", st.session_state.total_wins)
    with stat3:
        if st.session_state.total_games > 0:
            win_percentage = (st.session_state.total_wins / st.session_state.total_games) * 100
            st.metric("Persentase Menang", f"{win_percentage:.1f}%")
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
        for record in st.session_state.leaderboard[:10]:  # Batasi 10 teratas
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
        st.write("Belum ada data leaderboard")

    # =====================================
    # BAGIAN TIPS & STRATEGI
    # =====================================
    st.markdown("---")
    with st.expander("💡 Tips & Strategi Bermain"):
        st.markdown("""
        ### 🎮 Cara Bermain:
        1. Pilih level kesulitan dan jumlah hint
        2. Klik **Mulai Game Baru**
        3. Masukkan nama Anda dan mulai menebak!
        
        ### 🧠 Strategi Menang:
        - Gunakan **binary search** untuk efisiensi tebakan
        - Mulai dengan tebakan di tengah range
        - Sesuaikan range berdasarkan feedback
        - Manfaatkan hint saat benar-benar stuck
        
        ### 💡 Jenis Hint:
        - **Range Hint**: Menunjukkan range kecil yang berisi angka target
        - **Paritas Hint**: Menunjukkan apakah angka genap/ganjil
        - **Kelipatan Hint**: Menunjukkan angka bisa dibagi oleh berapa
        - **Prima Hint**: Menunjukkan apakah angka prima
        - **Jumlah Digit Hint**: Menunjukkan jumlah semua digit angka
        - Dan masih banyak hint kreatif lainnya!
        
        ### 💾 Penyimpanan Data:
        - Hasil permainan otomatis tersimpan di leaderboard
        - Statistik diupdate secara real-time
        """)