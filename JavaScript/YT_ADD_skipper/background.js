// background.js

let intervalId;

function startChecking() {
    intervalId = setInterval(function() {
        var isAdd = document.querySelector(".ytp-ad-player-overlay");
        var videoPlayer = document.querySelector('.html5-main-video');
        //var skipbtn = document.querySelector(".ytp-ad-skip-button-modern.ytp-button");

        if (isAdd) {
            if (videoPlayer && videoPlayer.playbackRate !== 16) {
                videoPlayer.playbackRate = 16;
            }

            /*if (skipbtn) {
                skipbtn.click();
            }*/
        } else {
            if (videoPlayer && videoPlayer.playbackRate !== 1) {
                videoPlayer.playbackRate = 1;
            }
        }
    }, 500); // check every 500ms
}

function stopChecking() {
    clearInterval(intervalId);
}

// Listen for messages from the popup script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.doCheck) {
        startChecking();
    } else {
        stopChecking();
    }
});

// Retrieve the stored doCheck value when the script is loaded
chrome.storage.local.get('doCheck', (result) => {
    if (result.doCheck) {
        startChecking();
    } else {
        stopChecking();
    }
});