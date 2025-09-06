// Update year and faux latest date
const y = new Date().getFullYear();
const elYear = document.getElementById('year');
if (elYear) elYear.textContent = y;
const d = new Date();
const elDate = document.getElementById('latest-date');
if (elDate) elDate.textContent = d.toLocaleDateString();


// Simple audio play/pause
const player = document.getElementById('player');
const playBtn = document.getElementById('audio-play');
if (player && playBtn) {
playBtn.addEventListener('click', () => {
if (player.paused) { player.play(); playBtn.textContent = '❚❚'; }
else { player.pause(); playBtn.textContent = '▶︎'; }
});
}
