
function showBox(){
    const bioBox = document.getElementById("bioBox");
    if (bioBox.style.display === "none") {
        bioBox.style.display = "flex"; // or "block"
    } else {
        bioBox.style.display = "none";
    }
}