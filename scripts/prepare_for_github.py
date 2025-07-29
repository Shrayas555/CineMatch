"""
GitHub Deployment Preparation Script

This script helps prepare the project for GitHub deployment by:
1. Compressing large model files
2. Creating a data download script
3. Setting up proper file structure
"""

import os
import gzip
import shutil
import pickle
from pathlib import Path

def compress_pickle_file(input_path, output_path):
    """Compress a pickle file using gzip."""
    print(f"Compressing {input_path}...")
    
    # Read the pickle file
    with open(input_path, 'rb') as f:
        data = f.read()
    
    # Compress and save
    with gzip.open(output_path, 'wb') as f:
        f.write(data)
    
    original_size = os.path.getsize(input_path) / (1024 * 1024)
    compressed_size = os.path.getsize(output_path) / (1024 * 1024)
    
    print(f"Compressed {input_path}: {original_size:.1f}MB -> {compressed_size:.1f}MB ({compressed_size/original_size*100:.1f}% reduction)")

def decompress_pickle_file(input_path, output_path):
    """Decompress a gzipped pickle file."""
    print(f"Decompressing {input_path}...")
    
    with gzip.open(input_path, 'rb') as f:
        data = f.read()
    
    with open(output_path, 'wb') as f:
        f.write(data)
    
    print(f"Decompressed to {output_path}")

def create_download_script():
    """Create a script to download compressed model files."""
    script_content = '''#!/usr/bin/env python3
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
'''
    
    with open('scripts/download_models.py', 'w') as f:
        f.write(script_content)
    
    print("Created scripts/download_models.py")

def create_github_workflow():
    """Create GitHub Actions workflow for automated deployment."""
    workflow_content = '''name: Deploy to Streamlit Cloud

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v3
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Download model files
      run: |
        python scripts/download_models.py
    
    - name: Test Streamlit app
      run: |
        streamlit run app.py --server.headless true --server.port 8501 &
        sleep 10
        curl -f http://localhost:8501 || exit 1
    
    - name: Deploy to Streamlit Cloud
      if: github.ref == 'refs/heads/main'
      run: |
        echo "Deployment to Streamlit Cloud is configured via the web interface"
        echo "Please ensure your repository is connected to Streamlit Cloud"
'''
    
    os.makedirs('.github/workflows', exist_ok=True)
    with open('.github/workflows/deploy.yml', 'w') as f:
        f.write(workflow_content)
    
    print("Created .github/workflows/deploy.yml")

def main():
    """Main function to prepare the project for GitHub."""
    print("Preparing CineMatch for GitHub deployment...")
    print("=" * 50)
    
    # Create scripts directory if it doesn't exist
    os.makedirs('scripts', exist_ok=True)
    
    # Compress large model files
    artifacts_dir = Path('artifacts')
    if artifacts_dir.exists():
        for pickle_file in artifacts_dir.glob('*.pkl'):
            if pickle_file.stat().st_size > 10 * 1024 * 1024:  # Files larger than 10MB
                compressed_file = pickle_file.with_suffix('.pkl.gz')
                compress_pickle_file(str(pickle_file), str(compressed_file))
    
    # Create download script
    create_download_script()
    
    # Create GitHub workflow
    create_github_workflow()
    
    # Create .gitattributes for large files
    gitattributes_content = '''*.pkl filter=lfs diff=lfs merge=lfs -text
*.pkl.gz filter=lfs diff=lfs merge=lfs -text
*.csv filter=lfs diff=lfs merge=lfs -text
'''
    
    with open('.gitattributes', 'w') as f:
        f.write(gitattributes_content)
    
    print("Created .gitattributes")
    
    print("\n" + "=" * 50)
    print("GitHub preparation completed!")
    print("\nNext steps:")
    print("1. Initialize Git repository: git init")
    print("2. Add files: git add .")
    print("3. Commit: git commit -m 'Initial commit'")
    print("4. Create GitHub repository")
    print("5. Push: git push origin main")
    print("6. Connect to Streamlit Cloud for deployment")
    print("\nNote: Large model files are now compressed and should be hosted separately")

if __name__ == "__main__":
    main() 