from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from .forms import CreateArticle
from django.contrib import messages
from .models import Article, Comment


# Create your views here.


def index(request):
    return render(request, "index.html")


def about(request):
    return render(request, "about.html")


@login_required(login_url="user:login")
def articles(request, article_id):
    return render(request, "articles.html", {"article_id": article_id})


@login_required(login_url="user:login")
def dashboard(request):
    articles = Article.objects.filter(author=request.user)
    c = {"articles": articles}
    return render(request, "dashboard.html", c)


@login_required(login_url="user:login")
def addarticle(request):
    form = CreateArticle(request.POST or None, request.FILES or None)
    if form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        article.save()
        messages.success(request, ("New Article Added!"))
        return redirect("index")

    return render(request, "addarticle.html", {"form": form})


@login_required(login_url="user:login")
def detail(request, id):
    # article = Article.objects.get(id=id)
    article = get_object_or_404(Article, id=id)

    comments = Comment.objects.filter(article=article)
    c = {"article": article, "comments": comments}

    return render(request, "detail.html", c)


@login_required(login_url="user:login")
def update(request, id):
    article = get_object_or_404(Article, id=id)
    form = CreateArticle(request.POST or None, request.FILES or None, instance=article)
    if form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        article.save()
        messages.success(request, ("Article Updated!"))
        return redirect("index")

    return render(request, "update.html", {"form": form, "article": article})


@login_required(login_url="user:login")
def delete(request, id):
    article = get_object_or_404(Article, id=id)
    article.delete()
    messages.success(request, ("Article Deleted!"))
    return redirect("article:dashboard")


def articlesPage(request):
    keyword = request.GET.get("keyword")
    if keyword:
        articles = Article.objects.filter(title__contains=keyword)
        return render(request, "articlesPage.html", {"articles": articles})

    articles = Article.objects.all().order_by("-created_date")
    c = {"articles": articles}
    return render(request, "articlesPage.html", c)


def comment(request, id):
    article = get_object_or_404(Article, id=id)
    if request.method == "POST":
        comment_author = request.POST.get("comment_author")
        comment_content = request.POST.get("comment_content")
        newComment = Comment(
            article=article,
            author=comment_author,  # changed from comment_author
            content=comment_content,  # changed from comment_content
        )
        newComment.save()

    return redirect(reverse("article:detail", kwargs={"id": id}))
