from django.forms import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.core.paginator import Paginator
from .models import *
from .forms import *
from django.contrib.auth import login
from django.db.models import Q
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from taggit.models import Tag


class MainPageView(View):

    def get(self, request):
        posts = Post.objects.filter(post_date__lte=timezone.now()).order_by('-post_date')
        pagination = Paginator(posts, 6)
        page_number = request.GET.get('page')
        page_obj = pagination.get_page(page_number)
        return render(request, 'home.html', context={
            'page_obj' : page_obj
         })

class PostPageView(View):
    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        last_posts = Post.objects.all().order_by('-id')[:5]
        comment_form = CommentForm()
        return render(request, 'post_detail.html', context={
            'post': post,
            'last_posts': last_posts,
            'comment_form': comment_form
    })

    def post(self, request, slug, *args, **kwargs):
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            text = request.POST['text']
            username = self.request.user
            post = get_object_or_404(Post, slug=slug)
            comment = Comment.objects.create(post=post, username=username, text=text)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        return render(request, 'myblog/post_detail.html', context={
            'comment_form': comment_form
        })



class SignUpView(View):

    def get(self, request):
        form = SignUpForm()
        return render(request, 'signup.html', context={
            'form' : form
        })

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
        return render(request, 'signup.html', context={
            'form' : form
        })


class SignInView(View):

    def get(self, request):
        form = SignInForm()
        return render(request, 'signin.html', context={
            'form' : form
        })

    def post(self, request):
        form = SignInForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=request.POST['username'],
                password=request.POST['password']
            )
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
        return render(request, 'signin.html', context={
            'form' : form
        })


class CreatePostView(View):

    def get(self, request):
        form = CreatePostForm()
        return render(request, 'create_post.html', context={
            'form' : form
        })

    def post(self, request):
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            slug = post.h1.split(' ')
            post.slug = '-'.join(slug)
            post.save()
            return HttpResponseRedirect('/')
        raise ValidationError(
            'Error'
        )


class EditProfileView(View):
    
    def get(self, request):
        form = EditProfileForm()
        return render(request, 'profile_page.html', context={
            'form' : form
        })
        
    def post(self, request):
        form = EditProfileForm(request.POST)
        if form.is_valid():
            new_username = form.cleaned_data.get('username')
            new_password = form.cleaned_data.get('password')
            new_first_name = form.cleaned_data.get('first_name')
            new_last_name = form.cleaned_data.get('last_name')
            new_email = form.cleaned_data.get('email')
            user = User.objects.get(username=request.user.username)
            user.username = new_username
            user.first_name = new_first_name
            user.last_name = new_last_name
            user.email = new_email
            user.set_password(new_password)
            user.save()
            return HttpResponseRedirect('/')
        raise ValidationError(
            'Error'
        )

class SearchView(View):

    def get(self, request):
        query = request.GET.get('q')
        results= ''
        if query:
            results = Post.objects.filter(
                Q(h1__icontains=query) | Q(text__icontains=query)
                )
            pagination = Paginator(results, 3)
            page_number = request.GET.get('page')
            page_obj = pagination.get_page(page_number)
            return render(request, 'search.html', context={
                'search' : 'Поиск',
                'results' : page_obj,
                'count' : pagination.count
            })


class FeedBackView(View):
    def get(self, request):
        form = FeedBackForm()
        return render(request, 'contact.html', context={
            'form': form,
            'title': 'Написать мне'
        })

    def post(self, request):
        form = FeedBackForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            from_email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            try:
                send_mail(f'От {name} | {subject} | {from_email}', message, from_email, ['babaev_aleksandr@icloud.com'])
            except BadHeaderError:
                return HttpResponse('Невалидный заголовок')
            return HttpResponseRedirect('success')
        return render(request, 'contact.html', context={
            'form': form,
        })


class SuccessView(View):
    def get(self, request):
        return render(request, 'success.html', context={
            'title': 'Спасибо'
        })


class TagView(View):
    def get(self, request, slug):
        tag = get_object_or_404(Tag, slug=slug)
        posts = Post.objects.filter(tag=tag)
        common_tags = Post.tag.most_common()
        return render(request, 'tag.html', context={
            'title': f'#ТЕГ {tag}',
            'posts': posts,
            'common_tags': common_tags
        })  