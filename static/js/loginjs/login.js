document.addEventListener('DOMContentLoaded', function () {
    // Переключение видимости пароля
    const passwordToggle = document.querySelector('.password-toggle');
    const passwordInput = document.getElementById('id_password');

    if (passwordToggle && passwordInput) {
        passwordToggle.addEventListener('click', function () {
            const showing = passwordInput.type === 'text';
            passwordInput.type = showing ? 'password' : 'text';
            this.textContent = showing ? '👁️' : '🙈';
        });
    }

    // Валидация формы
    const form = document.querySelector('.auth-form');
    if (form) {
        form.addEventListener('submit', function (e) {
            const username = document.getElementById('id_username');
            const password = document.getElementById('id_password');
            let isValid = true;

            // Удаляем предыдущие ошибки
            document.querySelectorAll('.error-message').forEach(el => el.remove());
            [username, password].forEach(input => input.classList.remove('error'));

            // Проверка заполнения полей
            if (!username.value.trim()) {
                isValid = false;
                username.classList.add('error');
                showError(username, 'Это поле обязательно для заполнения');
            }

            if (!password.value.trim()) {
                isValid = false;
                password.classList.add('error');
                showError(password, 'Это поле обязательно для заполнения');
            } else if (password.value.length < 8) {
                isValid = false;
                password.classList.add('error');
                showError(password, 'Пароль должен содержать минимум 8 символов');
            }

            if (!isValid) {
                e.preventDefault();
                const firstError = form.querySelector('.error');
                if (firstError) {
                    firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    firstError.focus();
                }
            }
        });
    }

    function showError(input, message) {
        const error = document.createElement('span');
        error.className = 'error-message';
        error.textContent = message;
        input.parentNode.appendChild(error);
    }

    document.body.classList.add('js-loaded');
});
