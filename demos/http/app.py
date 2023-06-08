# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li
    :license: MIT, see LICENSE for more details.
"""
import os
try:
    from urlparse import urlparse, urljoin
except ImportError:
    from urllib.parse import urlparse, urljoin

import logging
from jinja2 import escape
from jinja2.utils import generate_lorem_ipsum
from flask import Flask, make_response, request, redirect, url_for, abort, session, jsonify
from flask import json
import datetime

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'secret string')
app.permanent_session_lifetime = int((os.getenv('SESSION_LIFETIME',60)))


# get name value from query string and cookie
@app.route('/')
@app.route('/hello')
def hello():
    name = request.args.get('name')
    if name is None:
        name = request.cookies.get('name', 'Human')
    response = '<h1>Hello, %s!</h1>' % escape(name)  # escape name to avoid XSS
    # return different response according to the user's authentication status
    if 'logged_in' in session:
        response += '[Authenticated]'
    else:
        response += '[Not Authenticated]'
    return response


@app.route('/say')
def say():
    # res = os.getenv('SECRET_KEY')
    # res = os.getenv('SESSION_LIFETIME')
    res = request.referrer
    # logging.debug(request.full_path)
    # return redirect(request.referrer or url_for('hello'))
    host = urlparse(urljoin(request.host_url,request.full_path))
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url,request.full_path))
    if test_url.scheme in ('http','https') and ref_url.netloc == test_url.netloc:
        return "success"
    return str(host)


# redirect
@app.route('/hi')
def hi():
    return redirect(url_for('hello'))


# use int URL converter
@app.route('/goback/<int:year>')
def go_back(year):
    return 'Welcome to %d!' % (2023 - year)


# use any URL converter
@app.route('/colors/<any(blue, white, red):color>')
def three_colors(color):
    return '<p>Love is patient and kind. Love is not jealous or boastful or proud or rude.</p>'


@app.route('/firstname/<any(huang,chen):firstname>')
def show_name(firstname):
    return '<h1>first name is:%s</h1>' % firstname


# return error response
@app.route('/brew/<drink>')
def teapot(drink):
    if drink == 'coffee':
        abort(418)
    else:
        return 'A drop of tea.'


# 404
@app.route('/404')
def not_found():
    abort(404)


# return response with different formats
@app.route('/note', defaults={'content_type': 'text'})
@app.route('/note/<content_type>')
def note(content_type):
    content_type = content_type.lower()
    if content_type == 'text':
        body = '''Note
to: Peter
from: Jane
heading: Reminder
body: Don't forget the party!
'''
        response = make_response(body)
        response.mimetype = 'text/plain'
    elif content_type == 'html':
        body = '''<!DOCTYPE html>
<html>
<head></head>
<body>
  <h1>Note</h1>
  <p>to: Peter</p>
  <p>from: Jane</p>
  <p>heading: Reminder</p>
  <p>body: <strong>Don't forget the party!</strong></p>
</body>
</html>
'''
        response = make_response(body)
        response.mimetype = 'text/html'
    elif content_type == 'xml':
        body = '''<?xml version="1.0" encoding="UTF-8"?>
<note>
  <to>Peter</to>
  <from>Jane</from>
  <heading>Reminder</heading>
  <body>Don't forget the party!</body>
</note>
'''
        response = make_response(body)
        response.mimetype = 'application/xml'
    elif content_type == 'json':
        body = {"note": {
            "to": "Peter",
            "from": "Jane",
            "heading": "Remider",
            "body": "Don't forget the party!"
        }
        }
        response = jsonify(body)
        # equal to:
        # response = make_response(json.dumps(body))
        # response.mimetype = "application/json"
    else:
        abort(400)
    return response


@app.route('/fine')
def fine():
    # res = '''<h1>hello response</h1>
    # <p>Note:Jone</p>
    # <P>To:Peter</P>
    # <P>From:huangcheng</P>
    # <P>Heading:Reminder</P>
    # <P><strong>Body:do not forget the party</strong></P>'''
#     res = '''<?xml version="1.0" encoding="UTF-8"?>
# <note>
#     <to>Jone</to>
#     <from>Peter</from>
#     <heading>Reminder</heading>
#     <body>dont forget the party!</body>
# </note>'''
    res = {
        "note":{
            "to":"Jone",
            "from":"huang",
            "heading":"Reminder",
            "body":"dont forget the party!",
        }
    }
    response = make_response(json.dumps(res))
    # response = make_response(res)
    # response.mimetype = 'application/json'
    # response.headers['content-type'] = 'application/xml;charset=utf-8'
    # return response
    # return jsonify({"name":"huangcheng","age":12})
    # return jsonify(message="error"), 500
    return jsonify(name="huangcheng",age=12)


# set cookie
@app.route('/set/<name>')
def set_cookie(name):
    response = make_response(redirect(url_for('hello')))
    response.set_cookie('name', name)
    return response


# log in user
@app.route('/login')
def login():
    session['logged_in'] = True
    return redirect(url_for('hello'))


# protect view
@app.route('/admin')
def admin():
    if 'logged_in' not in session:
        abort(403)
    return 'Welcome to admin page.'


# log out user
@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in')
    return redirect(url_for('hello'))


# AJAX
@app.route('/post')
def show_post():
    post_body = generate_lorem_ipsum(n=2)
    return '''
<h1>A very long post</h1>
<div class="body">%s</div>
<button id="load">Load More</button>
<script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
<script type="text/javascript">
$(function() {
    $('#load').click(function() {
        $.ajax({
            url: '/more',
            type: 'get',
            success: function(data){
                $('.body').append(data);
            }
        })
    })
})
</script>''' % post_body


@app.route('/more')
def load_post():
    return generate_lorem_ipsum(n=1)


# redirect to last page
@app.route('/foo')
def foo():
    return '<h1>Foo page</h1><a href="%s">Do something and redirect</a>' \
           % url_for('do_something',xiayige=None)


@app.route('/bar')
def bar():
    return '<h1>Bar page</h1><a href="%s">Do something and redirect1</a>' \
           % url_for('do_something', next=request.full_path)


@app.route('/do-something')
def do_something():
    # do something here
    return redirect_back()
    # return redirect(url_for('hello'))
    # return redirect(request.args.get('xiayige',url_for('hello')))


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc


def redirect_back(default='hello', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            # logging.info(target+"********")
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))

@app.route('/helloo/<content_type>',defaults={'content_type':'json'})
def helloo(content_type):
    name = request.args.get('name','default name')
    head_type = content_type.lower()
    if head_type == 'text':
        res_text = '''
    <h1>welcome to my page</h1>
    <p>hello %s</p>
    <p>redirect page</p>
    '''% name
        response = make_response(res_text)
        response.mimetype = 'text/plain'
        return response
    elif head_type == 'xml':
        res_xml = '''<?xml version="1.0" encoding="UTF-8"?>
    <note>
    <page>xml page</page>
    <name>%s</name>
    </note>'''% name
        response = make_response(res_xml)
        response.mimetype = 'text/xml'
        return response
    elif head_type == 'html':
        res_html = '''
    <h1>welcome to my page</h1>
    <p>hello %s</p>
    <p>redirect page</p>
    '''% name
        response = make_response(res_html)
        response.mimetype = 'text/html'
        return response
    elif head_type == 'json':
        res_json = {
            "node":{
                'page name':'json page',
                'name':f'{name}',
                'headtype':'application/json',
                'last':'success',
            }
        }
        response = make_response(json.dumps(res_json))
        response.mimetype = 'application/json'
        return response
    else:
        abort(500)

@app.route('/loggin')
def loggin():
    session['status']=True
    session.permanent = True
    
    return redirect(url_for('helloo'))

@app.route('/adminn')
def adminn():
    if "status" in session:
        if session['status']:
            return "success"
        else:
            return "please login"
    else:
        abort(500)

@app.route('/loggout')
def loggout():
    if 'status' in session:
        session.pop('status')
    return "logout"

@app.route('/fooo')
def fooo():
    html_text = '''
    <h1>welcome fooo</h1>
    <a href='%s'>redirect url </a>
    ''' % url_for('loggin')
    return html_text

@app.route('/partline')
def partline():
    return 