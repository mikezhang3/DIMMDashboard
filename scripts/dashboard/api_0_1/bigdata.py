from flask import request,jsonify,current_app,session,Response,send_file
from datetime import datetime,timedelta
from scripts import redis_store,db,constants
import pandas as pd
from scripts.models import BIG_DATA
from . import api
from scripts.utils.response_code import RET
import json,os,xlsxwriter,sys
from io import BytesIO
import flask_excel as excel
import random
import statistics

base_dir = os.path.dirname(os.path.abspath(__file__))
# print (base_dir)
sys.path.append(base_dir)


# 定义HTMLParser的子类,用以复写HTMLParser中的方法
class EXCEL_WRITE(object):
    excel_file_save = ''
    csv_file_save = ''
    # 构造方法,定义data数组用来存储html中的数据
    def __init__(self):
        super(self.__class__,self).__init__()

    def write_excel(self,test_name_list,test_limit_list,tester_list,operator_list ,SN_list , Total_result_list ,fail_item_list ,test_cell_list,test_start_time_list,all_test_values_list):
        """
        This function for excel write .
        :param test_valus: test data
        :param title_total_list: all of test info
        :param passed_test_item: passed test item
        :param passed_limit: passed limit
        :return:
        """


        # time_now = datetime.strftime(datetime.now(),"%Y-%m-%d %H-%M-%S")
        # time_date = datetime.strftime(datetime.now(), "%Y-%m-%d")
        # if not os.path.exists(r'%s\reports\%s'%(base_dir,time_date)):
        #     os.makedirs(r'%s\reports\%s'%(base_dir,time_date), mode=0o777)
        # file_path1 = r'%s\reports\%s\excel_%s.xlsx' % (base_dir,time_date, time_now)
        # csv_path = r'%s\reports\%s\excel_%s.csv' % (base_dir,time_date, time_now)
        # EXCEL_WRITE.excel_file_save = file_path1
        # EXCEL_WRITE.csv_file_save = csv_path

        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet('html_to_excel')  # 新建sheet（sheet的名称为"AgingWIPs"）
        workfomat = workbook.add_format(dict(bold=True, border=1, align='center', valign='vcenter'))
        workfomat1 = workbook.add_format(dict(bold=True, border=1, align='center', valign='vcenter'))
        workfomat2 = workbook.add_format(dict(bold=True, border=1, align='left'))
        workfomat3 = workbook.add_format(dict(bold=True, border=1, align='center', valign='vcenter'))
        # headings0 = ['', '', '','','','','Test Group']  # 设置表头
        # headings = ['', '', '','','','','Test Name']  # 设置表头
        # headings2 = ['', '', '','','','','Low Limit']  # 设置表头
        # headings3 = ['Tester', 'Operator', 'Test Result', 'Test Cell','Fail Item','Test Start Time','Upper Limit']  # 设置表
        # 列写入
        headings0 = ['', '', 'Tester']  # 设置表头
        headings = ['', '',  'Operator']  # 设置表头1
        headings1 = ['', '',   'Test Result']  # 设置表头2
        headings2 = ['', '',  'Test Cell']  # 设置表头3
        headings3 = ['', '',  'Fail Item']  # 设置表头4
        headings4 = ['', '',  'Test Start Time']  # 设置表头5
        headings5 = ['Test Name', 'Lower Limit', 'Upper Limit']  # 设置表头6

        # create fail item list
        # print(test_values) Tester (0)
        headings0.extend(tester_list)
        headings.extend(operator_list)
        headings1.extend(Total_result_list)
        headings2.extend(test_cell_list)
        headings3.extend(fail_item_list)
        headings4.extend(test_start_time_list)
        headings5.extend(SN_list)
        worksheet.write_column('A1', headings0, cell_format=workfomat1)
        worksheet.write_column('B1', headings, cell_format=workfomat1)
        worksheet.write_column('D1', headings2, cell_format=workfomat1) # cell
        worksheet.write_column('E1', headings3, cell_format=workfomat1) # fail item
        worksheet.write_column('F1', headings4, cell_format=workfomat1) # test start time
        worksheet.write_column('G1', headings5, cell_format=workfomat1) # sn list
        worksheet.write_column('C1', headings1, cell_format=workfomat) # test result

        new_passed_limit_low = [i[0] for i in test_limit_list]
        new_passed_limit_upper = [i[1] for i in test_limit_list]

        worksheet.write_row('H1', test_name_list, cell_format=workfomat2)
        worksheet.write_row('H2', new_passed_limit_low, cell_format=workfomat2)
        worksheet.write_row('H3', new_passed_limit_upper, cell_format=workfomat2)

        for index,i in enumerate(all_test_values_list,4):
            worksheet.write_row('H%s' % index, i, cell_format=workfomat3)
            # print('i value is:', i)

        print('Finished the work ! handle task is:%s\n'%len(all_test_values_list))
        workbook.close()
        output.seek(0)
        return output

        # data = pd.read_excel(file_path1, 'html_to_excel', index_col=0) # read excel
        # data.to_csv(csv_path, encoding='utf-8')



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
    