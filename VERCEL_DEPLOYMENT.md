# ToneGPT Vercel Deployment Guide

## 🚀 Deploy ToneGPT to Vercel

Your ToneGPT app is now configured for Vercel deployment! Here's how to deploy it:

### Prerequisites
1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **GitHub Repository**: Your code is already on GitHub at `https://github.com/GitBenTank/ToneGPT.git`

### Deployment Steps

#### Option 1: Deploy via Vercel Dashboard (Recommended)
1. Go to [vercel.com/dashboard](https://vercel.com/dashboard)
2. Click **"New Project"**
3. Import your GitHub repository: `GitBenTank/ToneGPT`
4. Vercel will automatically detect it's a Python project
5. Configure the following settings:
   - **Framework Preset**: Other
   - **Root Directory**: `/` (leave as default)
   - **Build Command**: `pip install -r requirements.txt`
   - **Output Directory**: Leave empty
   - **Install Command**: `pip install -r requirements.txt`
6. Click **"Deploy"**

#### Option 2: Deploy via Vercel CLI
1. Install Vercel CLI: `npm i -g vercel`
2. In your project directory, run: `vercel`
3. Follow the prompts to link your GitHub repository
4. Deploy with: `vercel --prod`

### Configuration Files Created
- ✅ `vercel.json` - Vercel deployment configuration
- ✅ `package.json` - Node.js package configuration
- ✅ `Procfile` - Process file for web deployment
- ✅ `.vercelignore` - Files to exclude from deployment
- ✅ `requirements.txt` - Updated with Vercel dependencies

### Environment Variables
The following environment variables are automatically set:
- `STREAMLIT_SERVER_PORT=8501`
- `STREAMLIT_SERVER_ADDRESS=0.0.0.0`
- `STREAMLIT_SERVER_HEADLESS=true`
- `STREAMLIT_BROWSER_GATHER_USAGE_STATS=false`

### What Gets Deployed
- ✅ Core ToneGPT application (`streamlit_app.py`)
- ✅ All Python modules (`tonegpt/` directory)
- ✅ UI components (`ui/` directory)
- ✅ Data files (`data/` directory)
- ✅ All 1,631 FM9 blocks and models

### What's Excluded (via .vercelignore)
- ❌ Python cache files (`__pycache__/`)
- ❌ Virtual environments (`.venv/`)
- ❌ Large PDF files (manuals, guides)
- ❌ Test files and development scripts
- ❌ Temporary files

### Expected Performance
- **Cold Start**: ~10-15 seconds (first load)
- **Warm Start**: ~2-3 seconds (subsequent loads)
- **Memory Usage**: ~512MB-1GB (depending on model loading)
- **Timeout**: 60 seconds (Vercel limit)

### Troubleshooting
If deployment fails:
1. Check the Vercel build logs
2. Ensure all dependencies are in `requirements.txt`
3. Verify Python version compatibility
4. Check for any missing data files

### Post-Deployment
After successful deployment:
1. Your app will be available at `https://your-project-name.vercel.app`
2. Test the tone generation functionality
3. Monitor performance in Vercel dashboard
4. Set up custom domain if needed

### Cost Considerations
- **Vercel Free Tier**: 100GB bandwidth, 100GB-hours execution time
- **Pro Tier**: $20/month for unlimited bandwidth and execution time
- **Enterprise**: Custom pricing for high-traffic applications

Your ToneGPT app is now ready for professional deployment! 🎸
