import datetime

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .forms import NewsForm, CommentForm
from .models import Newstopic, Comment


# Create your views here.
def index(request):
    news = Newstopic.objects.filter(updated_at__lte=timezone.now()).order_by('updated_at')
    page = request.GET.get('page', 1)
    paginator = Paginator(news, 5)

    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        news = paginator.page(1)
    except EmptyPage:
        news = paginator.page(paginator.num_pages)
    return render(request, 'newsapp/index.html', {'news': news})


def news_detail(request, pk):
    news = get_object_or_404(Newstopic, pk=pk)
    return render(request, 'newsapp/news_detail.html', {'news': news, 'pk': pk})


def search(request):
    q = request.GET.get('query')
    news1 = Newstopic.objects.filter(Title__icontains=q)
    news2 = Newstopic.objects.filter(description__icontains=q)
    news = news1.union(news2)
    if news:
        return render(request, 'newsapp/search_results.html', {'news': news})
    else:
        return render(request, 'newsapp/nothing.html')


def news_new(request):
    if request.method == "POST":
        form = NewsForm(request.POST)
        if form.is_valid():
            news = form.save(commit=False)
            news.created_by = request.user
            news.updated_by = request.user
            news.updated_at = datetime.datetime.now()
            news.save()
            return redirect('newsapp:news_detail', pk=news.pk)
        else:
            pass
    else:
        form = NewsForm()
    return render(request, 'newsapp/news_edit.html', {'form': form})


def add_comment(request, pk):
    news = get_object_or_404(Newstopic, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.news = news
            comment.author = request.user
            comment.save()
            return redirect('newsapp:news_detail', pk=news.pk)
    else:
        form = CommentForm()
    return render(request, 'newsapp/add_comment.html', {'form': form})


# @login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    news = comment.news
    comment.delete()
    return redirect('newsapp:news_detail', pk=news.pk)
