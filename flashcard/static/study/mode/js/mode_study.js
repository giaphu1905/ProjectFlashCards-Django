const cards = document.querySelectorAll('.flip-card');
cards.forEach(card => {
    card.addEventListener('click', () => {
        card.classList.toggle('is-flipped');
    });
});

const btnMixCard = document.getElementById("btn-mix-card");
const icon = document.querySelector("#btn-mix-card i");
const describeBtnMix = document.getElementById("describe-btn-mix");
var isRotating = localStorage.getItem('isRotatingStudy') === 'true';

if (isRotating) {
    icon.classList.add("fa-spin");
    describeBtnMix.textContent = "Trộn thẻ đang BẬT";
} else {
    icon.classList.remove("fa-spin");
    describeBtnMix.textContent = "Trộn thẻ đang TẮT";
}

btnMixCard.addEventListener("click", function() {
    if (isRotating) {
        icon.classList.remove("fa-spin");
        isRotating = false;
    } else {
        icon.classList.add("fa-spin");
        isRotating = true;
    }
    localStorage.setItem('isRotatingStudy', isRotating);
});
