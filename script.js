// document.addEventListener('DOMContentLoaded', function() {
//   const videoPlayer = document.getElementById('videoPlayer');

//   function loadNextVideo() {
//     fetch('http://127.0.0.1:5000/next_video')
//         .then(response => response.blob()) // 获取响应内容并转换为Blob
//         .then(blob => {
//             const url = URL.createObjectURL(blob); // 创建Blob URL
//             videoPlayer.src = url;
//             videoPlayer.play();
//         });
// }

//   function loadPreviousVideo() {
//       fetch('http://127.0.0.1:5000/pre_video')
//           .then(response => response.blob()) // 获取响应内容并转换为Blob
//           .then(blob => {
//               const url = URL.createObjectURL(blob); // 创建Blob URL
//               videoPlayer.src = url;
//               videoPlayer.play();
//           });
//   }

//   window.loadNextVideo = loadNextVideo;
//   window.loadPreviousVideo = loadPreviousVideo;

//   document.addEventListener('keydown', function(event) {
//       switch (event.key) {
//           case 'ArrowRight':
//           case 'ArrowDown':
//               loadNextVideo();
//               event.preventDefault(); // 阻止事件的默认行为
//               event.stopPropagation(); // 阻止事件冒泡
//               break;
//           case 'ArrowLeft':
//           case 'ArrowUp':
//               loadPreviousVideo();
//               event.preventDefault(); // 阻止事件的默认行为
//               event.stopPropagation(); // 阻止事件冒泡
//               break;
//           default:
//               return;
//       }
//   });

//   document.addEventListener('wheel', function(event) {
//       if (event.deltaY > 0) {
//           loadNextVideo();
//           event.preventDefault(); // 阻止事件的默认行为
//           event.stopPropagation(); // 阻止事件冒泡
//       } else {
//           loadPreviousVideo();
//           event.preventDefault(); // 阻止事件的默认行为
//           event.stopPropagation(); // 阻止事件冒泡
//       }
//   });
//   loadNextVideo();
// });

window.addEventListener('DOMContentLoaded', (event) => {
  showPage('video-page');
});

document.addEventListener('DOMContentLoaded', function() {
  const videoPlayer = document.getElementById('video');

  function loadNextVideo() {
    fetch('http://127.0.0.1:5000/next_video')
        .then(response => response.blob()) // 获取响应内容并转换为Blob
        .then(blob => {
            const url = URL.createObjectURL(blob); // 创建Blob URL
            videoPlayer.src = url;
            videoPlayer.play();
        });
}

  function loadPreviousVideo() {
      fetch('http://127.0.0.1:5000/pre_video')
          .then(response => response.blob()) // 获取响应内容并转换为Blob
          .then(blob => {
              const url = URL.createObjectURL(blob); // 创建Blob URL
              videoPlayer.src = url;
              videoPlayer.play();
          });
  }

  window.loadNextVideo = loadNextVideo;
  window.loadPreviousVideo = loadPreviousVideo;

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
  var searchButton = document.querySelector('.search-btn');
    var loginButton = document.querySelector('.login-btn');
    // 为搜索按钮添加点击事件监听器
    searchButton.addEventListener('click', function() {
      alert('搜索功能还没实现，您先别急！');
      // 在这里可以编写其他搜索相关的代码逻辑
    });
    // 为登录按钮添加点击事件监听器
    loginButton.addEventListener('click', function() {
      alert('登录功能还没实现，您先别急！');
      // 在这里可以编写其他登录相关的代码逻辑
    });
  loadNextVideo();
});

function showPage(pageId) {
  // 获取所有页面的元素
  var pages = document.getElementsByClassName('page');
  
  // 遍历页面元素，根据 ID 判断要显示的页面
  for (var i = 0; i < pages.length; i++) {
    if (pages[i].id === pageId) {
      pages[i].style.display = 'block'; // 显示指定页面
    } else {
      pages[i].style.display = 'none'; // 隐藏其他页面
    }
  }
}

