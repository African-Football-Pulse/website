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

// Video mute/unmute toggle + samspel med theme-audio
const vid = document.querySelector('.hero-video');
const muteToggle = document.getElementById('muteToggle');
const theme = document.getElementById('theme-audio');

function updateMuteButton(){
  if (!muteToggle || !vid) return;
  muteToggle.textContent = vid.muted ? 'Unmute' : 'Mute';
  muteToggle.setAttribute('aria-label', vid.muted ? 'Unmute video' : 'Mute video');
}

if (vid && muteToggle) {
  vid.muted = true;
  updateMuteButton();

  muteToggle.addEventListener('click', async () => {
    try {
      vid.muted = !vid.muted;
      await vid.play();
    } catch(e){ /* ignore */ }
    updateMuteButton();
  });
}

if (theme && vid) {
  theme.addEventListener('play', () => {
    vid.muted = true;
    updateMuteButton();
  });
}
