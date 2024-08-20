
from flask import render_template, redirect
from flask import Blueprint
from flask_cors import CORS, cross_origin

bp_blog = Blueprint('blog', __name__, url_prefix='/blog')
CORS(bp_blog)


@bp_blog.route('/articles.html')
@cross_origin(methods=['GET'])
def articles():
    return render_template('blog/articles/articles.html', title='Articles')


@bp_blog.route('/article/azure-data-lake-storage-gen2.html')
@cross_origin(methods=['GET'])
def azure_data_lake_storage_gen2():
    return render_template('blog/articles/azure_data_lake_storage_gen2.html', title='Azure Data Lake Storage Gen2 in data analytics workloads')