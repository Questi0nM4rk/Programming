// script.js

let doCheck = false;

console.log('script.js');

document.addEventListener('DOMContentLoaded', () => {
    const toggleButton = document.getElementById('toggleButton');

    // Retrieve the stored doCheck value when the popup is opened
    chrome.storage.local.get('doCheck', (result) => {
        doCheck = result.doCheck || false;
        toggleButton.style.backgroundColor = doCheck ? 'green' : 'red';
    });

    toggleButton.addEventListener('click', () => {
        doCheck = !doCheck;
        toggleButton.style.backgroundColor = doCheck ? 'green' : 'red';

        // Store the new doCheck value whenever the button is clicked
        chrome.storage.local.set({ doCheck: doCheck });
    });
});
