let reservation_price = 0.0;
let reservation_duration = 0;

function searchParkingLots(){
    console.log("Searching lots...")
}

function confirm() {
    eel.confirmReservation(reservation_duration, reservation_price)().then(function() {
        console.log("Confirmed")
        window.location.href = 'confirmation.html';
    }).catch(function(error) {
        console.error("Error fetching data:", error);
    });
}
function cancel() {
    console.log("cancelled")
    let pk = document.getElementById("parking_lot");
    pk.innerHTML = original_pk;
}
let original_pk = document.getElementById("parking_lot")
function reserve() {
    console.log("Reserve");
    let hours = document.getElementById("num_hours").value;
    let pk = document.getElementById("parking_lot");
    original_pk = pk.innerHTML;
    pk.innerHTML = "";
    eel.getTicketPrice(hours)().then(function(price) {
        reservation_price = price;
        reservation_duration = hours;

        let temp = document.createElement('div');
        temp.style.color = "black"
        let text = `Do you want to reserve a parking spot at Parking Lot 1 for ${hours} hours, for a total of $${price}?`;
        temp.innerHTML = text;

        let confirmBtn = document.createElement("button");
        confirmBtn.innerText = "Confirm";
        confirmBtn.addEventListener("click", function() {
            confirm();
        });

        let cancelBtn = document.createElement("button");
        cancelBtn.innerText = "Cancel";
        cancelBtn.addEventListener("click", function() {
            cancel();
        });

        pk.appendChild(temp)
        pk.appendChild(confirmBtn)
        pk.appendChild(cancelBtn)
    }).catch(function(error) {
        console.error("Error fetching data:", error);
    });
}

eel.getRate()().then(function(rate) {
    console.log(rate)
    let header = document.getElementById("rate");
    header.innerText = header.innerText.replace(/\$\[lot_rate\]/g, rate);
}).catch(function(error) {
    console.error("Error fetching data:", error);
});