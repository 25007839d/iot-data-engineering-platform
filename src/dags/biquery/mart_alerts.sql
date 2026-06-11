CREATE OR REPLACE TABLE `project-7792d7ca-4ff6-4f52-91b.gold.mart_alerts`
AS

WITH alerts AS (

    SELECT
        GENERATE_UUID() AS alert_id,
        s.machine_id,
        m.machine_name,
        m.location,
        m.machine_owner_name,

        'HIGH_TEMPERATURE' AS alert_type,
        'HIGH' AS alert_severity,

        CONCAT(
            'Temperature exceeded threshold. Current Temperature = ',
            CAST(s.temperature AS STRING)
        ) AS alert_message,

        s.created_at AS alert_timestamp,
        FALSE AS email_sent_flag

    FROM `project-7792d7ca-4ff6-4f52-91b.silver.silver_sensor_data` s

    JOIN `project-7792d7ca-4ff6-4f52-91b.silver.silver_machine_master` m
    ON s.machine_id = m.machine_id

    WHERE s.temperature > 40

    UNION ALL

    SELECT
        GENERATE_UUID(),
        s.machine_id,
        m.machine_name,
        m.location,
        m.machine_owner_name,

        'OBJECT_DETECTED',
        'MEDIUM',

        'Object detected by sensor',

        s.created_at,
        FALSE

    FROM `project-7792d7ca-4ff6-4f52-91b.silver.silver_sensor_data` s

    JOIN `project-7792d7ca-4ff6-4f52-91b.silver.silver_machine_master` m
    ON s.machine_id = m.machine_id

    WHERE s.object_detected_flag = TRUE

    UNION ALL

    SELECT
        GENERATE_UUID(),
        s.machine_id,
        m.machine_name,
        m.location,
        m.machine_owner_name,

        'BUZZER_ACTIVE',
        'LOW',

        'Buzzer activated',

        s.created_at,
        FALSE

    FROM `project-7792d7ca-4ff6-4f52-91b.silver.silver_sensor_data` s

    JOIN `project-7792d7ca-4ff6-4f52-91b.silver.silver_machine_master` m
    ON s.machine_id = m.machine_id

    WHERE s.buzzer_active_flag = TRUE
)

SELECT *
FROM alerts;