// 创建悬浮框的代码
const floatingBox = document.createElement('div');
floatingBox.innerHTML = `
  <h1>URL Logger</h1>
  <button id="logUrl">Log Current URL</button>
  <i class="loading-icon fas fa-spinner fa-spin"></i>
`;

// 设置悬浮框的样式
floatingBox.style.position = 'fixed';
floatingBox.style.top = '10px'; // 距离页面顶部 10px
floatingBox.style.right = '10px'; // 距离页面右侧 10px
floatingBox.style.backgroundColor = 'rgba(255, 255, 255, 0.7)'; // 半透明白色背景
floatingBox.style.padding = '10px';
floatingBox.style.zIndex = '9999'; // 确保浮动框在最顶层

// 将悬浮框添加到页面中
document.body.appendChild(floatingBox);

// 获取加载图标元素
const loadingIcon = document.querySelector('.loading-icon');
loadingIcon.style.display = 'none'; // 初始隐藏加载图标

// 绑定按钮点击事件，获取当前页面 URL 并输出到控制台
document.getElementById('logUrl').addEventListener('click', function() {
  console.log('Current URL:', window.location.href);
});

// 监听插件图标的点击事件
chrome.action.onClicked.addListener(function(tab) {
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
