// app.js – AFP v2

document.addEventListener("DOMContentLoaded", () => {
  // Hamburger menu toggle
  const menuToggle = document.querySelector(".menu-toggle");
  const nav = document.querySelector("nav.nav");

  if (menuToggle && nav) {
    menuToggle.addEventListener("click", () => {
      nav.classList.toggle("show");
    });
  }

  // Language switcher
  const langSwitcher = document.getElementById("langSwitcher");
  if (langSwitcher) {
    langSwitcher.addEventListener("change", e => {
      window.location.href = e.target.value;
    });
  }
});
