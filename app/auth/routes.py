#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-01-07 11:07:00
# @Author  : OP (oldpottertom@icloud.com)
# @Link    : https://shenkeling.top
# @Version : $Id$

from app import db, app
from flask import render_template, flash, redirect, url_for, request
from app.auth.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post
from werkzeug.urls import url_parse

from . import bp

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: #登录成功
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(u'用户名或者密码错误')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        flash(u'欢迎你:{}!'.format(form.username.data))
        return redirect(next_page)
    return render_template('auth/login.html', title=u'登录', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(u'恭喜你，注册成功！！')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title=u'注册用户', form=form)
