#!/usr/bin/env python3
"""
Model Download Script for CineMatch

This script downloads the compressed model files needed for the movie recommendation system.
"""

import os
import urllib.request
import gzip
import pickle

def download_and_decompress():
    """Download and decompress model files."""
    
    # Create artifacts directory
    os.makedirs('artifacts', exist_ok=True)
    
    # URLs for compressed model files (you'll need to host these)
    model_files = {
        'similarity.pkl.gz': 'https://your-hosting-service.com/models/similarity.pkl.gz',
        'movies.pkl.gz': 'https://your-hosting-service.com/models/movies.pkl.gz',
        'movies_dict.pkl.gz': 'https://your-hosting-service.com/models/movies_dict.pkl.gz'
    }
    
    for filename, url in model_files.items():
        output_path = f'artifacts/{filename.replace(".gz", "")}'
        
        if not os.path.exists(output_path):
            print(f"Downloading {filename}...")
            try:
                # Download compressed file
                urllib.request.urlretrieve(url, f'artifacts/{filename}')
                
                # Decompress
                with gzip.open(f'artifacts/{filename}', 'rb') as f_in:
                    with open(output_path, 'wb') as f_out:
                        f_out.write(f_in.read())
                
                # Remove compressed file
                os.remove(f'artifacts/{filename}')
                print(f"Downloaded and decompressed {filename}")
                
            except Exception as e:
                print(f"Failed to download {filename}: {e}")
                print("Please manually download the model files")
        else:
            print(f"{filename.replace('.gz', '')} already exists")

if __name__ == "__main__":
    print("CineMatch Model Downloader")
    print("=" * 30)
    download_and_decompress()
