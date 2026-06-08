from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT")
)

cursor = conn.cursor()

# Clear any aborted transaction
conn.rollback()

# Create table automatically
cursor.execute("""
CREATE TABLE IF NOT EXISTS sensor_data_v1 (

    id BIGSERIAL PRIMARY KEY,

    machine_id VARCHAR(50) NOT NULL,

    temperature DOUBLE PRECISION,

    object_detected_flag BOOLEAN DEFAULT FALSE,

    buzzer_active_flag BOOLEAN DEFAULT FALSE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)
""")

conn.commit()

# ---------------- API ---------------- #

@app.route('/sensor', methods=['POST'])
def sensor():

    try:

        data = request.get_json()

        print("DATA RECEIVED:", data)

        machine_id = data.get("machine_id")
        temperature = data.get("temperature")

        # ESP32 sends vibration/current as 0 or 1
        object_detected_flag = bool(data.get("vibration"))
        buzzer_active_flag = bool(data.get("current"))

        query = """
        INSERT INTO sensor_data_v1
        (
            machine_id,
            temperature,
            object_detected_flag,
            buzzer_active_flag
        )
        VALUES (%s, %s, %s, %s)
        """

        values = (
            machine_id,
            temperature,
            object_detected_flag,
            buzzer_active_flag
        )

        print("VALUES:", values)

        cursor.execute(query, values)
        conn.commit()

        return jsonify({
            "message": "success",
            "received_data": data
        })

    except Exception as e:

        conn.rollback()

        print("ACTUAL ERROR:", repr(e))

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# ---------------- DASHBOARD ---------------- #

@app.route('/dashboard')
def dashboard():

    try:

        cursor.execute("""
        SELECT *
        FROM sensor_data_v1
        ORDER BY created_at DESC
        """)

        rows = cursor.fetchall()

    except Exception as e:

        conn.rollback()

        return f"Dashboard Error: {str(e)}"

    html = """
    <html>
    <head>
        <title>IoT Dashboard</title>
        <meta http-equiv="refresh" content="5">

        <style>
            body{
                font-family: Arial;
                background:#f4f4f4;
                padding:20px;
            }

            table{
                width:100%;
                border-collapse:collapse;
                background:white;
            }

            th, td{
                border:1px solid #ddd;
                padding:12px;
                text-align:center;
            }

            th{
                background:#007BFF;
                color:white;
            }
        </style>

    </head>

    <body>

    <h1>Live IoT Sensor Dashboard</h1>

    <table>

        <tr>
            <th>ID</th>
            <th>Machine ID</th>
            <th>Temperature</th>
            <th>Object Detected</th>
            <th>Buzzer Active</th>
            <th>Created At</th>
        </tr>
    """

    for row in rows:

        html += f"""
        <tr>
            <td>{row[0]}</td>
            <td>{row[1]}</td>
            <td>{row[2]} °C</td>
            <td>{row[3]}</td>
            <td>{row[4]}</td>
            <td>{row[5]}</td>
        </tr>
        """

    html += """
    </table>

    </body>
    </html>
    """

    return html

# ---------------- HOME ---------------- #

@app.route('/')
def home():
    return "IoT API Running Successfully"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))