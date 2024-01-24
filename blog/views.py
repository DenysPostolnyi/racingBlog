from django.shortcuts import render, get_object_or_404

from blog.models import Post


# Create your views here.

def index(request):
    latest_posts = Post.objects.all().order_by('-date')[:3]
    # latest_posts = sorted(posts, key=lambda item: item["date"], reverse=True)[-3:]
    return render(request, 'index.html', {
        "posts": latest_posts
    })


def posts(request):
    all_posts = Post.objects.all().order_by('-date')
    return render(request, 'all-posts.html', {
        "all_posts": all_posts
    })


def post_detail(request, slug):
    post_details = get_object_or_404(Post, slug=slug)
    return render(request, 'post-details.html', {
        "post": post_details,
        "tags": post_details.tags.all()
    })
    # try:
    #     founded_post = next(post for post in posts_data if post['slug'] == slug)
    #     return render(request, 'post-details.html', {
    #         "post": founded_post
    #     })
    # except StopIteration:
    #     return render(request, '404.html')
