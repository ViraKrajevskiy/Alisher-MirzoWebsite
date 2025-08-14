from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from main_app.models.model_news.news import News, Comment, NewsLike, CommentLikes


@require_POST
@login_required
def add_comment_news(request, news_id):
    news = get_object_or_404(News, id=news_id)
    text = request.POST.get('text')
    if text:
        Comment.objects.create(news=news, author=request.user, text=text)
    return redirect(f"/news/#album-{news_id}")


@login_required
def delete_comment_news(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author == request.user:
        news_id = comment.news.id
        comment.delete()
        return redirect(f"/news/#album-{news_id}")
    return redirect('/')


@login_required
def update_comment_news(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author != request.user:
        return redirect('/')

    if request.method == 'POST':
        new_text = request.POST.get('text')
        if new_text:
            comment.text = new_text
            comment.save()
        return redirect(f"/news/#album-{comment.news.id}")

    return render(request, 'pages_main_news/news.html', {'comment': comment})


@require_POST
@login_required
def like_news(request, news_id):
    news = get_object_or_404(News, id=news_id)
    user = request.user

    like_obj, created = NewsLike.objects.get_or_create(news=news, user=user)

    if not created:
        like_obj.delete()
        liked = False
    else:
        liked = True

    return JsonResponse({
        'likes_count': NewsLike.objects.filter(news=news).count(),
        'liked': liked
    })


@login_required
def like_comment_news(request, comment_id):
    try:
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        return JsonResponse({'error': 'Комментарий не найден'}, status=404)

    user = request.user
    like_obj, created = CommentLikes.objects.get_or_create(comment=comment, user=user)

    if not created:
        like_obj.delete()
        liked = False
    else:
        liked = True

    likes_count = CommentLikes.objects.filter(comment=comment).count()

    return JsonResponse({
        'liked': liked,
        'likes_count': likes_count
    })

def news_list(request):
    news_items = News.objects.all()

    edit_comment_id = request.POST.get('edit_comment_id')
    new_text = request.POST.get('edit_text')
    if edit_comment_id and new_text:
        comment = get_object_or_404(Comment, id=edit_comment_id, author=request.user)
        comment.text = new_text
        comment.save()
        return redirect(f"{request.path}#album-{comment.news.id}")

    delete_comment_id = request.POST.get('delete_comment_id')
    if delete_comment_id:
        comment = get_object_or_404(Comment, id=delete_comment_id, author=request.user)
        news_id = comment.news.id
        comment.delete()
        return redirect(f"{request.path}#album-{news_id}")

    return render(request, 'pages_main_news/news.html', {
        'albums': news_items,
        'edit_comment_id': str(edit_comment_id) if edit_comment_id else None
    })

