import datetime

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, CreateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView

from .forms import NewsForm, CommentForm, SearchForm
from .models import Newstopic, Comment


# Create your views here.
class IndexView(ListView):
    model = Newstopic
    paginate_by = 5
    template_name = 'newsapp/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        news = Newstopic.objects.filter(updated_at__lte=timezone.now()).order_by('-updated_at')
        paginator = Paginator(news, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            news = paginator.page(page)
        except PageNotAnInteger:
            news = paginator.page(1)
        except EmptyPage:
            news = paginator.page(paginator.num_pages)

        context['news'] = news
        return context


# def index(request):
#     news = Newstopic.objects.filter(updated_at__lte=timezone.now()).order_by('updated_at')
#     page = request.GET.get('page', 1)
#     paginator = Paginator(news, 5)
#
#     try:
#         news = paginator.page(page)
#     except PageNotAnInteger:
#         news = paginator.page(1)
#     except EmptyPage:
#         news = paginator.page(paginator.num_pages)
#     return render(request, 'newsapp/index.html', {'news': news})

class NewsDetailView(DetailView):
    model = Newstopic
    template_name = 'newsapp/news_detail.html'

    def get_context_data(self, **kwargs):
        context = super(NewsDetailView, self).get_context_data(**kwargs)
        news = Newstopic.objects.get(pk=self.kwargs['pk'])
        context['news'] = news
        return context


# def news_detail(request, pk):
#     news = get_object_or_404(Newstopic, pk=pk)
#     return render(request, 'newsapp/news_detail.html', {'news': news, 'pk': pk})


class SearchView(FormView):
    # pdb.set_trace()
    form_class = SearchForm
    success_url = reverse_lazy('search_results')
    template_name = 'newsapp/search_results.html'

    def get(self, request, *args, **kwargs):
        q = request.GET.get('search_query')
        # pdb.set_trace()
        news1 = Newstopic.objects.filter(title__icontains=q)
        news2 = Newstopic.objects.filter(description__icontains=q)
        news = news1.union(news2)
        return render(request, 'newsapp/search_results.html', {'news': news})
        # return super(NewNewsView, self).form_valid(form)
        # return self.render_to_response(self.get_context_data(news=news))


# def search(request):
#     q = request.GET.get('query')
#     news1 = Newstopic.objects.filter(title__icontains=q)
#     news2 = Newstopic.objects.filter(description__icontains=q)
#     news = news1.union(news2)
#     if news:
#         return render(request, 'newsapp/search_results.html', {'news': news})
#     else:
#         return render(request, 'newsapp/nothing.html')


class NewNewsView(FormView):
    form_class = NewsForm
    template_name = 'newsapp/news_edit.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.created_by = self.request.user
        news.updated_by = self.request.user
        news.updated_at = datetime.datetime.now()
        news.save()
        self.object = news
        return super(NewNewsView, self).form_valid(form)

    def get_success_url(self):
        return reverse('newsapp:news_detail', kwargs={'pk': self.object.pk})


# def news_new(request):
#     if request.method == "POST":
#         form = NewsForm(request.POST)
#         if form.is_valid():
#             news = form.save(commit=False)
#             news.created_by = request.user
#             news.updated_by = request.user
#             news.updated_at = datetime.datetime.now()
#             news.save()
#             return redirect('newsapp:news_detail', pk=news.pk)
#         else:
#             pass
#     else:
#         form = NewsForm()
#     return render(request, 'newsapp/news_edit.html', {'form': form})



class AddCommentView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'newsapp/add_comment.html'

    def form_valid(self, form):
        print(self.kwargs['pk'])
        comment = form.save(commit=False)
        comment.author = self.request.user
        comment.news = Newstopic.objects.get(pk=self.kwargs['pk'])
        comment.save()
        return super(AddCommentView, self).form_valid(form)

    def get_success_url(self):
        return reverse('newsapp:news_detail', kwargs={'pk': self.kwargs['pk']})


# def add_comment(request, pk):
#     news = get_object_or_404(Newstopic, pk=pk)
#     if request.method == "POST":
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.news = news
#             comment.author = request.user
#             comment.save()
#             return redirect('newsapp:news_detail', pk=news.pk)
#     else:
#         form = CommentForm()
#     return render(request, 'newsapp/add_comment.html', {'form': form})

class CommentRemoveView(DeleteView):
    model = Comment

    def form_valid(self, form):
        self.object = Comment.object.get(pk=self.kwargs['pk'])
        return super(NewNewsView, self).form_valid(form)

    def get_success_url(self):
        return reverse('newsapp:news_detail', kwargs={'pk': self.object.news.pk})

# def comment_remove(request, pk):
#     comment = get_object_or_404(Comment, pk=pk)
#     news = comment.news
#     comment.delete()
#     return redirect('newsapp:news_detail', pk=news.pk)
