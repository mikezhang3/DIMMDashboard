# setting the flask mode
CONFIG_MODE = "develop"
# CONFIG_MODE = "product"
# Define the redis host mane
REDIS_HOST_NAME = "127.0.0.1"
# saving the flag expires time for docker running.
FLAG_SAVE_REDIS_EXPIRES = 1200

# 图片验证码的redis 的有效期,单位 秒
IMAGE_CODE_REDIS_EXPIRES = 180

# 短信验证码的redis 的有效期,单位 秒
SMS_CODE_REDIS_EXPIRES = 180

# 发送短信验证的间隔
SEND_SMS_CODE_INTERVAL = 60

# 登录错误尝试次数
LOGIN_ERROR_MAX_TIMES =5

# 登录错误限制的时间，单位为秒
LOGIN_ERROR_FORBID_TIME = 300


# Aging WIP QTY info 保存redis 时间，单位为秒
WIPQTY_INFO_REDIS_EXPIRES = 300

# WIP analysis record info save redis time ,unit as sec
WIP_ANALYSIS_RECORDS_EXPIRES = 300

# Aging WIP list 每页数据容量
AGING_LIST_PAGE_CAPACITY =30

# Aging WIP LIST EXPIRE 保存redis 时间，单位为秒
AGING_LIST_PAGE_REDIS_EXPIRES = 300

# DEBUG user list expire

DEBUG_USER_LIST_REDIS_EXPIRES = 300