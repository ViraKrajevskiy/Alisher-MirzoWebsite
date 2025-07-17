from main_app.models.model_book.book import CommentBookLike, Book, BookLike


from django.http import JsonResponse, HttpResponseRedirect
from main_app.models import Comment
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

# Удаление комментария
@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(ComentBook, id=comment_id)
    if comment.author == request.user:
        comment.delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))

# Обновление комментария
@login_required
def update_comment(request, comment_id):
    comment = get_object_or_404(ComentBook, id=comment_id)
    if comment.author != request.user:
        return redirect('/')  # или выдать 403

    if request.method == 'POST':
        new_text = request.POST.get('text')
        if new_text:
            comment.text = new_text
            comment.save()
        return redirect(request.META.get('HTTP_REFERER', '/'))

    return render(request, 'pages_main_books/edit_comment.html', {'comment': comment})



@require_POST
@login_required
def like_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    like_obj, created = BookLike.objects.get_or_create(book=book, user=request.user)
    if not created:
        like_obj.delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))



from main_app.models.model_book.book import ComentBook  # ✅ правильно

@require_POST
@login_required
def like_comment(request, comment_id):
    comment = get_object_or_404(ComentBook, id=comment_id)  # ✅ исправили
    user = request.user

    if user in comment.likes.all():
        comment.likes.remove(user)
        liked = False
    else:
        comment.likes.add(user)
        liked = True

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'likes_count': comment.likes.count(),
            'liked': liked
        })

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    


@require_POST
@login_required
def add_comment(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    text = request.POST.get('text')
    if text:
        ComentBook.objects.create(book=book, author=request.user, text=text)
    return redirect(request.META.get('HTTP_REFERER', '/'))



from django.shortcuts import render, redirect, get_object_or_404
from main_app.models.model_book.book import Book, ComentBook
from django.contrib.auth.decorators import login_required


@login_required
def book_list(request):
    books = Book.objects.all()

    edit_comment_id = request.POST.get('edit_comment_id')
    new_text = request.POST.get('edit_text')
    if edit_comment_id and new_text:
        comment = get_object_or_404(ComentBook, id=edit_comment_id, author=request.user)
        comment.text = new_text
        comment.save()
        return redirect(request.path)

    delete_comment_id = request.POST.get('delete_comment_id')
    if delete_comment_id:
        comment = get_object_or_404(ComentBook, id=delete_comment_id, author=request.user)
        comment.delete()
        return redirect(request.path)

    return render(request, 'pages_main_books/book.html', {
        'books': books,
        'edit_comment_id': int(edit_comment_id) if edit_comment_id else None
    })

