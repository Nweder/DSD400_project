let isLogin = true;

        function toggleAuth() {
            isLogin = !isLogin;
            document.getElementById("authTitle").innerText = isLogin ? "Login" : "Sign Up";
            document.querySelector("#authForm button").innerText = isLogin ? "Login" : "Sign Up";
            document.getElementById("toggleAuth").innerHTML = isLogin
                ? 'New user? <a href="#" onclick="toggleAuth()">Sign Up</a>'
                : 'Already have an account? <a href="#" onclick="toggleAuth()">Login</a>';
        }

        function handleAuth() {
            let email = document.getElementById("email").value;
            let password = document.getElementById("password").value;

            if (!email || !password) {
                alert("⚠️ Please fill in all fields!");
                return;
            }

            let endpoint = isLogin ? "/api/login" : "/api/signup";
            let userData = { email: email, password: password };

            fetch(`http://yourserver.com${endpoint}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(userData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === "success") {
                    alert("✅ " + (isLogin ? "Logged in successfully!" : "Account created!"));
                    document.getElementById("authForm").classList.add("hidden");
                    document.getElementById("bookingForm").classList.remove("hidden");
                } else {
                    alert("❌ Error: " + data.message);
                }
            })
            .catch(error => alert("❌ An error occurred: " + error));
        }

        function fetchFilteredCars() {
            let brand = document.getElementById("brand").value;
            let size = document.getElementById("size").value;
            let fuelType = document.getElementById("fuelType").value;

            let queryParams = `?brand=${brand}&size=${size}&fuelType=${fuelType}`;

            fetch(`http://yourserver.com/api/get_cars${queryParams}`)
            .then(response => response.json())
            .then(data => {
                alert("✅ Cars fetched successfully!");
                console.log(data);  // Display in console for debugging
            })
            .catch(error => console.error("Error fetching cars:", error));
        }

        function submitBooking() {
            let userId = document.getElementById("userId").value;
            let carId = document.getElementById("carId").value;
            let dateFrom = document.getElementById("dateFrom").value;
            let dateTo = document.getElementById("dateTo").value;

            if (!userId || !carId || !dateFrom || !dateTo) {
                alert("⚠️ Please fill in all fields!");
                return;
            }

            let bookingData = { user_id: userId, car_id: carId, date_from: dateFrom, date_to: dateTo };

            fetch('http://yourserver.com/api/add_booking', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(bookingData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === "Booking added successfully") {
                    alert("✅ Booking confirmed!");
                    document.getElementById("bookingForm").reset();
                } else {
                    alert("⚠️ Error: " + data.error);
                }
            })
            .catch(error => alert("❌ An error occurred: " + error));
        }

        function fetchBookings() {
            fetch('http://yourserver.com/api/get_bookings')
            .then(response => response.json())
            .then(data => {
                let tblBody = document.getElementById("bookingTable").getElementsByTagName('tbody')[0];
                tblBody.innerHTML = ""; // Clear table
                data.forEach(function(booking) {
                    let row = `<tr>
                        <td>${booking.booking_id}</td>
                        <td>${booking.user_id}</td>
                        <td>${booking.car_id}</td>
                        <td>${booking.date_from}</td>
                        <td>${booking.date_to}</td>
                        <td>${booking.status}</td>
                    </tr>`;
                    tblBody.innerHTML += row;
                });
            })
            .catch(error => console.error("Error fetching bookings:", error));
        }