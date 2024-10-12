from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from blog.models import Blog_Post
from django.core.paginator import Paginator
import math
from .forms import BlogPostForm
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
# Create your views here.

def home(request):
        posts=Blog_Post.objects.all().order_by('-created_at')[:2]
        return render(request,'blog/home.html',{'posts':posts})


# dashboard view
@login_required(login_url='/')
def dashboard(request):
     posts=Blog_Post.objects.filter(author=request.user)
     no_of_post=4
     page=request.GET.get('page')
     if page is None:
            page=1
     else:
            page=int(page)      
     length=len(posts)
     posts=posts[(page-1)*no_of_post:page*no_of_post]
     if page>1:
         prev=page-1
     else:
           prev=None
     if page<math.ceil(length/no_of_post):        
        nxt=page+1
     else:
           nxt=None   
     
     context = {
        'posts': posts,
        'prev':prev,
        'nxt':nxt
    }
     return render(request,'blog/dashboard.html',context)



# views for display all posts
def blog_posts(request):
      posts = Blog_Post.objects.all() 
      no_of_post=4
      page=request.GET.get('page')
      if page is None:
            page=1
      else:
            page=int(page)      
      length=len(posts)
      posts=posts[(page-1)*no_of_post:page*no_of_post]
      if page>1:
         prev=page-1
      else:
           prev=None
      if page<math.ceil(length/no_of_post):        
        nxt=page+1
      else:
           nxt=None   
      context={
          'posts':posts,
          'prev':prev,
            'nxt':nxt
      }
      return render(request,'blog/blog_home.html',context)


# view for display a single 
def post_detail(request,id):
     post=Blog_Post.objects.get(pk=id)
     context={
          'post':post,
     }
     return render(request,'blog/post_detail.html',context)

# author will create post
@login_required
def create_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('dashboard')
    else:
        form = BlogPostForm()
    return render(request, 'blog/create_post.html', {'form': form})

# author will edit post
@login_required
def edit_post(request,id):
     try:
          # post=Blog_Post.objects.get(pk=id)
          post = get_object_or_404(Blog_Post, id=id, author=request.user)
          if request.method == 'POST':
               form=BlogPostForm(request.POST,instance=post)
               if form.is_valid():
                    form.save()
                    messages.success(request,"you have edtited successfully")
                    form=BlogPostForm()
                    # return redirect('edit_post',id=id)

     # in get method we get old data
          else:
             form = BlogPostForm(instance=post)
          return render(request, 'blog/edit_post.html', {'form': form})   
     except Exception as e:
          messages.warning(request,"something wenting wrong")

# this is for author post detail
def author_post_detail(request,id):
     post=Blog_Post.objects.get(pk=id)
     context={
          'post':post
     }
     return render(request,'blog/author_post_detail.html',context)

# author will delete  post but only by admin
def post_delete(request,id):
     post=Blog_Post.objects.get(pk=id)
     if request.method == 'POST':
          post.delete()
          return redirect('dashboard')
     return render(request,'blog/post_confirm_delete.html',{'post':post})     

# views for search
def search(request):
     if request.method == "GET":
          title=request.GET.get('title')
          if title!=None:
               posts=Blog_Post.objects.filter(title__icontains=title)
     context={
          'posts':posts

     }  
     return render(request,'blog/search.html',context)        



