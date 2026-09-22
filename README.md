# 🏃 Strava / Bellabeat Fitness Analytics — Interactive Streamlit Dashboard

A recruiter-friendly, interactive deployment of a smart-device fitness analytics case study
(FitBit Fitabase Tracking Data, 33 users, Apr 12 – May 12 2016), built for the **Bellabeat**
wellness-technology marketing case study.

Every chart in this app is built from **real data extracted directly out of the original
analysis notebook** (`STRAVA_FITNESS_DATA_ANALYTICS__CASE-STUDY.ipynb`) — nothing here is
simulated. The raw CSVs referenced by the notebook lived only on the original author's local
machine, so the underlying values were recovered from the embedded Plotly chart payloads
(940 activity logs, 410 sleep-nights, 33 users' segmentation profile, 67 weight entries, the
hour×day step heatmap, and the full correlation matrix) and reshaped into the `data/` folder
used by this app.

## 📁 Project structure

```
project/
├── app.py                     # Main Streamlit app (7 pages)
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── .streamlit/
│   └── config.toml            # Theme config
└── data/
    ├── daily_activity.csv     # 940 rows: steps, calories, sedentary min, date, tier
    ├── dow_agg.csv            # Avg steps/sedentary min by day of week
    ├── hourly_heatmap.csv     # Avg steps by hour × day-of-week (7×24 grid)
    ├── sleep_scatter.csv      # 410 rows: time in bed vs. time asleep
    ├── sleep_efficiency.csv   # 410 rows: sleep efficiency %
    ├── steps_vs_sleep.csv     # 410 rows: daytime steps vs. that night's sleep, by weekend flag
    ├── weight_log.csv         # 67 rows: weight (kg) over time, by user Id
    ├── user_segments.csv      # 33 rows: K-Means persona per user
    └── correlation_matrix.csv # 8×8 correlation matrix of key daily metrics
```

## 🖥️ Run it locally

```bash
cd project
pip install -r requirements.txt
streamlit run app.py
```

Then open the URL Streamlit prints (usually `http://localhost:8501`).

## ☁️ Deploy it for free (Streamlit Community Cloud) — recommended for your resume/portfolio link

1. Create a new **public** GitHub repository and push this entire `project/` folder to it
   (root of the repo should contain `app.py`, `requirements.txt`, `data/`, `.streamlit/`).
2. Go to **[share.streamlit.io](https://share.streamlit.io)** and sign in with GitHub.
3. Click **"New app"**, pick your repo/branch, and set the main file path to `app.py`.
4. Click **Deploy**. You'll get a public URL like `https://your-app-name.streamlit.app`
   — put this straight on your resume, LinkedIn, and GitHub README.

No extra configuration is needed — `requirements.txt` and `.streamlit/config.toml` are already
set up.

### Other free/low-cost options
- **Hugging Face Spaces** (Streamlit SDK) — similar one-click flow from a GitHub or HF repo.
- **Render / Railway** — use `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
  as the start command.

## ✏️ Before you share this with recruiters

Open `app.py`, go to the **"About the Analyst"** page section near the bottom of the file, and
replace the placeholder contact details (`your.email@example.com`, LinkedIn/GitHub/resume links)
with your real ones.

## 🧰 Tech stack

| Layer | Tools |
|---|---|
| Data prep | Python, pandas, numpy |
| Analysis & ML | K-Means clustering, StandardScaler (scikit-learn), OLS trendlines (statsmodels) |
| Visualization | Plotly (interactive), Matplotlib/Seaborn (static, in the source notebook) |
| Deployment | Streamlit |

## 📊 What's in the dashboard

1. **Overview** — KPIs, business task, tech stack, activity tier mix
2. **Activity Insights** — step distribution, steps vs. calories, weekly rhythm, hour×day heatmap (filterable by day/tier)
3. **Sleep & Recovery** — sleep efficiency, time-in-bed vs. asleep, steps↔sleep correlation
4. **User Segmentation** — K-Means personas (Sedentary / Moderately Active / Highly Active) as persona cards
5. **Weight & Correlations** — weight-over-time chart, full correlation heatmap
6. **Business Recommendations** — insights + recommendations table + limitations
7. **About the Analyst** — recruiter-facing bio, skills, and contact section (⚠️ edit before sharing)

## ⚠️ Limitations (inherited from the source case study)

Sample is small (33 users), short (1 month), from 2016, and demographically unknown — findings
are hypotheses to validate against first-party data, not final conclusions.
