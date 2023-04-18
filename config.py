import redis
from scripts import constants
class Config(object):
    """配置信息"""

    SECRET_KEY = "77sf7sd7afd7$3"
    #数据库
    SQLALCHEMY_DATABASE_URI = "mysql://root:agingwip@IMEDTDBACKUP:3306/agingwip"
    # 设置sqlalchemy自动更跟踪数据库
    SQLALCHEMY_TRACK_MODIFICATIONS =False
    # 设置sqlalchemy 超时回收并重新分配新的,时间单位 S
    SQLALCHEMY_POOL_RECYCLE = 2400
    # 查询时会显示原始SQL语句
    SQLALCHEMY_ECHO = False
    #redis config
    REDIS_HOST = constants.REDIS_HOST_NAME
    REDIS_PORT  = 6379

    #flask -Session 配置
    SESSION_TYPE = "redis"
    SESSION_REDIS = redis.StrictRedis(host = REDIS_HOST,port = REDIS_PORT)
    SESSION_USE_SIGNER = True #对cookie中session_id 进行隐藏
    PERMANENT_SESSION_LIFETIME = 86400 #cookie数据的有效期,单位秒
    MAIL_USE_SSL = False
    # MAIL_USERNAME = 'AgingWIP@jabil.com'
    MAIL_SERVER = "SHATEHQ"  # 设置服务器


class DevelopmentConfig(Config):
    """开发模式的配置信息"""
    DEBUG = True


class ProductionCofig(Config):
    """生产模式的配置信息"""
    pass


config_map = {

    "develop":DevelopmentConfig,
    "product":ProductionCofig

}