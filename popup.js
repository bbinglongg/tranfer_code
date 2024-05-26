document.addEventListener('DOMContentLoaded', function () {
  var options = document.getElementById('options');
  var loading = document.getElementById('loading');
  var error = document.getElementById('error');
  var closeErrorBtn = document.getElementById('closeError');

  options.addEventListener('change', function () {
    if (options.value === 'AIT') {
      loading.style.display = 'block';
      error.style.display = 'none';
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
            loading.style.display = 'none';
            chrome.tabs.update(tabs[0].id, { url: 'http://127.0.0.1:3000?page_id_list=' + JSON.stringify(data) });
          })
          .catch(error => {
            loading.style.display = 'none';
            error.style.display = 'block';
          });
      });
    }
  });

  closeErrorBtn.addEventListener('click', function () {
    error.style.display = 'none';
  });
});
