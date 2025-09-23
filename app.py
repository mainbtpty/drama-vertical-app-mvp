import streamlit as st
import sqlite3
import hashlib
import os
from moviepy.editor import VideoFileClip
from PIL import Image
from io import BytesIO
import base64

# Initialize directories
os.makedirs("videos", exist_ok=True)
os.makedirs("thumbnails", exist_ok=True)

# Hardcoded admin password (change this for security in real use)
ADMIN_PASSWORD = "admin123"

# Initialize SQLite database
conn = sqlite3.connect("videos.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS videos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        genre TEXT,
        description TEXT,
        local_path TEXT,
        thumbnail_path TEXT,
        duration INTEGER
    )
""")
conn.commit()

# Helper functions
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def trim_video(input_path, output_path, duration=120):
    try:
        clip = VideoFileClip(input_path)
        trimmed_clip = clip.subclip(0, duration)
        trimmed_clip.write_videofile(output_path, codec="libx264")
        clip.close()
        trimmed_clip.close()
        return output_path
    except Exception as e:
        st.error(f"Error trimming video: {e}")
        return None

def generate_thumbnail(video_path, output_path):
    try:
        clip = VideoFileClip(video_path)
        frame = clip.get_frame(1)  # Get frame at 1 second
        img = Image.fromarray(frame)
        img.save(output_path)
        clip.close()
        return output_path
    except Exception as e:
        st.error(f"Error generating thumbnail: {e}")
        return None

# Streamlit app
st.set_page_config(page_title="Drama Vertical App MVP", layout="centered")

# CSS for vertical video player (9:16 aspect ratio)
st.markdown("""
    <style>
        .video-container {
            width: 100%;
            max-width: 360px;
            aspect-ratio: 9 / 16;
            margin: auto;
            background: black;
            overflow: hidden;
        }
        video {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        .episode-list {
            margin-top: 20px;
        }
        .episode-item {
            cursor: pointer;
            padding: 10px;
            border-bottom: 1px solid #ccc;
        }
        .episode-item:hover {
            background-color: #f0f0f0;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar for navigation
page = st.sidebar.selectbox("Select Page", ["User View (Vertical App)", "Admin Dashboard"])

if page == "Admin Dashboard":
    st.header("Admin Dashboard - Upload & Manage Episodes")
    password = st.text_input("Enter Admin Password", type="password")
    if password and hash_password(password) == hash_password(ADMIN_PASSWORD):
        st.subheader("Upload New Episode")
        with st.form("upload_form"):
            title = st.text_input("Episode Title")
            genre = st.selectbox("Genre", ["Drama", "Comedy", "Telenovela", "Animation"])
            description = st.text_area("Description (e.g., Cliffhanger Ending Note)")
            duration = st.slider("Trim to Duration (seconds, 60-120 for 1-2 min)", 60, 120, 120)
            video_file = st.file_uploader("Upload Video (MP4)", type=["mp4"])
            submit = st.form_submit_button("Upload and Trim")
            if submit and video_file and title and description:
                # Save uploaded file temporarily
                temp_path = f"temp_{title}.mp4"
                with open(temp_path, "wb") as f:
                    f.write(video_file.read())
                # Trim video
                trimmed_path = f"videos/{title}.mp4"
                trimmed_path = trim_video(temp_path, trimmed_path, duration)
                if trimmed_path:
                    # Generate thumbnail
                    thumbnail_path = f"thumbnails/{title}.jpg"
                    generate_thumbnail(trimmed_path, thumbnail_path)
                    # Save metadata to SQLite
                    cursor.execute(
                        "INSERT INTO videos (title, genre, description, local_path, thumbnail_path, duration) VALUES (?, ?, ?, ?, ?, ?)",
                        (title, genre, description, trimmed_path, thumbnail_path, duration)
                    )
                    conn.commit()
                    st.success(f"Episode '{title}' uploaded and ready for viewing!")
                    os.remove(temp_path)  # Clean up temp file
    else:
        if password:
            st.error("Incorrect password.")
        else:
            st.info("Please enter the admin password to access the dashboard.")

elif page == "User View (Vertical App)":
    st.header("Drama Vertical App MVP - Short-Form Episodes")
    cursor.execute("SELECT id, title, genre, description, local_path, thumbnail_path FROM videos")
    videos = cursor.fetchall()
    if not videos:
        st.info("No episodes available yet. Showing a sample vertical drama clip for demo purposes.")
        # Hardcoded sample video URL for demo (short 15-second clip)
        sample_video_url = "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerMeltdowns.mp4"
        sample_title = "Sample Episode: The Meltdown"
        sample_genre = "Drama"
        sample_description = "A tense moment—will he break down? (Demo clip)"
        
        # Display hardcoded vertical video
        st.markdown(f"""
            <div class="video-container">
                <video controls autoplay loop>
                    <source src="{sample_video_url}" type="video/mp4">
                </video>
            </div>
            <h3>{sample_title}</h3>
            <p><b>Genre:</b> {sample_genre}</p>
            <p><b>Description (Cliffhanger):</b> {sample_description}</p>
        """, unsafe_allow_html=True)
    else:
        # Original code for uploaded videos
        if "current_video_index" not in st.session_state:
            st.session_state.current_video_index = 0

        video = videos[st.session_state.current_video_index]
        video_id, title, genre, description, local_path, thumbnail_path = video
        
        # Display vertical video player
        st.markdown(f"""
            <div class="video-container">
                <video controls autoplay loop>
                    <source src="data:video/mp4;base64,{base64.b64encode(open(local_path, 'rb').read()).decode()}" type="video/mp4">
                </video>
            </div>
            <h3>{title}</h3>
            <p><b>Genre:</b> {genre}</p>
            <p><b>Description (Cliffhanger):</b> {description}</p>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Previous Episode"):
                st.session_state.current_video_index = (st.session_state.current_video_index - 1) % len(videos)
                st.rerun()
        with col2:
            if st.button("Next Episode"):
                st.session_state.current_video_index = (st.session_state.current_video_index + 1) % len(videos)
                st.rerun()

        st.subheader("Browse Episodes")
        for idx, v in enumerate(videos):
            v_id, v_title, v_genre, v_desc, v_path, v_thumb = v
            if os.path.exists(v_thumb):
                st.image(v_thumb, caption=v_title, use_column_width=True)
            if st.button(f"{v_title} ({v_genre}) - {v_desc[:50]}...", key=f"episode_{v_id}"):
                st.session_state.current_video_index = idx
                st.rerun()

# Close database connection when app stops (optional, but good practice)
conn.close()
