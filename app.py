import pickle
import streamlit as st
import requests
import os

# --- Page Config ---
st.set_page_config(
    page_title="CineMatch",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Custom CSS ---
st.markdown("""
<style>
    /* Modern gradient background */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: white;
    }
    
    /* Sleek header */
    .main-header {
        font-family: 'Helvetica Neue', sans-serif;
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #ff4d4d, #f9cb28);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    /* Modern select box */
    .stSelectbox > div > div {
        background-color: rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.3);
        color: white !important;
        border-radius: 12px;
    }
    
    /* Placeholder text color */
    .stSelectbox > div > div > div[data-baseweb="select"] > div:first-child {
        color: #aaa !important;
    }
    
    /* Recommendation cards - removed circular shape and background */
    .movie-card {
        transition: all 0.3s ease;
        border-radius: 0; /* Removed circular/rounded corners */
        overflow: hidden;
        background: transparent; /* Removed background shape */
        padding: 15px;
        margin-bottom: 20px;
        height: 100%;
        display: flex;
        flex-direction: column;
    }
    
    .movie-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        /* Background remains transparent on hover */
    }
    
    /* Movie title with ellipsis */
    .movie-title {
        font-weight: bold;
        margin: 10px 0;
        color: white;
        text-align: center;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        width: 100%;
        font-size: 1rem;
        flex-shrink: 0;
    }
    
    /* Card content wrapper */
    .card-content {
        flex-grow: 1;
        display: flex;
        flex-direction: column;
    }
    
    /* Movie poster in cards */
    .card-poster {
        border-radius: 10px;
        width: 100%;
        height: 300px;
        object-fit: cover;
        flex-shrink: 0;
    }
    
    /* Modal poster */
    .modal-poster {
        border-radius: 12px;
        width: 100%;
        max-height: 350px;
        object-fit: contain;
    }
    
    /* Details button */
    .details-btn {
        margin-top: auto;
        flex-shrink: 0;
    }
    
    /* Modern buttons */
    .stButton > button {
        border-radius: 12px;
        background: linear-gradient(90deg, #ff416c, #ff4b2b);
        color: white;
        font-weight: 600;
        border: none;
        transition: all 0.3s;
        width: 100%;
    }
    
    /* Remove hover effect from buttons */
    .stButton > button:hover {
        transform: none;
        box-shadow: none;
    }
    
    /* Details modal */
    .details-container {
        background: rgba(15, 12, 41, 0.95);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        margin-bottom: 50px;
    }
    
    /* Responsive layout */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2.5rem;
        }
        .card-poster {
            height: 200px;
        }
    }
</style>
""", unsafe_allow_html=True)

# --- App Header ---
st.markdown('<h1 class="main-header">CineMatch</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; font-size:1.2rem; color:#aaa; margin-bottom:2rem;">Discover your next favorite movie</p>', unsafe_allow_html=True)

# --- Load Data ---
@st.cache_data
def load_data():
    import gzip
    # Try to load compressed files first, then fallback to uncompressed
    try:
        with gzip.open('artifacts/movies.pkl.gz', 'rb') as f:
            movies = pickle.load(f)
        with gzip.open('artifacts/similarity.pkl.gz', 'rb') as f:
            similarity = pickle.load(f)
    except FileNotFoundError:
        # Fallback to uncompressed files
        movies = pickle.load(open('artifacts/movies.pkl', 'rb'))
        similarity = pickle.load(open('artifacts/similarity.pkl', 'rb'))
    return movies, similarity

movies, similarity = load_data()

# --- Recommendation Engine ---
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(enumerate(similarity[index]), key=lambda x: x[1], reverse=True)
    return [
        {
            'title': movies.iloc[i[0]].title,
            'poster': fetch_poster(movies.iloc[i[0]].movie_id),
            'id': movies.iloc[i[0]].movie_id
        } 
        for i in distances[1:6]
    ]

# --- TMDB API Integration ---
# Get API key from environment variable or use default (for development)
TMDB_API_KEY = os.getenv('TMDB_API_KEY', '37f9391204e401d0a27a74894f911d05')

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}"
    data = requests.get(url).json()
    return f"https://image.tmdb.org/t/p/w500/{data.get('poster_path', '')}" if data.get('poster_path') else None

def fetch_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}"
    data = requests.get(url).json()
    return {
        'overview': data.get("overview", "No overview available."),
        'rating': data.get("vote_average", "N/A"),
        'release_date': data.get("release_date", "N/A"),
        'runtime': data.get("runtime", "N/A"),
        'genres': ", ".join([g['name'] for g in data.get('genres', [])])
    }

# --- Main App ---
def main():
    # Session state initialization
    if 'recommendations' not in st.session_state:
        st.session_state.recommendations = []
    if 'show_details' not in st.session_state:
        st.session_state.show_details = None
    
    # Movie selection - blank by default
    selected_movie = st.selectbox(
        "Search for a movie you love:",
        movies['title'].values,
        index=None,  # This makes it blank by default
        placeholder="Enter movie name...",
        key="movie_select"
    )
    
    # Recommendation button (disabled if no movie selected)
    if st.button("🎬 Get Recommendations", 
                use_container_width=True,
                disabled=not selected_movie):
        with st.spinner('Finding perfect matches...'):
            st.session_state.recommendations = recommend(selected_movie)
            st.session_state.show_details = None
    
    # Display recommendations
    if st.session_state.recommendations:
        st.subheader("Your Personalized Recommendations", divider="rainbow")
        cols = st.columns(5)
        for i, movie in enumerate(st.session_state.recommendations):
            with cols[i]:
                with st.container():
                    st.markdown('<div class="movie-card">', unsafe_allow_html=True)
                    st.markdown('<div class="card-content">', unsafe_allow_html=True)
                    
                    if movie['poster']:
                        st.image(movie['poster'], use_container_width=True, output_format="auto")
                    
                    # Truncated title with ellipsis
                    title = movie['title'] if len(movie['title']) <= 25 else f"{movie['title'][:22]}..."
                    st.markdown(f'<p class="movie-title" title="{movie["title"]}">{title}</p>', unsafe_allow_html=True)
                    
                    # Details button at fixed position
                    st.markdown('<div class="details-btn">', unsafe_allow_html=True)
                    if st.button("View Details", key=f"details_{i}", use_container_width=True):
                        st.session_state.show_details = movie
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)  # Close card-content
                    st.markdown('</div>', unsafe_allow_html=True)  # Close movie-card
    
    # Movie details modal
    if st.session_state.show_details:
        movie = st.session_state.show_details
        details = fetch_movie_details(movie['id'])
        
        with st.container():
            st.markdown('<div class="details-container">', unsafe_allow_html=True)
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(movie['poster'], width=250, output_format="auto")  # Fixed width
            with col2:
                st.markdown(f"<h2>{movie['title']}</h2>", unsafe_allow_html=True)
                # Format rating to one decimal place if not "N/A"
                try:
                    rating_val = float(details['rating'])
                    rating_display = f"{rating_val:.1f}"
                except:
                    rating_display = details['rating']
                st.markdown(f"⭐ **Rating:** {rating_display}/10")
                st.markdown(f"📅 **Release Date:** {details['release_date']}")
                st.markdown(f"⏱️ **Runtime:** {details['runtime']} mins")
                st.markdown(f"🎭 **Genres:** {details['genres']}")
                st.markdown(f"📖 **Overview:** {details['overview']}")
            
            if st.button("Close", use_container_width=True, type="primary"):
                st.session_state.show_details = None
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
