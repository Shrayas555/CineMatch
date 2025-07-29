"""
Data Processing Script for CineMatch Movie Recommendation System

This script processes the raw TMDB movie data and generates the necessary
pickle files for the recommendation system.
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os
import sys

def load_and_clean_data():
    """Load and clean the movie data from CSV files."""
    print("Loading movie data...")
    
    # Load the datasets
    movies_df = pd.read_csv('data/tmdb_5000_movies.csv')
    credits_df = pd.read_csv('data/tmdb_5000_credits.csv')
    
    print(f"Loaded {len(movies_df)} movies and {len(credits_df)} credits records")
    
    # Merge the datasets
    movies_df = movies_df.merge(credits_df, on='title')
    
    # Select relevant columns
    movies = movies_df[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]
    
    # Handle missing values
    movies['overview'] = movies['overview'].fillna('')
    movies['genres'] = movies['genres'].fillna('[]')
    movies['keywords'] = movies['keywords'].fillna('[]')
    movies['cast'] = movies['cast'].fillna('[]')
    movies['crew'] = movies['crew'].fillna('[]')
    
    return movies

def extract_features(text):
    """Extract features from JSON-like strings."""
    import ast
    try:
        features = ast.literal_eval(text)
        return ' '.join([feature['name'] for feature in features])
    except:
        return ''

def extract_director(crew_text):
    """Extract director name from crew information."""
    import ast
    try:
        crew = ast.literal_eval(crew_text)
        for person in crew:
            if person['job'] == 'Director':
                return person['name']
        return ''
    except:
        return ''

def create_soup(x):
    """Create a combined text soup for TF-IDF vectorization."""
    return ' '.join([x['overview'], x['genres'], x['keywords'], x['cast'], x['director']])

def generate_model():
    """Generate the recommendation model and save pickle files."""
    print("Starting model generation...")
    
    # Load and clean data
    movies = load_and_clean_data()
    
    # Extract features
    print("Extracting features...")
    movies['genres'] = movies['genres'].apply(extract_features)
    movies['keywords'] = movies['keywords'].apply(extract_features)
    movies['cast'] = movies['cast'].apply(extract_features)
    movies['director'] = movies['crew'].apply(extract_director)
    
    # Create soup for TF-IDF
    movies['soup'] = movies.apply(create_soup, axis=1)
    
    # TF-IDF Vectorization
    print("Creating TF-IDF vectors...")
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(movies['soup'])
    
    # Calculate cosine similarity
    print("Calculating similarity matrix...")
    similarity = cosine_similarity(tfidf_matrix, tfidf_matrix)
    
    # Create movies dictionary for easy lookup
    movies_dict = movies.set_index('title')['movie_id'].to_dict()
    
    # Save files
    print("Saving model files...")
    os.makedirs('artifacts', exist_ok=True)
    
    # Save similarity matrix
    with open('artifacts/similarity.pkl', 'wb') as f:
        pickle.dump(similarity, f)
    print("Saved similarity.pkl")
    
    # Save movies dataframe
    with open('artifacts/movies.pkl', 'wb') as f:
        pickle.dump(movies, f)
    print("Saved movies.pkl")
    
    # Save movies dictionary
    with open('artifacts/movies_dict.pkl', 'wb') as f:
        pickle.dump(movies_dict, f)
    print("Saved movies_dict.pkl")
    
    print("Model generation completed successfully!")
    print(f"Files saved in artifacts/ directory:")
    print(f"- similarity.pkl ({os.path.getsize('artifacts/similarity.pkl') / (1024*1024):.1f} MB)")
    print(f"- movies.pkl ({os.path.getsize('artifacts/movies.pkl') / (1024*1024):.1f} MB)")
    print(f"- movies_dict.pkl ({os.path.getsize('artifacts/movies_dict.pkl') / (1024*1024):.1f} MB)")

def download_data():
    """Download the required CSV files if they don't exist."""
    import urllib.request
    
    data_dir = 'data'
    os.makedirs(data_dir, exist_ok=True)
    
    # URLs for the datasets (you may need to update these)
    urls = {
        'tmdb_5000_movies.csv': 'https://raw.githubusercontent.com/your-repo/data/main/tmdb_5000_movies.csv',
        'tmdb_5000_credits.csv': 'https://raw.githubusercontent.com/your-repo/data/main/tmdb_5000_credits.csv'
    }
    
    for filename, url in urls.items():
        filepath = os.path.join(data_dir, filename)
        if not os.path.exists(filepath):
            print(f"Downloading {filename}...")
            try:
                urllib.request.urlretrieve(url, filepath)
                print(f"Downloaded {filename}")
            except Exception as e:
                print(f"Failed to download {filename}: {e}")
                print(f"Please manually download {filename} and place it in the {data_dir}/ directory")
        else:
            print(f"{filename} already exists")

if __name__ == "__main__":
    print("CineMatch Model Generator")
    print("=" * 30)
    
    # Check if data files exist
    if not os.path.exists('data/tmdb_5000_movies.csv') or not os.path.exists('data/tmdb_5000_credits.csv'):
        print("Data files not found. Attempting to download...")
        download_data()
    
    # Generate model
    try:
        generate_model()
    except Exception as e:
        print(f"Error generating model: {e}")
        print("Please ensure the data files are in the data/ directory")
        sys.exit(1) 