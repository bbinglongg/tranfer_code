document.addEventListener('DOMContentLoaded', function () {
  var btn = document.getElementById('btn');
  var loading = document.getElementById('loading');

  btn.addEventListener('click', function () {
    btn.disabled = true;
    btn.textContent = '';
    btn.style.display = 'none';
    loading.style.display = 'inline-block';

    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
      var pageURL = tabs[0].url;
      fetch('http://127.0.0.1:5041/v1/page_id_list', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ page_url: pageURL })
      })
        .then(response => {
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          return response.json();
        })
        .then(data => {
          var newURL = 'http://127.0.0.1:3000?page_id_list=' + JSON.stringify(data);
          chrome.tabs.create({ url: newURL });
          closePopup(1000); // Close popup after 1 second
        })
        .catch(error => {
          loading.style.display = 'none';
          btn.textContent = '操作错误';
          btn.style.display = 'inline-block';
          setTimeout(function () {
            closePopup(0);
          }, 3000); // Close popup after 3 seconds
        });
    });
  });

  function closePopup(delay) {
    setTimeout(function () {
      window.close();
    }, delay);
  }
});
