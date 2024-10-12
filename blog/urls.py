from django.urls import path
from blog import views
urlpatterns = [
     path('',views.home,name="home"),
     path('dashboard/',views.dashboard,name="dashboard"),
     path('blog/',views.blog_posts,name="blog"),
     path('post_detail/<int:id>/',views.post_detail,name="post_detail"),
     path('create/', views.create_post, name='create_post'),
     path('edit_post/<int:id>/',views.edit_post,name="edit_post"),
     path('author_post_detail/<int:id>/',views.author_post_detail,name="author_post_detail"),
     path('post/delete/<int:id>/',views.post_delete,name="post_delete"),
     path("search/",views.search,name="search"),
]