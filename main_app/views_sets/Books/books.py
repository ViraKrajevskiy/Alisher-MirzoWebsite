from main_app.models.model_book.book import CommentBookLike, BookLike
from main_app.models.model_book.book import Book
from main_app.models import ComentBook

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required


# Удаление комментария
@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(ComentBook, id=comment_id)
    if comment.author == request.user:
        book_id = comment.book.id
        comment.delete()
        return redirect(f"/books/#book-{book_id}")
    return redirect('/')

# Обновление комментария
@login_required
def update_comment(request, comment_id):
    comment = get_object_or_404(ComentBook, id=comment_id)
    if comment.author != request.user:
        return redirect('/')
    if request.method == 'POST':
        new_text = request.POST.get('text')
        if new_text:
            comment.text = new_text
            comment.save()
        return redirect(f"/books/#book-{comment.book.id}")
    return render(request, 'pages_main_books/book.html', {'comment': comment})

# Лайк книги
@require_POST
@login_required
def like_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    user = request.user

    like_obj, created = BookLike.objects.get_or_create(book=book, user=user)

    if not created:
        like_obj.delete()
        liked = False
    else:
        liked = True

    return JsonResponse({
        'likes_count': BookLike.objects.filter(book=book).count(),
        'liked': liked
    })



# Лайк комментария
@login_required
def like_comment(request, comment_id):
    comment = ComentBook.objects.get(pk=comment_id)
    user = request.user

    like_obj, created = CommentBookLike.objects.get_or_create(comment=comment, user=user)

    if not created:
        # Уже лайкал — значит, убираем лайк
        like_obj.delete()
        liked = False
    else:
        liked = True

    likes_count = CommentBookLike.objects.filter(comment=comment).count()

    return JsonResponse({
        'liked': liked,
        'likes_count': likes_count
    })

# Отображение списка книг с возможностью редактирования/удаления комментария
def book_list(request):
    books = Book.objects.all()

    edit_comment_id = request.POST.get('edit_comment_id')
    new_text = request.POST.get('edit_text')
    if edit_comment_id and new_text:
        comment = get_object_or_404(ComentBook, id=edit_comment_id, author=request.user)
        comment.text = new_text
        comment.save()
        return redirect(f"{request.path}#book-{comment.book.id}")

    delete_comment_id = request.POST.get('delete_comment_id')
    if delete_comment_id:
        comment = get_object_or_404(ComentBook, id=delete_comment_id, author=request.user)
        book_id = comment.book.id
        comment.delete()
        return redirect(f"{request.path}#book-{book_id}")

    return render(request, 'pages_main_books/book.html', {
        'books': books,
        'edit_comment_id': str(edit_comment_id) if edit_comment_id else None
    })


@require_POST
@login_required
def add_comment(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    text = request.POST.get('text')
    if text:
        ComentBook.objects.create(book=book, author=request.user, text=text)
    return redirect(f"/books/#book-{book_id}")




