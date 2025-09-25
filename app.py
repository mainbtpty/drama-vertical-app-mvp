import streamlit as st
import base64
import os

# Page config for mobile-like layout
st.set_page_config(page_title="ReelShort Clone MVP", layout="centered", initial_sidebar_state="collapsed")

# Hardcoded video metadata (local MP4s in repo)
videos = [
    {
        "file": "File0.mp4",
        "title": "Episode 1: Hidden Truths",
        "genre": "Drama",
        "description": "A secret unraveling—will she confront him? (20s cliffhanger)"
    },
    {
        "file": "File1.mp4",
        "title": "Episode 2: Fading Light",
        "genre": "Drama",
        "description": "Darkness looms—what’s her next move? (20s cliffhanger)"
    },
    {
        "file": "File2.mp4",
        "title": "Episode 3: Broken Bonds",
        "genre": "Drama",
        "description": "Trust shattered—can they rebuild? (20s cliffhanger)"
    },
    {
        "file": "File3.mp4",
        "title": "Episode 4: Last Chance",
        "genre": "Drama",
        "description": "One final moment—will it change everything? (20s cliffhanger)"
    }
]

# Check if video files exist in directory
for video in videos:
    if not os.path.exists(video["file"]):
        st.error(f"Video file {video['file']} not found in the app directory. Please ensure all MP4s are uploaded.")
        st.stop()

# CSS for ReelShort-like mobile UI (optimized for iPhone/Android Chrome)
st.markdown("""
    <style>
        /* Reset default margins and ensure full-screen mobile layout */
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
        /* Header with search bar */
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
        /* Navigation tabs */
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
        /* Video container (9:16 aspect ratio) */
        .video-container {
            width: 100%;
            aspect-ratio: 9/16;
            background: #000;
            margin: 0;
            overflow: hidden;
        }
        video {
            width: 100%;
            height: 100%;
            object-fit: cover;
            display: block;
        }
        /* Episode info */
        .episode-info {
            padding: 15px;
            background: #111;
            margin: 10px 0;
            border-radius: 8px;
            font-size: 14px;
        }
        /* Navigation buttons */
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
        /* Bottom navigation bar */
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
        /* Dummy placeholder */
        .dummy-placeholder {
            text-align: center;
            padding: 40px;
            color: #888;
            font-size: 16px;
        }
        /* Mobile-specific adjustments */
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

# Initialize session state
if "current_video_index" not in st.session_state:
    st.session_state.current_video_index = 0

# Debug: Display current video index
st.write(f"Debug: Current video index: {st.session_state.current_video_index}")

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
            <p><strong>Genre:</strong> {video['genre']}</p>
            <p><strong>Cliffhanger:</strong> {video['description']}</p>
        </div>
    """, unsafe_allow_html=True)
except Exception as e:
    st.error(f"Error loading video {video['file']}: {e}")
    st.stop()

# Navigation buttons (touch-friendly)
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("← Previous", key="prev", use_container_width=True):
        st.session_state.current_video_index = (st.session_state.current_video_index - 1) % len(videos)
        st.write(f"Debug: Switching to video index {st.session_state.current_video_index}")
        st.rerun()
with col2:
    if st.button("Next →", key="next", use_container_width=True):
        st.session_state.current_video_index = (st.session_state.current_video_index + 1) % len(videos)
        st.write(f"Debug: Switching to video index {st.session_state.current_video_index}")
        st.rerun()

# Bottom navigation bar with icons (dummy, touch-friendly)
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
