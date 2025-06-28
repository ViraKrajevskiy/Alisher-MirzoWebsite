document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('registrationForm');
    const passwordInput = document.getElementById('id_password');
    const confirmPasswordInput = document.getElementById('id_confirm_password');
    const strengthBar = document.getElementById('strength-bar');
    const strengthText = document.getElementById('strength-text');
    const passwordToggles = document.querySelectorAll('.password-toggle');
    const submitBtn = document.getElementById('submitBtn');

    // Подсветка label при фокусе
    document.querySelectorAll('input').forEach(input => {
        const label = input.previousElementSibling;
        if (label && label.tagName === 'LABEL') {
            input.addEventListener('focus', () => label.classList.add('focused'));
            input.addEventListener('blur', () => label.classList.remove('focused'));
        }
    });

    // Переключение видимости пароля
    passwordToggles.forEach(toggle => {
        toggle.addEventListener('click', function() {
            const input = this.parentNode.querySelector('input');
            if (input.type === 'password') {
                input.type = 'text';
                this.textContent = '🙈';
            } else {
                input.type = 'password';
                this.textContent = '👁️';
            }
        });
    });

    // Проверка сложности пароля
    if (passwordInput && strengthBar && strengthText) {
        passwordInput.addEventListener('input', function() {
            const password = this.value;
            const result = checkPasswordStrength(password);

            strengthBar.style.width = result.width;
            strengthBar.className = 'strength-bar ' + result.class;
            strengthText.textContent = result.text;
            strengthText.style.color = result.color;
        });
    }

    function checkPasswordStrength(password) {
        if (!password || password.length === 0) {
            return {
                width: '0%',
                class: '',
                text: '',
                color: 'transparent'
            };
        }

        let width = 0;
        let color = 'var(--error-color)';
        let text = 'Слишком короткий';
        let strengthClass = 'strength-weak';

        if (password.length < 4) {
            width = Math.min(30, (password.length / 4) * 30);
        }
        else if (password.length < 8) {
            width = 30 + ((password.length - 4) / 4) * 20;
            text = 'Слабый';
        }
        else {
            width = 50;
            text = 'Слабый';

            const hasLower = /[a-z]/.test(password);
            const hasUpper = /[A-Z]/.test(password);
            const hasNumber = /\d/.test(password);
            const hasSpecial = /[^a-zA-Z0-9]/.test(password);

            if (hasLower) width += 10;
            if (hasUpper) width += 10;
            if (hasNumber) width += 15;
            if (hasSpecial) width += 15;

            if (hasLower && hasUpper && hasNumber && hasSpecial) {
                width = 100;
            }

            if (width >= 80) {
                strengthClass = 'strength-strong';
                color = 'var(--success-color)';
                text = 'Сильный';
            }
            else if (width >= 60) {
                strengthClass = 'strength-medium';
                color = 'var(--warning-color)';
                text = 'Средний';
            }
        }

        width = Math.min(100, width);

        return {
            width: width + '%',
            class: strengthClass,
            text: text,
            color: color
        };
    }

    // Единый обработчик для проверки паролей
    function handlePasswordCheck() {
        const existingErrorMsg = confirmPasswordInput.parentNode.querySelector('.error-message');
        const shouldShowError = confirmPasswordInput.value &&
                               passwordInput.value !== confirmPasswordInput.value;

        if (shouldShowError) {
            if (!existingErrorMsg) {
                const newErrorMsg = document.createElement('span');
                newErrorMsg.className = 'error-message';
                newErrorMsg.textContent = 'Пароли не совпадают';
                confirmPasswordInput.parentNode.appendChild(newErrorMsg);
            }
            confirmPasswordInput.classList.add('error');
        } else {
            if (existingErrorMsg) existingErrorMsg.remove();
            confirmPasswordInput.classList.remove('error');
        }
    }


    // Проверка паролей при изменении любого из полей
    if (passwordInput && confirmPasswordInput) {
        passwordInput.addEventListener('input', handlePasswordCheck);
        confirmPasswordInput.addEventListener('input', handlePasswordCheck);
    }

    // Валидация формы
    form.addEventListener('submit', function(e) {
        let isValid = true;
        const errors = [];

        // Удаляем старые сообщения об ошибках
        document.querySelectorAll('.error-message').forEach(el => el.remove());
        document.querySelectorAll('input').forEach(input => input.classList.remove('error'));

        // Проверка обязательных полей
        document.querySelectorAll('input[required]').forEach(input => {
            if (!input.value.trim()) {
                isValid = false;
                input.classList.add('error');
                const msg = document.createElement('span');
                msg.className = 'error-message';
                msg.textContent = 'Это поле обязательно';
                input.parentNode.appendChild(msg);
                errors.push(`Поле "${input.previousElementSibling.textContent}" не заполнено`);
            }
        });

        // Проверка email
        const email = document.getElementById('id_email');
        if (email && email.value) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(email.value)) {
                isValid = false;
                email.classList.add('error');
                const msg = document.createElement('span');
                msg.className = 'error-message';
                msg.textContent = 'Некорректный email';
                email.parentNode.appendChild(msg);
                errors.push('Некорректный формат email');
            }
        }

        if (passwordInput && passwordInput.value.length < 8) {
            isValid = false;
            passwordInput.classList.add('error');
            const msg = document.createElement('span');
            msg.className = 'error-message';
            msg.textContent = 'Минимум 8 символов';
            passwordInput.parentNode.appendChild(msg);
            errors.push('Пароль слишком короткий');
        }

        // Проверка совпадения паролей
        if (passwordInput && confirmPasswordInput &&
            passwordInput.value !== confirmPasswordInput.value) {
            isValid = false;
            confirmPasswordInput.classList.add('error');
            const msg = document.createElement('span');
            msg.className = 'error-message';
            msg.textContent = 'Пароли не совпадают';
            confirmPasswordInput.parentNode.appendChild(msg);
            errors.push('Пароли не совпадают');
        }

        if (!isValid) {
            e.preventDefault();

            let errorsContainer = document.querySelector('.form-errors');
            if (!errorsContainer) {
                errorsContainer = document.createElement('div');
                errorsContainer.className = 'form-errors';
                form.prepend(errorsContainer);
            }

            errorsContainer.innerHTML = `
                <strong>Ошибки в форме:</strong>
                ${errors.map(err => `<div>• ${err}</div>`).join('')}
            `;

            const firstError = document.querySelector('.error');
            if (firstError) {
                firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
                firstError.focus();
            }
        } else {
            submitBtn.classList.add('btn-loading');
            submitBtn.disabled = true;
        }
    });
});