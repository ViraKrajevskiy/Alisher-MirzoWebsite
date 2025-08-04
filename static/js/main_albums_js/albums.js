// Предотвращаем автоматический скролл браузера к якорю
if (window.location.hash) {
    window.scrollTo(0, 0);
}

document.addEventListener('DOMContentLoaded', function () {
    const hash = window.location.hash;

    // Автоматически раскрыть нужный альбом по якорю
    if (hash.startsWith('#album-')) {
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

    // Кнопки «Подробнее»
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

    // Лайк на альбом
    document.querySelectorAll('.book-like').forEach(button => {
        button.addEventListener('click', function () {
            const albumId = this.dataset.bookId;
            const likesSpan = this.querySelector('.book-likes-count');

            fetch(`/albums/${albumId}/like/`, {
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

    // Лайк на комментарии
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

    // Получить csrf-токен из куки
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
