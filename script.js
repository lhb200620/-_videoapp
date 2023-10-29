const videoPlayer = document.getElementById('video');
const videoSources = ['video1.mp4', 'video2.mp4', 'video3.mp4', 'video4.mp4'];
let currentVideoIndex = 0;

function changeVideo(direction) {
  if (direction === 'next') {
    currentVideoIndex = (currentVideoIndex + 1) % videoSources.length;
  } else if (direction === 'prev') {
    currentVideoIndex = (currentVideoIndex - 1 + videoSources.length) % videoSources.length;
  }

  videoPlayer.src = videoSources[currentVideoIndex];
}

document.addEventListener('keydown', function(event) {
  if (event.key === 'ArrowRight' || event.key === 'ArrowDown') {
    changeVideo('next');
  } else if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') {
    changeVideo('prev');
  }
});

document.addEventListener('wheel', function(event) {
  if (event.deltaY > 0) {
    changeVideo('next');
  } else if (event.deltaY < 0) {
    changeVideo('prev');
  }
});