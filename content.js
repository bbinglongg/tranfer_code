// 创建一个 div 元素作为浮动框
const floatingBox = document.createElement('div');
floatingBox.innerHTML = '<h1>URL Logger</h1><button id="logUrl">Log Current URL</button>';

// 设置浮动框的样式
floatingBox.style.position = 'fixed';
floatingBox.style.top = '10px'; // 距离页面顶部 10px
floatingBox.style.left = '10px'; // 距离页面左侧 10px
floatingBox.style.backgroundColor = 'rgba(255, 255, 255, 0.7)'; // 半透明白色背景
floatingBox.style.padding = '10px';
floatingBox.style.zIndex = '9999'; // 确保浮动框在最顶层

// 将浮动框添加到页面中
document.body.appendChild(floatingBox);

// 绑定按钮点击事件，获取当前页面 URL 并输出到控制台
document.getElementById('logUrl').addEventListener('click', function() {
    console.log('Current URL:', window.location.href);
});