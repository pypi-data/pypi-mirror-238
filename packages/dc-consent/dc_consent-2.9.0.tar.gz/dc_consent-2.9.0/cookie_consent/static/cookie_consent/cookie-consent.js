document.addEventListener("DOMContentLoaded", function(e){
    const cookieModalWrapper = document.getElementById('cookie-consent-modal-wrapper');
    const settingsButton = cookieModalWrapper.querySelector('#ga-cookie-modal-settings');
    const detailsButton = cookieModalWrapper.querySelector('#ga-cookie-modal-details');
    const backButton = cookieModalWrapper.querySelector('#ga-cookie-modal-back');

    const formTab = cookieModalWrapper.querySelector('#ga-cookie-modal-main-tab');
    const settingsTab = cookieModalWrapper.querySelector('#ga-cookie-modal-tab-settings');
    const detailsTab = cookieModalWrapper.querySelector('#ga-cookie-modal-tab-details');

    settingsButton.addEventListener('click', () => {
        formTab.classList.remove('open');
        detailsTab.classList.remove('open');
        settingsTab.classList.add('open');
    });

    backButton.addEventListener('click', () => {
        formTab.classList.add('open');
        settingsTab.classList.remove('open');
        detailsTab.classList.remove('open');
    });

    detailsButton.addEventListener('click', () => {
        formTab.classList.remove('open');
        settingsTab.classList.remove('open');
        detailsTab.classList.add('open');
    });
});
