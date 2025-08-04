if (window.location.hash) {
    window.scrollTo(0, 0);
}

document.addEventListener('DOMContentLoaded', function () {
    const hash = window.location.hash;

    if (hash.startsWith('#album-')) {
        const card = document.querySelector(hash);
        if (card) {
            const expandedContent = card.querySelector('.expanded-content');
            const toggleButton = card.querySelector('.toggle-expand');

            if (expandedContent && toggleButton) {
                expandedContent.style.display = 'block';
                toggleButton.classList.add('expanded');

                setTimeout(() => {
                    card.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }, 100);
            }
        }
    }

    // Лайки для комментариев
    document.querySelectorAll('.comment-like').forEach(button => {
        button.addEventListener('click', function (e) {
            e.preventDefault();

            const commentId = this.dataset.commentId;
            const likesSpan = this.querySelector('.likes-count');
            if (!commentId || !likesSpan) return;

            fetch(`/news/comment/${commentId}/like/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({})
            })
            .then(response => {
                if (!response.ok) throw new Error('Ошибка при лайке');
                return response.json();
            })
            .then(data => {
                likesSpan.textContent = data.likes_count;
                this.classList.toggle('active', data.liked);
            })
            .catch(err => console.error(err));
        });
    });

    // Лайки новостей
    document.querySelectorAll('.book-like').forEach(button => {
        button.addEventListener('click', function (e) {
            e.preventDefault();

            const newsId = this.dataset.bookId;
            const likesSpan = this.querySelector('.book-likes-count');
            if (!newsId || !likesSpan) return;

            fetch(`/news/${newsId}/like/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({})
            })
            .then(response => {
                if (!response.ok) throw new Error('Ошибка при лайке новости');
                return response.json();
            })
            .then(data => {
                likesSpan.textContent = data.likes_count;
                this.classList.toggle('active', data.liked);
            })
            .catch(err => console.error(err));
        });
    });

    // Показать/скрыть "Подробнее"
    document.querySelectorAll('.toggle-expand').forEach(function (button) {
        button.addEventListener('click', function () {
            const card = button.closest('.news-card');
            const expandedContent = card.querySelector('.expanded-content');

            if (expandedContent.style.display === 'none' || !expandedContent.style.display) {
                expandedContent.style.display = 'block';
                button.classList.add('expanded');
            } else {
                expandedContent.style.display = 'none';
                button.classList.remove('expanded');
            }
        });
    });

    // Показать/скрыть комментарии
    document.querySelectorAll('.toggle-comments').forEach(function (button) {
        button.addEventListener('click', function () {
            const card = button.closest('.news-card');
            const commentSection = card.querySelector('.comment-section');

            if (commentSection.style.display === 'none' || !commentSection.style.display) {
                commentSection.style.display = 'block';
                button.classList.add('opened');
            } else {
                commentSection.style.display = 'none';
                button.classList.remove('opened');
            }
        });
    });

    // Показать/скрыть форму добавления комментария
    document.querySelectorAll('.toggle-add-comment').forEach(function (button) {
        button.addEventListener('click', function () {
            const card = button.closest('.news-card');
            const addCommentForm = card.querySelector('.add-comment-form');

            if (addCommentForm.style.display === 'none' || !addCommentForm.style.display) {
                addCommentForm.style.display = 'block';
                button.classList.add('opened');
            } else {
                addCommentForm.style.display = 'none';
                button.classList.remove('opened');
            }
        });
    });

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
