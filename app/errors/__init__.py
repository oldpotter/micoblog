# -*- coding: utf-8 -*-
__author__ = 'op'

from flask import Blueprint

bp = Blueprint('errors', __name__)

from app.errors import handlers
