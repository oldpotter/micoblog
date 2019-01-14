# -*- coding: utf-8 -*-
from flask import flash, redirect, url_for, request, render_template
from flask_login import login_required, current_user
from app import app
from app.main import bp
from app.main.forms import PostForm, EditProfileForm
from app.models import Post, User
from app import db
from datetime import datetime

__author__ = 'op'

@bp.route('/', methods=('GET', 'POST'))
@bp.route('/index', methods=('GET', 'POST'))
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash(u'发布成功')
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    pagination = current_user.following_post().paginate(page, app.config['POSTS_PER_PAGE'], False)
    # next_url = url_for('index', page=posts.next_num) if posts.has_next else None
    # prev_url = url_for('index', page=posts.prev_num) if posts.has_prev else None
    return render_template('index.html', title=u'主页', posts=pagination.items, form=form, pagination=pagination)





@bp.route('/user/<username>')
@login_required
def user(username):
    '''
    个人主页
    :param username:
    :return:
    '''
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    pagination = user.posts.paginate(page, app.config['POSTS_PER_PAGE'], False)
    # next_url = url_for('user', page=posts.next_num, username=username) if posts.has_next else None
    # prev_url = url_for('user', page=posts.prev_num, username=username) if posts.has_prev else None
    return render_template('user.html', user=user, posts=pagination.items, pagination=pagination)


@bp.route('/edit_profile', methods=('GET', 'POST'))
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash(u'更新已经保存成功！！')
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title=u'编辑', form=form)


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@bp.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(u'没找到用户:{}'.format(username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash(u'你不能关注你自己')
        return redirect(url_for('main.user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash(u'你成功关注了{}'.format(username))
    return redirect(url_for('main.user', username=username))

@bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(u'没找到用户:{}'.format(username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash(u'你不能取消关注你自己')
        return redirect(url_for('main.user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash(u'你取消了对{}的关注'.format(username))
    return redirect(url_for('main.user', username=username))


@bp.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
    # next_url = url_for('explore', page=posts.next_num) if posts.has_next else None
    # prev_url = url_for('explore', page=posts.prev_num) if posts.has_prev else None
    return render_template('index.html', title=u'发现', posts=pagination.items, pagination=pagination)


