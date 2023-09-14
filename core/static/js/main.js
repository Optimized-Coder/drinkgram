uploadBarToggle = document.getElementById("upload-bar-toggle");
uploadBar = document.getElementById("upload-bar");
arrow = document.getElementById("arrow");

uploadBarToggle.addEventListener("click", function() {
    uploadBar.classList.toggle("hidden");
    arrow.classList.toggle("fa-arrow-down");
    arrow.classList.toggle("fa-arrow-up");
});