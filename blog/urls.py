from django.urls import path
from .  import views
urlpatterns = [
    #path('',views.starting_page,name='starting_page'),
    path('',views.StartingPageView.as_view(),name='starting_page'),
    #path('posts',views.posts,name='posts_page'),
    path('posts',views.PostView.as_view(),name='posts_page'),
    #path('posts/<slug:slug>',views.post_detail,name='post_detail_page'),
    path('posts/<slug:slug>',views.PostDetailView.as_view(),name='post_detail_page'),
    path("read-later",views.ReadLaterView.as_view(),name='read-later')
]
