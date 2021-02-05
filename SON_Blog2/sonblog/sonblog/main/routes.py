from flask import Blueprint, request, render_template
from flask_login import current_user
from sonblog.models import Posts

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    curpage = request.args.get('page', 1, type=int)
    feed = Posts.query.order_by(Posts.date_posted.desc()).paginate(per_page=5, page=curpage)
    if current_user.is_authenticated:
        hometitle = current_user.username
    else:
        hometitle = None
    return render_template('home.html', posts=feed, title=hometitle)


@main.route('/about')
def about():
    return render_template('about.html')

