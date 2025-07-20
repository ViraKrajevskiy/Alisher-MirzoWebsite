from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from main_app.models.model_albums.albums import Album, ComentAlbum, AlbumLike, CommentAlbumLike

@require_POST
@login_required
def add_comment_album(request, album_id):
    album = get_object_or_404(Album, id=album_id)
    text = request.POST.get('text')
    if text:
        ComentAlbum.objects.create(album=album, author=request.user, text=text)
    return redirect(f"/albums/#album-{album_id}")


@login_required
def delete_comment_album(request, comment_id):
    comment = get_object_or_404(ComentAlbum, id=comment_id)
    if comment.author == request.user:
        album_id = comment.album.id
        comment.delete()
        return redirect(f"/albums/#album-{album_id}")
    return redirect('/')


@login_required
def update_comment_album(request, comment_id):
    comment = get_object_or_404(ComentAlbum, id=comment_id)
    if comment.author != request.user:
        return redirect('/')
    if request.method == 'POST':
        new_text = request.POST.get('text')
        if new_text:
            comment.text = new_text
            comment.save()
        return redirect(f"/albums/#album-{comment.album.id}")
    return render(request, 'pages_main_albums/albums.html', {'comment': comment})


@require_POST
@login_required
def like_album(request, album_id):
    album = get_object_or_404(Album, id=album_id)
    user = request.user

    like_obj, created = AlbumLike.objects.get_or_create(album=album, user=user)

    if not created:
        like_obj.delete()
        liked = False
    else:
        liked = True

    return JsonResponse({
        'likes_count': AlbumLike.objects.filter(album=album).count(),
        'liked': liked
    })


@login_required
def like_comment_album(request, comment_id):
    comment = get_object_or_404(ComentAlbum, id=comment_id)
    user = request.user

    like_obj, created = CommentAlbumLike.objects.get_or_create(comment=comment, user=user)

    if not created:
        like_obj.delete()
        liked = False
    else:
        liked = True

    likes_count = CommentAlbumLike.objects.filter(comment=comment).count()

    return JsonResponse({
        'liked': liked,
        'likes_count': likes_count
    })


def album_list(request):
    albums = Album.objects.all()

    edit_comment_id = request.POST.get('edit_comment_id')
    new_text = request.POST.get('edit_text')
    if edit_comment_id and new_text:
        comment = get_object_or_404(ComentAlbum, id=edit_comment_id, author=request.user)
        comment.text = new_text
        comment.save()
        return redirect(f"{request.path}#album-{comment.album.id}")

    delete_comment_id = request.POST.get('delete_comment_id')
    if delete_comment_id:
        comment = get_object_or_404(ComentAlbum, id=delete_comment_id, author=request.user)
        album_id = comment.album.id
        comment.delete()
        return redirect(f"{request.path}#album-{album_id}")

    return render(request, 'pages_main_albums/albums.html', {
        'albums': albums,
        'edit_comment_id': str(edit_comment_id) if edit_comment_id else None
    })

