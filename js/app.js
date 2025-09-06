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
const vid = document.getElementById('heroVideo');
const muteToggle = document.getElementById('muteToggle');
const theme = document.getElementById('theme-audio');

function updateMuteButton(){
  if (!muteToggle || !vid) return;
  muteToggle.textContent = vid.muted ? 'Unmute' : 'Mute';
  muteToggle.setAttribute('aria-label', vid.muted ? 'Unmute video' : 'Mute video');
}
if (vid && muteToggle) {
  vid.muted = true; // start muted for autoplay policy
  updateMuteButton();
  muteToggle.addEventListener('click', async () => {
    try {
      vid.muted = !vid.muted;
      await vid.play();
    } catch(e){}
    updateMuteButton();
  });
}
if (theme && vid) {
  theme.addEventListener('play', () => { vid.muted = true; updateMuteButton(); });
}

// Subscribe form -> send mailto to Zoho inbox (static site friendly)
const subForm = document.getElementById('subscribeForm');
const subEmail = document.getElementById('subEmail');
if (subForm && subEmail) {
  subForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const email = subEmail.value.trim();
    if (!email) return;
    const subject = 'AFP newsletter subscribe';
    const body = `email=${email}`;
    window.location.href = `mailto:subscribe@africanfootball.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
  });
}
