# -*- coding: utf-8 -*-
__author__ = 'op'

import unittest

from app import db, app
from app.models import User, Post
from datetime import datetime, timedelta

class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hash(self):
        u = User(username='老波特')
        u.set_password('1234')
        self.assertFalse(u.check_password('4321'))
        self.assertTrue(u.check_password('1234'))


    def test_follow(self):
        u1 = User(username='张三', email='zs@example.com')
        u2 = User(username='李四', email='lisi@example.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.following.all(), [])
        self.assertEqual(u2.follower.all(), [])

        u1.follow(u2)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.following.count(), 1)
        self.assertEqual(u1.following.first().username, '李四')
        self.assertEqual(u2.follower.count(), 1)
        self.assertEqual(u2.follower.first().username, '张三')

        u1.unfollow(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.following.count(), 0)
        self.assertEqual(u2.follower.count(), 0)


    def test_following_post(self):
        # 创建用户
        u1 = User(username='铜钱草1', email='t1@qq.com')
        u2 = User(username='铜钱草2', email='t2@qq.com')
        u3 = User(username='铜钱草3', email='t3@qq.com')
        u4 = User(username='铜钱草4', email='t4@qq.com')
        db.session.add_all([u1, u2, u3, u4])

        # 创建文章
        now = datetime.utcnow()
        p1 = Post(body='文章11111', author=u1, timestamp=now + timedelta(1))
        p2 = Post(body='文章22222', author=u2, timestamp=now + timedelta(2))
        p3 = Post(body='文章33333', author=u3, timestamp=now + timedelta(3))
        p4 = Post(body='文章44444', author=u4, timestamp=now + timedelta(4))
        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()

        u1.follow(u2)
        u1.follow(u4)
        u2.follow(u3)
        u3.follow(u4)
        db.session.commit()

        following_post1 = u1.following_post().all()
        following_post2 = u2.following_post().all()
        following_post3 = u3.following_post().all()
        following_post4 = u4.following_post().all()
        self.assertEqual(following_post1, [p4, p2, p1])
        self.assertEqual(following_post2, [p3, p2])
        self.assertEqual(following_post3, [p4, p3])
        self.assertEqual(following_post4, [p4])

if __name__ == '__main__':
    unittest.main()