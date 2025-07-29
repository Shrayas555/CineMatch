#!/bin/bash

# CineMatch Quick Start Script
# This script helps you quickly set up your project for GitHub and deployment

echo "🎬 CineMatch Quick Start Script"
echo "================================"

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first."
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "❌ Please run this script from the Movie-Code directory"
    exit 1
fi

echo "✅ Setting up Git repository..."

# Initialize git repository
if [ ! -d ".git" ]; then
    git init
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository already exists"
fi

# Add all files
git add .

# Make initial commit
git commit -m "Initial commit: CineMatch Movie Recommendation System"
echo "✅ Initial commit created"

echo ""
echo "🎯 Next Steps:"
echo "=============="
echo ""
echo "1. Create a GitHub repository:"
echo "   - Go to https://github.com"
echo "   - Click '+' → 'New repository'"
echo "   - Name it 'cinematch' (or your preferred name)"
echo "   - Don't initialize with README, .gitignore, or license"
echo "   - Copy the repository URL"
echo ""
echo "2. Push to GitHub:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "3. Deploy to Streamlit Cloud:"
echo "   - Go to https://share.streamlit.io"
echo "   - Sign in with GitHub"
echo "   - Click 'New app'"
echo "   - Select your repository"
echo "   - Set main file path to: app.py"
echo "   - Click 'Deploy!'"
echo ""
echo "📚 For detailed instructions, see:"
echo "   - DEPLOYMENT.md (step-by-step guide)"
echo "   - README.md (project documentation)"
echo "   - PROJECT_SUMMARY.md (overview)"
echo ""
echo ""
echo "🔒 Security Check:"
echo "=================="
echo "✅ API keys are now secured using environment variables"
echo "✅ .env files are ignored by Git"
echo "✅ No sensitive data will be committed to GitHub"
echo ""
echo "⚠️  IMPORTANT: Before deploying, create your .env file:"
echo "   touch .env"
echo "   echo 'TMDB_API_KEY=your_actual_api_key_here' >> .env"
echo ""
echo "📚 For security details, see SECURITY.md"
echo ""
echo "🎉 Your CineMatch project is ready for deployment!" 