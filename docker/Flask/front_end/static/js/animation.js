const rotatingBox = document.getElementById("rotatingBox");
let isPaused = false;

rotatingBox.addEventListener("mouseenter", () => {
    if (!isPaused) {
        rotatingBox.classList.add("paused");
        isPaused = true;
    }
});

rotatingBox.addEventListener("mouseleave", () => {
    if (isPaused) {
        rotatingBox.classList.remove("paused");
        isPaused = false;
    }
});

rotatingBox.addEventListener("click", () => {
    if (isPaused) {
        rotatingBox.classList.remove("paused");
    } else {
        rotatingBox.classList.add("paused");
    }
    isPaused = !isPaused;
});





