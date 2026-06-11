CREATE OR REPLACE TABLE `project-7792d7ca-4ff6-4f52-91b.gold.mart_machine_daily_kpi`
AS

SELECT
    s.event_date,
    s.machine_id,
    m.machine_name,
    m.location,
    m.machine_type,

    AVG(s.temperature) AS avg_temperature,
    MAX(s.temperature) AS max_temperature,
    MIN(s.temperature) AS min_temperature,

    SUM(CAST(s.object_detected_flag AS INT64)) AS object_detection_count,
    SUM(CAST(s.buzzer_active_flag AS INT64)) AS buzzer_count,

    COUNT(*) AS total_events

FROM `project-7792d7ca-4ff6-4f52-91b.silver.silver_sensor_data` s

INNER JOIN `project-7792d7ca-4ff6-4f52-91b.silver.silver_machine_master` m
ON s.machine_id = m.machine_id

GROUP BY
    s.event_date,
    s.machine_id,
    m.machine_name,
    m.location,
    m.machine_type;