// GLOBAL VARIABLES

let maxSpeed = 0;

let alerts = 0;

let watchId = null;

let lastAlertTime = 0;

// REAL DISTANCE TRACKING

let totalDistance = 0;

let lastLatitude = null;

let lastLongitude = null;

// LIVE LOCATION

let cachedLocation = "Fetching Location...";

// BACKEND URL

const API_URL = "http://localhost:5002";

// DISTANCE CALCULATION

function calculateDistance(

    lat1,
    lon1,
    lat2,
    lon2

) {

    const R = 6371;

    let dLat =
        (lat2 - lat1)
        * Math.PI / 180;

    let dLon =
        (lon2 - lon1)
        * Math.PI / 180;

    let a =

        Math.sin(dLat / 2)
        * Math.sin(dLat / 2)

        +

        Math.cos(lat1 * Math.PI / 180)

        *

        Math.cos(lat2 * Math.PI / 180)

        *

        Math.sin(dLon / 2)

        *

        Math.sin(dLon / 2);

    let c =

        2 * Math.atan2(
            Math.sqrt(a),
            Math.sqrt(1 - a)
        );

    return R * c;
}

// START TRIP

function startTrip() {

    totalDistance = 0;

    lastLatitude = null;

    lastLongitude = null;

    fetch(`${API_URL}/start-trip`, {

        method: "POST"

    })

    .then(() => {

        console.log("✅ Trip Started");

        startTracking();

    })

    .catch((err) => {

        console.log(

            "❌ Start Trip Error:",

            err
        );

    });
}

// END TRIP

function endTrip() {

    navigator.geolocation.clearWatch(watchId);

    fetch(`${API_URL}/end-trip`, {

        method: "POST"

    })

    .then(res => res.json())

    .then(data => {

        alert(data.summary);

    })

    .catch((err) => {

        console.log(

            "❌ End Trip Error:",

            err
        );

    });
}

// START TRACKING

function startTracking() {

    watchId = navigator.geolocation.watchPosition(

        async (position) => {

            let latitude =
                position.coords.latitude;

            let longitude =
                position.coords.longitude;

            let speed =
                position.coords.speed;

            // REAL DISTANCE

            if (

                lastLatitude !== null

                &&

                lastLongitude !== null

            ) {

                let distance =
                calculateDistance(

                    lastLatitude,
                    lastLongitude,

                    latitude,
                    longitude
                );

                totalDistance += distance;
            }

            lastLatitude = latitude;

            lastLongitude = longitude;

            // NULL SPEED HANDLING

            if (speed == null) {

                speed = 0;
            }

            // TEST MODE
            // let kmh = 120;

            // FOR REAL SPEED LATER:
            let kmh = speed * 3.6;

            if (isNaN(kmh)) {

                kmh = 0;
            }

            // LIVE SPEED UI

            document.getElementById("speed")
            .innerText =
            kmh.toFixed(2) + " km/h";

            // LIVE LOCATION FETCH

            try {

                let response =
                await fetch(

`https://nominatim.openstreetmap.org/reverse?format=json&accept-language=en&lat=${latitude}&lon=${longitude}`

                );

                let data =
                await response.json();

                let city =

                    data.address.city

                    || data.address.town

                    || data.address.village

                    || data.address.hamlet

                    || "Unknown";

                let state =

                    data.address.state

                    || "";

                cachedLocation =
                `${city}, ${state}`;

            }

            catch (err) {

                console.log(

                    "❌ Location API Error",

                    err
                );

                cachedLocation =
                "Location Unavailable";
            }

            // SHOW LOCATION

            document.getElementById("location")
            .innerText =
            cachedLocation;

            // MAX SPEED

            if (kmh > maxSpeed) {

                maxSpeed = kmh;

                document.getElementById("maxSpeed")
                .innerText =
                maxSpeed.toFixed(2);
            }

            // OVER SPEED

            if (kmh > 100) {

                document.getElementById("status")
                .innerText =
                "OVER SPEEDING";

                document.getElementById("status")
                .style.color =
                "#c0392b";

                // ALERT COOLDOWN

                if (

                    Date.now()
                    - lastAlertTime

                    > 10000

                ) {

                    lastAlertTime =
                    Date.now();

                    alerts++;

                    document.getElementById("alerts")
                    .innerText =
                    alerts;
                }

            }

            else {

                document.getElementById("status")
                .innerText =
                "SAFE DRIVING";

                document.getElementById("status")
                .style.color =
                "#55705c";
            }

            // SEND TO BACKEND

            fetch(`${API_URL}/update-speed`, {

                method: "POST",

                headers: {

                    "Content-Type":
                    "application/json"
                },

                body: JSON.stringify({

                    speed: kmh,

                    distance: totalDistance,

                    location:
                    cachedLocation
                })
            })

            .then(() => {

                console.log(
                    "✅ Speed Sent"
                );

            })

            .catch((err) => {

                console.log(

                    "❌ Backend Error:",

                    err
                );

            });

        },

        // GPS ERROR

        (error) => {

            console.log(

                "❌ GPS Error:",

                error
            );

        },

        // GPS OPTIONS

        {

            enableHighAccuracy: true,

            maximumAge: 0,

            timeout: 5000
        }
    );
}