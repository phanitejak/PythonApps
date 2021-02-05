from flask import Blueprint, redirect, url_for, request, render_template, flash
from flask_login import login_user, current_user, logout_user, login_required
from sonblog import db, bcrypt
from sonblog.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, ResetPassword, ResetPassword_Request
from sonblog.models import User, Posts
from sonblog.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    regiform = RegistrationForm()
    if regiform.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(regiform.password.data).decode('utf-8')
        createuser = User(username=regiform.username.data, email=regiform.email.data, password=hashed_password)
        db.session.add(createuser)
        db.session.commit()
        flash(f'Account Created for {regiform.username.data}!', 'success')
        return redirect(url_for('users.userlogin'))
    return render_template('register.html', title='Register', form=regiform)


@users.route('/login', methods=['GET', 'POST'])
def userlogin():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    loginform = LoginForm()
    if loginform.validate_on_submit():
        dbuser = User.query.filter_by(email=loginform.email.data).first()
        if dbuser and bcrypt.check_password_hash(dbuser.password, loginform.password.data):
            login_user(dbuser, remember=loginform.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Failed. Please check email/password', 'danger')
    return render_template('login.html', title='Login', form=loginform)


@users.route('/logout')
def userlogout():
    logout_user()
    return redirect(url_for('users.userlogin'))



@users.route('/account', methods=['GET', 'POST'])
@login_required
def useraccount():
    accform = UpdateAccountForm()
    if accform.validate_on_submit():
        if accform.picture.data:
            picture_file = save_picture(accform.picture.data)
            current_user.image_file = picture_file
        current_user.username = accform.username.data
        current_user.email = accform.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.useraccount'))
    elif request.method == 'GET':
        accform.username.data = current_user.username
        accform.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=accform)


@users.route("/user/<string:username>")
def user_post(username):
    curpage = request.args.get('page', 1, type=int)
    thisuser = User.query.filter_by(username=username).first_or_404()
    feed = Posts.query .filter_by(author=thisuser).order_by(Posts.date_posted.desc()).paginate(per_page=5, page=curpage)
    return render_template('user_posts.html', posts=feed, title='My Posts', user=thisuser)


@users.route('/reset_pass_request', methods=['GET', 'POST'])
def reset_pass_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    reqform = ResetPassword_Request()
    if reqform.validate_on_submit():
        userreq = User.query.filter_by(email=reqform.email.data).first()
        send_reset_email(userreq)
        flash('An email is sent to your email to reset the password', 'info')
        return redirect(url_for('users.userlogin'))
    return render_template('reset_pass_request.html', title='Reset Password Request', form=reqform)


@users.route('/reset_pass/<token>', methods=['GET', 'POST'])
def reset_pass(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('Invalid/Expired token. Please retry.', 'warning')
        return redirect(url_for('users.reset_pass_request'))
    resetform = ResetPassword()
    if resetform.validate_on_submit():
        hashedpass = bcrypt.generate_password_hash(resetform.password.data).decode('utf-8')
        user.password = hashedpass
        db.session.commit()
        flash('Your Password is updated. Please login.', 'success')
        return redirect(url_for('users.userlogin'))
    return render_template('reset_pass.html', title='Reset Password', form=resetform)
