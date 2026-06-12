import mysql.connector

# MYSQL CONNECTION

db = mysql.connector.connect(

    host="localhost",

    user="root",

    password="YOUR_MYSQL_PASSWORD",

    database="speed_alert_system"
)

cursor = db.cursor()

# SAVE TRIP

def save_trip(

    total_distance,
    average_speed,
    max_speed,
    overspeed_count,
    rating,
    trip_time,
    location
):

    query = """

    INSERT INTO trips (

        total_distance,
        average_speed,
        max_speed,
        overspeed_count,
        rating,
        trip_time,
        location

    )

    VALUES (%s,%s,%s,%s,%s,%s,%s)

    """

    values = (

        total_distance,
        average_speed,
        max_speed,
        overspeed_count,
        rating,
        trip_time,
        location
    )

    cursor.execute(query, values)

    db.commit()

    print("✅ Trip Saved To MySQL")