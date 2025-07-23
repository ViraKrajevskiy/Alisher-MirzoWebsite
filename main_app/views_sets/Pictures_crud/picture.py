# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from main_app.models.model_picture.picture import Picture, CommentPicture, PictureLike, CommentPictureLike


def picture_list(request):
    pictures = Picture.objects.all()
    return render(request, 'pages_main_picture/picture_list.html', {'pictures': pictures})


@require_POST
@login_required
def add_comment_picture(request, picture_id):
    picture = get_object_or_404(Picture, id=picture_id)
    text = request.POST.get('text')
    if text:
        CommentPicture.objects.create(picture=picture, author=request.user, text=text)
    return redirect(f"/picture/#album-{picture_id}")


@require_POST
@login_required
def delete_comment_picture(request, comment_id):
    comment = get_object_or_404(CommentPicture, id=comment_id)
    if comment.author == request.user:
        picture_id = comment.picture.id
        comment.delete()
        return redirect(f"/picture/#album-{picture_id}")
    return redirect('/')


@require_POST
@login_required
def update_comment_picture(request, comment_id):
    comment = get_object_or_404(CommentPicture, id=comment_id)
    if comment.author == request.user:
        new_text = request.POST.get('text')
        if new_text:
            comment.text = new_text
            comment.save()
        return redirect(f"/picture/#album-{comment.picture.id}")
    return redirect('/')


@require_POST
@login_required
def like_picture(request, picture_id):
    picture = get_object_or_404(Picture, id=picture_id)
    user = request.user

    like_obj, created = PictureLike.objects.get_or_create(picture=picture, user=user)
    if not created:
        like_obj.delete()
        liked = False
    else:
        liked = True

    return JsonResponse({
        'likes_count': picture.likes.count(),
        'liked': liked
    })


@login_required
def like_comment_picture(request, comment_id):
    comment = get_object_or_404(CommentPicture, id=comment_id)
    user = request.user

    like_obj, created = CommentPictureLike.objects.get_or_create(comment=comment, user=user)
    if not created:
        like_obj.delete()
        liked = False
    else:
        liked = True

    return JsonResponse({
        'liked': liked,
        'likes_count': comment.likes.count()
    })