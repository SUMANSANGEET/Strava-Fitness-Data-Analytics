# 🏃 STRAVA FITNESS DATA ANALYTICS

### Interactive Fitness Behavior, Activity & Wellness Analytics Dashboard

> **An end-to-end Data Analytics case study transforming wearable fitness data into interactive business insights using Python, DuckDB, Pandas, Plotly, and Streamlit.**

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Interactive%20Dashboard-FF4B4B?logo=streamlit)](https://streamlit.io/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas)](https://pandas.pydata.org/)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive%20Visuals-3F4F75?logo=plotly)](https://plotly.com/)
[![DuckDB](https://img.shields.io/badge/DuckDB-Analytics%20SQL-FFF000?logo=duckdb)](https://duckdb.org/)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-181717?logo=github)](https://github.com/)

---

## 🌐 Live Interactive Dashboard

### 🚀 Explore the deployed application

**Strava Fitness Data Analytics Dashboard:https://strava-fitness-data-analytics-5axdpravmv6anttketqop4.streamlit.app/**

The dashboard provides an interactive analytical experience for exploring:

* 📊 Fitness KPIs
* 👟 Daily activity patterns
* 🔥 Calories and activity intensity
* 😴 Sleep behavior
* 📈 Steps and fitness relationships
* 🗓️ Weekday/weekend patterns
* 🧩 User segmentation
* 🔗 Correlation analysis
* 🧠 Data-driven fitness insights

> **Live Demo:** Open the Streamlit application from the repository's project links.

---

# 📌 Executive Summary

The **Strava Fitness Data Analytics Case Study** is an end-to-end analytics project designed to demonstrate how raw wearable-device data can be transformed into actionable insights through a combination of:

**Data Engineering → Data Cleaning → Exploratory Data Analysis → SQL Analytics → Statistical Analysis → Interactive Visualization → Business Insights**

The project analyzes activity, movement, calories, sleep, intensity, heart-rate, and weight-related data to understand behavioral patterns and relationships within fitness-tracking data.

Rather than presenting static charts, the project converts analytical outputs into an **interactive Streamlit dashboard**, allowing users and recruiters to explore different dimensions of fitness behavior.

---

# 🎯 Business Problem

Fitness platforms generate large volumes of behavioral data, but raw tracking data alone does not provide meaningful business insight.

The analytical challenge is:

> **How can wearable fitness data be transformed into meaningful insights about activity, exercise intensity, calories, sleep, and user behavior?**

This project addresses that challenge by building a reusable analytics workflow capable of:

* Identifying activity trends
* Comparing movement behavior
* Understanding calorie expenditure
* Exploring sleep patterns
* Measuring relationships between fitness variables
* Segmenting users based on behavioral characteristics
* Presenting insights through an interactive dashboard

---

# 🎯 Project Objectives

### 1. Understand User Activity

Analyze:

* Total steps
* Total distance
* Active minutes
* Sedentary minutes
* Daily movement patterns

### 2. Analyze Calorie Expenditure

Investigate relationships between:

* Steps
* Activity intensity
* Distance
* Active minutes
* Calories burned

### 3. Analyze Sleep Behavior

Explore:

* Total minutes asleep
* Total time in bed
* Sleep efficiency
* Sleep/activity relationships

### 4. Identify Behavioral Patterns

Analyze:

* Day-of-week patterns
* Weekend vs weekday behavior
* Activity intensity
* Sedentary behavior

### 5. Build Interactive Visual Analytics

Create recruiter-friendly visualizations using:

* Plotly
* Streamlit
* KPI cards
* Interactive filters
* Scatter plots
* Correlation matrices
* Heatmaps
* Distribution charts
* Segmentation visuals

### 6. Generate Business Insights

Translate analytical findings into practical insights that can support:

* Fitness-product strategy
* User engagement
* Personalized recommendations
* Wellness analytics
* Customer segmentation
* Product feature development

---

# 💼 Business Use Cases

## 🏋️ Fitness & Wellness Platforms

Understand how users interact with fitness-tracking features.

## 📱 Fitness Application Analytics

Identify:

* Active users
* Engagement patterns
* Activity intensity
* Usage behavior

## 🎯 User Segmentation

Group users based on behavioral characteristics such as:

* Activity level
* Steps
* Calories
* Sleep
* Sedentary behavior

## 🔔 Personalized Engagement

Insights can support personalized:

* Activity reminders
* Workout recommendations
* Sleep suggestions
* Goal-setting experiences

## 📊 Product Analytics

Fitness companies can use similar analytics workflows to evaluate:

* Feature engagement
* User behavior
* Activity trends
* Retention-related signals

---

# 🧩 Dataset

The project works with wearable fitness-tracker data containing multiple granularities of activity and wellness information.

The repository includes data covering areas such as:

| Dataset Category  | Examples                                    |
| ----------------- | ------------------------------------------- |
| Daily Activity    | Steps, distance, calories, activity minutes |
| Daily Calories    | Daily calorie expenditure                   |
| Daily Intensities | Light, moderate and high-intensity activity |
| Daily Steps       | Daily step measurements                     |
| Hourly Activity   | Hour-level movement and calorie patterns    |
| Minute Activity   | Fine-grained activity measurements          |
| Sleep             | Sleep duration and time in bed              |
| Heart Rate        | Heart-rate observations                     |
| Weight            | Weight and BMI-related logs                 |

The source dataset is a publicly available Fitbit fitness-tracker dataset containing activity, sleep, heart-rate and related wearable measurements.

### ⚠️ Data Limitation

The dataset represents a relatively small sample of consenting fitness-tracker users and a limited observation period. Therefore, results should be interpreted as **exploratory patterns within the dataset**, not as population-level health conclusions.

---

# 🏗️ Project Architecture

```text
                  ┌─────────────────────────┐
                  │    Raw Fitness Data     │
                  │ CSV / Excel Datasets    │
                  └────────────┬────────────┘
                               │
                               ▼
                  ┌─────────────────────────┐
                  │    Data Ingestion       │
                  │ Pandas + DuckDB         │
                  └────────────┬────────────┘
                               │
                               ▼
                  ┌─────────────────────────┐
                  │ Data Cleaning & QA       │
                  │ Missing Values           │
                  │ Duplicates               │
                  │ Data Types               │
                  │ Date Transformation      │
                  └────────────┬────────────┘
                               │
                               ▼
                  ┌─────────────────────────┐
                  │ Feature Engineering      │
                  │ KPIs                     │
                  │ Sleep Efficiency         │
                  │ Day-of-Week              │
                  │ Activity Metrics         │
                  └────────────┬────────────┘
                               │
                               ▼
              ┌──────────────────────────────────┐
              │ Exploratory & Statistical        │
              │ Analysis                         │
              │                                  │
              │ Correlation                      │
              │ Distribution                     │
              │ Trend Analysis                   │
              │ Segmentation                     │
              └───────────────┬──────────────────┘
                              │
                              ▼
                  ┌─────────────────────────┐
                  │ Interactive Analytics   │
                  │ Plotly + Streamlit      │
                  └────────────┬────────────┘
                               │
                               ▼
                  ┌─────────────────────────┐
                  │ Business Insights       │
                  │ & Recommendations       │
                  └─────────────────────────┘
```

---

# 🔄 Analytics Workflow

## Phase 1 — Data Collection

Collected and organized the available wearable fitness datasets.

## Phase 2 — Data Preparation

Performed:

* Schema inspection
* Data-type validation
* Missing-value analysis
* Duplicate detection
* Date/time conversion
* Column standardization
* Dataset integration

## Phase 3 — Data Transformation

Created analytical features including:

* Day of week
* Weekend indicator
* Activity categories
* Sleep efficiency
* Aggregated daily metrics
* User-level metrics
* Correlation features

## Phase 4 — Exploratory Data Analysis

Investigated:

* Activity distributions
* Steps
* Calories
* Distance
* Sleep
* Activity intensity
* Sedentary behavior

## Phase 5 — Analytical Modeling

Applied analytical techniques such as:

* Aggregation
* Correlation analysis
* Segmentation
* Trend analysis
* Comparative analysis
* Statistical exploration

## Phase 6 — Visualization

Developed interactive Plotly visualizations embedded inside Streamlit.

## Phase 7 — Dashboard

Converted the analysis into an interactive analytics product rather than a static notebook.

---

# 📊 Dashboard Experience

The Streamlit application is designed around a recruiter-friendly analytics workflow.

## 🏠 Executive Overview

Provides a high-level view of the dataset using KPI cards and summary metrics.

Typical KPI categories include:

```text
👥 Users
👟 Steps
🔥 Calories
📍 Distance
🏃 Active Minutes
😴 Sleep
```

The objective is to give decision-makers an immediate understanding of the dataset before moving into deeper analysis.

---

# 📈 Visual Analytics

## 👟 Steps Analysis

Interactive charts explore:

* Daily steps
* Step distributions
* User-level activity
* Day-of-week patterns

### Business Question

> When and how frequently are users physically active?

---

# 🔥 Calories Analysis

Examines calorie expenditure against activity-related variables.

Potential relationships include:

```text
Steps
   │
   ├──────────────► Calories
   │
Activity Minutes
   │
   └──────────────► Calories
```

This allows users to investigate whether greater activity levels are associated with greater energy expenditure.

---

# 🏃 Activity Intensity

Activity is explored through categories such as:

* Sedentary
* Lightly Active
* Fairly Active
* Very Active

The dashboard allows comparison of activity intensity and its relationship with other fitness metrics.

---

# 😴 Sleep Analytics

Sleep analysis focuses on:

* Total minutes asleep
* Total time in bed
* Sleep efficiency
* Sleep/activity relationships

### Example analytical metric

```text
Sleep Efficiency
=
Total Minutes Asleep
────────────────────
Total Time In Bed
× 100
```

This transforms raw sleep measurements into a more interpretable KPI.

---

# 🔗 Correlation Analysis

A correlation matrix is used to investigate relationships between numerical fitness variables.

Example variables:

```text
Steps
Distance
Calories
Active Minutes
Sedentary Minutes
Sleep
```

The purpose is **exploratory**, not causal inference.

> Correlation between two variables does not establish that one variable causes the other.

---

# 🧩 User Segmentation

Behavioral segmentation can be used to identify different user profiles based on fitness metrics.

Example conceptual segments:

```text
                FITNESS USERS
                     │
       ┌─────────────┼─────────────┐
       │             │             │
   Highly Active  Moderate      Low Activity
       │             │             │
   High Steps     Balanced      Sedentary
   High Activity  Behavior      Behavior
```

This can support personalized engagement and fitness-product analytics.

---

# 📊 Key Analytical Questions

The project investigates questions such as:

### Activity

* How active are users on a typical day?
* What are the dominant activity levels?
* How do steps vary across days?

### Calories

* How are calories related to steps?
* How does activity intensity relate to calorie expenditure?
* Which activity metrics are most strongly associated with calories?

### Sleep

* How much do users sleep?
* How much time do users spend in bed?
* How does sleep efficiency vary?
* What relationships exist between activity and sleep?

### Behavior

* How does weekday behavior differ from weekend behavior?
* How much time do users spend sedentary?
* Are there distinct behavioral user segments?

---

# 💡 Business Insights Framework

Rather than treating every statistical relationship as a business conclusion, the project uses a structured framework:

```text
DATA
  ↓
PATTERN
  ↓
STATISTICAL RELATIONSHIP
  ↓
BUSINESS INTERPRETATION
  ↓
ACTIONABLE OPPORTUNITY
```

This helps separate:

**What the data shows**

from

**What the business might investigate next.**

---

# 📌 Recommendations Framework

Based on the observed behavioral patterns, a fitness platform could investigate:

### 1. Personalized Activity Goals

Use historical activity behavior to create personalized targets.

### 2. Engagement Notifications

Use activity patterns to identify opportunities for contextual reminders.

### 3. Sleep-Aware Experiences

Combine sleep and activity information to create more holistic wellness dashboards.

### 4. User Segmentation

Develop different engagement strategies for different behavioral profiles.

### 5. Fitness KPI Monitoring

Track:

* Steps
* Calories
* Active minutes
* Sleep
* Sedentary time

through a unified dashboard.

> These are analytical opportunities rather than medical recommendations.

---

# 🛠️ Technology Stack

| Category             | Technology                           |
| -------------------- | ------------------------------------ |
| Programming          | Python                               |
| Data Manipulation    | Pandas, NumPy                        |
| Analytics SQL        | DuckDB                               |
| Visualization        | Plotly                               |
| Dashboard            | Streamlit                            |
| Statistical Analysis | SciPy / Statsmodels where applicable |
| Machine Learning     | Scikit-learn where applicable        |
| Data Storage         | CSV / Excel / analytical extracts    |
| Development          | Jupyter Notebook / Python            |
| Version Control      | Git & GitHub                         |
| Deployment           | Streamlit Cloud                      |

---

# 📂 Repository Structure

```text
STRAVA FITNESS DATA ANALYTICS CASE-STUDY/
│
├── app.py
├── requirements.txt
├── README.md
│
├── STRAVA FITNESS DATA ANALYTICS CASE-STUDY.ipynb
├── STRAVA FITNESS APP.pptx
│
├── data/
│   ├── correlation_matrix.csv
│   ├── daily_activity.csv
│   ├── dow_agg.csv
│   ├── hourly_heatmap.csv
│   ├── sleep_efficiency.csv
│   ├── sleep_scatter.csv
│   ├── steps_vs_sleep.csv
│   ├── user_segments.csv
│   └── weight_log.csv
│
├── figures/
│   └── 02_steps_vs_calories.png
│
└── Data Files/
    └── mturkfitbit_export_4.12.16-5.12.16/
        └── Fitabase Data/
            ├── dailyActivity_merged.csv
            ├── dailyCalories_merged.csv
            ├── dailyIntensities_merged.csv
            ├── dailySteps_merged.csv
            ├── hourlyCalories_merged.csv
            ├── hourlyIntensities_merged.csv
            ├── hourlySteps_merged.csv
            ├── minuteCaloriesNarrow_merged.csv
            ├── minuteCaloriesWide_merged.csv
            ├── minuteIntensitiesNarrow_merged.csv
            ├── minuteIntensitiesWide_merged.csv
            ├── minuteMETsNarrow_merged.csv
            ├── minuteSleep_merged.csv
            ├── minuteStepsNarrow_merged.csv
            ├── minuteStepsWide_merged.csv
            ├── sleepDay_merged.csv
            ├── weightLogInfo_merged.csv
            └── heartrate_seconds_merged.csv
```

---

# ⚙️ Installation & Setup

## 1. Clone the repository

```bash
git clone https://github.com/SUMANSANGEET/Strava-Fitness-Data-Analytics.git
```

## 2. Navigate into the project

```bash
cd Strava-Fitness-Data-Analytics
```

## 3. Create a virtual environment

```bash
python -m venv venv
```

## 4. Activate the environment — Windows

```bash
venv\Scripts\activate
```

## 5. Install dependencies

```bash
pip install -r requirements.txt
```

## 6. Run the Streamlit dashboard

```bash
streamlit run app.py
```

The application will open in your browser.

---

# ☁️ Deployment

The dashboard is designed for deployment through **Streamlit Cloud**.

Deployment workflow:

```text
GitHub Repository
       ↓
requirements.txt
       ↓
Streamlit Cloud
       ↓
Dependency Installation
       ↓
app.py
       ↓
Interactive Dashboard
```

---

# 🔍 Data Quality & Analytical Considerations

Wearable-device datasets can contain:

* Missing observations
* Uneven user participation
* Different tracking durations
* Outliers
* Incomplete sleep records
* Different levels of device usage

Therefore, the analysis considers data completeness and consistency before interpreting patterns.

### Important

This project is an **analytics and visualization case study**.

It should not be interpreted as:

* Medical advice
* Clinical research
* Population-level health research
* Causal evidence

---

# 📈 Recruiter Value

This project demonstrates practical skills across the complete analytics lifecycle:

### Data Analytics

* Data cleaning
* Data transformation
* Exploratory analysis
* Statistical analysis
* KPI development

### SQL / Analytics Engineering

* DuckDB
* Analytical queries
* Aggregations
* Dataset integration

### Visualization

* Plotly
* Interactive charts
* Heatmaps
* Correlation analysis
* KPI dashboards

### Python

* Pandas
* NumPy
* Data processing
* Feature engineering

### Business Intelligence

* Business questions
* KPI design
* Segmentation
* Insight generation
* Decision-support dashboards

### Deployment

* Git
* GitHub
* Streamlit
* Cloud deployment

---

# ⭐ Project Highlights

```text
✔ End-to-End Data Analytics Project
✔ Interactive Streamlit Dashboard
✔ DuckDB Analytical SQL
✔ Pandas-Based Data Transformation
✔ Plotly Interactive Visualizations
✔ Fitness KPI Analysis
✔ Activity & Calorie Analytics
✔ Sleep Analytics
✔ Correlation Analysis
✔ User Segmentation
✔ Business Use Cases
✔ GitHub Version Control
✔ Streamlit Cloud Deployment
```

---

# 🧠 What This Project Demonstrates

The key objective of this project is not simply to create charts.

It demonstrates the ability to move from:

> **Raw Data → Analytical Question → Data Preparation → Analysis → Visualization → Insight → Business Opportunity**

This is the workflow expected from a practical **Data Analyst / BI Analyst / Product Analyst** working with behavioral datasets.

---

# 👨‍💻 Author

## **P Suman Sangeet**

**PGDM — Big Data Analytics**
Asia Pacific Institute of Management
Batch: 2025–27

### Core Analytics Skills

```text
Python
SQL
MySQL
DuckDB
Advanced Excel
Power BI
Tableau
Pandas
NumPy
Plotly
Streamlit
Data Visualization
Business Analytics
Statistical Analysis
```

---

# 📬 Project Focus

**Data Analytics | Business Intelligence | Fitness Analytics | Behavioral Analytics | Interactive Dashboards**

---

# 🔖 Tags

`Data Analytics` `Python` `SQL` `DuckDB` `Pandas` `Plotly` `Streamlit` `Fitness Analytics` `Data Visualization` `Business Intelligence` `EDA` `KPI Dashboard` `User Segmentation` `Sleep Analytics` `Activity Analytics` `GitHub Portfolio`

---

## ⭐ If you found this project useful

Feel free to explore the repository, review the analytical workflow, and experiment with the interactive dashboard.

**Built with Python + SQL + Analytics + Visualization + Business Thinking.**
