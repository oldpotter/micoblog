#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-01-07 14:02:43
# @Author  : OP (oldpottertom@icloud.com)
# @Link    : https://shenkeling.top
# @Version : $Id$

from . import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


# 粉丝表
follow = db.Table('follow',
                db.Column('following_id', db.Integer, db.ForeignKey('user.id')),# 被关注者id
                db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),# 粉丝id
                )


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    # 关注的人列表
    following = db.relationship('User', secondary=follow,
                            primaryjoin=(follow.c.follower_id == id),
                            secondaryjoin=(follow.c.following_id == id),
                            backref=db.backref('follower', lazy='dynamic'),
                            lazy='dynamic'
                            )

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self):
        return 'https://upload.jianshu.io/users/upload_avatars/8678824/19b8d8be-2430-46b7-ab23-2648d78e5428?imageMogr2/auto-orient/strip|imageView2/1/w/300/h/300/format/webp'

    def is_following(self, user):
        '''
        是否正在关注此用户
        :param user: 用户
        :return:
        '''
        return self.following.filter(follow.c.following_id == user.id).count() > 0

    def follow(self, user):
        '''
        关注某用户
        :param user: 关注的用户
        :return:
        '''
        if not self.is_following(user):
            self.following.append(user)

    def unfollow(self, user):
        '''
        取消关注某用户
        :param user:
        :return:
        '''
        if self.is_following(user):
            self.following.remove(user)


    def following_post(self):
        '''
        返回关注人的文章和自己的文章
        :return:
        '''
        following_post = Post.query.join(follow, follow.c.following_id == Post.user_id).filter(follow.c.follower_id == self.id)
        own_post = Post.query.filter_by(user_id=self.id)
        return following_post.union(own_post).order_by(Post.timestamp.desc())


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
