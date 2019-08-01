#--*--encoding--*--
from django.shortcuts import render
from django.http import HttpResponse
from .models import Article
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone #引入timezone模块
import datetime

# Create your views here.
class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)

def index(request):
    return render(request, 'index.html')

# 获取所有
@csrf_exempt
def all(request):
    if request.method == 'GET':
        pageSize = int(request.GET.get('pageSize'))
        pageNumber = int(request.GET.get('pageNumber'))
        searchText = request.GET.get('searchText')
        sortName = request.GET.get('sortName')
        sortOrder = request.GET.get('sortOrder')
    
    total = Article.objects.all().count()
    articles = Article.objects.order_by('-id')[(pageNumber-1)*pageSize:(pageNumber)*pageSize]
    rows = []
    data = {"total": total, "rows": rows}
    for article in articles:
        rows.append({'id': article.id, 'title': article.title, 'content': article.content, 'create_time': article.create_time})
        
    return HttpResponse(json.dumps(data, cls=CJsonEncoder), content_type="application/json")

# 增加
@csrf_exempt
def add(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        article = Article(title = title, content = content, create_time = timezone.now())
        r = article.save()
        ret = {"ret": True, 'title': title, 'content': content, 'r': r}
        return HttpResponse(json.dumps(ret))

def article(request, article_id):
    article = Article.objects.get(pk = article_id)
    return render(request, 'article.html', {'article': article})

# 删除
@csrf_exempt
def delete(request):
    return_dict = {"ret": True, "errMsg": "", "rows": []}
    article_ids = request.POST.getlist('ids')
    for id in article_ids:
        Article.objects.filter(id=int(id)).delete()
    return HttpResponse(json.dumps(return_dict))

# 编辑
@csrf_exempt
def edit(request):
    return_dict = {"ret": True, "errMsg": "", "msg": ''}
    if request.method == 'POST':
        id = request.POST.get('id')
        title = request.POST.get('title')
        content = request.POST.get('content')
        Article.objects.filter(id=id).update(title=title, content=content)
        return_dict['msg'] = '修改成功'
    
    return HttpResponse(json.dumps(return_dict), content_type="application/json")    

# 获取单条数据
@csrf_exempt
def get_a_article(request):
    return_dict = {"ret": True, "errMsg": "", "title": '', 'content': '', 'id': ''}
    
    if request.method == 'POST':
        id = request.POST.get('id')
        article = Article.objects.filter(id=id)[0].__dict__
        return_dict['title'] = article['title']
        return_dict['content'] = article['content']
        return_dict['id'] = article['id']
        
    return HttpResponse(json.dumps(return_dict), content_type="application/json")
        


    
    