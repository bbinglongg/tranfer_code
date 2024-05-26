document.addEventListener('DOMContentLoaded', function() {
  // 获取加载图标元素
  const loadingIcon = document.querySelector('.loading-icon');

  // 监听插件图标的点击事件
  chrome.browserAction.onClicked.addListener(function(tab) {
    // 显示加载图标
    loadingIcon.style.display = 'block';

    // 获取当前页面 URL
    const pageURL = tab.url;

    // 发起 POST 请求到指定的 URL
    fetch('http://hkl20143361:5001/v1/page_id_list', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ page_url: pageURL })
    })
    .then(response => {
      if (response.ok) {
        console.log('POST request successful');
      } else {
        console.error('POST request failed');
      }
      // 隐藏加载图标
      loadingIcon.style.display = 'none';
    })
    .catch(error => {
      console.error('POST request error:', error);
      // 隐藏加载图标
      loadingIcon.style.display = 'none';
    });
  });
});
