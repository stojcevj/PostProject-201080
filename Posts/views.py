from django.db.models import Q
from django.shortcuts import render, redirect

import Posts
from Posts.forms import PostsForm, BlockForm
from Posts.models import Post, BlockedProfile, Profile


# Create your views here.


def posts(request):
    qs = Post.objects.all()

    if request.user.is_superuser:
        context = {'posts': qs}
        return render(request, 'posts.html', context=context)

    if not request.user.is_authenticated:
        context = {'posts': None}
        return render(request, 'posts.html', context=context)

    im_blocked = BlockedProfile.objects.filter(users__profile_user_id=request.user.id).all()
    i_blocked = BlockedProfile.objects.filter(blocked_by__profile_user_id=request.user.id).all()
    check_if_blocked = []
    check_if_i_blocked = []
    for row in im_blocked.values_list():
        check_if_blocked.append(row[1])

    for row in i_blocked.values_list():
        check_if_i_blocked.append(row[2])

    qs = qs.exclude(Q(post_profile_id__in=check_if_blocked) | Q(post_profile_id__in=check_if_i_blocked))
    qs = qs.exclude(post_profile_id=Profile.objects.filter(profile_user=request.user.id).get())
    context = {'posts': qs}

    return render(request, 'posts.html', context=context)


def post_add(request):
    if request.method == 'POST':
        form_data = PostsForm(data=request.POST, files=request.FILES)
        if form_data.is_valid():
            post = form_data.save(commit=False)
            post.post_profile = Profile.objects.filter(profile_user=request.user.id).get()
            post.save()
            return redirect('posts')

    context = {'form': PostsForm}
    return render(request, 'add.html', context)


def profile(request):
    qs = Profile.objects.filter(profile_user_id=request.user.id).get()
    qs_posts = Post.objects.filter(post_profile_id=request.user.id).all()
    context = {'profile': qs, 'posts': qs_posts}

    return render(request, 'profile.html', context=context)


def blocked_users(request):
    if request.method == 'POST':
        form_data = BlockForm(data=request.POST, files=request.FILES)
        if form_data.is_valid():
            block = form_data.save(commit=False)
            block.blocked_by = Profile.objects.filter(profile_user_id=request.user.id).get()
            block.save()
            return redirect('blocked_users')

    qs = BlockedProfile.objects.filter(blocked_by=Profile.objects.filter(profile_user_id=request.user.id).get()).all()
    context = {'form': BlockForm, 'users': qs}
    return render(request, 'blockedusers.html', context=context)
