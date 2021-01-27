import os
import secrets

from PIL import Image
from flask_mail import Message
from flask import url_for, current_app
from sonblog import mail


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password reset request', sender='noreply@sonblog.com', recipients=user.email)
    msg.body = f'''
        To Reset your password, please visit :
        {url_for('users.reset_pass', token=token, _external=True)} 

        If you did not request this, please ignore. No changes are made to your account.
    '''
    mail.send(msg)
