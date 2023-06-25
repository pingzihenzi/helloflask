# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li
    :license: MIT, see LICENSE for more details.
"""
import os
from flask import Flask, render_template, flash, redirect, url_for, Markup

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'secret string')
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True


def say():
    return "i am a say"
app.add_template_global(say,name='hi') ## 方法名，自定义名称hi用于其他视图函数调用，或者是template中调用

user = {
    'username': 'Grey Li',
    'bio': 'A boy who loves movies and music.',
}

movies = [
    {'name': 'My Neighbor Totoro', 'year': '1988'},
    {'name': 'Three Colours trilogy', 'year': '1993'},
    {'name': 'Forrest Gump', 'year': '1994'},
    {'name': 'Perfect Blue', 'year': '1997'},
    {'name': 'The Matrix', 'year': '1999'},
    {'name': 'Memento', 'year': '2000'},
    {'name': 'The Bucket list', 'year': '2007'},
    {'name': 'Black Swan', 'year': '2010'},
    {'name': 'Gone Girl', 'year': '2014'},
    {'name': 'CoCo', 'year': '2017'},
]


@app.route('/watchlist')
def watchlist():
    return render_template('watchlist.html', user=user, movies=movies)


@app.route('/')
def index():
    return render_template('index.html')


# register template context handler
@app.context_processor
def inject_info():
    foolish = 'I am lier.'
    return dict(foo=foolish)  # equal to: return {'foo': foo}

# @app.context_processor
def test_info():
    text = 'this is a text'
    return dict(hell=text)
app.context_processor(test_info)

@app.context_processor
def range_num():
    star_numbers = range(1,100)
    return dict(numbers=star_numbers)


# register template global function
@app.template_global()
def bar():
    return 'I am bar.'

# @app.template_global
def sayhi():
    return "none"
app.add_template_global(sayhi,name='sayhi')

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/wi')
def wi():
    text = Markup('<h1>hello wi</h1>')
    return render_template('index.html',text=text)


# register template filter
@app.template_filter()
def musical(s):
    return s + Markup(' &#9835;')


# register template test
@app.template_test()
def baz(n):
    if n == 'baz':
        return True
    return False

def test1():
    return "this is test1"
app.jinja_env.globals['test1'] = test1

test2 = 'im test2'
app.jinja_env.globals['test2'] = test2

def smiling(s):
    return s + ':-)'
app.jinja_env.filters['smiling'] = smiling


@app.route('/watchlist2')
def watchlist_with_static():
    return render_template('watchlist_with_static.html', user=user, movies=movies)


# message flashing
@app.route('/flash')
def just_flash():
    flash('I am flash, who is looking for me?')
    return redirect(url_for('index'))


# 404 error handler
@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


# 500 error handler
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500
