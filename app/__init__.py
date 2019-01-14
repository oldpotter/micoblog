#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-01-07 11:01:59
# @Author  : OP (oldpottertom@icloud.com)
# @Link    : https://shenkeling.top
# @Version : v0.1

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap


app = Flask(__name__)
app.config.from_object(Config) #导入配置信息
db = SQLAlchemy(app) # ORM
migrate = Migrate(app, db) # 数据库迁移
login = LoginManager(app)# 登录
login.login_view = 'auth.login'
bootstrap = Bootstrap(app)#bootstrap库

from errors import bp as errors_bp
app.register_blueprint(errors_bp)

from auth import bp as auth_bp
app.register_blueprint(auth_bp)

from main import bp as main_bp
app.register_blueprint(main_bp)

from . import models
from app.auth import routes
