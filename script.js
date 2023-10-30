document.addEventListener('DOMContentLoaded', function() {
    const videoPlayer = document.getElementById('video');
    let currentVideoIndex = 1;
    const videoCount = 20; // 视频总数，根据实际情况修改
  
    // 监听键盘事件
    document.addEventListener('keydown', function(event) {
      switch (event.key) {
        case 'ArrowRight':
        case 'ArrowDown':
          currentVideoIndex = (currentVideoIndex % videoCount) + 1;
          break;
        case 'ArrowLeft':
        case 'ArrowUp':
          currentVideoIndex = (currentVideoIndex - 2 + videoCount) %videoCount + 1;
          break;
        default:
          return;
      }
  
      videoPlayer.src = `video${currentVideoIndex}.mp4`;
      videoPlayer.play();
    });
  
    // 监听鼠标滚轮事件
    document.addEventListener('wheel', function(event) {
      if (event.deltaY > 0) {
        currentVideoIndex = (currentVideoIndex % videoCount) + 1;
      } else {
        currentVideoIndex = (currentVideoIndex - 2 + videoCount) % videoCount + 1;
      }
  
      videoPlayer.src = `video${currentVideoIndex}.mp4`;
      videoPlayer.play();
    });
  });