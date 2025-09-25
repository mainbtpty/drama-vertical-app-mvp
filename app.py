import streamlit as st
import base64
import os

# Page config for mobile-like layout
st.set_page_config(page_title="ReelShort Clone MVP", layout="centered", initial_sidebar_state="collapsed")

# Hardcoded video metadata (local MP4s in repo)
videos = [
    {
        "file": "File0.mp4",
        "title": "Episode 1: Lava",
        "genre": "Drama",
        "description": "A 20-second emotional journey—will it erupt? (Cliffhanger demo)"
    },
    {
        "file": "File1.mp4",
        "title": "Episode 2: Switch",
        "genre": "Drama",
        "description": "A quick twist—what's the switch? (Cliffhanger demo)"
    },
    {
        "file": "File2.mp4",
        "title": "Episode 3: 20 Seconds",
        "genre": "Drama",
        "description": "Time is running out—what happens next? (Cliffhanger demo)"
    },
    {
        "file": "File3.mp4",
        "title": "Episode 4: 2012 Moment",
        "genre": "Drama",
        "description": "A dramatic second—will they survive? (Cliffhanger demo)"
    }
]

# CSS for ReelShort-like mobile UI (dark theme, vertical player, icons)
st.markdown("""
    <style>
        .main { max-width: 360px; margin: auto; background-color: #000; color: #fff; }
        .header { background-color: #000; padding: 10px; border-bottom: 1px solid #333; }
        .search-bar { width: 100%; padding: 8px; background: #222; border: none; border-radius: 20px; color: #fff; }
        .nav-tabs { display: flex; justify-content: space-around; background: #111; padding: 10px; }
        .nav-tab { color: #fff; background: none; border: none; padding: 8px 12px; cursor: pointer; }
        .nav-tab.active { border-bottom: 2px solid #ff4d4d; }
        .video-container { width: 100%; aspect-ratio: 9/16; background: #000; margin: 20px 0; }
        video { width: 100%; height: 100%; object-fit: cover; }
        .episode-info { padding: 10px; background: #111; margin-bottom: 20px; }
        .bottom-nav { position: fixed; bottom: 0; width: 100%; max-width: 360px; background: #000; display: flex; justify-content: space-around; padding: 10px; border-top: 1px solid #333; }
        .bottom-icon { color: #fff; font-size: 24px; cursor: pointer; }
        .dummy-placeholder { text-align: center; padding: 40px; color: #888; }
    </style>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
""", unsafe_allow_html=True)

# Header with search bar
st.markdown('<div class="header"><input type="text" class="search-bar" placeholder="Search shows..."></div>', unsafe_allow_html=True)

# Navigation tabs (dummy)
tab_names = ["Popular", "New", "Ranking", "Categories", "Asian"]
selected_tab = st.selectbox("Navigation", tab_names, key="nav_tab", format_func=lambda x: x)  # Dummy selectbox styled as tabs

# Dummy tab content (same video feed for all)
st.markdown('<div class="nav-tabs">', unsafe_allow_html=True)
for tab in tab_names:
    active_class = "nav-tab active" if tab == selected_tab else "nav-tab"
    st.markdown(f'<button class="{active_class}">{tab}</button>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Main video feed (local MP4s, vertical play)
if "current_video_index" not in st.session_state:
    st.session_state.current_video_index = 0

video = videos[st.session_state.current_video_index]
try:
    with open(video["file"], "rb") as f:
        video_data = f.read()
    video_b64 = base64.b64encode(video_data).decode()
    st.markdown(f"""
        <div class="video-container">
            <video controls autoplay loop muted playsinline>
                <source src="data:video/mp4;base64,{video_b64}" type="video/mp4">
                Your browser does not support the video tag.
            </video>
        </div>
        <div class="episode-info">
            <h3>{video['title']}</h3>
            <p><b>Genre:</b> {video['genre']}</p>
            <p><b>Description (Cliffhanger):</b> {video['description']}</p>
        </div>
    """, unsafe_allow_html=True)
except Exception as e:
    st.error(f"Error loading video {video['file']}: {e}")
    st.stop()

# Navigation buttons (dummy swipe simulation)
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("← Previous"):
        st.session_state.current_video_index = (st.session_state.current_video_index - 1) % len(videos)
        st.rerun()
with col2:
    if st.button("Next →"):
        st.session_state.current_video_index = (st.session_state.current_video_index + 1) % len(videos)
        st.rerun()

# Bottom navigation bar with icons (dummy)
st.markdown("""
    <div class="bottom-nav">
        <span class="bottom-icon">🏠</span> <!-- Home -->
        <span class="bottom-icon">❤️</span> <!-- For You -->
        <span class="bottom-icon">📋</span> <!-- My List -->
        <span class="bottom-icon">⭐</span> <!-- Rewards -->
        <span class="bottom-icon">👤</span> <!-- Profile -->
    </div>
""", unsafe_allow_html=True)

# Dummy functionality for bottom icons (placeholders)
if st.button("Home (Dummy)"): st.write("Home: Discover trending series.")
if st.button("For You (Dummy)"): st.write("For You: Personalized recommendations.")
if st.button("My List (Dummy)"): st.write("My List: Your watchlist.")
if st.button("Rewards (Dummy)"): st.write("Rewards: Earn coins for ads!")
if st.button("Profile (Dummy)"): st.write("Profile: Your account settings.")

# Footer note
st.caption("ReelShort Clone MVP – Vertical drama playback (test on mobile view).")
