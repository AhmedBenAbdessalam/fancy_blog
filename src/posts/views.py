from django.shortcuts import render, get_object_or_404, redirect
from django.http import request
from .models import Post, Category, Author, PostView
from marketing.models import Signup
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count, Q
from .forms import CommentForm, PostForm


def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None


def get_category_count():
    return Post.objects.values(
        'categories__title').annotate(Count('categories__title'))


def index(request):

    featured_posts = Post.objects.filter(featured=True)
    # latest 3 posts
    latest_posts = Post.objects.order_by('-timestamp')[:3]

    if request.method == "POST":
        email = request.POST["email"]
        new_signup = Signup(email=email)
        new_signup.save()

    context = {
        'featured_posts': featured_posts,
        'latest_posts': latest_posts
    }
    return render(request, "index.html", context)


def blog(request):
    search = request.GET.get('q')
    if search:
        post_list = Post.objects.filter(Q(title__icontains=search) | Q(
            overview__icontains=search)).distinct()
    else:
        post_list = Post.objects.all().order_by('-timestamp')
    paginator = Paginator(post_list, 4)
    page_request_var = "page"
    page_number = request.GET.get(page_request_var)
    page = paginator.get_page(page_number)

    most_recent = Post.objects.order_by('-timestamp')[:3]

    categories_count = get_category_count()

    context = {
        'page': page,
        'page_request_var': page_request_var,
        'most_recent': most_recent,
        'categories_count': categories_count
    }
    return render(request, "blog.html", context)


def post(request, id):
    most_recent = Post.objects.order_by('-timestamp')[:3]
    categories_count = get_category_count()
    post = get_object_or_404(Post, id=id)
    if request.user.is_authenticated:
        PostView.objects.get_or_create(user=request.user, post=post)

    form = CommentForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid:
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect('post-detail', id=id)
    context = {
        'post': post,
        'most_recent': most_recent,
        'categories_count': categories_count,
        'form': form
    }
    return render(request, "post.html", context)


def post_create(request):
    title = "Create"
    form = PostForm(request.POST or None, request.FILES or None)
    author = get_author(request.user)
    if request.method == "POST":
        if form.is_valid:
            form.instance.author = author
            form.save()
            return redirect('post-detail', id=form.instance.id)
    context = {
        'title': title,
        'form': form
    }
    return render(request, "post_create.html", context)


def post_update(request, id):
    title = "Update"
    post = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if request.method == "POST":
        if form.is_valid:
            form.save()

    context = {
        'title': title,
        'form': form
    }
    return render(request, 'post_create.html', context)


def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect('blog')
