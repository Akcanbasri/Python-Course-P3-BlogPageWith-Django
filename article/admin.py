from django.contrib import admin
from .models import Article, Comment


# Register your models here.

admin.site.register(Comment)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "created_date"]
    list_display_links = ["title"]
    search_fields = ["title"]
    list_filter = ["created_date"]
    # delete some articles from admin panel
    actions = ["delete_selected"]

    class Meta:
        model = Article
