from django.shortcuts import render, HttpResponse, get_object_or_404
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from .models import Blog

# Create your views here.
def allblogs(request):
    # blogs = Blog.objects
    # blogs = Blog.published.filter(title__startswith='My')
    # return render(request, 'blog/allblogs.html', {'blogs':blogs})

    # object_list = Blog.published.all()
    object_list = Blog.objects.all()
    paginator = Paginator(object_list, 3) # 3 posts in each page
    page = request.GET.get('page')
    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        blogs = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        blogs = paginator.page(paginator.num_pages)
    return render(request,'blog/allblogs.html',
                          {'page': page,
                          'blogs': blogs})



def detail(request, blog_id):
    detailblog = get_object_or_404(Blog, pk=blog_id)
    return render(request, 'blog/detail.html', {'blog':detailblog})

# def HomePage(request):
#     return HttpResponse('My Home Page')
