-- ============================================================
-- Bellabeat / Strava Fitness Data Analytics — SQL Data Model
-- Star-style schema: 1 dimension (users/personas) + 2 fact tables
-- ============================================================

DROP TABLE IF EXISTS fact_hourly_activity;
DROP TABLE IF EXISTS fact_daily_activity;
DROP TABLE IF EXISTS dim_user;

-- ------------------------------------------------------------
-- dim_user: one row per user, carrying the persona/segment
-- assigned by the clustering step in the notebook.
-- ------------------------------------------------------------
CREATE TABLE dim_user (
    Id                  INTEGER PRIMARY KEY,
    AvgSteps            REAL,
    AvgVeryActiveMin    REAL,
    AvgSedentaryMin     REAL,
    AvgCalories         REAL,
    LoggedDays          INTEGER,
    Segment             INTEGER,
    SegmentName         TEXT
);

-- ------------------------------------------------------------
-- fact_daily_activity: one row per user per day.
-- Activity + sleep already merged upstream in the notebook.
-- ------------------------------------------------------------
CREATE TABLE fact_daily_activity (
    Id                          INTEGER NOT NULL,
    ActivityDate                TEXT NOT NULL,   -- ISO date, YYYY-MM-DD
    TotalSteps                  INTEGER,
    TotalDistance                REAL,
    TrackerDistance               REAL,
    LoggedActivitiesDistance      REAL,
    VeryActiveDistance            REAL,
    ModeratelyActiveDistance      REAL,
    LightActiveDistance           REAL,
    SedentaryActiveDistance       REAL,
    VeryActiveMinutes           INTEGER,
    FairlyActiveMinutes         INTEGER,
    LightlyActiveMinutes        INTEGER,
    SedentaryMinutes            INTEGER,
    Calories                    INTEGER,
    DayOfWeek                   TEXT,
    IsWeekend                   INTEGER,          -- 0/1
    ZeroActivityDay              INTEGER,          -- 0/1
    TotalActiveMinutes           INTEGER,
    ActivityTier                 TEXT,
    TotalMinutesAsleep           REAL,
    TotalTimeInBed                REAL,
    SleepEfficiencyPct            REAL,
    HasSleepData                  INTEGER,          -- 0/1
    PRIMARY KEY (Id, ActivityDate),
    FOREIGN KEY (Id) REFERENCES dim_user(Id)
);

CREATE INDEX idx_daily_date ON fact_daily_activity(ActivityDate);
CREATE INDEX idx_daily_tier ON fact_daily_activity(ActivityTier);
CREATE INDEX idx_daily_weekend ON fact_daily_activity(IsWeekend);

-- ------------------------------------------------------------
-- fact_hourly_activity: one row per user per hour.
-- ------------------------------------------------------------
CREATE TABLE fact_hourly_activity (
    Id                  INTEGER NOT NULL,
    ActivityHour        TEXT NOT NULL,    -- ISO datetime, YYYY-MM-DD HH:MM:SS
    StepTotal           INTEGER,
    Calories             INTEGER,
    TotalIntensity        INTEGER,
    AverageIntensity       REAL,
    Hour                 INTEGER,
    DayOfWeek             TEXT,
    PRIMARY KEY (Id, ActivityHour),
    FOREIGN KEY (Id) REFERENCES dim_user(Id)
);

CREATE INDEX idx_hourly_hour ON fact_hourly_activity(Hour);
CREATE INDEX idx_hourly_dow ON fact_hourly_activity(DayOfWeek);
