from django.shortcuts import render, HttpResponse, redirect
from .forms import CreateArticle
from django.contrib import messages
from .models import Article


# Create your views here.


def index(request):
    return render(request, "index.html")


def about(request):
    return render(request, "about.html")


def articles(request, article_id):
    return render(request, "articles.html", {"article_id": article_id})


def dashboard(request):
    articles = Article.objects.filter(author=request.user)
    c = {"articles": articles}
    return render(request, "dashboard.html", c)


def addarticle(request):
    form = CreateArticle(request.POST or None)
    if form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        article.save()
        messages.success(request, ("New Article Added!"))
        return redirect("index")

    return render(request, "addarticle.html", {"form": form})


def detail(request, id):
    article = Article.objects.get(id=id)
    return render(request, "detail.html", {"article": article})