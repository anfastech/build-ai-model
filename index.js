// const dropdownButton = document.getElementById('dropdown-button');
// const dropdownMenu = document.getElementById('dropdown-menu');

document.getElementById("menu-button").addEventListener("click", function () {
  document.getElementById("dropdown-menu-mobile").classList.toggle("hidden");
});

document
  .getElementById("dropdown-button")
  .addEventListener("click", function () {
    document.getElementById("dropdown-menu").classList.toggle("hidden");
  });

document
  .getElementById("dropdown-button-mobile")
  .addEventListener("click", function () {
    document
      .getElementById("dropdown-menu-mobile-pages")
      .classList.toggle("hidden");
  });
document.addEventListener("click", function (event) {
  if (event.target !== dropdownButton && !dropdownMenu.contains(event.target)) {
    dropdownMenu.classList.add("hidden");
  }
});
console.log("JavaScript is linked and running.");

const scrollContainer = document.getElementById("scroll-container");
const incrementButton = document.getElementById("increment-button");
const decrementButton = document.getElementById("decrement-button");
const progressBar = document.getElementById("progress");
const progressBarContainer = document.getElementById("progress-bar");
let scrollAmount = 370; // Adjust the scroll amount as needed

incrementButton.addEventListener("click", () => {
  scrollContainer.scrollLeft += scrollAmount;
  updateProgressBar();
});

decrementButton.addEventListener("click", () => {
  scrollContainer.scrollLeft -= scrollAmount;
  updateProgressBar();
});
function updateProgressBar() {
  const scrollPosition = scrollContainer.scrollLeft;
  const containerWidth =
    scrollContainer.scrollWidth - scrollContainer.clientWidth;
  const progress = (scrollPosition / containerWidth) * 100;
  progressBar.style.width = `${progress}%`;
}

function hamburgerMenu() {
  const menu = document.getElementById("menu");
  menu.classList.toggle("hidden");
}
const menuButton = document.getElementById("menu-button");
menuButton.addEventListener("click", hamburgerMenu);
