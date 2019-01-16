#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-01-07 12:03:11
# @Author  : OP (oldpottertom@icloud.com)
# @Link    : https://shenkeling.top
# @Version : $Id$

import os
from dotenv import load_dotenv

env_file_path = os.path.join(os.getcwd(), '.env')
load_dotenv(env_file_path)

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or '1234qwer'
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	POSTS_PER_PAGE = 3 # 每页显示的文章数量
