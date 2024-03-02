from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.text import slugify
from django.views import View
from django.views.generic import ListView

from blog.forms import CommentForm, PostForm
from blog.models import Post, Tag, Author


# Create your views here.
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'login.html', {
                'error': "Login or password is incorrect"
            })
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('/')


class StartingPageView(ListView):
    # index
    template_name = 'index.html'
    model = Post
    ordering = ["-date"]
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset[:3]
        return data


# def index(request):
#     latest_posts = Post.objects.all().order_by('-date')[:3]
#     # latest_posts = sorted(posts, key=lambda item: item["date"], reverse=True)[-3:]
#     return render(request, 'index.html', {
#         "posts": latest_posts
#     })

class AllPostsView(ListView):
    # posts
    template_name = 'all-posts.html'
    model = Post
    ordering = ["-date"]
    context_object_name = 'all_posts'


# def posts(request):
#     all_posts = Post.objects.all().order_by('-date')
#     return render(request, 'all-posts.html', {
#         "all_posts": all_posts
#     })


class SinglePostView(View):
    # post_detail
    # template_name = 'post-details.html'
    # model = Post

    def is_stored_post(self, request, post_id):
        stored_posts = request.session.get('stored_posts')

        if stored_posts is not None and len(stored_posts) != 0:
            is_saved_for_later = post_id in stored_posts
        else:
            is_saved_for_later = False

        return is_saved_for_later

    def get(self, request, slug):
        post = Post.objects.get(slug=slug)

        context = {
            'post': post,
            'tags': post.tags.all(),
            'comment_form': CommentForm(),
            'comments': post.comments.all().order_by('-id'),
            'is_saved_for_later': self.is_stored_post(request, post.id),
        }
        return render(request, 'post-details.html', context)

    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse("post-detail-page", args=[slug]))

        context = {
            'post': post,
            'tags': post.tags.all(),
            'comment_form': comment_form,
            'comments': post.comments.all().order_by('-id'),
            'is_saved_for_later': self.is_stored_post(request, post.id),
        }
        return render(request, "post-details.html", context)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['tags'] = self.object.tags.all()
    #     context['comment_form'] = CommentForm()
    #     return context


class CreateOrUpdatePost(LoginRequiredMixin, View):
    template_name = 'create_or_update_post.html'
    form_class = PostForm

    def get(self, request, slug=None):
        if slug:
            post = Post.objects.get(slug=slug)
            form = self.form_class(instance=post)
            form.fields['tags'].queryset = Tag.objects.all()
        else:
            form = self.form_class()
            form.fields['tags'].queryset = Tag.objects.all()

        return render(request, self.template_name, {'form': form, 'post_slug': slug})

    def post(self, request, slug=None):
        if slug:
            post = Post.objects.get(slug=slug)
            form = self.form_class(request.POST, request.FILES, instance=post)
        else:
            form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            author = Author.objects.first()
            post = form.save(commit=False)
            post.author = author
            post.slug = slugify(post.title)
            post.save()
            return redirect(reverse('post-detail-page', args=[post.slug]))

        return render(request, self.template_name, {'form': form})


# def post_detail(request, slug):
#     post_details = get_object_or_404(Post, slug=slug)
#     return render(request, 'post-details.html', {
#         "post": post_details,
#         "tags": post_details.tags.all()
#     })

# try:
#     founded_post = next(post for post in posts_data if post['slug'] == slug)
#     return render(request, 'post-details.html', {
#         "post": founded_post
#     })
# except StopIteration:
#     return render(request, '404.html')

class ReadLaterView(View):
    def post(self, request):
        stored_posts = request.session.get('stored_posts')

        if stored_posts is None:
            stored_posts = []

        post_id = int(request.POST.get('post_id'))

        if post_id not in stored_posts:
            stored_posts.append(post_id)
        else:
            stored_posts.remove(post_id)

        request.session['stored_posts'] = stored_posts

        return HttpResponseRedirect(reverse("main-page"))

    def get(self, request):
        stored_posts = request.session.get('stored_posts')

        context = {}

        if stored_posts is None or len(stored_posts) == 0:
            context['posts'] = []
            context['has_posts'] = False
        else:
            context['has_posts'] = True
            context['posts'] = Post.objects.filter(id__in=stored_posts)

        return render(request, "stored_posts.html", context)
