document.addEventListener('DOMContentLoaded', function() {
  var logUrlButton = document.getElementById('logUrl');
  logUrlButton.addEventListener('click', function() {
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
      var currentUrl = tabs[0].url;
      console.log('Current URL:', currentUrl);
    });
  });
});
