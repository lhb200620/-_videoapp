document.addEventListener('DOMContentLoaded', function() {
  const videoPlayer = document.getElementById('videoPlayer');

  function loadNextVideo() {
      fetch('http://127.0.0.1:5000/next_video').then(response => {
          videoPlayer.src = response.url;
          videoPlayer.play();
      });
  }

  function loadPreviousVideo() {
      fetch('http://127.0.0.1:5000/pre_video').then(response => {
          videoPlayer.src = response.url;
          videoPlayer.play();
      });
  }

  // window.loadNextVideo = loadNextVideo;
  // window.loadPreviousVideo = loadPreviousVideo;

  document.addEventListener('keydown', function(event) {
      switch (event.key) {
          case 'ArrowRight':
          case 'ArrowDown':
              loadNextVideo();
              event.preventDefault(); // 阻止事件的默认行为
              event.stopPropagation(); // 阻止事件冒泡
              break;
          case 'ArrowLeft':
          case 'ArrowUp':
              loadPreviousVideo();
              event.preventDefault(); // 阻止事件的默认行为
              event.stopPropagation(); // 阻止事件冒泡
              break;
          default:
              return;
      }
  });

  document.addEventListener('wheel', function(event) {
      if (event.deltaY > 0) {
          loadNextVideo();
          event.preventDefault(); // 阻止事件的默认行为
          event.stopPropagation(); // 阻止事件冒泡
      } else {
          loadPreviousVideo();
          event.preventDefault(); // 阻止事件的默认行为
          event.stopPropagation(); // 阻止事件冒泡
      }
  });
});
