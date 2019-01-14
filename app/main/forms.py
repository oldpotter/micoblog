# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, StringField
from wtforms.validators import DataRequired, Length, ValidationError
from app.models import User

__author__ = 'op'

class PostForm(FlaskForm):
    post = TextAreaField(u'说点什么吧', validators=[DataRequired(), Length(min=1, max=140)])
    submit = SubmitField(u'提交')


class EditProfileForm(FlaskForm):
    username = StringField(u'用户名', validators=[DataRequired()])
    about_me = TextAreaField(u'关于我', validators=[Length(min=0, max=140)])
    submit = SubmitField(u'更新')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if self.original_username != username.data:
            user = User.query.filter_by(username=username.data).first()
            if user is not None:
                raise ValidationError(u'用户名已经存在')