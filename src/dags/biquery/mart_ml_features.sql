INSERT INTO `project-7792d7ca-4ff6-4f52-91b.gold.mart_ml_features1`
(
    machine_id,
    machine_name,
    machine_type,
    location,
    machine_age_days,
    event_date,
    event_hour,
    avg_temperature,
    max_temperature,
    object_detection_count,
    buzzer_count,
    total_events
)

SELECT

    s.machine_id,
    m.machine_name,
    m.machine_type,
    m.location,
    m.machine_age_days,

    s.event_date,
    s.event_hour,

    AVG(s.temperature) AS avg_temperature,
    MAX(s.temperature) AS max_temperature,

    SUM(CAST(s.object_detected_flag AS INT64))
        AS object_detection_count,

    SUM(CAST(s.buzzer_active_flag AS INT64))
        AS buzzer_count,

    COUNT(*) AS total_events

FROM `project-7792d7ca-4ff6-4f52-91b.silver.silver_sensor_data` s

INNER JOIN `project-7792d7ca-4ff6-4f52-91b.silver.silver_machine_master` m
ON s.machine_id = m.machine_id

GROUP BY

    s.machine_id,
    m.machine_name,
    m.machine_type,
    m.location,
    m.machine_age_days,

    s.event_date,
    s.event_hour;