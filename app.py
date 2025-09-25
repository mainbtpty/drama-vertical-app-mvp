import streamlit as st
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

# Check if video files exist in directory
for video in videos:
    if not os.path.exists(video["file"]):
        st.error(f"Video file {video['file']} not found in the app directory. Please ensure all MP4s (File0.mp4, File1.mp4, File2.mp4, File3.mp4) are uploaded to the repo root.")
        st.stop()

# CSS for ReelShort-like mobile UI (optimized for iPhone/Android Chrome)
st.markdown("""
    <style>
        html, body { margin: 0; padding: 0; overflow-x: hidden; }
        .main {
            width: 100%;
            max-width: 360px;
            margin: 0 auto;
            background-color: #000;
            color: #fff;
            min-height: 100vh;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }
        .header {
            background-color: #000;
            padding: 12px;
            border-bottom: 1px solid #333;
            position: sticky;
            top: 0;
            z-index: 100;
        }
        .search-bar {
            width: 100%;
            padding: 10px 15px;
            background: #222;
            border: none;
            border-radius: 20px;
            color: #fff;
            font-size: 16px;
            box-sizing: border-box;
        }
        .nav-tabs {
            display: flex;
            justify-content: space-around;
            background: #111;
            padding: 10px;
            overflow-x: auto;
            white-space: nowrap;
            -webkit-overflow-scrolling: touch;
        }
        .nav-tab {
            color: #fff;
            background: none;
            border: none;
            padding: 10px 15px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 500;
        }
        .nav-tab.active {
            border-bottom: 2px solid #ff4d4d;
            color: #ff4d4d;
        }
        .video-container {
            width: 100%;
            aspect-ratio: 9/16;
            background: #000;
            margin: 20px 0;
            overflow: hidden;
        }
        video {
            width: 100%;
            height: 100%;
            object-fit: cover;
            display: block;
        }
        .episode-info {
            padding: 15px;
            background: #111;
            margin: 10px 0;
            border-radius: 8px;
            font-size: 14px;
        }
        .nav-button {
            font-size: 16px;
            padding: 12px;
            border-radius: 8px;
            background: #ff4d4d;
            color: #fff;
            border: none;
            width: 100%;
            font-weight: 500;
            touch-action: manipulation;
        }
        .bottom-nav {
            position: fixed;
            bottom: 0;
            width: 100%;
            max-width: 360px;
            background: #000;
            display: flex;
            justify-content: space-around;
            padding: 12px;
            border-top: 1px solid #333;
            z-index: 100;
        }
        .bottom-icon {
            color: #fff;
            font-size: 28px;
            cursor: pointer;
            padding: 10px;
            min-width: 48px;
            text-align: center;
        }
        .bottom-icon:hover {
            color: #ff4d4d;
        }
        .dummy-placeholder {
            text-align: center;
            padding: 40px;
            color: #888;
            font-size: 16px;
        }
        @media only screen and (max-width: 400px) {
            .main { width: 100%; max-width: 100%; }
            .video-container { width: 100%; }
            .search-bar { font-size: 14px; padding: 8px 12px; }
            .nav-tab { font-size: 12px; padding: 8px 10px; }
            .bottom-icon { font-size: 24px; padding: 8px; }
            .nav-button { font-size: 14px; padding: 10px; }
            .episode-info { font-size: 12px; padding: 10px; }
        }
    </style>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
""", unsafe_allow_html=True)

# Header with search bar
st.markdown('<div class="header"><input type="text" class="search-bar" placeholder="Search shows..."></div>', unsafe_allow_html=True)

# Navigation tabs (dummy)
tab_names = ["Popular", "New", "Ranking", "Categories", "Asian"]
selected_tab = st.selectbox("Navigation", tab_names, key="nav_tab", format_func=lambda x: x, label_visibility="collapsed")
st.markdown('<div class="nav-tabs">', unsafe_allow_html=True)
for tab in tab_names:
    active_class = "nav-tab active" if tab == selected_tab else "nav-tab"
    st.markdown(f'<button class="{active_class}">{tab}</button>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Main video feed (local MP4s, vertical play)
if "current_video_index" not in st.session_state:
    st.session_state.current_video_index = 0

# Debug: Display current video index
st.write(f"Debug: Current video index: {st.session_state.current_video_index}, Playing: {videos[st.session_state.current_video_index]['file']}")

video = videos[st.session_state.current_video_index]
try:
    st.video(video["file"], format="video/mp4", start_time=0)
    st.markdown(f"""
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
    if st.button("← Previous", key="prev_button"):
        st.session_state.current_video_index = (st.session_state.current_video_index - 1) % len(videos)
        st.rerun()
with col2:
    if st.button("Next →", key="next_button"):
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
if st.button("Home (Dummy)", key="home"): 
    st.markdown('<div class="dummy-placeholder">Home: Discover trending series.</div>', unsafe_allow_html=True)
if st.button("For You (Dummy)", key="foryou"): 
    st.markdown('<div class="dummy-placeholder">For You: Personalized recommendations.</div>', unsafe_allow_html=True)
if st.button("My List (Dummy)", key="mylist"): 
    st.markdown('<div class="dummy-placeholder">My List: Your watchlist.</div>', unsafe_allow_html=True)
if st.button("Rewards (Dummy)", key="rewards"): 
    st.markdown('<div class="dummy-placeholder">Rewards: Earn coins for ads!</div>', unsafe_allow_html=True)
if st.button("Profile (Dummy)", key="profile"): 
    st.markdown('<div class="dummy-placeholder">Profile: Your account settings.</div>', unsafe_allow_html=True)

# Footer note
st.caption("ReelShort Clone MVP – Vertical drama playback (optimized for mobile Chrome).")
