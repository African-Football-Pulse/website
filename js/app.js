// Update year and faux latest date
const y = new Date().getFullYear();
const elYear = document.getElementById('year');
if (elYear) elYear.textContent = y;
const d = new Date();
const elDate = document.getElementById('latest-date');
if (elDate) elDate.textContent = d.toLocaleDateString();


// redan i din fil: year + trailer play-knapp
const y = new Date().getFullYear();
const elYear = document.getElementById('year');
if (elYear) elYear.textContent = y;
const elDate = document.getElementById('latest-date');
if (elDate) elDate.textContent = new Date().toISOString().slice(0,10);

// trailer play/pause
const player = document.getElementById('player');
const playBtn = document.getElementById('audio-play');
if (player && playBtn) {
  playBtn.addEventListener('click', () => {
    if (player.paused) { player.play(); playBtn.textContent = '❚❚'; }
    else { player.pause(); playBtn.textContent = '▶︎'; }
  });
}

// Unmute video on click (autoplay policy: startas alltid muted)
const vid = document.querySelector('.hero-video');
const unmute = document.getElementById('unmute');
if (vid && unmute) {
  unmute.addEventListener('click', async () => {
    try {
      vid.muted = false;
      await vid.play();
      unmute.classList.add('hidden');
    } catch (e) {
      // om blockerat, lämna knappen synlig
      console.debug('Could not unmute autoplay video:', e);
    }
  });
}
