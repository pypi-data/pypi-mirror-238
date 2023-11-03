document.addEventListener("DOMContentLoaded", function(e){
    const cookieModalWrapper = document.getElementById('cookie-consent-modal-wrapper');

    if (!cookieModalWrapper) {
        console.warn('Cookie consent modal wrapper not found.');
        return;
    }

    const tabs = {}
    let buttons = cookieModalWrapper.querySelectorAll('.ga-cookie-modal-btn');
    for (let i=0; i<buttons.length; i++) {
        const btn = buttons[i];
        const target = btn.dataset.target;

        if (!target) {
            continue;
        }

        tabs[target] = cookieModalWrapper.querySelector(target);
        
        btn.addEventListener('click', function(e){
            e.preventDefault();
            for (let tab in tabs) {
                tabs[tab].classList.remove('open');
            }
            tabs[target].classList.add('open');
        });
    }
});
