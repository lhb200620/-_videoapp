window.addEventListener('DOMContentLoaded', (event) => {
  showPage('video-page');
});

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

    // 获取搜索按钮和登录按钮
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

    // // 获取所有分类按钮的集合
    // var categoryButtons = document.getElementsByClassName('category-btn');
    // // 遍历分类按钮集合，并为每个按钮添加点击事件监听器
    // for (var i = 0; i < categoryButtons.length; i++) {
    //   // 使用立即调用的函数表达式，传递按钮索引作为参数
    //   (function(index) {
    //     // 为每个按钮添加点击事件监听器
    //     categoryButtons[index].addEventListener('click', function() {
    //       // 在控制台输出相应的分类名称
    //       alert(categoryButtons[index].textContent);
    //       // 在这里可以编写您想要执行的其他代码逻辑
    //     });
    //   })(i);
    // }

  });

// 显示指定 ID 的页面，隐藏其他页面
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

function playVideo(videoSrc) {
  var videoPlayer = document.getElementById('video');
  videoPlayer.src = videoSrc;
  showPage('video-page'); // 切换到视频播放页面
}