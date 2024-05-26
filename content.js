// 创建悬浮框的代码
const floatingBox = document.createElement('div');
floatingBox.innerHTML = '<h1>URL Logger</h1><button id="logUrl">Log Current URL</button>';

// 设置悬浮框的样式
floatingBox.style.position = 'fixed';
floatingBox.style.top = '10px'; // 距离页面顶部 10px
floatingBox.style.right = '10px'; // 距离页面右侧 10px
floatingBox.style.backgroundColor = 'rgba(255, 255, 255, 0.7)'; // 半透明白色背景
floatingBox.style.padding = '10px';
floatingBox.style.zIndex = '9999'; // 确保浮动框在最顶层

// 将悬浮框添加到页面中
document.body.appendChild(floatingBox);

// 绑定按钮点击事件，获取当前页面 URL 并输出到控制台
document.getElementById('logUrl').addEventListener('click', function() {
  console.log('Current URL:', window.location.href);
});

// 监听页面卸载事件，在页面卸载时移除悬浮框
window.addEventListener('beforeunload', function() {
  floatingBox.remove();
});
