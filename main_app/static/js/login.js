document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('.auth-form');
    if (!form) return;

    const inputs = form.querySelectorAll('input');
    const passwordInput = document.getElementById('id_password');
    const confirmPasswordInput = document.getElementById('id_confirm_password');
    const strengthBar = document.getElementById('strength-bar');
    const passwordToggle = document.querySelector('.password-toggle');

    // Функция для создания сообщения об ошибке
    const createErrorMessage = (message, parent, id = '') => {
        if (id && document.getElementById(id)) return;
        const errorMsg = document.createElement('span');
        errorMsg.className = 'error-message';
        if (id) errorMsg.id = id;
        errorMsg.textContent = message;
        parent.appendChild(errorMsg);
        return errorMsg;
    };

    // Подсветка label и фокус
    inputs.forEach(input => {
        const label = input.parentNode.querySelector('label');
        if (!label) return;

        input.addEventListener('focus', () => {
            label.classList.add('focused');
            input.classList.add('focused');
        });

        input.addEventListener('blur', () => {
            label.classList.remove('focused');
            input.classList.remove('focused');
        });

        // Удаление ошибки при вводе
        input.addEventListener('input', () => {
            input.classList.remove('error');
            const error = input.parentNode.querySelector('.error-message');
            if (error) error.remove();
        });
    });

    // Оценка сложности пароля
    if (passwordInput && strengthBar) {
        passwordInput.addEventListener('input', function () {
            const password = this.value;
            let strength = 0;

            const hasMinLength = password.length >= 8;
            const hasMixedCase = /[a-z]/.test(password) && /[A-Z]/.test(password);
            const hasNumbers = /\d/.test(password);
            const hasSpecialChars = /[^a-zA-Z\d]/.test(password);

            if (hasMinLength) strength++;
            if (hasMixedCase) strength++;
            if (hasNumbers) strength++;
            if (hasSpecialChars) strength++;

            const strengthLevels = [
                { width: '20%', color: 'var(--error-color)', text: 'Слабый' },
                { width: '40%', color: 'var(--error-color)', text: 'Слабый' },
                { width: '60%', color: 'var(--warning-color)', text: 'Средний' },
                { width: '80%', color: 'var(--success-color)', text: 'Сильный' },
                { width: '100%', color: 'var(--success-color)', text: 'Очень сильный' }
            ];

            const currentLevel = strengthLevels[strength] || strengthLevels[0];
            strengthBar.style.width = currentLevel.width;
            strengthBar.style.backgroundColor = currentLevel.color;
            strengthBar.setAttribute('data-strength', currentLevel.text);
        });
    }

    // Переключение видимости пароля
    if (passwordToggle) {
        passwordToggle.addEventListener('click', function () {
            const input = passwordInput || document.querySelector('input[type="password"]');
            const showing = input.type === 'text';
            input.type = showing ? 'password' : 'text';
            this.innerHTML = showing ? '👁️' : '🙈';
        });
    }

    // Проверка совпадения паролей
    if (passwordInput && confirmPasswordInput) {
        let timeout;
        confirmPasswordInput.addEventListener('input', function () {
            clearTimeout(timeout);
            timeout = setTimeout(() => {
                const mismatch = this.value && this.value !== passwordInput.value;
                const errorId = 'password-mismatch';

                if (mismatch) {
                    this.classList.add('error');
                    createErrorMessage('Пароли не совпадают', this.parentNode, errorId);
                } else {
                    this.classList.remove('error');
                    const error = document.getElementById(errorId);
                    if (error) error.remove();
                }
            }, 300);
        });
    }

    // Валидация при отправке
    form.addEventListener('submit', function (e) {
        let isValid = true;
        const errorMessages = [];

        document.querySelectorAll('.error-message').forEach(el => el.remove());
        inputs.forEach(input => input.classList.remove('error'));

        inputs.forEach(input => {
            if (!input.value.trim() && input.hasAttribute('required')) {
                isValid = false;
                input.classList.add('error');
                createErrorMessage('Это поле обязательно для заполнения', input.parentNode);
                errorMessages.push(`Поле "${input.previousElementSibling?.textContent || 'Поле'}" не заполнено`);
            }
        });

        const emailInput = form.querySelector('input[type="email"]');
        if (emailInput && emailInput.value) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(emailInput.value)) {
                isValid = false;
                emailInput.classList.add('error');
                createErrorMessage('Введите корректный email', emailInput.parentNode);
                errorMessages.push('Некорректный формат email');
            }
        }

        if (passwordInput && confirmPasswordInput && passwordInput.value !== confirmPasswordInput.value) {
            isValid = false;
            confirmPasswordInput.classList.add('error');
            if (!confirmPasswordInput.parentNode.querySelector('#password-mismatch')) {
                createErrorMessage('Пароли не совпадают', confirmPasswordInput.parentNode, 'password-mismatch');
            }
            errorMessages.push('Пароли не совпадают');
        }

        if (passwordInput && passwordInput.value.length > 0 && passwordInput.value.length < 8) {
            isValid = false;
            passwordInput.classList.add('error');
            createErrorMessage('Пароль должен содержать минимум 8 символов', passwordInput.parentNode);
            errorMessages.push('Пароль слишком короткий');
        }

        if (!isValid) {
            e.preventDefault();

            const existingContainer = form.querySelector('.form-errors');
            const container = existingContainer || document.createElement('div');
            container.className = 'form-errors';
            container.innerHTML = `
                <strong>Исправьте следующие ошибки:</strong>
                ${errorMessages.map(msg => `<div>• ${msg}</div>`).join('')}
            `;
            if (!existingContainer) form.prepend(container);

            const firstError = form.querySelector('.error');
            if (firstError) {
                firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
                firstError.focus();
            }
        }
    });

    // Признак того, что JS загружен
    document.body.classList.add('js-loaded');
});
