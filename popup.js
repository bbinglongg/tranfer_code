document.addEventListener('DOMContentLoaded', function () {
  var btn = document.getElementById('btn');

  btn.addEventListener('click', function () {
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
      var pageURL = tabs[0].url;
      fetch('http://127.0.0.1:5041/v1/page_id_list', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ page_url: pageURL })
      })
        .then(response => response.json())
        .then(data => {
          chrome.tabs.update(tabs[0].id, { url: 'http://127.0.0.1:3000?page_id_list=' + JSON.stringify(data) });
        })
        .catch(error => {
          // 如果请求失败，暂时不处理
        });
    });
  });
});
