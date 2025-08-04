document.addEventListener('DOMContentLoaded', function () {
    const toggleButtons = document.querySelectorAll('.toggle-expand');

    toggleButtons.forEach(button => {
        button.addEventListener('click', () => {
            const pictureId = button.dataset.id;
            const expanded = document.getElementById(`expanded-${pictureId}`);
            expanded.classList.toggle('visible');
        });
    });

    // hash-автопрокрутка
    const hash = window.location.hash;
    if (hash.startsWith('#picture-')) {
        const targetCard = document.querySelector(hash);
        if (targetCard) {
            const toggleBtn = targetCard.querySelector('.toggle-expand');
            if (toggleBtn) {
                toggleBtn.click();
                window.scrollTo({
                    top: targetCard.offsetTop - 20,
                    behavior: 'smooth'
                });
            }
        }
    }
});
