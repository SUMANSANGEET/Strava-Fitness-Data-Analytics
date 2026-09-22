"""
Strava / Bellabeat Fitness Analytics — Interactive Case Study Dashboard
Author: P Suman Sangeet (Data Science & AI Intern)

A recruiter-facing, interactive Streamlit deployment of a smart-device fitness
analytics case study (FitBit Fitabase tracking data, 33 users, 04/12/2016-05/12/2016).

Run locally:   streamlit run app.py
Deploy free:   push this folder to a public GitHub repo, then deploy on
               https://share.streamlit.io (Streamlit Community Cloud) pointing
               at app.py — no server config needed beyond requirements.txt.
"""

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
import duckdb

# ──────────────────────────────────────────────────────────────────────────
# PAGE CONFIG & GLOBAL STYLE
# ──────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Strava Fitness Analytics | P Suman Sangeet",
    page_icon="assets/strava_logo.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

BRAND = {
    "blue": "#2E86AB",
    "orange": "#F26419",
    "magenta": "#A23B72",
    "green": "#3CB371",
    "ink": "#1B2430",
    "muted": "#6B7685",
}
TIER_ORDER = ["Sedentary (<5k)", "Lightly Active (5k-7.5k)", "Fairly Active (7.5k-10k)", "Very Active (10k+)"]
TIER_COLORS = {
    "Sedentary (<5k)": "#C7D3DD",
    "Lightly Active (5k-7.5k)": "#7FB3D5",
    "Fairly Active (7.5k-10k)": "#2E86AB",
    "Very Active (10k+)": "#F26419",
}
DOW_ORDER = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
SEG_ORDER = ["Sedentary Users", "Moderately Active Users", "Highly Active Users"]
SEG_COLORS = {"Sedentary Users": "#C7D3DD", "Moderately Active Users": "#2E86AB", "Highly Active Users": "#F26419"}

CUSTOM_CSS = f"""
<style>
:root {{ --cyan:#00E5FF; --orange:#FF6B35; --pink:#FF3CAC; --green:#39FF88; }}
.stApp {{ background: radial-gradient(circle at 8% 8%,rgba(0,229,255,.10),transparent 28%), radial-gradient(circle at 92% 12%,rgba(255,60,172,.09),transparent 25%), linear-gradient(135deg,#050B14 0%,#07111F 50%,#0A1524 100%); color:#F4F8FF; }}
.main {{ background:transparent; }}
#MainMenu,footer {{ visibility:hidden; }}
.stApp::before {{ content:""; position:fixed; inset:0; pointer-events:none; opacity:.11; background-image:linear-gradient(rgba(0,229,255,.06) 1px,transparent 1px),linear-gradient(90deg,rgba(0,229,255,.06) 1px,transparent 1px); background-size:42px 42px; mask-image:linear-gradient(to bottom,black,transparent 88%); }}
.hero {{ position:relative; overflow:hidden; padding:2.35rem 2.5rem; border-radius:24px; background:radial-gradient(circle at 85% 20%,rgba(0,229,255,.30),transparent 25%),radial-gradient(circle at 15% 80%,rgba(255,60,172,.18),transparent 30%),linear-gradient(120deg,#0B1D31,#102C45 48%,#071827); border:1px solid rgba(0,229,255,.24); box-shadow:0 18px 55px rgba(0,0,0,.42),0 0 34px rgba(0,229,255,.08); color:white; margin-bottom:1.6rem; }}
.hero h1 {{ margin:0 0 .4rem; font-size:2.25rem; font-weight:850; letter-spacing:-.035em; text-shadow:0 0 22px rgba(0,229,255,.20); }}
.hero p {{ margin:0; font-size:1.02rem; color:#D9E8F7; line-height:1.55; }}
.hero .tagline {{ display:inline-block; margin-top:1rem; padding:.38rem .9rem; background:rgba(0,229,255,.10); border:1px solid rgba(0,229,255,.28); color:#BDF7FF; border-radius:999px; font-size:.82rem; font-weight:700; }}
.kpi-card {{ background:linear-gradient(145deg,rgba(18,35,56,.88),rgba(8,20,34,.78)); backdrop-filter:blur(14px); border-radius:18px; padding:1.15rem 1.25rem; border:1px solid rgba(159,176,197,.14); border-left:4px solid var(--cyan); height:100%; box-shadow:0 12px 30px rgba(0,0,0,.24),0 0 22px rgba(0,229,255,.05); transition:.18s ease; }}
.kpi-card:hover {{ transform:translateY(-3px); border-color:rgba(0,229,255,.38); box-shadow:0 16px 36px rgba(0,0,0,.32),0 0 26px rgba(0,229,255,.10); }}
.kpi-card .label {{ font-size:.72rem; color:#8EA5BC; text-transform:uppercase; letter-spacing:.10em; font-weight:750; }}
.kpi-card .value {{ font-size:1.72rem; font-weight:850; color:#F5FBFF; margin-top:.18rem; text-shadow:0 0 15px rgba(0,229,255,.10); }}
.kpi-card .sub {{ font-size:.78rem; color:#91A6BB; margin-top:.25rem; }}
.insight-box {{ background:linear-gradient(135deg,rgba(16,35,56,.86),rgba(8,20,34,.78)); backdrop-filter:blur(12px); border-radius:16px; padding:1.05rem 1.25rem; margin-bottom:.8rem; border:1px solid rgba(255,107,53,.16); border-left:4px solid var(--orange); box-shadow:0 10px 28px rgba(0,0,0,.20); color:#DCE8F4; }}
.insight-box b {{ color:#FFF; }}
.persona-card {{ background:linear-gradient(145deg,rgba(17,34,54,.92),rgba(7,17,29,.86)); backdrop-filter:blur(14px); border-radius:18px; padding:1.3rem 1.4rem; box-shadow:0 14px 32px rgba(0,0,0,.25); height:100%; border:1px solid rgba(159,176,197,.13); border-top:5px solid var(--accent); color:#DCE8F4; }}
.persona-card h3 {{ margin-top:0; color:#FFF; }}
.badge {{ display:inline-block; padding:.18rem .62rem; border-radius:999px; background:rgba(0,229,255,.08); border:1px solid rgba(0,229,255,.16); color:#BDF7FF; font-size:.72rem; font-weight:700; margin-right:.3rem; }}
section[data-testid="stSidebar"] {{ background:radial-gradient(circle at 50% 0%,rgba(0,229,255,.10),transparent 32%),linear-gradient(180deg,#06111E,#081625); border-right:1px solid rgba(0,229,255,.12); box-shadow:12px 0 40px rgba(0,0,0,.22); }}
section[data-testid="stSidebar"] * {{ color:#E7F2FC !important; }}
.stButton > button {{ border:1px solid rgba(0,229,255,.28); background:linear-gradient(135deg,rgba(0,229,255,.13),rgba(46,134,171,.18)); color:#E9FBFF; border-radius:12px; box-shadow:0 0 18px rgba(0,229,255,.06); }}
.stButton > button:hover {{ border-color:rgba(0,229,255,.60); box-shadow:0 0 22px rgba(0,229,255,.16); }}
.stTabs [data-baseweb="tab-list"] {{ gap:.4rem; background:rgba(7,18,31,.55); padding:.35rem; border-radius:14px; border:1px solid rgba(0,229,255,.10); }}
.stTabs [data-baseweb="tab"] {{ border-radius:10px; color:#9FB0C5; }}
.stTabs [aria-selected="true"] {{ background:rgba(0,229,255,.10); color:#BDF7FF; }}
h1,h2,h3,h4 {{ color:#F5FAFF !important; letter-spacing:-.02em; }}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────
# DATA LOADING (cached)
# ──────────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    daily = pd.read_csv("data/daily_activity.csv", parse_dates=["ActivityDate"])
    dow_agg = pd.read_csv("data/dow_agg.csv")
    heatmap = pd.read_csv("data/hourly_heatmap.csv", index_col=0)
    heatmap.columns = [int(c) for c in heatmap.columns]
    sleep_scatter = pd.read_csv("data/sleep_scatter.csv")
    sleep_eff = pd.read_csv("data/sleep_efficiency.csv")
    steps_sleep = pd.read_csv("data/steps_vs_sleep.csv")
    weight = pd.read_csv("data/weight_log.csv", parse_dates=["Date"])
    segments = pd.read_csv("data/user_segments.csv")
    corr = pd.read_csv("data/correlation_matrix.csv", index_col=0)
    return daily, dow_agg, heatmap, sleep_scatter, sleep_eff, steps_sleep, weight, segments, corr


daily, dow_agg, heatmap, sleep_scatter, sleep_eff, steps_sleep, weight, segments, corr = load_data()


@st.cache_resource
def get_sql_engine(_daily, _dow_agg, _sleep_scatter, _sleep_eff, _steps_sleep, _weight, _segments):
    """In-memory DuckDB engine so the SQL Analysis page can run real SQL against
    the same tables that power the rest of the dashboard."""
    con = duckdb.connect(database=":memory:")
    con.register("daily_activity", _daily)
    con.register("dow_agg", _dow_agg)
    con.register("sleep_scatter", _sleep_scatter)
    con.register("sleep_efficiency", _sleep_eff)
    con.register("steps_vs_sleep", _steps_sleep)
    con.register("weight_log", _weight)
    con.register("user_segments", _segments)
    return con


sql_engine = get_sql_engine(daily, dow_agg, sleep_scatter, sleep_eff, steps_sleep, weight, segments)

SQL_TABLES = {
    "daily_activity": daily,
    "dow_agg": dow_agg,
    "sleep_scatter": sleep_scatter,
    "sleep_efficiency": sleep_eff,
    "steps_vs_sleep": steps_sleep,
    "weight_log": weight,
    "user_segments": segments,
}

PRESET_QUERIES = {
    "Avg steps & calories by activity tier": """SELECT
    ActivityTier,
    COUNT(*)                    AS user_days,
    ROUND(AVG(TotalSteps), 0)   AS avg_steps,
    ROUND(AVG(Calories), 0)     AS avg_calories,
    ROUND(AVG(SedentaryMinutes), 0) AS avg_sedentary_min
FROM daily_activity
GROUP BY ActivityTier
ORDER BY avg_steps DESC;""",
    "Weekday vs. weekend rhythm": """SELECT
    DayOfWeek,
    ROUND(AVG(AvgSteps), 0)        AS avg_steps,
    ROUND(AVG(AvgSedentaryMin), 0) AS avg_sedentary_min
FROM dow_agg
GROUP BY DayOfWeek
ORDER BY avg_steps DESC;""",
    "Nights below the 85% sleep-efficiency threshold": """SELECT
    COUNT(*) FILTER (WHERE SleepEfficiencyPct < 85) AS nights_below_85,
    COUNT(*)                                         AS total_nights,
    ROUND(100.0 * COUNT(*) FILTER (WHERE SleepEfficiencyPct < 85) / COUNT(*), 1) AS pct_below_85
FROM sleep_efficiency;""",
    "Persona summary from clustering output": """SELECT
    SegmentName,
    COUNT(*)                        AS users,
    ROUND(AVG(AvgSteps), 0)         AS avg_steps,
    ROUND(AVG(AvgVeryActiveMin), 1) AS avg_very_active_min,
    ROUND(AVG(AvgSedentaryMin), 0)  AS avg_sedentary_min,
    ROUND(AVG(AvgCalories), 0)      AS avg_calories
FROM user_segments
GROUP BY SegmentName
ORDER BY avg_steps DESC;""",
    "Top 5 most active users by average steps": """SELECT
    Id,
    SegmentName,
    ROUND(AvgSteps, 0)   AS avg_steps,
    ROUND(AvgCalories, 0) AS avg_calories,
    LoggedDays
FROM user_segments
ORDER BY AvgSteps DESC
LIMIT 5;""",
    "Weight-logging adoption": """SELECT
    COUNT(DISTINCT Id)                              AS users_who_logged_weight,
    COUNT(*)                                         AS total_entries,
    ROUND(COUNT(*) * 1.0 / COUNT(DISTINCT Id), 1)    AS avg_entries_per_user
FROM weight_log;""",
}

PLOTLY_LAYOUT = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(8,20,34,0.42)",
    font=dict(family="Inter, Helvetica, Arial", color="#DCEAF7"),
    margin=dict(t=60, l=10, r=10, b=10),
    legend=dict(orientation="h", y=-0.18, font=dict(color="#B9CDE0")),
    hoverlabel=dict(bgcolor="#0B1D31", bordercolor="#00E5FF", font=dict(color="#F5FBFF")),
    xaxis=dict(gridcolor="rgba(159,176,197,0.10)", zerolinecolor="rgba(0,229,255,0.16)"),
    yaxis=dict(gridcolor="rgba(159,176,197,0.10)", zerolinecolor="rgba(0,229,255,0.16)"),
)


def kpi_card(col, label, value, sub=""):
    col.markdown(
        f"""<div class="kpi-card">
                <div class="label">{label}</div>
                <div class="value">{value}</div>
                <div class="sub">{sub}</div>
            </div>""",
        unsafe_allow_html=True,
    )


# ──────────────────────────────────────────────────────────────────────────
# SIDEBAR — NAVIGATION + GLOBAL FILTERS
# ──────────────────────────────────────────────────────────────────────────
with st.sidebar:

    # ─────────────────────────────────────────────
    # STRAVA BRAND LOGO
    # ─────────────────────────────────────────────
    st.image(
        "assets/strava_logo.png",
        use_container_width=True
    )

    st.markdown(
        """
        <div style="
            text-align:center;
            margin-top:-10px;
            margin-bottom:15px;
        ">
            <h3 style="
                color:#FFFFFF;
                margin-bottom:3px;
                font-size:1.15rem;
            ">
                Strava Fitness Analytics
            </h3>
            <p style="
                color:#B8C4D0;
                font-size:0.78rem;
                margin-top:0;
            ">
                Interactive Fitness Intelligence
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    page = st.radio(
        "Navigate",
        [
            "🏠 Overview",
            "🔥 Activity Insights",
            "😴 Sleep & Recovery",
            "🧬 User Segmentation",
            "🗃️ SQL Analysis",
            "⚖️ Weight & Correlations",
            "💡 Business Recommendations",
            "👤 About the Analyst",
        ],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.markdown("### 🔎 Filters")
    st.caption("Apply to Activity Insights & Sleep pages")
    selected_days = st.multiselect("Day of week", DOW_ORDER, default=DOW_ORDER)
    selected_tiers = st.multiselect("Activity tier", TIER_ORDER, default=TIER_ORDER)
    st.markdown("---")
    st.caption("📊 Dataset: FitBit Fitabase Tracking Data")
    st.caption("33 users · Apr 12 – May 12, 2016")
    st.caption("940 activity logs · 410 sleep logs")

# Apply global filters to a working copy of daily data
daily_f = daily[daily["DayOfWeek"].isin(selected_days) & daily["ActivityTier"].isin(selected_tiers)].copy()
if daily_f.empty:
    st.warning("No data matches the current filters — showing full dataset instead.")
    daily_f = daily.copy()

# ══════════════════════════════════════════════════════════════════════════
# PAGE 1 — OVERVIEW
# ══════════════════════════════════════════════════════════════════════════
if page == "🏠 Overview":
    st.markdown(
        f"""<div class="hero">
                <h1>🏃 Strava Fitness Analytics</h1>
                <p>An interactive fitness intelligence platform transforming
                smart-device activity, sleep, behavioral segmentation and
                wellness data into actionable insights.
                An end-to-end case study turning FitBit smart-device data into actionable business
                insights for <b>Bellabeat</b>, a wellness-technology company for women — covering data
                cleaning, SQL-style aggregation, exploratory analysis, unsupervised ML segmentation,
                and this interactive Streamlit deployment layer.</p>
                <span class="tagline">📌 Prepared by P Suman Sangeet · LABMENTIX Data Analytics &amp; AI Intern</span>
            </div>""",
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)
    kpi_card(c1, "Users Tracked", "33", "Unique FitBit device wearers")
    kpi_card(c2, "Logged Activity Days", f"{len(daily):,}", "Apr 12 – May 12, 2016 (31 days)")
    kpi_card(c3, "Avg. Daily Steps", f"{daily['TotalSteps'].mean():,.0f}", "CDC general-health benchmark: ~7,500")
    kpi_card(c4, "Avg. Daily Calories", f"{daily['Calories'].mean():,.0f}", "kcal burned per user-day")

    st.write("")
    c5, c6, c7, c8 = st.columns(4)
    kpi_card(c5, "Sleep Tracking Adoption", "24 / 33", "73% of users logged sleep at all")
    kpi_card(c6, "Weight Logging Adoption", "8 / 33", "24% — the weakest-adopted feature")
    kpi_card(c7, "Median Sleep Efficiency", f"{sleep_eff['SleepEfficiencyPct'].median():.0f}%", "Time asleep ÷ time in bed")
    kpi_card(c8, "Behavioral Personas Found", "3", "via K-Means clustering on activity features")

    st.write("")
    left, right = st.columns([1.3, 1])
    with left:
        st.subheader("🎯 Business Task")
        st.write(
            "Bellabeat's co-founder wants the marketing analytics team to analyze smart-device usage "
            "data from a comparable fitness tracker (FitBit) in order to uncover behavioral trends and "
            "translate them into growth opportunities for **Bellabeat's own product line and marketing "
            "strategy**. This dashboard operationalizes that analysis into something a stakeholder can "
            "explore interactively rather than read as a static report."
        )
        st.subheader("🛠️ Technology Stack")
        stack_cols = st.columns(3)
        stack_cols[0].markdown("**Data Prep**\n\n- Python (pandas, numpy)\n- Data cleaning & feature engineering")
        stack_cols[1].markdown("**Analysis & ML**\n\n- SQL-style aggregation\n- K-Means clustering (scikit-learn)\n- Statistical correlation (statsmodels)")
        stack_cols[2].markdown("**Visualization**\n\n- Plotly (interactive)\n- Matplotlib / Seaborn (static)\n- **Streamlit** (this app)")
    with right:
        st.subheader("📈 Activity Tier Mix")
        tier_counts = daily["ActivityTier"].value_counts().reindex(TIER_ORDER).reset_index()
        tier_counts.columns = ["ActivityTier", "Days"]
        fig = px.pie(
            tier_counts, names="ActivityTier", values="Days", hole=0.55,
            color="ActivityTier", color_discrete_map=TIER_COLORS,
            category_orders={"ActivityTier": TIER_ORDER},
        )
        fig.update_traces(textinfo="percent", textfont_size=12)
        fig.update_layout(
            **PLOTLY_LAYOUT,
            height=340,
            showlegend=True
        )

        fig.update_layout(
            legend=dict(
                orientation="h",
                y=-0.25,
                font=dict(size=10)
            )
        )
        st.plotly_chart(fig, use_container_width=True)

    st.info(
        "💡 **Use the sidebar** to jump between analysis modules, or filter Activity/Sleep pages by "
        "day of week and activity tier to explore specific behavioral slices of the cohort.",
        icon="💡",
    )

# ══════════════════════════════════════════════════════════════════════════
# PAGE 2 — ACTIVITY INSIGHTS
# ══════════════════════════════════════════════════════════════════════════
elif page == "🔥 Activity Insights":
    st.header("🔥 Activity Insights")
    st.caption(f"Showing {len(daily_f):,} of {len(daily):,} user-days based on current sidebar filters.")

    c1, c2, c3 = st.columns(3)
    kpi_card(c1, "Avg Steps (filtered)", f"{daily_f['TotalSteps'].mean():,.0f}")
    kpi_card(c2, "Avg Calories (filtered)", f"{daily_f['Calories'].mean():,.0f}")
    kpi_card(c3, "Avg Sedentary Minutes (filtered)", f"{daily_f['SedentaryMinutes'].mean():,.0f}",
              f"≈ {daily_f['SedentaryMinutes'].mean()/60:.1f} hrs/day")
    st.write("")

    tab1, tab2, tab3, tab4 = st.tabs(
        ["📊 Step Distribution", "⚡ Steps vs Calories", "📅 Weekly Rhythm", "🕐 Time-of-Day Heatmap"]
    )

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            fig = px.histogram(
                daily_f, x="TotalSteps", nbins=40, color_discrete_sequence=[BRAND["blue"]],
                title="Daily Step Distribution",
            )
            fig.add_vline(x=7500, line_dash="dash", line_color=BRAND["orange"],
                          annotation_text="CDC benchmark (7.5k)", annotation_position="top")
            fig.update_layout(**PLOTLY_LAYOUT, height=420, xaxis_title="Total Steps", yaxis_title="User-days")
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = px.box(
                daily_f, x="ActivityTier", y="TotalSteps", color="ActivityTier",
                category_orders={"ActivityTier": TIER_ORDER}, color_discrete_map=TIER_COLORS,
                title="Steps by Activity Tier",
            )
            fig.update_layout(**PLOTLY_LAYOUT, height=420, showlegend=False, xaxis_title="", yaxis_title="Total Steps")
            st.plotly_chart(fig, use_container_width=True)
        st.markdown(
            f"""<div class="insight-box"><b>Reading this:</b> Sedentary and Very Active days each make up
            ~32% of logged days (303 each), with Lightly/Fairly Active tiers in between. Activity is
            <b>bimodal</b> rather than clustered around a "typical" user — messaging should speak to two
            very different audiences, not one average one.</div>""",
            unsafe_allow_html=True,
        )

    with tab2:
        fig = px.scatter(
            daily_f, x="TotalSteps", y="Calories", color="ActivityTier", size="SedentaryMinutes",
            size_max=18, opacity=0.75, category_orders={"ActivityTier": TIER_ORDER},
            color_discrete_map=TIER_COLORS,
            hover_data={"ActivityDate": True, "DayOfWeek": True, "SedentaryMinutes": True},
            title="Steps vs. Calories Burned (bubble size = sedentary minutes that day)",
            labels={"TotalSteps": "Total Steps", "Calories": "Calories Burned"},
        )
        fig.update_layout(**PLOTLY_LAYOUT, height=480)
        st.plotly_chart(fig, use_container_width=True)
        r = daily_f["TotalSteps"].corr(daily_f["Calories"])
        st.markdown(
            f"""<div class="insight-box"><b>Correlation (steps ↔ calories): {r:.2f}.</b> The relationship is
            strong and expected, but at any given step count, days with more sedentary minutes (larger
            bubbles) tend to burn <i>fewer</i> calories for the same steps — a hook for "move more
            efficiently, not just more" messaging.</div>""",
            unsafe_allow_html=True,
        )

    with tab3:
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(x=dow_agg["DayOfWeek"], y=dow_agg["AvgSteps"], name="Avg Steps",
                              marker_color=BRAND["blue"]), secondary_y=False)
        fig.add_trace(go.Scatter(x=dow_agg["DayOfWeek"], y=dow_agg["AvgSedentaryMin"], name="Avg Sedentary Min",
                                  mode="lines+markers", line=dict(color=BRAND["orange"], width=3)),
                      secondary_y=True)
        fig.update_layout(**PLOTLY_LAYOUT, height=460, title_text="Average Steps & Sedentary Time by Day of Week")
        fig.update_yaxes(title_text="Avg Steps", secondary_y=False)
        fig.update_yaxes(title_text="Avg Sedentary Minutes", secondary_y=True)
        st.plotly_chart(fig, use_container_width=True)
        peak_day = dow_agg.loc[dow_agg["AvgSteps"].idxmax(), "DayOfWeek"]
        low_day = dow_agg.loc[dow_agg["AvgSteps"].idxmin(), "DayOfWeek"]
        st.markdown(
            f"""<div class="insight-box"><b>{peak_day}</b> sees the highest average steps in the cohort,
            while <b>{low_day}</b> sees the lowest — a distinct weekday/weekend rhythm that engagement
            campaigns should be aware of rather than treating every day the same.</div>""",
            unsafe_allow_html=True,
        )

    with tab4:
        fig = px.imshow(
            heatmap.reindex(DOW_ORDER), color_continuous_scale="Tealrose_r", aspect="auto",
            labels=dict(x="Hour of Day", y="Day of Week", color="Avg Steps"),
            title="Average Steps by Hour of Day and Day of Week",
        )
        fig.update_layout(**PLOTLY_LAYOUT, height=460)
        st.plotly_chart(fig, use_container_width=True)
        flat = heatmap.reindex(DOW_ORDER).reset_index().melt(id_vars="index", var_name="Hour", value_name="Steps")
        peak = flat.loc[flat["Steps"].idxmax()]
        st.markdown(
            f"""<div class="insight-box"><b>Peak activity window:</b> {peak['index']} around
            {int(peak['Hour'])}:00, averaging ~{peak['Steps']:.0f} steps in that hour across the cohort —
            the natural window for an in-app reminder or timed challenge push.</div>""",
            unsafe_allow_html=True,
        )

# ══════════════════════════════════════════════════════════════════════════
# PAGE 3 — SLEEP & RECOVERY
# ══════════════════════════════════════════════════════════════════════════
elif page == "😴 Sleep & Recovery":
    st.header("😴 Sleep & Recovery")
    st.caption("410 user-nights of sleep data logged by 24 of the 33 tracked users.")

    c1, c2, c3 = st.columns(3)
    kpi_card(c1, "Sleep-Nights Logged", f"{len(sleep_scatter):,}")
    kpi_card(c2, "Median Sleep Efficiency", f"{sleep_eff['SleepEfficiencyPct'].median():.0f}%")
    kpi_card(c3, "Nights Below 85% Efficiency", f"{(sleep_eff['SleepEfficiencyPct'] < 85).mean():.0%}",
              "Clinical 'good sleep' threshold")
    st.write("")

    col1, col2 = st.columns(2)
    with col1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=sleep_scatter["TotalTimeInBed"], y=sleep_scatter["TotalMinutesAsleep"],
                                  mode="markers", marker=dict(color=BRAND["magenta"], opacity=0.65),
                                  name="User-nights"))
        max_val = sleep_scatter[["TotalTimeInBed", "TotalMinutesAsleep"]].max().max()
        fig.add_trace(go.Scatter(x=[0, max_val], y=[0, max_val], mode="lines",
                                  line=dict(dash="dash", color="gray"), name="Perfect efficiency (y=x)"))
        fig.update_layout(**PLOTLY_LAYOUT, height=420, title="Time Asleep vs. Time in Bed",
                           xaxis_title="Minutes in Bed", yaxis_title="Minutes Asleep")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.histogram(sleep_eff, x="SleepEfficiencyPct", nbins=30, color_discrete_sequence=[BRAND["green"]],
                            title="Sleep Efficiency Distribution")
        fig.add_vline(x=85, line_dash="dash", line_color=BRAND["orange"],
                      annotation_text="Good threshold (85%)", annotation_position="top")
        fig.update_layout(**PLOTLY_LAYOUT, height=420, xaxis_title="Sleep Efficiency (%)", yaxis_title="Nights")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Does daytime activity relate to that night's sleep?")
    fig = px.scatter(
        steps_sleep, x="TotalSteps", y="TotalMinutesAsleep", color="IsWeekend", trendline="ols",
        color_discrete_sequence=[BRAND["blue"], BRAND["orange"]],
        labels={"TotalSteps": "Total Steps That Day", "TotalMinutesAsleep": "Minutes Asleep That Night",
                "IsWeekend": "Weekend"},
    )
    fig.update_layout(**PLOTLY_LAYOUT, height=460)
    st.plotly_chart(fig, use_container_width=True)
    r2 = steps_sleep["TotalSteps"].corr(steps_sleep["TotalMinutesAsleep"])
    strength = "weak/negligible" if abs(r2) < 0.2 else "moderate" if abs(r2) < 0.5 else "strong"
    st.markdown(
        f"""<div class="insight-box"><b>Correlation (steps ↔ sleep minutes): {r2:.2f} — a {strength}
        relationship.</b> Bellabeat should avoid marketing claims implying "walk more, sleep better" on
        evidence this thin — the two behaviors are better positioned as <b>separate wellness pillars</b>
        to track, not causally linked ones.</div>""",
        unsafe_allow_html=True,
    )

# ══════════════════════════════════════════════════════════════════════════
# PAGE 4 — USER SEGMENTATION
# ══════════════════════════════════════════════════════════════════════════
elif page == "🧬 User Segmentation":
    st.header("🧬 User Segmentation — Data-Driven Personas")
    st.write(
        "Rather than treating all 33 users as one segment, each user's **average daily behavior** "
        "(steps, very-active minutes, sedentary minutes, calories) was standardized and clustered with "
        "**K-Means (k=3)** — the most recruiter-visible piece of this project, since it turns unsupervised "
        "ML output directly into a marketing artifact."
    )

    fig = px.scatter(
        segments, x="AvgSteps", y="AvgVeryActiveMin", size="AvgCalories", color="SegmentName",
        category_orders={"SegmentName": SEG_ORDER}, color_discrete_map=SEG_COLORS,
        hover_data={"Id": True, "LoggedDays": True, "AvgSedentaryMin": ":.0f"},
        title="User Segments from K-Means Clustering (bubble size = avg. daily calories)",
        labels={"AvgSteps": "Avg Daily Steps", "AvgVeryActiveMin": "Avg Very Active Minutes/Day"},
        size_max=40,
    )
    fig.update_layout(**PLOTLY_LAYOUT, height=520)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Persona Cards")
    seg_summary = segments.groupby("SegmentName")[
        ["AvgSteps", "AvgVeryActiveMin", "AvgSedentaryMin", "AvgCalories", "LoggedDays"]
    ].mean().reindex(SEG_ORDER)
    counts = segments["SegmentName"].value_counts()

    persona_meta = {
        "Sedentary Users": {
            "accent": "#C7D3DD", "emoji": "🛋️",
            "journey": "Getting Started",
            "note": "Largest segment. Messaging should focus on small, achievable daily wins rather than performance imagery.",
        },
        "Moderately Active Users": {
            "accent": BRAND["blue"], "emoji": "🚶",
            "journey": "Building Consistency",
            "note": "Solid baseline habits with room to grow. Good target for streaks, reminders, and light challenges.",
        },
        "Highly Active Users": {
            "accent": BRAND["orange"], "emoji": "🏃",
            "journey": "Performance",
            "note": "Smallest but most engaged segment. Candidates for advanced metrics, PR tracking, and community/leaderboard features.",
        },
    }

    cols = st.columns(3)
    for i, seg in enumerate(SEG_ORDER):
        row = seg_summary.loc[seg]
        meta = persona_meta[seg]
        with cols[i]:
            st.markdown(
                f"""<div class="persona-card" style="--accent:{meta['accent']}">
                        <h3>{meta['emoji']} {seg}</h3>
                        <span class="badge">{int(counts.get(seg,0))} users</span>
                        <span class="badge">{meta['journey']} journey</span>
                        <p style="margin-top:0.9rem; color:#374151; font-size:0.92rem;">{meta['note']}</p>
                        <hr style="margin:0.8rem 0; border-color:#EEE;">
                        <p style="font-size:0.85rem; margin:0.2rem 0;"><b>Avg Steps/day:</b> {row['AvgSteps']:,.0f}</p>
                        <p style="font-size:0.85rem; margin:0.2rem 0;"><b>Avg Very Active Min:</b> {row['AvgVeryActiveMin']:.1f}</p>
                        <p style="font-size:0.85rem; margin:0.2rem 0;"><b>Avg Sedentary Min:</b> {row['AvgSedentaryMin']:,.0f}</p>
                        <p style="font-size:0.85rem; margin:0.2rem 0;"><b>Avg Calories:</b> {row['AvgCalories']:,.0f}</p>
                        <p style="font-size:0.85rem; margin:0.2rem 0;"><b>Avg Days Logged:</b> {row['LoggedDays']:.0f}/31</p>
                    </div>""",
                unsafe_allow_html=True,
            )

    st.write("")
    with st.expander("📋 View full per-user segment table"):
        st.dataframe(
            segments[["Id", "SegmentName", "AvgSteps", "AvgVeryActiveMin", "AvgSedentaryMin", "AvgCalories", "LoggedDays"]]
            .sort_values(["SegmentName", "AvgSteps"], ascending=[True, False])
            .round(1),
            use_container_width=True, hide_index=True,
        )

# ══════════════════════════════════════════════════════════════════════════
# PAGE 5 — SQL ANALYSIS
# ══════════════════════════════════════════════════════════════════════════
elif page == "🗃️ SQL Analysis":
    st.header("🗃️ SQL Analysis & Insights")
    st.write(
        "Explore the same fitness data through real **DuckDB SQL**. This module is designed "
        "to demonstrate query design, aggregation, segmentation, KPI extraction and "
        "business storytelling — not just display SQL syntax."
    )

    # ── SQL INSIGHT KPI LAYER ───────────────────────────────────────────────
    try:
        sql_kpi_activity = sql_engine.execute("""
            SELECT
                COUNT(*) AS user_days,
                ROUND(AVG(TotalSteps), 0) AS avg_steps,
                ROUND(AVG(Calories), 0) AS avg_calories,
                ROUND(AVG(SedentaryMinutes), 0) AS avg_sedentary_min
            FROM daily_activity;
        """).df().iloc[0]

        sql_kpi_sleep = sql_engine.execute("""
            SELECT
                COUNT(*) AS nights,
                ROUND(AVG(SleepEfficiencyPct), 1) AS avg_sleep_efficiency,
                ROUND(100.0 * COUNT(*) FILTER (WHERE SleepEfficiencyPct < 85) / COUNT(*), 1)
                    AS pct_below_85
            FROM sleep_efficiency;
        """).df().iloc[0]

        sql_kpi_weight = sql_engine.execute("""
            SELECT
                COUNT(DISTINCT Id) AS users_logging_weight,
                COUNT(*) AS weight_entries,
                ROUND(100.0 * COUNT(DISTINCT Id) / 33, 1) AS adoption_pct
            FROM weight_log;
        """).df().iloc[0]

        sql_kpi_segments = sql_engine.execute("""
            SELECT COUNT(DISTINCT SegmentName) AS personas
            FROM user_segments;
        """).df().iloc[0]

        k1, k2, k3, k4 = st.columns(4)
        kpi_card(k1, "SQL User-Days", f"{int(sql_kpi_activity['user_days']):,}",
                 "Rows queried from daily_activity")
        kpi_card(k2, "SQL Avg Steps", f"{sql_kpi_activity['avg_steps']:,.0f}",
                 "AVG(TotalSteps)")
        kpi_card(k3, "SQL Sleep <85%", f"{sql_kpi_sleep['pct_below_85']:.1f}%",
                 "FILTER aggregation")
        kpi_card(k4, "SQL Personas", f"{int(sql_kpi_segments['personas'])}",
                 "COUNT(DISTINCT SegmentName)")
    except Exception as e:
        st.warning(f"SQL KPI layer could not be calculated: {e}")

    st.write("")

    # ── BUSINESS INSIGHTS GENERATED FROM SQL ────────────────────────────────
    st.subheader("🧠 SQL-Derived Business Insights")
    try:
        tier_sql = sql_engine.execute("""
            SELECT ActivityTier,
                   COUNT(*) AS user_days,
                   ROUND(AVG(TotalSteps), 0) AS avg_steps,
                   ROUND(AVG(Calories), 0) AS avg_calories
            FROM daily_activity
            GROUP BY ActivityTier
            ORDER BY avg_steps DESC;
        """).df()

        dow_sql = sql_engine.execute("""
            SELECT DayOfWeek,
                   ROUND(AVG(AvgSteps), 0) AS avg_steps,
                   ROUND(AVG(AvgSedentaryMin), 0) AS avg_sedentary_min
            FROM dow_agg
            GROUP BY DayOfWeek
            ORDER BY avg_steps DESC;
        """).df()

        persona_sql = sql_engine.execute("""
            SELECT SegmentName,
                   COUNT(*) AS users,
                   ROUND(AVG(AvgSteps), 0) AS avg_steps,
                   ROUND(AVG(AvgCalories), 0) AS avg_calories
            FROM user_segments
            GROUP BY SegmentName
            ORDER BY avg_steps DESC;
        """).df()

        weight_sql = sql_engine.execute("""
            SELECT COUNT(DISTINCT Id) AS users,
                   COUNT(*) AS entries,
                   ROUND(COUNT(*) * 1.0 / COUNT(DISTINCT Id), 1) AS avg_entries_per_user
            FROM weight_log;
        """).df().iloc[0]

        top_tier = tier_sql.iloc[0]
        low_tier = tier_sql.iloc[-1]
        peak_day_sql = dow_sql.iloc[0]
        low_day_sql = dow_sql.iloc[-1]
        largest_persona = persona_sql.loc[persona_sql["users"].idxmax()]

        insight_cols = st.columns(3)
        with insight_cols[0]:
            st.markdown(
                f"""<div class="insight-box">
                <b>📈 Activity segmentation:</b><br>
                <b>{top_tier['ActivityTier']}</b> has the highest SQL-derived average
                steps at <b>{top_tier['avg_steps']:,.0f}</b>, while
                <b>{low_tier['ActivityTier']}</b> averages <b>{low_tier['avg_steps']:,.0f}</b>.
                SQL aggregation makes the behavioral gap directly auditable.
                </div>""",
                unsafe_allow_html=True,
            )
        with insight_cols[1]:
            st.markdown(
                f"""<div class="insight-box">
                <b>📅 Weekly rhythm:</b><br>
                <b>{peak_day_sql['DayOfWeek']}</b> ranks highest for average steps
                (<b>{peak_day_sql['avg_steps']:,.0f}</b>), while
                <b>{low_day_sql['DayOfWeek']}</b> is lowest
                (<b>{low_day_sql['avg_steps']:,.0f}</b>).
                This supports day-aware engagement planning.
                </div>""",
                unsafe_allow_html=True,
            )
        with insight_cols[2]:
            st.markdown(
                f"""<div class="insight-box">
                <b>🧬 Persona intelligence:</b><br>
                <b>{largest_persona['SegmentName']}</b> is the largest SQL-derived
                segment with <b>{int(largest_persona['users'])}</b> users.
                Weight logging has only <b>{int(weight_sql['users'])}</b> users represented,
                highlighting a measurable tracking-adoption gap.
                </div>""",
                unsafe_allow_html=True,
            )

        st.dataframe(
            tier_sql,
            use_container_width=True,
            hide_index=True,
        )
    except Exception as e:
        st.error(f"Could not generate SQL-derived insights: {e}")

    st.write("")

    # ── AVAILABLE TABLES ────────────────────────────────────────────────────
    with st.expander("📚 SQL Data Dictionary — Available Tables & Columns", expanded=False):
        for tname, tdf in SQL_TABLES.items():
            st.markdown(f"**`{tname}`** — {len(tdf):,} rows")
            st.code(", ".join(tdf.columns), language="text")

    # ── CURATED QUERIES ─────────────────────────────────────────────────────
    st.subheader("🔍 Curated SQL Queries")
    query_choice = st.selectbox("Pick a business question", list(PRESET_QUERIES.keys()))
    preset_sql = PRESET_QUERIES[query_choice]

    st.code(preset_sql, language="sql")

    try:
        preset_result = sql_engine.execute(preset_sql).df()
        st.success(f"Query executed successfully • {len(preset_result):,} row(s) returned")
        st.dataframe(preset_result, use_container_width=True, hide_index=True)

        # Lightweight visual interpretation for selected SQL output.
        if len(preset_result.columns) >= 2 and not preset_result.empty:
            numeric_cols = preset_result.select_dtypes(include=np.number).columns.tolist()
            label_cols = [c for c in preset_result.columns if c not in numeric_cols]

            if label_cols and numeric_cols:
                visual_col1, visual_col2 = st.columns([1.15, 1])
                with visual_col1:
                    chart_col = st.selectbox(
                        "SQL result metric to visualize",
                        numeric_cols,
                        key=f"sql_metric_{query_choice}",
                    )
                    x_col = label_cols[0]
                    chart_df = preset_result.copy()
                    fig_sql = px.bar(
                        chart_df,
                        x=x_col,
                        y=chart_col,
                        color=x_col,
                        title=f"SQL Result Visualization — {chart_col}",
                        text=chart_col,
                    )
                    fig_sql.update_traces(texttemplate="%{text}", textposition="outside")
                    fig_sql.update_layout(
                        **PLOTLY_LAYOUT,
                        height=390,
                        showlegend=False,
                        xaxis_title="",
                        yaxis_title=chart_col.replace("_", " ").title(),
                    )
                    st.plotly_chart(fig_sql, use_container_width=True)

                with visual_col2:
                    st.markdown("#### 💬 What this query tells a stakeholder")
                    stakeholder_messages = {
                        "Avg steps & calories by activity tier":
                            "Compare behavioral intensity with energy expenditure and identify where engagement is concentrated.",
                        "Weekday vs. weekend rhythm":
                            "Use SQL aggregation to identify the strongest and weakest days for movement and sedentary behavior.",
                        "Nights below the 85% sleep-efficiency threshold":
                            "Quantify the share of logged nights below the selected sleep-efficiency benchmark.",
                        "Persona summary from clustering output":
                            "Translate ML segmentation into a compact SQL-ready business table for BI reporting.",
                        "Top 5 most active users by average steps":
                            "Spot-check the most active user profiles behind the highly active segment.",
                        "Weight-logging adoption":
                            "Measure feature adoption and average logging frequency among users who recorded weight.",
                    }
                    st.markdown(
                        f"""<div class="insight-box">
                        <b>Business interpretation:</b><br>
                        {stakeholder_messages.get(query_choice, "Use the returned SQL table to validate the dashboard's behavioral patterns.")}
                        </div>""",
                        unsafe_allow_html=True,
                    )
    except Exception as e:
        st.error(f"Query failed: {e}")

    # ── CUSTOM READ-ONLY SQL ────────────────────────────────────────────────
    st.write("")
    st.subheader("✍️ SQL Playground — Ask Your Own Business Question")
    st.caption(
        "Run read-only SELECT/WITH queries against the available tables. "
        "Example: compare activity tiers, calculate averages, filter users, or rank segments."
    )

    custom_sql = st.text_area(
        "SQL query",
        value=PRESET_QUERIES["Avg steps & calories by activity tier"],
        height=180,
        label_visibility="collapsed",
    )

    run = st.button("▶️ Run SQL Insight", type="primary")

    if run:
        stripped = custom_sql.strip().lower()

        # Guardrail: permit only read-oriented statements.
        if not (stripped.startswith("select") or stripped.startswith("with")):
            st.error("Only read-only `SELECT` or `WITH ... SELECT` queries are allowed.")
        else:
            blocked = ["insert ", "update ", "delete ", "drop ", "alter ", "create ", "replace ", "truncate ", "copy "]
            if any(token in stripped for token in blocked):
                st.error("Write/DDL operations are blocked. Use a read-only analytical query.")
            else:
                try:
                    result = sql_engine.execute(custom_sql).df()
                    st.success(f"SQL insight generated • {len(result):,} row(s) returned")
                    st.dataframe(result, use_container_width=True, hide_index=True)

                    if result.empty:
                        st.info("The query ran successfully but returned no rows.")
                    else:
                        st.markdown(
                            """<div class="insight-box">
                            <b>🔎 SQL Insight:</b> Use this result to validate a hypothesis,
                            identify a behavioral pattern, or create a KPI that can be promoted
                            into a BI dashboard. The query is executed directly against the
                            in-memory DuckDB session.
                            </div>""",
                            unsafe_allow_html=True,
                        )
                except Exception as e:
                    st.error(f"Query failed: {e}")

# PAGE 6 — WEIGHT & CORRELATIONS
# ══════════════════════════════════════════════════════════════════════════
elif page == "⚖️ Weight & Correlations":
    st.header("⚖️ Weight Logging & Cross-Metric Correlations")

    c1, c2, c3 = st.columns(3)
    n_weight_users = weight["Id"].nunique()
    kpi_card(c1, "Users Who Logged Weight", f"{n_weight_users} / 33", f"{n_weight_users/33:.0%} adoption")
    kpi_card(c2, "Total Weight Entries", f"{len(weight)}")
    kpi_card(c3, "Median Weight Logged", f"{weight['WeightKg'].median():.1f} kg")
    st.write("")

    weight_plot = weight.copy()
    weight_plot["Id"] = weight_plot["Id"].astype(str)
    fig = px.line(
        weight_plot.sort_values("Date"), x="Date", y="WeightKg", color="Id", markers=True,
        title=f"Logged Weight Over Time ({n_weight_users} users who logged at all)",
        labels={"WeightKg": "Weight (kg)"},
    )
    fig.update_traces(line=dict(width=2))
    fig.update_layout(**PLOTLY_LAYOUT, height=440, legend_title_text="User Id")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(
        """<div class="insight-box"><b>Weight logging is the weakest-adopted tracked behavior</b> in the
        dataset — under a quarter of users logged it even once, and most entries were typed in manually
        rather than auto-synced. This is a concrete UX opportunity: friction in logging is a real adoption
        barrier that a smart scale integration could remove.</div>""",
        unsafe_allow_html=True,
    )

    st.subheader("Correlation Overview — All Key Daily Metrics")
    fig = px.imshow(
        corr, text_auto=True, color_continuous_scale="RdBu_r", zmin=-1, zmax=1,
        title="Correlation Matrix — Daily Activity & Sleep Metrics",
    )
    fig.update_layout(**PLOTLY_LAYOUT, height=560)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(
        """<div class="insight-box"><b>Reading this:</b> Steps and distance are near-perfectly correlated
        (as expected), moderate-to-strong positive links exist between active-minute categories and
        calories, and sedentary minutes correlate <b>negatively</b> with sleep duration (-0.60) — the
        strongest cross-domain relationship in the dataset, stronger than the steps↔sleep link on the
        Sleep &amp; Recovery page.</div>""",
        unsafe_allow_html=True,
    )

# ══════════════════════════════════════════════════════════════════════════
# PAGE 7 — BUSINESS RECOMMENDATIONS
# ══════════════════════════════════════════════════════════════════════════
elif page == "💡 Business Recommendations":
    st.header("💡 Key Insights & Recommendations for Bellabeat")

    insights = [
        ("Activity is skewed toward moderate, not high, engagement",
         "A large share of user-days fall in the Sedentary/Lightly Active tiers — most users are not "
         "consistently hitting 10k+ steps, so messaging built around \"high performer\" imagery will "
         "alienate the majority."),
        ("Weekends show a distinct behavior shift",
         "Sedentary minutes and step totals move together differently on weekends vs. weekdays — "
         "engagement campaigns should be day-of-week aware, not one-size-fits-all."),
        ("There's a clear time-of-day activity peak",
         "The hourly heatmap shows a concentrated activity window (typically early evening) — the "
         "natural time slot for reminder notifications or in-app challenges."),
        ("Sleep tracking is under-adopted relative to step tracking",
         "24 of 33 users logged sleep vs. all 33 for steps, and a meaningful share of nights fall below "
         "85% sleep efficiency — an opportunity for Bellabeat to differentiate on sleep coaching, not "
         "just step counting."),
        ("Steps and same-night sleep show only a weak relationship",
         "Bellabeat should avoid marketing claims implying \"walk more, sleep better\" without stronger "
         "evidence from its own first-party data."),
        ("Weight logging is the weakest-adopted feature",
         "Only 24% of users logged weight, mostly via manual entry — friction in logging is a real "
         "adoption barrier relevant to Bellabeat's own app/scale UX."),
        ("Three data-driven user personas emerge from clustering",
         "Sedentary / Moderately Active / Highly Active — a starting point for segmented marketing "
         "rather than a single generic campaign."),
    ]
    for i, (title, body) in enumerate(insights, start=1):
        st.markdown(
            f"""<div class="insight-box"><b>{i}. {title}.</b><br>{body}</div>""",
            unsafe_allow_html=True,
        )

    st.subheader("📋 Recommendations Table")
    rec_df = pd.DataFrame({
        "Insight": [
            "Majority sit below 10k steps/day",
            "Distinct weekday/weekend rhythm",
            "Sleep tracking under-used vs. steps",
            "Low sleep efficiency in a chunk of nights",
            "Weak steps↔sleep correlation",
            "Weight logging has lowest adoption",
            "Three distinct usage personas",
        ],
        "Recommendation": [
            "Reframe messaging from \"elite performance\" to small, achievable daily wins (e.g. \"beat yesterday\") to avoid alienating the majority segment",
            "Schedule push notifications & challenges on weekdays around the identified peak hour; use weekends for lighter, recovery-themed content",
            "Position Bellabeat's sleep-tracking + coaching features as a key differentiator vs. competitors who only emphasize steps",
            "Introduce in-app sleep-hygiene tips triggered when efficiency drops below a threshold",
            "Avoid over-claiming activity improves sleep in marketing copy; market them as two separate wellness pillars users should track independently",
            "Simplify weight-logging UX (e.g. auto-sync via Bellabeat's smart scale) to close the biggest engagement gap",
            "Build three lightweight in-app journeys (Getting Started / Building Consistency / Performance) mapped to the sedentary/moderate/high-active segments",
        ],
    })
    st.dataframe(rec_df, use_container_width=True, hide_index=True)

    st.subheader("⚠️ Limitations & Next Steps")
    st.markdown(
        """
- Sample is small (33 users), short (1 month), from 2016, and demographically unknown — treat findings
  as **hypotheses to validate**, not final conclusions.
- Recommend Bellabeat run this same analysis on its **own first-party user data** (with gender/age known)
  before finalizing campaign spend.
- Next steps: push the cleaned tables into SQL for a queryable model, build a Power BI/Tableau
  exec-level dashboard, and continue extending this Streamlit layer with live data refresh.
        """
    )

# ══════════════════════════════════════════════════════════════════════════
# PAGE 8 — ABOUT THE ANALYST
# ══════════════════════════════════════════════════════════════════════════
elif page == "👤 About the Analyst":
    st.markdown(
        f"""<div class="hero">
                <h1>👤 P Suman Sangeet</h1>
                <p>Data Science &amp; AI Intern — turning raw device data into decisions.</p>
                <span class="tagline">Open to Data Analyst / Data Science opportunities</span>
            </div>""",
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([1.3, 1])
    with col1:
        st.subheader("About this project")
        st.write(
            "This dashboard is the deployment layer of an end-to-end analytics case study: cleaning raw "
            "FitBit smart-device exports, engineering behavioral features, running SQL-style aggregations "
            "and exploratory analysis in Python, applying K-Means clustering for customer segmentation, "
            "and packaging the results as static (Matplotlib/Seaborn) and interactive (Plotly/Streamlit) "
            "visuals aimed at a non-technical marketing stakeholder."
        )
        st.subheader("Skills demonstrated")
        skill_cols = st.columns(2)
        skill_cols[0].markdown(
            "- Data cleaning & feature engineering (pandas)\n"
            "- Exploratory data analysis\n"
            "- Statistical correlation & OLS trendlines\n"
            "- Unsupervised ML (K-Means, StandardScaler)"
        )
        skill_cols[1].markdown(
            "- Interactive visualization (Plotly)\n"
            "- Dashboard engineering (Streamlit)\n"
            "- Business storytelling & recommendations\n"
            "- Static reporting visuals (Matplotlib/Seaborn)"
        )
        st.subheader("Contact")
        st.markdown(
            "✏️ *Update these with your real links before sharing this dashboard:*\n\n"
            "- 📧 Email: `sumansangeet789@gmail.com`\n"
            "- 💼 LinkedIn: `linkedin.com/in/p-suman-sangeet`\n"
            "- 💻 GitHub: `github.com/SUMANSANGEET`\n"
            "- 📄 Resume: link to a hosted PDF"
        )
    with col2:
        st.subheader("Project snapshot")
        st.markdown(
            f"""<div class="persona-card" style="--accent:{BRAND['blue']}">
                    <p><b>📁 Dataset:</b> FitBit Fitabase Tracking Data</p>
                    <p><b>👥 Users:</b> 33</p>
                    <p><b>🗓️ Window:</b> Apr 12 – May 12, 2016</p>
                    <p><b>📊 Records analyzed:</b> 940 activity logs, 410 sleep logs, 67 weight entries</p>
                    <p><b>🧰 Stack:</b> Python, pandas, scikit-learn, statsmodels, Plotly, Matplotlib/Seaborn, Streamlit</p>
                    <p><b>🎯 Deliverable:</b> Bellabeat marketing-strategy recommendations</p>
                </div>""",
            unsafe_allow_html=True,
        )
        st.write("")
        st.info(
            "💡 This entire dashboard runs from data extracted directly out of the original analysis "
            "notebook — every chart reflects real values from the underlying case study.",
            icon="✅",
        )

st.markdown("---")
st.caption("Strava / Bellabeat Fitness Analytics Dashboard · Built with Streamlit + Plotly · Data: FitBit Fitabase Tracking Data (2016)")