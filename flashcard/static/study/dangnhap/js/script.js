const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');

// Lưu trạng thái của container vào Local Storage khi người dùng bấm nút đăng ký
signUpButton.addEventListener('click', () => {
  console.log("Lưu trạng thái của container");
  container.classList.add("right-panel-active");
  localStorage.setItem("containerState", "right-panel-active");
});

// Khôi phục trạng thái của container từ Local Storage khi trang được tải lại
document.addEventListener("DOMContentLoaded", () => {
  console.log("Khôi phục trạng thái của container");
  const containerState = localStorage.getItem("containerState");
  if (containerState === "right-panel-active") {
    container.classList.add("right-panel-active");
  }
});

// Xóa trạng thái của container khỏi Local Storage khi người dùng bấm nút đăng nhập
signInButton.addEventListener('click', () => {
  console.log("Xóa trạng thái của container");
  container.classList.remove("right-panel-active");
  localStorage.removeItem("containerState");
});
