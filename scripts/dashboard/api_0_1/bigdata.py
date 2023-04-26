from flask import request,jsonify,current_app,session,Response,send_file
from datetime import datetime,timedelta
from scripts import redis_store,db,constants
import pandas as pd
from scripts.models import BIG_DATA
from . import api
from scripts.utils.response_code import RET
from scripts.utils.commons import login_required
import json,os,xlsxwriter,sys
from io import BytesIO
import flask_excel as excel
from urllib.parse import quote
import random
import statistics

base_dir = os.path.dirname(os.path.abspath(__file__))
# print (base_dir)
sys.path.append(base_dir)


class Time_convert(object):
    """
    Time convert for date time
    """
    def __init__(self):
        super(self.__class__,self).__init__()

    def time_covert(self,time_s):
        end_time = time_s.replace('/', '-').strip()
        hours = int(end_time.split(' ')[1].split(':')[0])
        if 'PM' == end_time.split(' ')[-1].strip():
            if int(end_time.split(' ')[1].split(':')[0]) == 12:
                pass
            else:
                hours = int(end_time.split(' ')[1].split(':')[0]) + 12
        elif 'AM' == end_time.split(' ')[-1].strip():
            if int(end_time.split(' ')[1].split(':')[0]) == 12:
                hours = 0
        new_time = datetime.strptime(end_time.split(' ')[0] + ' %s:%s:00' % (hours, end_time.split(' ')[1].split(':')[1].strip()),"%m-%d-%Y %H:%M:%S")
        return new_time


@api.route("/bigdata/Get_group_names",methods = ["GET"])
def Get_group_items():
    """
    :return:
    """
    redis_key = "Get_big_data_group_items"
    page = 1
    try:
        resp_json = redis_store.hget(redis_key, page)
    except Exception as e:
        current_app.logger.error(e)
    else:
        if resp_json:
            return (resp_json, 200, {"Content-Type": "application/json"})

    item_list = []
    # item_dict = {}
    big_app = BIG_DATA()
    # 转换成字典
    for index, item in enumerate(big_app.Get_group_names(), 1):
        item_list.append([index, item])
    resp_dict = dict(errno=RET.OK, errmsg="OK", data={"group_items": item_list})
    resp_json = json.dumps(resp_dict)
    try:
        redis_store.setex(redis_key, constants.WIPQTY_INFO_REDIS_EXPIRES, resp_json)
    except Exception as e:
        current_app.logger.error(e)
    return resp_json, 200, {"Content-Type": "application/json"}





@api.route("/bigdata/Get_workcell",methods = ["GET"])
def Get_bigdata_wc():
    """
    return：parmars
    """

    redis_key = "Get_big_data_group_items"
    group_name = request.args.get("group_name","")
    page = 1
    try:
        resp_json = redis_store.hget(redis_key, page)
    except Exception as e:
        current_app.logger.error(e)
    else:
        if resp_json:
            return (resp_json, 200, {"Content-Type": "application/json"})

    item_list = []
    # item_dict = {}
    big_app = BIG_DATA()
    # 转换成字典
    for item in big_app.Get_workcell_items(group_name):
        item_list.append(item)
    resp_dict = dict(errno=RET.OK, errmsg="OK", data={"wc_items": item_list})
    resp_json = json.dumps(resp_dict)
    try:
        redis_store.setex(redis_key, constants.WIPQTY_INFO_REDIS_EXPIRES, resp_json)
    except Exception as e:
        current_app.logger.error(e)
    return resp_json, 200, {"Content-Type": "application/json"}



@api.route("/bigdata/Get_bigdata_pn_items",methods = ["GET"])
def Get_bigdata_pn_items():

    wc_id = request.args.get("wc_id","")
    print('waht is wc id:',wc_id)
    redis_key = "Get_big_data_pn_items_by_{}".format(wc_id)
    
    page = 1
    try:
        resp_json = redis_store.hget(redis_key, page)
    except Exception as e:
        current_app.logger.error(e)
    else:
        if resp_json:
            return (resp_json, 200, {"Content-Type": "application/json"})

    item_list = []
    # item_dict = {}
    big_app = BIG_DATA()
    # 转换成字典
    for item in big_app.Get_pn_items(wc_id):
        item_list.append(item)
    resp_dict = dict(errno=RET.OK, errmsg="OK", data={"pn_items": item_list})
    resp_json = json.dumps(resp_dict)
    try:
        redis_store.setex(redis_key, constants.WIPQTY_INFO_REDIS_EXPIRES, resp_json)
    except Exception as e:
        current_app.logger.error(e)
    return resp_json, 200, {"Content-Type": "application/json"}


@api.route("/bigdata/Query_testers",methods = ["GET"])
def Get_bigdata_tester_items():
    wc_id = request.args.get("wc_id","")
    pn = request.args.get("pn","")
    redis_key = "Get_big_testers_items_by_{}_{}".format(wc_id,pn)
    
    page = 1
    try:
        resp_json = redis_store.hget(redis_key, page)
    except Exception as e:
        current_app.logger.error(e)
    else:
        if resp_json:
            return (resp_json, 200, {"Content-Type": "application/json"})

    item_list = []
    # item_dict = {}
    big_app = BIG_DATA()
    # 转换成字典
    for item in big_app.Get_tester_names(wc_id,pn):
        item_list.append(item)
    resp_dict = dict(errno=RET.OK, errmsg="OK", data={"tester_items": item_list})
    resp_json = json.dumps(resp_dict)
    try:
        redis_store.setex(redis_key, constants.WIPQTY_INFO_REDIS_EXPIRES, resp_json)
    except Exception as e:
        current_app.logger.error(e)
    return resp_json, 200, {"Content-Type": "application/json"}



@api.route("/bigdata/get_test_items",methods = ["GET"])
def Get_bigdata_test_items():
    """ [Bigdata_limitation].[dbo].[Get_test_items] (@group_name varchar(128),@wc_name varchar(128),@pn varchar(128)) """

    group_name= request.args.get("group_name","")
    wc_name = request.args.get("wc_name","")
    pn = request.args.get("pn","")
    redis_key = "Get_big_test_items_by_{}_{}_{}".format(group_name,wc_name,pn)
    
    page = 1
    try:
        resp_json = redis_store.hget(redis_key, page)
    except Exception as e:
        current_app.logger.error(e)
    else:
        if resp_json:
            return (resp_json, 200, {"Content-Type": "application/json"})

    item_list = []
    # item_dict = {}
    big_app = BIG_DATA()
    # 转换成字典
    for item in big_app.Get_test_items(group_name,wc_name,pn):
        item_list.append(item)
    resp_dict = dict(errno=RET.OK, errmsg="OK", data={"test_items": item_list})
    resp_json = json.dumps(resp_dict)
    try:
        redis_store.setex(redis_key, constants.WIPQTY_INFO_REDIS_EXPIRES, resp_json)
    except Exception as e:
        current_app.logger.error(e)
    return resp_json, 200, {"Content-Type": "application/json"}



@api.route("/bigdata/Get_test_data",methods = ["GET"])
def Get_test_data():
    """
    Get test item from SQL server .
    :return:
    """
    time_app = Time_convert()
    group_name = request.args.get("group_name","")
    workcell_name = request.args.get("workcell")
    wc_id = request.args.get("wc_id","")
    part_number = request.args.get("part_num")
    tester = request.args.get("tester","")
    start_time = request.args.get("starttime")
    end_time = request.args.get("endtime")
    test_item = request.args.get("testitem")
    defalut_value =request.args.get("defalut","YES")
    test_value_list = []
    if defalut_value == "NO":
        time_list = [start_time,end_time,test_item]
    else:
        start_time = datetime.strftime(datetime.now() - timedelta(days=1),'%m-%d-%Y %H:%M:%S')
        end_time = datetime.strftime(datetime.now(),'%m-%d-%Y %H:%M:%S')
        time_list = [start_time,end_time,test_item]

    # print(time_list)
    if all(time_list):
        start_time = time_app.time_covert(start_time)
        end_time = time_app.time_covert(end_time)
        big_app = BIG_DATA()

        # print(time_list)


        if defalut_value == "NO":
            testdata_list,limit = big_app.Get_test_data(group_name,wc_id,part_number,test_item,start_time,end_time,tester)         
            out_limit_list = big_app.Get_out_limit_qty(test_item,start_time,end_time,workcell_name,part_number,tester)
 
        else:

            for i in range(1,20):
                start_time = datetime.strftime(datetime.now() - timedelta(hours=i*8),'%m-%d-%Y %H:%M:%S')
                end_time = datetime.strftime(datetime.now(),'%m-%d-%Y %H:%M:%S')
                testdata_list,limit,time_list1 = big_app.Get_test_default_data(group_name,wc_id,part_number,test_item,start_time,end_time,tester)
                out_limit_list = big_app.Get_out_limit_default_qty(test_item,start_time,end_time,workcell_name,part_number,tester)
                if len(testdata_list) > 0:
                    break

            if time_list1:
                start_time = time_list1[0]
                end_time = time_list1[1]
            
        if len(testdata_list) >90:
            
            # test_value_list1 = random.sample(testdata_list, 90)
            test_value_list1 = testdata_list[:91] 
            # [test_value_list.append(str(i[1])) for i in test_value_list1]

            # print('",'.join(test_value_list)+'"')

            # test_value_list = []
            [test_value_list.append(i[1]) for i in test_value_list1 if i[1] < limit[1] and i[1] > limit[0]]

        else:
            [test_value_list.append(i[1]) for i in testdata_list if i[1] < limit[1] and i[1] > limit[0]]


        # 计算平均值和标准偏差
        mean = statistics.mean(test_value_list)
        stdev = statistics.stdev(test_value_list)

        # 计算cpk值
        cpk = min((limit[1] - mean) / (3 * stdev), (mean - limit[0]) / (3 * stdev))

        # print('Mike-------:',testdata_list,limit)
        if testdata_list:
            resp_dict = dict(errno=RET.OK, errmsg="OK", data={"test_data": testdata_list,"test_limit":limit,"time_list":[datetime.strftime(start_time,'%Y-%m-%d %H:%M:%S'),datetime.strftime(end_time,'%Y-%m-%d %H:%M:%S')],"test_item_name":test_item,"out_limit_list":out_limit_list,"test_value_list":test_value_list,"cpk":cpk})
            resp_json = json.dumps(resp_dict)
            return resp_json, 200, {"Content-Type": "application/json"}
        else:
            return jsonify(errno=RET.NODATA, errmsg="No Data in data base .")
    else:
        return jsonify(errno=RET.PARAMERR, errmsg="Parameters is not complete .")

        


@api.route("/bigdata/Get_barchart",methods = ["GET"])

def Get_barchart():
    """_summary_
       Get barchart 
       [Bigdata_limitation].[dbo].[get_last7_extracted] 'IMED','MEDTRONIC','DIMM'
    """
    redis_key = "Get_big_bar_charts"
    
    page = 1
    try:
        resp_json = redis_store.hget(redis_key, page)
    except Exception as e:
        current_app.logger.error(e)
    else:
        if resp_json:
            return (resp_json, 200, {"Content-Type": "application/json"})

    item_list = []
    item_dict = {}
    big_app = BIG_DATA()
    # 转换成字典

    group_name = "IMED"
    wc_name = "MEDTRONIC"
    family = "DIMM"

    item_list = big_app.Get_bar_charts_qty(group_name,wc_name,family)
    for item in big_app.Get_bar_charts_qty(group_name,wc_name,family):
        item_dict[item[0]] = item[1]
    resp_dict = dict(errno=RET.OK, errmsg="OK", data={"chart_items":item_dict,"today_qty":item_list[-1][1]})
    resp_json = json.dumps(resp_dict)
    try:
        redis_store.setex(redis_key, constants.WIPQTY_INFO_REDIS_EXPIRES, resp_json)
    except Exception as e:
        current_app.logger.error(e)
    return resp_json, 200, {"Content-Type": "application/json"}
    


@api.route("/bigdata/Get_cpkchart",methods = ["GET"])

def Get_cpkchart():
    """_summary_
       Get barchart 
       
    """

    test_item = request.args.get("test_item","")
    redis_key = "Get_daily_cpk_charts_by_item_{}".format(test_item)
    
    page = 1
    # try:
    #     resp_json = redis_store.hget(redis_key, page)
    # except Exception as e:
    #     current_app.logger.error(e)
    # else:
    #     if resp_json:
    #         return (resp_json, 200, {"Content-Type": "application/json"})

    big_app = BIG_DATA()
    date_list = []
    sum_list = []
    # 转换成字典

    pn_list = []

    # get the pn list 
    for item in big_app.Get_pn_items('83'):
        pn_list.append(item)
    
    # fix the pn list 

    pn_list = ['MD7006063-006-A-R','MD7006076-008-A-R','MD7006076-009-2-R']

    print('test item is:',test_item)
    for pn in pn_list:
        value_list = []
        [value_list.append(j[2]) for j in big_app.Get_daily_cpk(test_item) if j[1] == pn and j[2] != 0 ]
        # make sure value list len less than 8
        if value_list and len(value_list)>7 :
            value_list = value_list[:8]
        sum_list.append([pn,value_list])
        
    # [date_list.append(datetime.strftime(datetime.now() + timedelta(days= -i),'%Y-%m-%d'))  for i in range(1,15)]

    # date_list = sorted(date_list,reverse=False)


    # print('what is sum list :',sum_list)


    resp_dict = dict(errno=RET.OK, errmsg="OK", data={"pn_list":pn_list, "sum_data":sum_list,"date_list":date_list})
    resp_json = json.dumps(resp_dict)
    try:
        redis_store.setex(redis_key, constants.WIPQTY_INFO_REDIS_EXPIRES, resp_json)
    except Exception as e:
        current_app.logger.error(e)
    return resp_json, 200, {"Content-Type": "application/json"}
    



@api.route("/dimm/Download_excel",methods = ["GET"])
@login_required
def download_applyrecords():
    
    g_name = request.args.get('group_name','')
    wc_name = request.args.get('workcell','')
    pn = request.args.get('part_num','')
    tester = request.args.get('tester','')
    start_time = request.args.get('starttime','')
    end_time = request.args.get('endtime','')
    option = request.args.get('download','NO')
    time_app = Time_convert()
    try:
        start_time = time_app.time_covert(start_time) 
        end_time = time_app.time_covert(end_time) 
    except Exception as e:
        print(e)
        return jsonify(errno=RET.PARAMERR, errmsg="DateTime Format Error.")
    
    big_app = BIG_DATA()
    dimm_data = big_app.Get_dimm_excel_data(tester,start_time,end_time)

    if len(dimm_data) < 1:
        return  jsonify(errno=RET.NODATA,errmsg='No data in database.')


    if option == "YES":
        
        time_str = datetime.strftime(datetime.now(),'%Y_%m_%d_%H%M%S')
        file_name = quote(r'dimm_rec_%s_%s.xlsx' % (wc_name,time_str))
        EXPORT_TITLE = "Dimm test records\nDIMM 测试记录"
        spare_th = ['id','Customer','Customer_id','Upload_Datetime','Tester','Operator','PN','SN','Test_Result','Test_Cell','Test_Start_Time','Test_End_Time','Test_Mode','P1_dist','P2_dist','P3_dist','P4_dist','Script','Script_Hash','Log_path','Remark']

        output = BytesIO()
        workbook = xlsxwriter.Workbook(output, {"in_memory": True})  # new create xlsx file
        fmt = dict(
                    border=1,
                    align="center",
                    text_wrap=True,
                    valign="vcenter",
                    font_size=11
                )
        fmt_blue = dict(
                    border=1,
                    align="center",
                    text_wrap=True,
                    valign="vcenter",
                    font_size=11,
                    font_color= "#00b0f0"
                )


        fmt1 = dict(
                    align="left",
                    text_wrap=False,
                    valign="vcenter",
                    font_size=9,
                    
                )


        fmt_blue1 = dict(
                    align="left",
                    text_wrap=False,
                    valign="vcenter",
                    font_size=9,
                    font_color= "#00b0f0"
                )
        
        
        normal = workbook.add_format(fmt)
        normal_blue = workbook.add_format(fmt_blue)
        normal_blue1 = workbook.add_format(fmt_blue1)
        normal1 = workbook.add_format(fmt1)

        bold = workbook.add_format(dict(fmt, bold=True))
        ws = workbook.add_worksheet('Dimm_Values') 
        ws.merge_range("A1:U1", EXPORT_TITLE, bold)
        ws.set_row(0, 44)
        # write title as below 
        [ws.write(1,index,i,normal) for index,i in enumerate(spare_th,0) if index not in [2,3,4,5]]
        [ws.write(1,index,i,normal_blue) for index,i in enumerate(spare_th,0) if index in [2,3,4,5]]
        [ws.set_column(i, i, 20) for i in range(1,9,1)]
        [ws.set_column(i, i, 20) for i in range(9,17,1)]
        [ws.set_column(i, i, 40) for i in range(17,20,1)]
        # get workcell data from db .

        ws.write_row('A2',spare_th,bold)
        for index,dimm_data_s in enumerate( dimm_data,3):
            ws.write_row('A%s' %index, dimm_data_s,normal)

        workbook.close()
        output.seek(0)
        print(file_name)
        # rv = send_file(output,as_attachment =True, download_name = file_name)
        rv = send_file(output,as_attachment=True,  attachment_filename = file_name)
        rv.headers['Content-Disposition']+=";filename*=utf-8''{}".format(file_name)
        return rv 
    else:
        return jsonify(errno=RET.OK, errmsg="Got the data ,will download the excel .")

