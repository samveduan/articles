from django.db import models

# Create your models here.
class Article(models.Model):
    title = models.CharField('标题', max_length=64)
    content = models.TextField('内容', null=True)
    create_time = models.DateTimeField('发布时间')
    
    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '文章'
    
    def __str__(self):
        return self.title
    
class Category(models.Model):
    name = models.CharField('分类', max_length=100)
    
    class Meta:
        verbose_name = '分类'
        verbose_name_plural = '分类'
        
    def __str__(self):
        return self.name    

class Tags(models.Model):
    name = models.CharField('标签', max_length=100)
    
    class Meta:
        verbose_name = '标签'
        verbose_name_plural = "标签"
    
    def __str__(self):
        return self.name