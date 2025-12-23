# Deployment Guide

## Backend Deployment to Render

### Step 1: Prepare Your Repository
1. Ensure all changes are committed and pushed to GitHub
2. Make sure `render.yaml` and `backend_requirements.txt` are in the root directory

### Step 2: Deploy to Render
1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" and select "Blueprint"
3. Connect your GitHub repository: `https://github.com/adityakr1108/Supplier_Performance_Predictor_Analysis.git`
4. Render will automatically detect the `render.yaml` file
5. Click "Apply" to create the service

### Step 3: Configure Environment Variables
Add the following environment variables in the Render dashboard:
- `AZURE_AI_ENDPOINT` - Your Azure AI endpoint URL
- `AZURE_AI_KEY` - Your Azure AI API key
- `AZURE_OPENAI_API_KEY` - Your Azure OpenAI API key
- `AZURE_OPENAI_ENDPOINT` - Your Azure OpenAI endpoint
- `LANGSMITH_API_KEY` - Your LangSmith API key (optional)

The other variables are pre-configured in `render.yaml`.

### Step 4: Get Your Backend URL
Once deployed, your backend will be available at:
```
https://supplier-predictor-backend.onrender.com
```
(The exact URL will be shown in the Render dashboard)

---

## Frontend Deployment to Vercel

### Option 1: Deploy via Vercel CLI

1. Install Vercel CLI:
```bash
npm install -g vercel
```

2. Login to Vercel:
```bash
vercel login
```

3. Deploy from the project root:
```bash
vercel --prod
```

### Option 2: Deploy via Vercel Dashboard

1. Go to [Vercel Dashboard](https://vercel.com/new)
2. Import your GitHub repository: `https://github.com/adityakr1108/Supplier_Performance_Predictor_Analysis.git`
3. Configure the project:
   - **Framework Preset**: Other
   - **Root Directory**: `./` (leave as root)
   - **Build Command**: Leave empty
   - **Output Directory**: Leave empty
   - **Install Command**: `pip install -r frontend_requirements.txt`

4. Add Environment Variables:
   - `BACKEND_API_URL` - Your Render backend URL (e.g., `https://supplier-predictor-backend.onrender.com`)

5. Click "Deploy"

### Important Notes for Streamlit on Vercel

⚠️ **Streamlit applications don't work well on Vercel** because:
- Vercel is designed for serverless functions with short execution times
- Streamlit requires a long-running server process
- WebSocket connections (used by Streamlit) are limited on Vercel

### Alternative: Deploy Frontend to Streamlit Cloud

**Recommended approach for Streamlit apps:**

1. Go to [Streamlit Cloud](https://streamlit.io/cloud)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository: `adityakr1108/Supplier_Performance_Predictor_Analysis`
5. Set main file path: `frontend/app.py`
6. Click "Advanced settings" and add environment variables:
   - `BACKEND_API_URL` - Your Render backend URL
   - Copy other required variables from your `.env` file
7. Click "Deploy"

Your app will be available at: `https://[your-app-name].streamlit.app`

---

## Alternative: Deploy Both to Render

If you prefer to keep everything on one platform:

### Backend on Render (Already configured)
Follow steps above

### Frontend on Render

1. In Render Dashboard, click "New +" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - **Name**: supplier-predictor-frontend
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r frontend_requirements.txt`
   - **Start Command**: `streamlit run frontend/app.py --server.port=$PORT --server.address=0.0.0.0`
4. Add environment variables
5. Click "Create Web Service"

---

## Post-Deployment Configuration

### Update Frontend to Use Backend URL

After deploying the backend, update the frontend code to use the production backend URL.

In `frontend/app.py`, update the API endpoint:

```python
# Use environment variable for backend URL
BACKEND_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000")
```

### Test Your Deployment

1. Test backend health:
```bash
curl https://your-backend-url.onrender.com/health
```

2. Test frontend by visiting your Streamlit Cloud URL

3. Verify that frontend can communicate with backend

---

## Troubleshooting

### Backend Issues
- Check Render logs in the dashboard
- Verify all environment variables are set correctly
- Ensure the health check endpoint returns 200 OK

### Frontend Issues
- Check Streamlit Cloud logs
- Verify BACKEND_API_URL is set correctly
- Check CORS settings in backend if you get connection errors

### CORS Configuration
If frontend can't connect to backend, add CORS middleware in `backend/main.py`:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-url.streamlit.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Estimated Costs

- **Render Free Tier**: 
  - 750 hours/month for web services
  - Services sleep after 15 minutes of inactivity
  - Cold start time: ~30 seconds

- **Streamlit Cloud Free Tier**:
  - 1 private app
  - Unlimited public apps
  - Shared resources

- **Vercel Free Tier** (if used):
  - Not recommended for Streamlit
  - Better for static sites or Next.js apps
