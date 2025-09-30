// Toggle hamburger menu
document.addEventListener("DOMContentLoaded", () => {
  const menuToggle = document.querySelector('.menu-toggle');
  const nav = document.querySelector('nav.nav');

  if (menuToggle && nav) {
    menuToggle.addEventListener('click', () => {
      nav.classList.toggle('show');
    });
  }

  // Language switch
  const langSwitcher = document.getElementById("langSwitcher");
  if (langSwitcher) {
    langSwitcher.addEventListener("change", e => {
      window.location.href = e.target.value;
    });
  }
});

