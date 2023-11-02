document.addEventListener("DOMContentLoaded", function(e){
    const cookieModalWrapper = document.getElementById('cookie-consent-modal-wrapper');
    const settingsButton = cookieModalWrapper.querySelector('#ga-cookie-modal-settings');
    const backButton = cookieModalWrapper.querySelector('#ga-cookie-modal-back');

    const formTab = cookieModalWrapper.querySelector('#ga-cookie-modal-main-tab');
    const settingsTab = cookieModalWrapper.querySelector('#ga-cookie-modal-tab-settings');

    settingsButton.addEventListener('click', () => {
        formTab.classList.remove('open');
        settingsTab.classList.add('open');
    });

    backButton.addEventListener('click', () => {
        formTab.classList.add('open');
        settingsTab.classList.remove('open');
    });
});
