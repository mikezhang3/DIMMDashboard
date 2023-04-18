from .import api
from flask import request,jsonify,current_app,session,g
from scripts.utils.response_code import RET
import mkldap as domain_login
from scripts.utils.commons import login_required
from scripts.models import Tester_Fixture
from scripts import redis_store,db,constants
from scripts.models import User
from sqlalchemy.exc import IntegrityError
import re


@api.route("/sessions", methods=["POST"])
def login():
    """用户登录
    参数： 手机号、密码， json
    """
    # 获取参数
    req_dict = request.get_json()
    mobile = req_dict.get("mobile")
    password = req_dict.get("password")

    # print(mobile,password)
    # print(type(mobile),type(password))

    # 校验参数
    # 参数完整的校验
    if not all([mobile, password]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")

    # 域用户登录
    if not re.match(r"^[1][3,4,5,7,8][0-9]{9}$", mobile):
        ldap_auth = domain_login.LDAP_AUTH()
        result = ldap_auth.Server_connection(mobile,password)
        if result:
            session["name"] = result.get("alien_name","UNKOWN")
            session["mobile"] = "none"
            session["user_id"] = result.get("emp_ID","UNKOWN")
            session["emp_title"] = result.get("emp_title","UNKOWN")
            return jsonify(errno=RET.OK, errmsg="登录成功")

    # 手机号的格式
    # if not re.match(r"1[34578]\d{9}", mobile):
    if not re.match(r"^[1][3,4,5,7,8][0-9]{9}$", mobile):
        return jsonify(errno=RET.PARAMERR, errmsg="手机号格式错误")

    # 判断错误次数是否超过限制，如果超过限制，则返回
    # redis记录： "access_nums_请求的ip": "次数"
    user_ip = request.remote_addr  # 用户的ip地址
    try:
        access_nums = redis_store.get("access_num_%s" % user_ip)
    except Exception as e:
        current_app.logger.error(e)
    else:
        if access_nums is not None and int(access_nums) >= constants.LOGIN_ERROR_MAX_TIMES:
            return jsonify(errno=RET.REQERR, errmsg="错误次数过多，请稍后重试")

    # 从数据库中根据手机号查询用户的数据对象
    try:
        user = User.query.filter_by(mobile=mobile).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="获取用户信息失败")

    # 用数据库的密码与用户填写的密码进行对比验证
    if user is None or not user.check_password(password):
        # 如果验证失败，记录错误次数，返回信息
        try:
            # redis的incr可以对字符串类型的数字数据进行加一操作，如果数据一开始不存在，则会初始化为1
            redis_store.incr("access_num_%s" % user_ip)
            redis_store.expire("access_num_%s" % user_ip, constants.LOGIN_ERROR_FORBID_TIME)
        except Exception as e:
            current_app.logger.error(e)

        return jsonify(errno=RET.DATAERR, errmsg="用户名或密码错误")

    # 如果验证相同成功，保存登录状态， 在session中
    session["name"] = user.name
    session["mobile"] = user.mobile
    session["user_id"] = user.id
    session["emp_title"] = "UNKOWN"
   

    return jsonify(errno=RET.OK, errmsg="登录成功")


@api.route("/session", methods=["GET"])
@login_required
def check_login():
    """检查登陆状态"""
    # 尝试从session中获取用户的名字
    name = session.get("name")
    # 如果session中数据name名字存在，则表示用户已登录，否则未登录

    # Get Role info from sql .
    role_info = ''
    if name is not None:
        fixture_ap = Tester_Fixture()
        user_list = fixture_ap.Get_role_for_maintain(g.user_id)
        if user_list:
            role_info = user_list[0][2]
        else:
            role_info = ''

    if name is not None:
        return jsonify(errno=RET.OK, errmsg="true", data={"name": name,"role":role_info,"emp_title":session.get("emp_title","UNKOWN")})
    else:
        return jsonify(errno=RET.SESSIONERR, errmsg="false")


@api.route("/session", methods=["DELETE"])
def logout():
    """登出"""
    # 清除session数据
    session.clear()
    return jsonify(errno=RET.OK, errmsg="OK")

