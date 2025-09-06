// Year + "latest" date
const elYear = document.getElementById('year');
if (elYear) elYear.textContent = new Date().getFullYear();
const elDate = document.getElementById('latest-date');
if (elDate) elDate.textContent = new Date().toISOString().slice(0,10);

// Trailer play/pause
const player = document.getElementById('player');
const playBtn = document.getElementById('audio-play');
if (player && playBtn) {
  playBtn.addEventListener('click', () => {
    if (player.paused) { player.play(); playBtn.textContent = '❚❚'; }
    else { player.pause(); playBtn.textContent = '▶︎'; }
  });
}

// Unmute video on click (autoplay starts muted by policy)
const vid = document.querySelector('.hero-video');
const unmute = document.getElementById('unmute');
if (vid && unmute) {
  unmute.addEventListener('click', async () => {
    try {
      vid.muted = false;
      await vid.play();
      unmute.classList.add('hidden');
    } catch (e) {
      console.debug('Could not unmute autoplay video:', e);
    }
  });
}
