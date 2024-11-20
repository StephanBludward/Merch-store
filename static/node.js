const NUM_BURGERS = 100; // Number of burgers
const BURGER_SPEED = 2; // Speed of movement

// Function to generate a random number between min and max
function random(min, max) {
    return Math.random() * (max - min) + min;
}

// Burger container
const burgerContainer = document.querySelector('.burger-background');

// Array to store burger data
const burgers = [];

// Create burgers and add to the DOM
for (let i = 0; i < NUM_BURGERS; i++) {
    const burger = document.createElement('div');
    burger.classList.add('burger');
    burger.style.left = `${random(0, window.innerWidth - 50)}px`;
    burger.style.top = `${random(0, window.innerHeight - 50)}px`;

    // Ensure the velocity is never zero
    let dx = random(-BURGER_SPEED, BURGER_SPEED);
    let dy = random(-BURGER_SPEED, BURGER_SPEED);
    while (dx === 0) dx = random(-BURGER_SPEED, BURGER_SPEED); // Prevent dx = 0
    while (dy === 0) dy = random(-BURGER_SPEED, BURGER_SPEED); // Prevent dy = 0

    burger.dataset.dx = dx;
    burger.dataset.dy = dy;

    // Append to the burger container
    burgerContainer.appendChild(burger);

    // Add burger to the array
    burgers.push(burger);
}

// Detect mouse movement
document.addEventListener('mousemove', (e) => {
    const mouseX = e.clientX;
    const mouseY = e.clientY;

    burgers.forEach(burger => {
        const rect = burger.getBoundingClientRect();
        const burgerX = rect.left + rect.width / 2;
        const burgerY = rect.top + rect.height / 2;

        const distance = Math.sqrt(
            Math.pow(burgerX - mouseX, 2) + Math.pow(burgerY - mouseY, 2)
        );

        // If the mouse is close to the burger, make it "swim away"
        if (distance < 100) {
            const angle = Math.atan2(burgerY - mouseY, burgerX - mouseX);
            burger.dataset.dx = Math.cos(angle) * BURGER_SPEED * 2;
            burger.dataset.dy = Math.sin(angle) * BURGER_SPEED * 2;
        }
    });
});

// Animate burgers
function moveBurgers() {
    burgers.forEach(burger => {
        // Get current position
        let x = parseFloat(burger.style.left);
        let y = parseFloat(burger.style.top);

        // Get velocity
        let dx = parseFloat(burger.dataset.dx);
        let dy = parseFloat(burger.dataset.dy);

        // Update position
        x += dx;
        y += dy;

        // Check for collisions with walls
        if (x <= 0 || x >= window.innerWidth - 50) {
            dx = -dx; // Reverse horizontal direction
        }
        if (y <= 0 || y >= window.innerHeight - 50) {
            dy = -dy; // Reverse vertical direction
        }

        // Update position and velocity
        burger.style.left = `${x}px`;
        burger.style.top = `${y}px`;
        burger.dataset.dx = dx;
        burger.dataset.dy = dy;
    });

    // Request the next animation frame
    requestAnimationFrame(moveBurgers);
}

// Start the animation
moveBurgers();
