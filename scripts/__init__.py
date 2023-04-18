import logging
from logging.handlers import RotatingFileHandler
import pymysql
pymysql.install_as_MySQLdb()
import redis
from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from config import config_map
from flask_mail import Mail
from flask_apscheduler import APScheduler
from scripts.utils.commons import Reconverter

#数据库
db = SQLAlchemy(session_options = {'autocommit':False})
#创建redis 连接对象
redis_store = None

#创建 mail 连接对象
mail = None

# 创建 任务对象
ScheduleTask = None

# 配置日志信息
# 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024*1024*100, backupCount=10)
# 创建日志记录的格式                 日志等级    输入日志信息的文件名 行数    日志信息
formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
# 为刚创建的日志记录器设置日志记录格式
file_log_handler.setFormatter(formatter)
# 为全局的日志工具对象（flask app使用的）添加日记录器
logging.getLogger().addHandler(file_log_handler)
# 设置日志的记录等级
logging.basicConfig(level=logging.DEBUG)  # 调试debug级


#工厂模式
def create_app(config_name):
    """
    create flask work mode .
    :param config_name: str  configuration name ("development"/"production")
    :return: app object
    """
    app = Flask(__name__)
    #根据配置模式的名字，获取配置参数的类
    config_class = config_map.get(config_name)
    app.config.from_object(config_class)
    #使用app 初始化db
    db.init_app(app)
    # 使用app 初始化邮件
    global mail
    mail = Mail(app)
    # 使用app 初始化task
    global ScheduleTask
    ScheduleTask = APScheduler()
    ScheduleTask.init_app(app)

    #初始化redis 工具
    global  redis_store
    redis_store = redis.StrictRedis(host=config_class.REDIS_HOST, port=config_class.REDIS_PORT)
    # 利用flask -session,将session 数据保存到redis
    Session(app)
    # 为flask补充csrf 防护机制
    CSRFProtect(app)

    #为flask 添加自定义转换器
    app.url_map.converters["re"] = Reconverter


    #注册蓝图
    from scripts.dashboard import api_0_1
    app.register_blueprint(api_0_1.api,url_prefix="/api/v0.1")

    #注册提供静态文件的蓝图
    from scripts import web_html
    app.register_blueprint(web_html.html)
    return app

