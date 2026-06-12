from flask import Flask, request, jsonify
from flask_cors import CORS
from database import save_trip
from twilio.rest import Client
from voice_alert import speak_alert

import time
from datetime import datetime

# FLASK

app = Flask(__name__)

CORS(app)

# CONFIG

SPEED_LIMIT = 100

# TWILIO

ACCOUNT_SID = "YOUR_TWILIO_SID"

AUTH_TOKEN = "YOUR_TWILIO_TOKEN"

TWILIO_NUMBER = "whatsapp:+14155238886"

EMERGENCY_CONTACTS = [

    "YOUR_PHONE_NUMBER"

]

client = Client(
    ACCOUNT_SID,
    AUTH_TOKEN
)

# GLOBAL VARIABLES

trip_start_time = None

trip_distance = 0

max_speed = 0

overspeed_count = 0

speed_list = []

last_alert_time = 0

current_location = "Unknown"

# DRIVER RATING

def calculate_rating(overspeed):

    if overspeed == 0:

        return 5

    elif overspeed <= 2:

        return 4

    elif overspeed <= 5:

        return 3

    else:

        return 2

# WHATSAPP + AI VOICE ALERT

def send_whatsapp(message):

    # AI VOICE ALERT

    speak_alert(

        "Warning. Overspeed detected. Please reduce your speed."

    )

    # WHATSAPP MESSAGE

    for contact in EMERGENCY_CONTACTS:

        try:

            client.messages.create(

                body=message,

                from_=TWILIO_NUMBER,

                to=f"whatsapp:{contact}"

            )

            print("✅ WhatsApp Sent")

        except Exception as e:

            print("❌ WhatsApp Error:", e)

# START TRIP

@app.route("/start-trip", methods=["POST"])

def start_trip():

    global trip_start_time
    global trip_distance
    global max_speed
    global overspeed_count
    global speed_list

    trip_start_time = time.time()

    trip_distance = 0

    max_speed = 0

    overspeed_count = 0

    speed_list = []

    print("🚗 Trip Started")

    return jsonify({

        "message": "Trip Started"

    })

# UPDATE SPEED

@app.route("/update-speed", methods=["POST"])

def update_speed():

    global trip_distance
    global max_speed
    global overspeed_count
    global speed_list
    global last_alert_time
    global current_location

    try:

        data = request.json

        speed = float(

            data.get("speed", 0)

        )

        distance = float(

            data.get("distance", 0)

        )

        location = data.get(

            "location",

            "Unknown"

        )

        current_location = location

        speed_list.append(speed)

        # REAL DISTANCE

        trip_distance = distance

        # MAX SPEED

        if speed > max_speed:

            max_speed = speed

        print(

            f"🚗 Live Speed: {speed:.2f} km/h"

        )

        # OVER SPEED ALERT

        if speed > SPEED_LIMIT:

            # 30 sec cooldown

            if time.time() - last_alert_time > 30:

                last_alert_time = time.time()

                overspeed_count += 1

                message = f"""

🚨 OVER SPEED ALERT

🚗 Current Speed: {speed:.2f} km/h

⚠ Speed Limit: {SPEED_LIMIT} km/h

🚨 Overspeed Count: {overspeed_count}

📍 Location:
{current_location}

🕒 Time:
{datetime.now().strftime('%H:%M:%S')}

📍 Drive Safely

"""

                # SEND ALERT

                send_whatsapp(message)

                print("🚨 Overspeed Alert Sent")

        return jsonify({

            "status": "updated"

        })

    except Exception as e:

        print("❌ Update Speed Error:", e)

        return jsonify({

            "error": str(e)

        }), 500

# END TRIP

@app.route("/end-trip", methods=["POST"])

def end_trip():

    global trip_start_time

    try:

        total_time = int(

            (time.time() - trip_start_time) / 60

        )

        # DRIVER RATING

        rating = calculate_rating(

            overspeed_count

        )

        # AVERAGE SPEED

        average_speed = 0

        if len(speed_list) > 0:

            average_speed = (

                sum(speed_list)

                / len(speed_list)

            )

        # SAVE TO MYSQL

        save_trip(

            trip_distance,

            average_speed,

            max_speed,

            overspeed_count,

            rating,

            f"{total_time} Minutes",

            current_location
        )

        # TRIP SUMMARY

        summary = f"""

🏁 TRIP COMPLETED

🚗 Total Distance: {trip_distance:.2f} KM

⏱ Total Time: {total_time} Minutes

🚨 Overspeed Events: {overspeed_count}

⭐ Driver Safety Rating: {rating}/5

📍 Last Location: {current_location}

🕒 Trip Ended: {datetime.now().strftime('%H:%M:%S')}

✅ Drive Safely

"""

        # SEND SUMMARY

        send_whatsapp(summary)

        print("🏁 Trip Summary Sent")

        return jsonify({

            "summary": summary

        })

    except Exception as e:

        print("❌ End Trip Error:", e)

        return jsonify({

            "error": str(e)

        }), 500

# GET ALL TRIPS

@app.route("/get-trips")

def get_trips():

    try:

        import mysql.connector

        # MYSQL CONNECTION

        conn = mysql.connector.connect(

            host="localhost",

            user="root",

            password="YOUR_MYSQL_PASSWORD",

            database="speed_alert_system"
        )

        cursor = conn.cursor(

            dictionary=True
        )

        # FETCH DATA

        cursor.execute(

            "SELECT * FROM trips ORDER BY id DESC"
        )

        trips = cursor.fetchall()

        conn.close()

        return jsonify(trips)

    except Exception as e:

        print(

            "❌ Dashboard Error:",

            e
        )

        return jsonify({

            "error": str(e)

        })
    
# HOME

@app.route("/")

def home():

    return "🚗 Smart Speed Alert Backend Running"

# RUN APP

if __name__ == "__main__":

    print("🚀 Starting Smart Speed Alert Backend")

    app.run(

        host="0.0.0.0",

        port=5002,

        debug=True
    )