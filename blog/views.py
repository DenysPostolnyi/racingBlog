from datetime import date

from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render

# Create your views here.

posts_data = [
    {
        "slug": "hike-in-the-mountains",
        "image": "mountains.jpg",
        "author": "Denys",
        "date": date(2021, 7, 21),
        "title": "Mountain Hiking",
        "excerpt": "Some text",
        "content": """
        Lorem ipsum dolor sit amet, consectetur adipisicing elit. Alias aspernatur beatae eius iure iusto porro quasi
            sunt vero. A debitis dignissimos dolorem magnam magni quidem quisquam rerum vero voluptas voluptatum.
        """
    }
]


def index(request):
    latest_posts = sorted(posts_data, key=lambda item: item["date"], reverse=True)[:3]
    return render(request, 'index.html', {
        "posts": latest_posts
    })


def posts(request):
    return render(request, 'all-posts.html', {
        "all_posts": posts_data
    })


def post_detail(request, slug):
    try:
        founded_post = next(post for post in posts_data if post['slug'] == slug)
        return render(request, 'post-details.html', {
            "post": founded_post
        })
    except StopIteration:
        return render(request, '404.html')
