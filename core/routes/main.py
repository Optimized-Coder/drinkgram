from flask import Blueprint, redirect, url_for, request, render_template
from ..extensions import db
from ..models import Photo

from flask_login import current_user

import uuid
import boto3
import os

main = Blueprint('main', __name__)

ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/')
def index():
    return render_template('index.html', current_user=current_user)

# POST
@main.route('/upload/', methods=['GET', 'POST'])
def upload():
    # if not current_user.is_authenticated:
        # return redirect(url_for('auth.login'))
    if request.method == 'POST':
        uploaded_file = request.files['file-to-upload']
        if uploaded_file and allowed_file(uploaded_file.filename):

            new_file_name = uuid.uuid4().hex + '.' + uploaded_file.filename.rsplit('.', 1)[1].lower()
            bucket_name = 'barpicsphotos'

            s3 = boto3.resource(
                service_name='s3',
                region_name='eu-west-2',
                aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
            )

            s3.Bucket(bucket_name).\
                    upload_fileobj(uploaded_file, new_file_name)
            
            photo = Photo(
                user_id=current_user.id,
                name=new_file_name,
                url = f'https://barpicsphotos.s3.eu-west-2.amazonaws.com/{new_file_name}',
            )
            db.session.add(photo)
            db.session.commit()
            return redirect(url_for('main.index')) 
    return render_template('upload.html')