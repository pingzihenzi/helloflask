# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li
    :license: MIT, see LICENSE for more details.
"""
import click
from flask import Flask

app = Flask(__name__)


# the minimal Flask application
@app.route('/')
def index():
    return '<h1>Hello, World!!!</h1>'


# bind multiple URL for one view function
@app.route('/hi')
@app.route('/hello')
def say_hello():
    return '<h1>Hello, Flask!</h1>'


# dynamic route, URL variable default
@app.route('/greet', defaults={'name': 'Programmer'})
@app.route('/greet/<name>')
def greet(name):
    return '<h1>Hello, %s!</h1>' % name


# custom flask cli command
@app.cli.command()
def hello():
    """Just say hello."""
    click.echo('Hello, Human!')

@app.cli.command()
def say():
    """My command"""
    click.echo("hellop huangcheng")

@click.command()
@click.option('--count',default=1,help='Number of greetings.')
@click.option('--name',prompt='Your name',help='The person to greet.')
def say(count,name):
    for x in range(count):
        click.echo('hello %s!' % name)


if __name__ =='__main__':
    # say()
    app.run(port=5001,debug=True)
