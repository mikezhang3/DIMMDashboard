
from flask import Blueprint


# 创建蓝图对象
api = Blueprint("api_0_1", __name__)


# 导入蓝图的视图
from . import passport,bigdata