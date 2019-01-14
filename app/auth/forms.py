#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-01-07 12:38:27
# @Author  : OP (oldpottertom@icloud.com)
# @Link    : https://shenkeling.top
# @Version : $Id$

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from app.models import User


class LoginForm(FlaskForm):
    username = StringField(u'用户名', validators=[DataRequired()])
    password = PasswordField(u'密码', validators=[DataRequired()])
    remember_me = BooleanField(u'记住我')
    submit = SubmitField(u'登录')


class RegistrationForm(FlaskForm):
    username = StringField(u'用户名', validators=[DataRequired()])
    email = StringField(u'电子邮箱', validators=[DataRequired(), Email()])
    password = PasswordField(u'密码', validators=[DataRequired()])
    password_again = PasswordField(u'重复密码', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(u'注册用户')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(u'用户名已存在')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(u'电子邮件已经存在')





