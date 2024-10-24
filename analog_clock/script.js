function updateClock() {
    const now = new Date();
    const seconds = now.getSeconds();
    const minutes = now.getMinutes();
    const hours = now.getHours();

    // Update the analog clock hands
    const secondHand = document.getElementById('second');
    const minuteHand = document.getElementById('minute');
    const hourHand = document.getElementById('hour');

    const secondDegrees = ((seconds / 60) * 360) + 90; // Adding 90 degrees to offset the initial rotation
    const minuteDegrees = ((minutes / 60) * 360) + ((seconds / 60) * 6) + 90; // +6 for each second
    const hourDegrees = ((hours / 12) * 360) + ((minutes / 60) * 30) + 90; // +30 for each minute

    secondHand.style.transform = `rotate(${secondDegrees}deg)`;
    minuteHand.style.transform = `rotate(${minuteDegrees}deg)`;
    hourHand.style.transform = `rotate(${hourDegrees}deg)`;

    // Update the digital time
    const digitalTime = document.getElementById('digital-time');
    digitalTime.innerHTML = now.toLocaleTimeString();
}

// Initial call to display the clock immediately
updateClock();
// Update the clock every second
setInterval(updateClock, 1000);
