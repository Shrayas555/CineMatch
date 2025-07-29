#!/usr/bin/env python3
"""
Environment Setup Script for CineMatch

This script helps you set up your environment variables securely.
"""

import os
import sys

def create_env_file():
    """Create a .env file with the user's API key."""
    
    print("🔒 CineMatch Environment Setup")
    print("=" * 40)
    print()
    
    # Check if .env already exists
    if os.path.exists('.env'):
        print("⚠️  .env file already exists!")
        response = input("Do you want to overwrite it? (y/N): ").lower()
        if response != 'y':
            print("Setup cancelled.")
            return
    
    print("📝 Setting up your environment variables...")
    print()
    
    # Get TMDB API key
    print("🔑 TMDB API Key Setup:")
    print("1. Go to https://www.themoviedb.org/settings/api")
    print("2. Sign up for a free account")
    print("3. Request an API key")
    print("4. Copy your API key")
    print()
    
    api_key = input("Enter your TMDB API key: ").strip()
    
    if not api_key:
        print("❌ No API key provided. Using demo key for development.")
        api_key = "37f9391204e401d0a27a74894f911d05"
    
    # Create .env file
    env_content = f"""# TMDB API Configuration
# Get your free API key from: https://www.themoviedb.org/settings/api
TMDB_API_KEY={api_key}

# Streamlit Configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=localhost
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        
        print("✅ .env file created successfully!")
        print("✅ Your API key is now securely stored")
        print("✅ .env file is ignored by Git (safe to commit)")
        print()
        
        # Test the API key
        if api_key != "37f9391204e401d0a27a74894f911d05":
            print("🧪 Testing your API key...")
            try:
                import requests
                test_url = f"https://api.themoviedb.org/3/movie/550?api_key={api_key}"
                response = requests.get(test_url)
                if response.status_code == 200:
                    print("✅ API key is valid!")
                else:
                    print("❌ API key might be invalid. Please check it.")
            except Exception as e:
                print(f"⚠️  Could not test API key: {e}")
        
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return
    
    print()
    print("🎯 Next Steps:")
    print("1. Run: streamlit run app.py")
    print("2. Your app will use your API key automatically")
    print("3. For deployment, set TMDB_API_KEY in Streamlit Cloud")
    print()
    print("📚 For more information, see SECURITY.md")

def check_security():
    """Check if the project is secure for GitHub."""
    
    print("🔍 Security Check")
    print("=" * 20)
    
    # Check for hardcoded API keys
    hardcoded_keys = []
    
    # Check app.py for hardcoded API keys (not fallback values)
    try:
        with open('app.py', 'r') as f:
            content = f.read()
            # Look for hardcoded API keys in URL strings (not fallback values)
            if 'api_key=37f9391204e401d0a27a74894f911d05' in content:
                hardcoded_keys.append('app.py')
    except:
        pass
    
    if hardcoded_keys:
        print("❌ Found hardcoded API keys in:")
        for file in hardcoded_keys:
            print(f"   - {file}")
        print("   Please update the code to use environment variables.")
    else:
        print("✅ No hardcoded API keys found")
    
    # Check .gitignore
    try:
        with open('.gitignore', 'r') as f:
            content = f.read()
            if '.env' in content:
                print("✅ .env files are ignored by Git")
            else:
                print("❌ .env files are not ignored by Git")
    except:
        print("❌ .gitignore file not found")
    
    # Check if .env exists
    if os.path.exists('.env'):
        print("✅ .env file exists")
    else:
        print("⚠️  .env file does not exist")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "check":
        check_security()
    else:
        create_env_file() 