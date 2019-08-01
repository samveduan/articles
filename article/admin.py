from django.contrib import admin
from .models import Article, Category, Tags

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'create_time', )
    list_display_link = ('title',)
    
# Register your models here.
admin.site.register(Article, ArticleAdmin)
admin.site.register(Category)
admin.site.register(Tags)
