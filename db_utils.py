"""
db_utils.py
Data access helpers for the Bellabeat Streamlit app.
All functions read from bellabeat.db (built by build_db.py in the SQL folder).
"""

import sqlite3
from pathlib import Path
import pandas as pd
import streamlit as st

DB_PATH = Path(__file__).parent / "bellabeat.db"


def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)


@st.cache_data
def load_dim_user() -> pd.DataFrame:
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM dim_user", conn)
    conn.close()
    return df


@st.cache_data
def load_daily() -> pd.DataFrame:
    conn = get_connection()
    df = pd.read_sql(
        """
        SELECT d.*, u.SegmentName
        FROM fact_daily_activity d
        JOIN dim_user u ON u.Id = d.Id
        """,
        conn,
        parse_dates=["ActivityDate"],
    )
    conn.close()
    return df


@st.cache_data
def load_hourly() -> pd.DataFrame:
    conn = get_connection()
    df = pd.read_sql(
        """
        SELECT h.*, u.SegmentName
        FROM fact_hourly_activity h
        JOIN dim_user u ON u.Id = h.Id
        """,
        conn,
        parse_dates=["ActivityHour"],
    )
    conn.close()
    return df


# ------------------------------------------------------------
# Derived metrics (operate on already-loaded, already-filtered
# DataFrames so the segment filter applies everywhere)
# ------------------------------------------------------------

def kpis(daily: pd.DataFrame) -> dict:
    n_users = daily["Id"].nunique()
    n_days = len(daily)
    avg_steps = daily["TotalSteps"].mean()
    sleep_logging_pct = (
        daily.groupby("Id")["HasSleepData"].max().mean() * 100
    )
    avg_sleep_eff = daily.loc[daily["HasSleepData"] == 1, "SleepEfficiencyPct"].mean()
    return {
        "n_users": n_users,
        "n_days": n_days,
        "avg_steps": avg_steps,
        "sleep_logging_pct": sleep_logging_pct,
        "avg_sleep_eff": avg_sleep_eff,
    }


def tier_distribution(daily: pd.DataFrame) -> pd.DataFrame:
    order = ["Sedentary (<5k)", "Lightly Active (5k-7.5k)", "Fairly Active (7.5k-10k)", "Very Active (10k+)"]
    out = (
        daily["ActivityTier"].value_counts(normalize=True).mul(100).round(1)
        .reindex(order).reset_index()
    )
    out.columns = ["ActivityTier", "PctOfDays"]
    return out


def weekday_weekend(daily: pd.DataFrame) -> pd.DataFrame:
    g = daily.assign(DayType=daily["IsWeekend"].map({1: "Weekend", 0: "Weekday"}))
    out = g.groupby("DayType").agg(
        AvgSteps=("TotalSteps", "mean"),
        AvgSedentaryMin=("SedentaryMinutes", "mean"),
        AvgVeryActiveMin=("VeryActiveMinutes", "mean"),
        AvgCalories=("Calories", "mean"),
    ).round(1).reset_index()
    return out


def hourly_heatmap(hourly: pd.DataFrame) -> pd.DataFrame:
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    pivot = hourly.pivot_table(
        index="DayOfWeek", columns="Hour", values="StepTotal", aggfunc="mean"
    ).reindex(day_order)
    return pivot


def sleep_stats(daily: pd.DataFrame, threshold: float = 85.0) -> dict:
    logged = daily.loc[daily["HasSleepData"] == 1]
    n_nights = len(logged)
    below = (logged["SleepEfficiencyPct"] < threshold).sum()
    pct_below = 100 * below / n_nights if n_nights else 0
    return {
        "n_nights": n_nights,
        "n_below": int(below),
        "pct_below": pct_below,
        "efficiency_series": logged["SleepEfficiencyPct"],
    }


def steps_sleep_correlation(daily: pd.DataFrame) -> tuple[float, pd.DataFrame]:
    logged = daily.loc[daily["HasSleepData"] == 1, ["TotalSteps", "TotalMinutesAsleep"]].dropna()
    corr = logged["TotalSteps"].corr(logged["TotalMinutesAsleep"])
    return round(corr, 3), logged


def persona_summary(dim_user: pd.DataFrame) -> pd.DataFrame:
    out = dim_user.groupby("SegmentName").agg(
        NumUsers=("Id", "nunique"),
        AvgSteps=("AvgSteps", "mean"),
        AvgVeryActiveMin=("AvgVeryActiveMin", "mean"),
        AvgSedentaryMin=("AvgSedentaryMin", "mean"),
        AvgCalories=("AvgCalories", "mean"),
    ).round(1).sort_values("AvgSteps", ascending=False).reset_index()
    return out
