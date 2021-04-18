# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from app.home import blueprint
from flask import render_template, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from app import login_manager
from redis import Redis
from jinja2 import TemplateNotFound
import random

redis = Redis(host='localhost', port=6379)

@blueprint.route('/index')
@login_required
def index():

    return render_template('index.html', segment='index')

@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith( '.html' ):
            template += '.html'

        # Detect the current page
        segment = get_segment( request )

        # Serve the file (if exists) from app/templates/FILE.html
        return render_template( template, segment=segment )

    except TemplateNotFound:
        return render_template('page-404.html'), 404
    
    except:
        return render_template('page-500.html'), 500

# Helper - Extract current page name from request 
def get_segment( request ): 

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment    

    except:
        return None  


@blueprint.route('/index/update/metadata', methods=["GET", "POST"])
def update_metadata():
    if request.method == 'POST':
        print("function call")
        temp = redis.lpop('requests')
        if temp != None:
            return jsonify(request_rate=float(temp),
                       response_time=-1,
                       server_scale=-1)
        temp = redis.lpop('workload')
        if temp != None:
            return jsonify(request_rate=-1,
                       response_time=float(temp),
                       server_scale=-1)
        temp = redis.lpop('scale')
        if temp != None:
            return jsonify(request_rate=-1,
                       response_time=-1,
                       server_scale=int(temp))

        return jsonify(request_rate=-1,
                       response_time=-1,
                       server_scale=-1)
        