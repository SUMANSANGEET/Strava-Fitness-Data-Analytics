"""
Bellabeat / Strava Fitness Data Analytics — Streamlit App
Run with: streamlit run app.py
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

from db_utils import (
    load_dim_user, load_daily, load_hourly,
    kpis, tier_distribution, weekday_weekend,
    hourly_heatmap, sleep_stats, steps_sleep_correlation,
    persona_summary,
)

BRAND_COLORS = ["#2E86AB", "#F26419", "#5C946E", "#A23B72", "#F6AE2D", "#8E44AD"]

st.set_page_config(page_title="Bellabeat Fitness Analytics", page_icon="🏃‍♀️", layout="wide")

px.defaults.color_discrete_sequence = BRAND_COLORS
px.defaults.template = "plotly_white"

# ------------------------------------------------------------
# Sidebar: navigation + global persona filter
# ------------------------------------------------------------
st.sidebar.title("🏃‍♀️ Bellabeat Analytics")
page = st.sidebar.radio(
    "Go to",
    ["Overview", "Activity Trends", "Time-of-Day", "Sleep & Wellness", "User Personas"],
)

dim_user = load_dim_user()
daily_all = load_daily()
hourly_all = load_hourly()

segments = sorted(dim_user["SegmentName"].unique())
selected_segments = st.sidebar.multiselect("Filter by persona", segments, default=segments)

st.sidebar.caption(
    "Data: FitBit Fitabase tracking data, 33 users, "
    "04/12/2016 – 05/12/2016. Directional evidence, not a "
    "representative market study."
)

daily = daily_all[daily_all["SegmentName"].isin(selected_segments)]
hourly = hourly_all[hourly_all["SegmentName"].isin(selected_segments)]
dim_user_f = dim_user[dim_user["SegmentName"].isin(selected_segments)]

if daily.empty:
    st.warning("No data for the selected persona filter — pick at least one segment in the sidebar.")
    st.stop()

# ============================================================
# PAGE 1 — Overview
# ============================================================
if page == "Overview":
    st.title("Overview")
    k = kpis(daily)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Users", f"{k['n_users']}")
    c2.metric("Avg Daily Steps", f"{k['avg_steps']:,.0f}")
    c3.metric("% Logging Sleep", f"{k['sleep_logging_pct']:.0f}%")
    c4.metric("Avg Sleep Efficiency", f"{k['avg_sleep_eff']:.1f}%" if not np.isnan(k['avg_sleep_eff']) else "n/a")

    st.markdown("---")
    st.subheader("Activity tier mix")
    tiers = tier_distribution(daily)
    fig = px.bar(tiers, x="ActivityTier", y="PctOfDays", text="PctOfDays",
                 labels={"PctOfDays": "% of user-days"})
    fig.update_traces(texttemplate="%{text}%", textposition="outside")
    st.plotly_chart(fig, width='stretch')
    st.caption(
        "Most user-days are NOT high-intensity (10k+ steps) — messaging built around "
        "'high performer' imagery risks alienating the majority of users."
    )

# ============================================================
# PAGE 2 — Activity Trends
# ============================================================
elif page == "Activity Trends":
    st.title("Activity Trends")

    st.subheader("Weekday vs. weekend rhythm")
    ww = weekday_weekend(daily)
    fig = px.bar(ww.melt(id_vars="DayType", value_vars=["AvgSteps", "AvgSedentaryMin"]),
                 x="DayType", y="value", color="variable", barmode="group",
                 labels={"value": "Average", "variable": "Metric"})
    st.plotly_chart(fig, width='stretch')

    st.subheader("Daily steps over time")
    trend = daily.groupby("ActivityDate")["TotalSteps"].mean().reset_index()
    fig2 = px.line(trend, x="ActivityDate", y="TotalSteps", labels={"TotalSteps": "Avg steps (all users)"})
    st.plotly_chart(fig2, width='stretch')

    st.subheader("Steps distribution by persona")
    fig3 = px.box(daily, x="SegmentName", y="TotalSteps", color="SegmentName")
    fig3.update_layout(showlegend=False)
    st.plotly_chart(fig3, width='stretch')

# ============================================================
# PAGE 3 — Time-of-Day
# ============================================================
elif page == "Time-of-Day":
    st.title("Time-of-Day Patterns")

    pivot = hourly_heatmap(hourly)
    fig = go.Figure(data=go.Heatmap(
        z=pivot.values, x=pivot.columns, y=pivot.index,
        colorscale="Blues", colorbar={"title": "Avg steps"},
    ))
    fig.update_layout(xaxis_title="Hour of day", yaxis_title="Day of week")
    st.plotly_chart(fig, width='stretch')

    hourly_avg = hourly.groupby("Hour")["StepTotal"].mean().reset_index()
    peak_hour = int(hourly_avg.loc[hourly_avg["StepTotal"].idxmax(), "Hour"])
    st.caption(
        f"Peak average step activity occurs around **{peak_hour}:00** — "
        "the natural window for reminder notifications or in-app challenges."
    )

    fig2 = px.line(hourly_avg, x="Hour", y="StepTotal", markers=True,
                    labels={"StepTotal": "Avg steps"})
    st.plotly_chart(fig2, width='stretch')

# ============================================================
# PAGE 4 — Sleep & Wellness
# ============================================================
elif page == "Sleep & Wellness":
    st.title("Sleep & Wellness")

    threshold = st.slider("Sleep efficiency threshold (%)", 50, 100, 85)
    s = sleep_stats(daily, threshold=threshold)

    c1, c2, c3 = st.columns(3)
    c1.metric("Logged nights", f"{s['n_nights']}")
    c2.metric(f"Nights below {threshold}%", f"{s['n_below']}")
    c3.metric("% below threshold", f"{s['pct_below']:.1f}%")

    fig = px.histogram(s["efficiency_series"], nbins=20,
                        labels={"value": "Sleep efficiency (%)"})
    fig.add_vline(x=threshold, line_dash="dash", line_color="#F26419")
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, width='stretch')

    st.subheader("Steps vs. same-night sleep duration")
    corr, scatter_df = steps_sleep_correlation(daily)
    st.caption(f"Pearson correlation: **{corr}** — a weak relationship in this sample.")
    fig2 = px.scatter(scatter_df, x="TotalSteps", y="TotalMinutesAsleep", trendline="ols",
                       labels={"TotalMinutesAsleep": "Minutes asleep"})
    st.plotly_chart(fig2, width='stretch')

    st.info(
        "Avoid marketing claims that imply 'walk more, sleep better' without stronger "
        "evidence — this sample shows only a weak relationship between the two."
    )

# ============================================================
# PAGE 5 — User Personas
# ============================================================
elif page == "User Personas":
    st.title("User Personas")

    summary = persona_summary(dim_user_f)
    st.dataframe(summary, width='stretch', hide_index=True)

    fig = px.bar(summary, x="SegmentName", y="AvgSteps", color="SegmentName", text="NumUsers")
    fig.update_traces(texttemplate="n=%{text}", textposition="outside")
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, width='stretch')

    st.markdown("---")
    st.subheader("User drill-down")
    user_id = st.selectbox("Select a user", sorted(daily["Id"].unique()))
    user_daily = daily[daily["Id"] == user_id].sort_values("ActivityDate")
    seg = user_daily["SegmentName"].iloc[0]
    st.caption(f"Persona: **{seg}**")

    fig2 = px.line(user_daily, x="ActivityDate", y="TotalSteps", markers=True)
    fig2.add_hline(y=10000, line_dash="dash", line_color="#5C946E",
                   annotation_text="10k step goal")
    st.plotly_chart(fig2, width='stretch')
