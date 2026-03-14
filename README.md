# Smart Fertilizer Calculator — Web App
ICAR/SAU NPK Recommendations | IFFCO Prices Jan 2025

## Files
```
fertilizer_webapp/
├── app.py            ← Streamlit web app (main file)
├── core.py           ← Calculation logic
├── requirements.txt  ← Dependencies
└── README.md         ← This file
```

---

## Run Locally (Your PC)

### Step 1 — Install Streamlit (one time only)
```bash
pip install streamlit pandas
```

### Step 2 — Run the app
```bash
cd fertilizer_webapp
streamlit run app.py
```

### Step 3 — Open browser
It will automatically open: http://localhost:8501

---

## Deploy FREE on Streamlit Cloud

### Step 1 — Create GitHub account
Go to https://github.com and sign up (free)

### Step 2 — Create a new repository
- Click "New repository"
- Name it: fertilizer-calculator
- Set to Public
- Click "Create repository"

### Step 3 — Upload your files
Upload these 3 files to GitHub:
- app.py
- core.py
- requirements.txt

### Step 4 — Deploy on Streamlit Cloud
1. Go to https://share.streamlit.io
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository: fertilizer-calculator
5. Main file: app.py
6. Click "Deploy!"

### Step 5 — Done!
Your app will be live at:
https://[your-username]-fertilizer-calculator.streamlit.app

---

## Deploy FREE on Render.com (Alternative)

### Step 1 — Push code to GitHub (same as above)

### Step 2 — Go to https://render.com
- Sign up free
- Click "New Web Service"
- Connect your GitHub repo

### Step 3 — Configure
- Build Command: `pip install -r requirements.txt`
- Start Command: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`

### Step 4 — Deploy
Click "Create Web Service" — it deploys automatically!

---

## Features
- 28 crops: Cereals, Oilseeds, Pulses, Commercial, Vegetables
- 9 fertilizer combinations ranked by cost
- Supports Hectare, Bigha, Acre, Katha
- Sulphur alerts for oilseeds/onion
- ICAR/SAU source cited for every crop
- IFFCO official MRP Jan 2025
- Mobile friendly

## Data Sources
- ICAR-IISS Bhopal (wheat, soybean)
- ICAR-CRRI (rice)
- DRMR Bharatpur (mustard)
- ICAR-CICR (cotton)
- AAU Gujarat (tomato)
- SAU (all other crops)
- IFFCO Price List January 2025
