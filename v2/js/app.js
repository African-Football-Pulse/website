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

  // Play video on click
  document.querySelectorAll(".video-frame-portrait").forEach(frame => {
    const playBtn = frame.querySelector(".play-toggle");
    const videoSrc = frame.dataset.video;
    if (playBtn) {
      playBtn.addEventListener("click", () => {
        frame.innerHTML = `
          <video class="hero-video-portrait" autoplay muted loop playsinline>
            <source src="${videoSrc}" type="video/mp4" />
          </video>
          <button class="mute-toggle">Unmute</button>
        `;
        const video = frame.querySelector("video");
        const muteBtn = frame.querySelector(".mute-toggle");
        muteBtn.addEventListener("click", () => {
          video.muted = !video.muted;
          muteBtn.textContent = video.muted ? "Unmute" : "Mute";
        });
      });
    }
  });
});
