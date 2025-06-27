// Добавляем эффект при загрузке страницы
        document.addEventListener('DOMContentLoaded', function() {
            const inputs = document.querySelectorAll('input');

            inputs.forEach(input => {
                // Добавляем эффект при фокусе
                input.addEventListener('focus', function() {
                    this.parentNode.querySelector('label').style.color = 'var(--primary-color)';
                });

                // Убираем эффект при потере фокуса
                input.addEventListener('blur', function() {
                    this.parentNode.querySelector('label').style.color = '#555';
                });
            });

            // Добавляем валидацию в реальном времени
            const form = document.querySelector('.auth-form');
            form.addEventListener('submit', function(e) {
                let isValid = true;

                inputs.forEach(input => {
                    if (!input.value.trim()) {
                        isValid = false;
                        input.style.borderColor = 'var(--error-color)';
                        const errorMsg = document.createElement('span');
                        errorMsg.className = 'error-message';
                        errorMsg.textContent = 'Это поле обязательно для заполнения';
                        input.parentNode.appendChild(errorMsg);
                    }
                });

                if (!isValid) {
                    e.preventDefault();
                }
            });
        });