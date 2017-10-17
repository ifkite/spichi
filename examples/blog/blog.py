# -*- coding: utf-8 -*-
'''
# =============================================================================
#      FileName: blog.py
#          Desc: 
#        Author: ifkite
#         Email: holahello@163.com
#      HomePage: http://github.com/ifkite
#      python version: 2.7.10
#    CreateTime: 2017-10-11 21:28:37
# =============================================================================
'''


import os
from datetime import datetime
from spichi.spichi import create_app
from spichi.views import View

conf_path = os.path.dirname(os.path.abspath(__file__))
app = create_app(path=conf_path)
cache = app.caches['redis'].cache
from sqlalchemy.sql import text


def get_now():
    return str(datetime.now())

def serialize_rowproxy(rowproxy):
    if isinstance(rowproxy, list):
        return [r.items() for r in rowproxy if hasattr(r, 'items')]
    else:
        return rowproxy.items() if hasattr(rowproxy, 'items') else ''

_s = serialize_rowproxy

# example
@app.route('/', 'home')
def home(request):
    '''
    home page
    '''
    return _s(app.databases['mysql'].execute(text(
            'select title, created_time, category \
                    from article \
                    where is_deleted = 0 \
                    order by created_time limit 5'
            )).fetchall())


@app.route('/articles/<aid>', 'article')
def article(request, aid):
    '''
    read an article
    '''
    return _s(app.databases['mysql'].execute(text(
        'select title, created_time, category, content \
                from article \
                where id=:id and is_deleted = 0'
        ), id=aid).fetchone())


@app.route('/cms/articles/', 'article_create')
def article_create(request):
    '''
    '''
    # check login
    # check request
    # create content
    app.databases['mysql'].execute(text(
        'insert into article(title, created_time, modified_time, description, content) \
                values(:title, :created_time, :modified_time, :description, :content)'),
        title=request.form['title'],
        created_time=get_now(),
        modified_time=get_now(),
        description=request.form['description'],
        content=request.form['content']
        )


@app.route_class('/cms/articles/<aid>', 'article_cms')
class ArticleCms(View):
    def put(self, request, aid):
        # check login
        # check request
        # return 200 status
        app.databases['mysql'].execute(text(
            'update article \
                    set title=:title, description:=description, content=:content \
                    where id=:id'),
            title=request.form['title'],
            description=request.form['description'],
            content=request.form['content'],
            id=aid
            )

    def delete(self, request, aid):
        # check login
        # chech request
        # return 204 status
        app.databases['mysql'].execute(text(
            'update article \
                    set is_deleted=1\
                    where id=:id'),
                    id=aid)
