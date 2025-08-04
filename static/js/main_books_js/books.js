document.addEventListener('DOMContentLoaded', function () {
    // Автоматически открыть книгу по якорю (если есть)
    const hash = window.location.hash;
    if (hash.startsWith('#book-')) {
        const card = document.querySelector(hash);
        if (card) {
            const expandedContent = card.querySelector('.expanded-content');
            const toggleButton = card.querySelector('.toggle-expand');
            if (expandedContent && toggleButton) {
                expandedContent.style.display = 'block';
                toggleButton.textContent = 'Скрыть';
            }
        }
    }

    // Кнопка «Подробнее»
    document.querySelectorAll('.toggle-expand').forEach(button => {
        button.addEventListener('click', function () {
            const card = this.closest('.book-card');
            const expandedContent = card.querySelector('.expanded-content');

            if (expandedContent.style.display === 'block') {
                expandedContent.style.display = 'none';
                this.textContent = 'Подробнее';
            } else {
                expandedContent.style.display = 'block';
                this.textContent = 'Скрыть';
            }
        });
    });

    // Лайки на комментарии
    document.querySelectorAll('.comment-like').forEach(button => {
        button.addEventListener('click', function (e) {
            e.preventDefault();
            e.stopPropagation();

            const commentId = this.dataset.commentId;
            const likesSpan = this.querySelector('.likes-count');

            fetch(`/comments/${commentId}/like/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({})
            })
            .then(response => response.json())
            .then(data => {
                likesSpan.textContent = data.likes_count;
                this.classList.toggle('active', data.liked);
            });
        });
    });

    // Лайки на книги
    document.querySelectorAll('.book-like').forEach(button => {
        button.addEventListener('click', function () {
            const bookId = this.dataset.bookId;
            const likesSpan = this.querySelector('.book-likes-count');

            fetch(`/books/${bookId}/like/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({})
            })
            .then(response => response.json())
            .then(data => {
                likesSpan.textContent = data.likes_count;
                this.classList.toggle('active', data.liked);
            });
        });
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
