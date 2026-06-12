// API URL

const API_URL = "http://127.0.0.1:5002/get-trips";

// LOAD DASHBOARD DATA

async function loadTrips() {

    try {

        // FETCH DATA FROM BACKEND

        let response = await fetch(

            API_URL
        );

        let trips = await response.json();

        // TABLE BODY

        let table = document.getElementById(

            "tripTable"
        );

        // CLEAR OLD DATA

        table.innerHTML = "";

        // TOTAL STATS

        let totalTrips = trips.length;

        let totalAlerts = 0;

        let averageRating = 0;

        // LOOP THROUGH TRIPS

        trips.forEach((trip) => {

            totalAlerts += trip.overspeed_count;

            averageRating += trip.rating;

            // CREATE TABLE ROW

            let row = `

                <tr>

                    <td>${trip.id}</td>

                    <td>${Number(trip.total_distance).toFixed(2)} KM</td>

                    <td>${Number(trip.average_speed).toFixed(2)} km/h</td>

                    <td>${Number(trip.max_speed).toFixed(2)} km/h</td>

                    <td>${trip.overspeed_count}</td>

                    <td>${trip.rating}/5</td>

                    <td>${trip.location}</td>

                </tr>

            `;

            table.innerHTML += row;
        });

        // AVERAGE RATING

        if (totalTrips > 0) {

            averageRating =
                averageRating / totalTrips;
        }

        // UPDATE DASHBOARD STATS

        document.getElementById(

            "totalTrips"
        ).innerText = totalTrips;

        document.getElementById(

            "totalAlerts"
        ).innerText = totalAlerts;

        document.getElementById(

            "averageRating"
        ).innerText =
            averageRating.toFixed(1);

    }

    catch (error) {

        console.log(

            "❌ Dashboard Error:",

            error
        );
    }
}

// AUTO LOAD

loadTrips();

// AUTO REFRESH EVERY 5 SEC

setInterval(

    loadTrips,

    5000
);