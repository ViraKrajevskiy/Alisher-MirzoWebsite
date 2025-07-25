from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from main_app.models.model_picture.picture import Picture, CommentPicture, PictureLike, CommentPictureLike


def picture_list(request):
    pictures = Picture.objects.all()
    return render(request, 'pages_main_picture/picture_list.html', {'pictures': pictures})


from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from main_app.models.model_picture.picture import Picture, PictureLike, CommentPicture, CommentPictureLike

@require_POST
@login_required
def like_picture(request, picture_id):
    picture = get_object_or_404(Picture, id=picture_id)
    like_obj, created = PictureLike.objects.get_or_create(picture=picture, user=request.user)
    if not created:
        like_obj.delete()
        liked = False
    else:
        liked = True
    return JsonResponse({
        'liked': liked,
        'likes_count': picture.likes.count(),
    })

@require_POST
@login_required
def like_comment_picture(request, comment_id):
    comment = get_object_or_404(CommentPicture, id=comment_id)
    like_obj, created = CommentPictureLike.objects.get_or_create(comment=comment, user=request.user)
    if not created:
        like_obj.delete()
        liked = False
    else:
        liked = True
    return JsonResponse({
        'liked': liked,
        'likes_count': comment.likes.count(),
    })



@require_POST
@login_required
def add_comment_picture(request, picture_id):
    picture = get_object_or_404(Picture, id=picture_id)
    text = request.POST.get('text')
    if text:
        CommentPicture.objects.create(picture=picture, author=request.user, text=text)
    return redirect('picture_list')


@require_POST
@login_required
def delete_comment_picture(request, comment_id):
    comment = get_object_or_404(CommentPicture, id=comment_id)
    if comment.author == request.user:
        comment.delete()
    return redirect('picture_list')


@require_POST
@login_required
def update_comment_picture(request, comment_id):
    comment = get_object_or_404(CommentPicture, id=comment_id)
    if comment.author == request.user:
        new_text = request.POST.get('text')
        if new_text:
            comment.text = new_text
            comment.save()
    return redirect('picture_list')
