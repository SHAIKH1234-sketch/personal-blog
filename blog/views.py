from django.shortcuts import render,get_object_or_404
from .models import Post
from django.views.generic.base import TemplateView
from django.views.generic import ListView,DetailView
from .forms import CommentsForm
from django.views import View
from django.urls import reverse
from django.http import HttpResponseRedirect
# Create your views here.

class StartingPageView(ListView):
    template_name='blog/index.html'
    model=Post
    ordering=['-date']
    context_object_name='posts'

    def get_queryset(self):
        base_query=super().get_queryset()
        data=base_query[:3]
        return data
'''def starting_page(request):
    latest_post=Post.objects.all().order_by("-date")[:3]
    return render(request,'blog/index.html',{"posts":latest_post})'''
class PostView(ListView):
    template_name='blog/all-posts.html'
    model=Post
    context_object_name='all_posts'
    ordering=['-date']

'''def posts(request):
    all_posts=Post.objects.all().order_by('-date')
    return render(request,'blog/all-posts.html',{"all_posts":all_posts})'''

class PostDetailView(View):
    def is_stored_post(self,request,post_id):
        stored_posts=request.session.get('stored_posts')
        if stored_posts is not  None:
            is_save_for_later=post_id in stored_posts
        else:
            is_save_for_later=False
        return is_save_for_later

    def get(self,request,slug):
        post=Post.objects.get(slug=slug)
        context={
        "post":post,
        "post_tag":post.tags.all(),
        "comments_form":CommentsForm(),
        "comments":post.comments.all().order_by('-id'),
        "is_save_for_later":self.is_stored_post(request,post.id)
        }
        return render(request,'blog/post-detail.html',context)
    def post(self,request,slug):
        comments_form=CommentsForm(request.POST)
        post=Post.objects.get(slug=slug)
        if comments_form.is_valid():
            comment=comments_form.save(commit=False)
            comment.post=post
            comment.save()
            return HttpResponseRedirect(reverse("post_detail_page",args=[slug]))

        context={
        "post":post,
        "post_tag":post.tags.all(),
        "comments_form":comments_form,
        "comments":post.comments.all().order_by('-id'),
        "is_save_for_later":self.is_stored_post(request,post_id),
        }
        return render(request,'blog/post-detail.html',context)

class ReadLaterView(View):
    def get(self,request):
        stored_posts=request.session.get("stored_posts")

        context={}
        if stored_posts is None or len(stored_posts)==0:
            context["posts"]=[]
            context['has_posts']=False
        else:
            posts=Post.objects.filter(id__in=stored_posts)
            context["posts"]=posts
            context['has_posts']=True
        return render(request,'blog/stored-posts.html',context)



    def post(self,request):
        stored_posts=request.session.get("stored_posts")

        if stored_posts is None:
            stored_posts=[]
        post_id=int(request.POST['post_id'])#from hidden form
        if post_id not in stored_posts:
            stored_posts.append(post_id)
        else:
            stored_posts.remove(post_id)#when e click post later button
        request.session['stored_posts']=stored_posts

        return HttpResponseRedirect("/blog/")
