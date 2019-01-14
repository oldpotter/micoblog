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

db = SQLAlchemy()  # ORM
migrate = Migrate()  # 数据库迁移
login = LoginManager()  # 登录
bootstrap = Bootstrap()  # bootstrap库


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)  # 导入配置信息
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    login.login_view = 'auth.login'
    bootstrap.init_app(app)

    from errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from main import bp as main_bp
    app.register_blueprint(main_bp)

    return app

