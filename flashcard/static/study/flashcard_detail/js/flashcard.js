const cards = document.querySelectorAll('.flip-card');
cards.forEach(card => {
    card.addEventListener('click', () => {
        card.classList.toggle('is-flipped');
    });
});

$(document).ready(function() {
    $("#toggle-heart").click(function() {
        $(this).find("i").toggleClass("far fas");
    });
});

const stars = document.querySelectorAll(".fas.fa-star");
stars.forEach(star => {
    star.addEventListener('click', () => {
        star.classList.toggle('text-warning');
    });
});

// Lấy phần tử dropdown-toggle
const dropdownToggle = document.querySelector('#dropdownSort');

// Lấy danh sách các phần tử dropdown-item
const dropdownItems = document.querySelectorAll('.dropdown-item');

// Lắng nghe sự kiện click trên mỗi phần tử dropdown-item
dropdownItems.forEach(function(item) {
    item.addEventListener('click', function(event) {
        // Lấy nội dung của mục được chọn
        var selectedItem = this.textContent;
        // Thay đổi nội dung của dropdown-toggle thành nội dung của dropdown-item được click
        dropdownToggle.textContent = item.textContent;
        // Lưu trữ tên của nút được chọn trong localStorage
        localStorage.setItem('selectedItem', selectedItem);
    });
});
var selectedItem = localStorage.getItem('selectedItem');
if (selectedItem) {
    dropdownToggle.textContent = selectedItem;
};

const btnMixCard = document.getElementById("btn-mix-card");
const icon = document.querySelector("#btn-mix-card i");
const describeBtnMix = document.getElementById("describe-btn-mix");
var isRotating = localStorage.getItem('isRotating') === 'true';

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
    localStorage.setItem('isRotating', isRotating);
});

// Lấy tất cả các nút có lớp "mode-learning-button"
const ModeItemBtn = document.querySelectorAll('.ModeLearningItem');

// Xử lý sự kiện nhấp vào các nút
ModeItemBtn.forEach(function(item) {
    item.addEventListener('click', function(event) {
        // Lấy nội dung của mục được chọn
        var selectedModeItem = this.textContent;
        // Lưu trữ tên của nút được chọn trong localStorage
        localStorage.setItem('selectedItemModeName', selectedModeItem);
    });
});