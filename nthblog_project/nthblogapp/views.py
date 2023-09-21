from django.shortcuts import render,get_object_or_404,redirect, HttpResponseRedirect, Http404
from django.http.response import HttpResponse
from .models import Post,Comment
from .forms import PostCreateForm,PostEditForm,CreateUserForm, CommentForm
from django.contrib.auth import logout,login,authenticate
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger


def register_page(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            form = CreateUserForm()
            return render(request, 'register.html', {'form': form})
    else:
        form = CreateUserForm()
        return render(request,'register.html',{'form':form})


def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,'Login Success')
            return redirect('post_list')
        else:
            messages.warning(request,'Invalid Username or Password')
            return redirect('login')
    else:
        return render(request,'login.html')



def logout_page(request):
    logout(request)
    messages.success(request,'Logout Successful')
    return redirect('login')

def index(request):
    return HttpResponse("Hello NTH")

def post_list(request):
    posts_list = Post.objects.all().order_by('-id')
    query = request.POST.get('q')
    if query:
        posts_list = Post.objects.filter(
            Q(title__contains=query) |
            Q(author__username__contains=query) |
            Q(body__contains=query)
        )
    paginator = Paginator(posts_list,4)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request,'post_list.html',{'posts':posts})

def post_detail(request,id,slug):
    post = get_object_or_404(Post,id=id, slug=slug)
    comments = Comment.objects.filter(post=post, reply=None).order_by('-id')
    is_liked = False
    is_favourite = False
    if post.likes.filter(id=request.user.id).exists():
        is_liked = True
    if request.method == "POST":
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            content = request.POST.get('content')
            reply_id = request.POST.get('comment_id')
            comment_qs = None
            if reply_id:
                comment_qs = Comment.objects.get(id=reply_id)
            comment = Comment.objects.create(post=post, user=request.user, content=content, reply=comment_qs)
            comment.save()
            return HttpResponseRedirect(post.get_absolute_url())
    else:
        comment_form = CommentForm()
    if post.favourite.filter(id=request.user.id).exists():
        is_favourite = True
    return render(request,'post_detail.html',{
        'post':post,
        'is_liked':is_liked,
        'total_likes':post.total_likes(),
        'is_favourite':is_favourite,
        'comments':comments,
        'comment_form':comment_form
    })


def post_create(request):
    if request.method == "POST":
        form = PostCreateForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_list')
        else:
            form = PostCreateForm()
            return render(request,'post_create.html',{'form':form})
    else:
        form = PostCreateForm()
        return render(request,'post_create.html',{'form':form})


def post_edit(request,id):
    post = get_object_or_404(Post,id=id)
    if post.author != request.user:
        raise Http404()
    else:
        if request.method == "POST":
            form = PostEditForm(request.POST or None, instance=post)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(post.get_absolute_url())
        else:
            form = PostEditForm(instance=post)
            context = {'form':form,'post':post}
            return render(request,'post_edit.html',context)


def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    if post.author != request.user:
        raise Http404()
    post.delete()
    return redirect('post_list')


def like_post(request):
    post_id = request.POST.get('post_id')
    post = get_object_or_404(Post, id=post_id)
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked = False
    else:
        post.likes.add(request.user)
        is_liked = True
    return HttpResponseRedirect(post.get_absolute_url())


def favourite_post(request,id):
    post = get_object_or_404(Post,id=id)
    if post.favourite.filter(id=request.user.id).exists():
        post.favourite.remove(request.user)
    else:
        post.favourite.add(request.user)
    return HttpResponseRedirect(post.get_absolute_url())


def post_favourite_list(request):
    user = request.user
    favourite_posts = user.favourite.all()
    return render(request,'post_favourite_lists.html',{'favourite_posts':favourite_posts})










