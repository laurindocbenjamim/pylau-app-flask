
from flask import render_template, redirect, session, request
from flask import Blueprint
from flask_cors import CORS, cross_origin

bp_blog = Blueprint('blog', __name__, url_prefix='/blog')
CORS(bp_blog)

welcome_title = "Our Blog"
welcome_message = "Explore our latest news"

@bp_blog.route('/')
@cross_origin(methods=['GET'])
def blog():
    session['current_page'] = 'blog'
    return render_template('blog/blog.html', title="Blog",  welcome_title=welcome_title, welcome_message=welcome_message)

@bp_blog.route('/articles')
@cross_origin(methods=['GET'])
def articles():
    session['current_page'] = 'blog'
    return render_template('blog/articles/articles.html', title='Articles',  welcome_title=welcome_title, welcome_message=welcome_message)


@bp_blog.route('/article/azure-data-lake-storage-gen2')
@cross_origin(methods=['GET'])
def azure_data_lake_storage_gen2():
    session['current_page'] = 'blog'
    return render_template('blog/articles/azure_data_lake_storage_gen2.html', title='Azure Data Lake Storage Gen2 in data analytics workloads',  welcome_title=welcome_title, welcome_message=welcome_message)

@bp_blog.route('/article/data-driven')
@cross_origin(methods=['GET'])
def data_driven():
    session['current_page'] = 'blog'
    return render_template('blog/articles/data-driven.html', title='Data Driven',  welcome_title=welcome_title, welcome_message=welcome_message)