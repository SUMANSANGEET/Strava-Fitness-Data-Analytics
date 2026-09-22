-- ============================================================
-- Bellabeat / Strava Fitness Data Analytics
-- Analytical queries — each maps to a Key Insight from the notebook
-- Run against bellabeat.db
-- ============================================================

-- ------------------------------------------------------------
-- Q1. Activity tier distribution
-- (Insight 1: most user-days are NOT 10k+ steps)
-- ------------------------------------------------------------
SELECT
    ActivityTier,
    COUNT(*)                                            AS UserDays,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM fact_daily_activity), 1) AS PctOfDays
FROM fact_daily_activity
GROUP BY ActivityTier
ORDER BY UserDays DESC;


-- ------------------------------------------------------------
-- Q2. Weekday vs. weekend rhythm
-- (Insight 2: sedentary minutes & steps shift together on weekends)
-- ------------------------------------------------------------
SELECT
    CASE WHEN IsWeekend = 1 THEN 'Weekend' ELSE 'Weekday' END AS DayType,
    ROUND(AVG(TotalSteps), 0)          AS AvgSteps,
    ROUND(AVG(SedentaryMinutes), 0)    AS AvgSedentaryMin,
    ROUND(AVG(VeryActiveMinutes), 1)   AS AvgVeryActiveMin,
    ROUND(AVG(Calories), 0)            AS AvgCalories
FROM fact_daily_activity
GROUP BY DayType;


-- ------------------------------------------------------------
-- Q3. Time-of-day peak (hourly average steps across all users)
-- (Insight 3: identify the natural notification window)
-- ------------------------------------------------------------
SELECT
    Hour,
    ROUND(AVG(StepTotal), 1)   AS AvgSteps,
    ROUND(AVG(TotalIntensity), 2) AS AvgIntensity
FROM fact_hourly_activity
GROUP BY Hour
ORDER BY AvgSteps DESC;
-- Peak hour = top row. Full ORDER BY Hour ASC to see the full daily curve.


-- ------------------------------------------------------------
-- Q4a. Sleep tracking adoption
-- (Insight 4: 24 of 33 users ever logged sleep)
-- ------------------------------------------------------------
SELECT
    COUNT(DISTINCT Id)                                              AS TotalUsers,
    COUNT(DISTINCT CASE WHEN HasSleepData = 1 THEN Id END)          AS UsersWithSleepData,
    ROUND(100.0 * COUNT(DISTINCT CASE WHEN HasSleepData = 1 THEN Id END)
          / COUNT(DISTINCT Id), 1)                                  AS PctUsersLogging
FROM fact_daily_activity;

-- Q4b. Sleep efficiency — share of logged nights below 85%
SELECT
    COUNT(*)                                                        AS LoggedNights,
    SUM(CASE WHEN SleepEfficiencyPct < 85 THEN 1 ELSE 0 END)        AS NightsBelow85Pct,
    ROUND(100.0 * SUM(CASE WHEN SleepEfficiencyPct < 85 THEN 1 ELSE 0 END)
          / COUNT(*), 1)                                            AS PctBelow85
FROM fact_daily_activity
WHERE HasSleepData = 1;


-- ------------------------------------------------------------
-- Q5. Steps vs. same-night sleep duration — Pearson correlation
-- (Insight 5: weak relationship — computed via raw SQL formula
--  since SQLite has no built-in CORR())
-- ------------------------------------------------------------
WITH stats AS (
    SELECT
        AVG(TotalSteps)          AS mean_x,
        AVG(TotalMinutesAsleep)  AS mean_y
    FROM fact_daily_activity
    WHERE HasSleepData = 1
)
SELECT
    ROUND(
        SUM((TotalSteps - stats.mean_x) * (TotalMinutesAsleep - stats.mean_y))
        /
        (
            SQRT(SUM((TotalSteps - stats.mean_x) * (TotalSteps - stats.mean_x)))
            *
            SQRT(SUM((TotalMinutesAsleep - stats.mean_y) * (TotalMinutesAsleep - stats.mean_y)))
        )
    , 3) AS PearsonCorr_Steps_Sleep
FROM fact_daily_activity, stats
WHERE HasSleepData = 1;


-- ------------------------------------------------------------
-- Q6. Persona / segment summary
-- (Insight 7: three data-driven personas from clustering)
-- ------------------------------------------------------------
SELECT
    SegmentName,
    COUNT(*)                       AS NumUsers,
    ROUND(AVG(AvgSteps), 0)        AS AvgSteps,
    ROUND(AVG(AvgVeryActiveMin), 1) AS AvgVeryActiveMin,
    ROUND(AVG(AvgSedentaryMin), 0)  AS AvgSedentaryMin,
    ROUND(AVG(AvgCalories), 0)      AS AvgCalories
FROM dim_user
GROUP BY SegmentName
ORDER BY AvgSteps DESC;


-- ------------------------------------------------------------
-- Q7. Per-user daily engagement (drives Streamlit "user drill-down" view)
-- ------------------------------------------------------------
SELECT
    d.Id,
    u.SegmentName,
    d.ActivityDate,
    d.TotalSteps,
    d.ActivityTier,
    d.SleepEfficiencyPct
FROM fact_daily_activity d
JOIN dim_user u ON u.Id = d.Id
WHERE d.Id = 1503960366   -- swap in any Id for drill-down
ORDER BY d.ActivityDate;

-- ------------------------------------------------------------
-- NOTE: weight-logging adoption (Insight 6, 24% of users) is not
-- reproducible here — weightLogInfo_merged.csv was not part of the
-- three exported cleaned tables, so it isn't in this model. Load
-- weightLogInfo_merged.csv separately (a dim_weight or fact_weight
-- table keyed on Id) if you want that metric queryable too.
-- ------------------------------------------------------------
