from datetime import datetime,timedelta
from urllib import request
# from AgingWIP import constants
from werkzeug.security import generate_password_hash,check_password_hash
from . import db
import pyodbc
import platform

class BaseModel(object):
    """模型基类，为每个模型补充创建时间与更新时间"""
    create_time = db.Column(db.DateTime, default=datetime.now)  # 记录的创建时间
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)  # 记录的更新时间





class User(BaseModel, db.Model):
    """用户"""
    __tablename__ = "AgingWIP_user_profile"
    id = db.Column(db.Integer, primary_key=True)  # 用户编号
    name = db.Column(db.String(32), unique=True, nullable=False)  # 用户暱称
    password_hash = db.Column(db.String(128), nullable=False)  # 加密的密码
    mobile = db.Column(db.String(11), unique=True, nullable=False)  # 手机号
    email = db.Column(db.String(128),unique=True)                   #邮箱
    role = db.Column(db.String(32), default="staff", nullable=False)  # 用户角色
    real_name = db.Column(db.String(32))  # 真实姓名
    avatar_url = db.Column(db.String(128))  # 用户头像路径
    # relation_wip = db.relationship("Debug_records", backref="user")  # 相关wip
    # 加上property 装饰器后，会把函数变为属性，属性名即为函数名
    @property
    def password(self):
        """对密码进行加密"""
        # print(user.password ) # 读取属性时被调用
        #函数的返回值会作为属性值
        # return "XXXX"
        raise AttributeError("这个属性只能设置，不能读取")


    # 使用这个装饰器，对应设置属性操作
    @password.setter
    def password(self,value):
        """
        设置属性 user.password = "XXXXXX"
        :param value: 设置属性值时的数据,value 就是"XXXXXX",原如的明文密码
        :return:
        """
        self.password_hash = generate_password_hash(value)

    def check_password(self,passwd):
        """这是检验密码的正确性
        :param passwd:用户填写的原始密码
        :return :如果正确，返回True,否则返回False
        """
        return check_password_hash(self.password_hash,passwd)




class Tester_Fixture(object):
    """
    Query SN from database .
    :param N/A
    return : one obj
    """
    def __new__(cls):
        cls.instance =None
        if cls.instance is None:
            obj = super(__class__,cls).__new__(cls)
            # 获取当前系统平台
            sys = platform.system()
            if sys == "Windows":
                sql_name = '{SQL Server}'
            elif sys == "Linux":
                sql_name = '{ODBC Driver 17 for SQL Server}'
            else:
                print("Can not running on an other system.")
            obj.odbc = pyodbc.connect('DRIVER=%s;SERVER=imedtdbackup;DATABASE=IMED_TESTERS;UID=sa;PWD=J@abil+123'%sql_name)
            cls.instance = obj
        return cls.instance

    def to_dict(self,fixture_s,index):
        """
        board info to dict
        :return: dict
        """
        fixture_dict = {
            "Fixture_seq":index,
            "Workcell":fixture_s[0],
            "Test_PM_ID":fixture_s[1],
            "Register_time": fixture_s[2],
            "Computer_name": fixture_s[3],
            "Jabil_link":fixture_s[4],
            "Test_type":fixture_s[5],
            "Test_SW":fixture_s[6],
            "Write_program": fixture_s[7],
            "PIC_engineer": fixture_s[8],
            "PIC_Leader": fixture_s[9],
            "Is_EOL": fixture_s[10],
            "Is_Tracking": fixture_s[11],
            "Last_status": fixture_s[12],
            "Consecutive_offline_days": fixture_s[13],
            "Last_Day_transmitted_Qty": fixture_s[14]

        }
        return fixture_dict


    def to_dict_m(self,fixture_s,index):
        """
        board info to dict
        :return: dict
        """
        print('mike====',fixture_s)
        fixture_dict = {
            "Fixture_seq":index,
            "Fixture_id":fixture_s[0],
            "Workcell":fixture_s[1],
            "Station":fixture_s[2],
            "Test_PM_ID":fixture_s[3],
            "Register_time": fixture_s[4],
            "Computer_name": fixture_s[5],
            "Jabil_link":fixture_s[9],
            "Test_type":fixture_s[7],
            "Test_SW":fixture_s[6],
            "Write_program": fixture_s[10],
            "PIC_engineer": fixture_s[19],
            "PIC_Leader": fixture_s[20],
            "Is_EOL": fixture_s[23],
            "Is_Tracking": fixture_s[24]

        }
        return fixture_dict



    def get_workcell(self):
        """
        :return:wc_list
        """
        cursor = self.odbc.cursor()
        temp_list = []
        command = """ [dbo].[Get_all_wc] """
        print(command)
        cursor.execute(command)
        rows = cursor.fetchall()
        cursor.close()

        if rows:
            temp_list = [i[0] for i in rows]

        return temp_list

    def Get_fixture_name(self,fixture_id):
        """
        :param fixture_id:
        :return:
        """
        cursor = self.odbc.cursor()
        temp_list = []
        command = """ [dbo].[Get_TESTER_name_by_id] '%s' """ % fixture_id
        print(command)
        cursor.execute(command)
        rows = cursor.fetchall()
        cursor.close()

        if rows:
            temp_list = [i for i in rows]
        # print('rows is:',rows)
        return temp_list

    def Del_tester_m(self, fixture_id):
        """
        :param fixture_id:
        :return:
        """
        try:
            cursor = self.odbc.cursor()
            command = """ [dbo].[Del_tester_for_maintain_by_id] '%s' """ % fixture_id
            # print(command)
            cursor.execute(command)
            cursor.commit()
            command = """[dbo].[SYNC_TESTER_MK]"""
            cursor.execute(command)
            cursor.commit()
            cursor.close()
            return True
        except Exception as e:
            return False


    def Get_Fixture_maintain(self,fixture_name):
        """
        :return:
        """
        cursor = self.odbc.cursor()
        temp_list = []
        command = """ [dbo].[Get_Fixture_for_maintain] '%s' """%fixture_name
        # print(command)
        cursor.execute(command)
        rows = cursor.fetchall()
        cursor.close()

        if rows:
            temp_list = [i for i in rows]

        return temp_list

    def Get_Fixture_single(self,fixture_name):
        """
        :return:
        """
        cursor = self.odbc.cursor()
        temp_list = []
        command = """ [dbo].[Get_Fixture] '%s' """%fixture_name
        # print(command)
        cursor.execute(command)
        rows = cursor.fetchall()
        cursor.close()

        if rows:
            temp_list = [i for i in rows]

        return temp_list


    def Get_maintain_testers(self,wc):
        """
        :param wc:
        :return:
        """
        cursor = self.odbc.cursor()
        temp_list = []
        command = """ [dbo].[Get_TESTER_for_maintain] '%s' """ % wc
        # print(command)
        cursor.execute(command)
        rows = cursor.fetchall()
        cursor.close()

        if rows:
            temp_list = [i for i in rows]

        return temp_list

    def Get_role_for_maintain(self,user_id):
        """
        :param user_id:
        :return:
        """
        cursor = self.odbc.cursor()
        temp_list = []
        command = """ [dbo].[Get_Role_for_maintain] '%s' """ % user_id
        # print(command)
        cursor.execute(command)
        rows = cursor.fetchall()
        cursor.close()

        if rows:
            temp_list = [i for i in rows]

        return temp_list


    def Get_wc_list_for_maintain(self):
        """
        :return: list
        """
        cursor = self.odbc.cursor()
        temp_list = []
        command = """[dbo].[Get_wc_list_for_maintain]"""
        cursor.execute(command)
        rows = cursor.fetchall()
        cursor.close()

        if rows:
            temp_list = [i for i in rows]

        return temp_list


    def Get_fixture_for_maintian_by_id(self,fixture_id):
        """
        :param fixture_id:
        :return:
        """
        cursor = self.odbc.cursor()
        temp_list = []
        command = """[dbo].[Get_tester_for_maintain_by_id] '%s' """%fixture_id
        cursor.execute(command)
        rows = cursor.fetchall()
        cursor.close()

        if rows:
            temp_list = [i for i in rows]

        return temp_list


    def to_dict_for_fixture_maintain(self,fixture_info_list):
        """
        :param fixture_info_list:
        :return: dict
        """

        fixture_detail_dict = {
            "id":fixture_info_list[0],
            "workcell":fixture_info_list[1],
            "station":fixture_info_list[2],
            "test_pm_id":fixture_info_list[3],
            "register_date":fixture_info_list[4],
            "computer_name":fixture_info_list[5],
            "os_type":fixture_info_list[6],
            "test_type":fixture_info_list[7],
            "test_sw":fixture_info_list[8],
            "jabil_link":fixture_info_list[9],
            "write_program":fixture_info_list[10],
            "auto_tars":fixture_info_list[11],
            "mes_tis":fixture_info_list[12],
            "auto_scan":fixture_info_list[13],
            "finger_scan":fixture_info_list[14],
            "tars_file_locked":fixture_info_list[15],
            "test_limits":fixture_info_list[16],
            "pc_screen_saver":fixture_info_list[17],
            "double_scan":fixture_info_list[18],
            "pic_engineer":fixture_info_list[19],
            "pic_leader":fixture_info_list[20],
            "remark":fixture_info_list[21],
            "healthy_score":fixture_info_list[22],
            "is_eol":fixture_info_list[23],
            "is_tracking":fixture_info_list[24]

        }

        return fixture_detail_dict

    def Update_tester_info_for_maintain_items(self,value_list,tester_id):
        """
        :param value_list: list
        :param tester_id: id
        :return: bool
        """
        cursor = self.odbc.cursor()
        for value_list_s in value_list:
            if value_list_s[1]:
                try:
                    command = "update [IMED_TESTERS].[dbo].[Testers] set [%s] = '%s' where [id] = '%s' "%(value_list_s[0],value_list_s[1],tester_id)
                    # print(command)
                    cursor.execute(command)
                    cursor.commit()
                except Exception as e:
                    print(e)
                    cursor.close()
                    return False
        cursor.close()
        return True




    def Update_tester_info_for_maintain_bool(self,value_list,tester_id):
        """
        :param command_list:
        :return:bool
        """
        name_list = "update [IMED_TESTERS].[dbo].[Testers] set "
        for index,value_s in enumerate(value_list,0):
            if index == 0:
                name_list += " [%s] = %s "%(value_s[0],value_s[1])
            else:
                name_list += " ,[%s] = %s " % (value_s[0], value_s[1])
        name_list += "where [id] = '%s' "%tester_id
        try:
            cursor = self.odbc.cursor()
            cursor.execute(name_list)
            cursor.commit()
            command = """[dbo].[SYNC_TESTER_MK]"""
            cursor.execute(command)
            cursor.commit()
            cursor.close()
            return True
        except Exception as e:
            return False

    def addtester_for_maintain(self,tester_info_list):
        """
        :param tester_info_list:
        :return:

        sample :insert into [FVT_DebugWIP].[dbo].[TET_List]([Emp_No],[Chinese_Name],[WorkCell],[NT_Account],[MES_Name],[MESUserID],[MESWindowsUserID]) values ('1167335','宋平','Medtronic','1167335','Ping Song','1167335','1167335')

        """
        a = ['[' + str(i[0]) + ']' for i in tester_info_list]
        b = [str(i[1]) for i in tester_info_list]
        command = """ insert into [IMED_TESTERS].[dbo].[Testers](""" + ",".join(a) + ")values (" + "'" + "','".join(b) + "')"
        # print('mike command is:',command)

        cursor = self.odbc.cursor()
        try:
            cursor.execute(command)
            cursor.commit()
            cursor.close()
            return True
        except Exception as e:
            return False


    def Insert_modify_records(self,val_list):
        """
        :param val_list:list
        :return: bool
        """

        current_time = datetime.strftime(datetime.now(),"%Y-%m-%d %H:%M:%S")
        command = """[dbo].[Insert_tester_records] '%s','%s','%s','%s','%s' """%(current_time,val_list[0],val_list[1],val_list[2],val_list[3])

        cursor = self.odbc.cursor()
        try:
            cursor.execute(command)
            cursor.commit()
            command = """[dbo].[SYNC_TESTER_MK]"""
            cursor.execute(command)
            cursor.commit()
            cursor.close()
            return True
        except Exception as e:
            return False



    def Get_Fixture_list(self,wc,func_name,func_val):
        """
        :return:
        """
        cursor = self.odbc.cursor()
        temp_list = []
        command = """ [dbo].[Get_TESTER] '%s','%s','%s' """%(wc,func_name,func_val)
        # print(command)
        cursor.execute(command)
        rows = cursor.fetchall()
        cursor.close()

        if rows:
            temp_list = [i for i in rows]

        return temp_list

    def Get_Fixture_list_last_stutus(self,wc):
        """
        :return:
        """
        cursor = self.odbc.cursor()
        temp_list = []
        command = """ [dbo].[Get_TESTER_last_status] '%s' """%wc
        # print(command)
        cursor.execute(command)
        rows = cursor.fetchall()
        cursor.close()

        if rows:
            temp_list = [i for i in rows]

        return temp_list

    def Get_Fixture_details(self,wc):
        """
        :return:
        """
        cursor = self.odbc.cursor()
        temp_list = []
        command = """ [dbo].[Get_tester_status] '%s' """%wc
        # print(command)
        cursor.execute(command)
        rows = cursor.fetchall()
        cursor.close()

        if rows:
            temp_list = [i for i in rows]

        return temp_list

    def to_fixture_dict(self,fixture_detail_s):
        """
        board info to dict
        :return: dict
        """
        fixture_detail_dict = {
            "Workcell":fixture_detail_s[0],
            "Total_Tester":fixture_detail_s[1],
            "Online_Qty": fixture_detail_s[2],
            "Offline_Qty": fixture_detail_s[3],
            "Skip_Qty": fixture_detail_s[4],
            "Jabil_link_Qty":fixture_detail_s[5],
            "Jabil_unlink_Qty":fixture_detail_s[6],
            "Non_Eol_Qty":fixture_detail_s[7],
            "Eol_Qty":fixture_detail_s[8],
            "Program_Qty": fixture_detail_s[9],
            "Non_program_Qty": fixture_detail_s[10],
            "Tracking_Qty": fixture_detail_s[11],
            "Non_Tracking_Qty": fixture_detail_s[12],
            "Auto_Qty":fixture_detail_s[13],
            "Manual_Qty":fixture_detail_s[14],
            "SEMI_Qty":fixture_detail_s[15],
            "Total_transmitted_Qty":fixture_detail_s[16],

        }
        return fixture_detail_dict
    def Get_fixture_colum(self):
        """
        :return:
        """
        cursor = self.odbc.cursor()
        temp_list = []
        command = """ [dbo].[Get_TESTERS_Tracking_COL_NAME]"""
        # print(command)
        cursor.execute(command)
        rows = cursor.fetchall()
        cursor.close()

        if rows:
            temp_list = [i[0] for i in rows]

        return temp_list

    def Get_tester_colum(self):
        """
        :return:
        """
        cursor = self.odbc.cursor()
        temp_list = []
        command = """ [dbo].[Get_TESTERS_COL_NAME]"""
        # print(command)
        cursor.execute(command)
        rows = cursor.fetchall()
        cursor.close()

        if rows:
            temp_list = [i[3] for i in rows]

        return temp_list



class QueryResult(object):
    """
    Query SN from database .
    :param N/A
    return : one obj
    """
    instance =None
    work_cell_dict = {}
    def __new__(cls):
        if cls.instance is None:
            obj = super(QueryResult,cls).__new__(cls)
            # 获取当前系统平台
            sys = platform.system()
            if sys == "Windows":
                sql_name = '{SQL Server}'
            elif sys == "Linux":
                sql_name = '{ODBC Driver 17 for SQL Server}'
            else:
                print("Can not running on an other system.")
            obj.odbc = pyodbc.connect('DRIVER=%s;SERVER=cnshah0tesql01;DATABASE=dwtt;UID=teuser;PWD=te@shanghai'%sql_name)
            cls.instance = obj
        return cls.instance
    def Get_WIPID(self,sn):
        """
        :param sn:str
        :return: wipid  likes :888882255
        """

        cursor =self.odbc.cursor()
        cmd = "Select min(Wip_ID) as wipid from shasqlv01a.jems.dbo.WP_Wip with (nolock) where SerialNumber= '%s' "%sn
        cursor.execute(cmd)
        row = cursor.fetchone()
        print(row,type(row))
        if row[0]:
            wipid = str(row[0])
            cursor.close()
            return wipid
        else :
            return False

    def Get_WIPID_max(self,sn):
        """
        :param sn:str
        :return: wipid  likes :888882255
        """
        cursor =self.odbc.cursor()
        cursor.execute("Select max(Wip_ID) from shasqlv01a.jems.dbo.WP_Wip with (nolock) where SerialNumber= '%s' "%sn)
        row = cursor.fetchone()
        if row[0]:
            wipid = str(row[0])
            cursor.close()
            return wipid
        else :
            return False

    def getPN(self,sn):
        """
        :param sn:
        :return:
        """
        cursor = self.odbc.cursor()
        command = """ Select [Assembly],Number from shasqlv01a.jems.dbo.CR_Assemblies with (nolock) where 
        Assembly_ID in (Select Assembly_ID from shasqlv01a.jems.dbo.WP_AssemblyRouteWip with (nolock) 
         where Wip_ID in (Select Wip_ID from shasqlv01a.jems.dbo.WP_Wip with (nolock) where SerialNumber='%s'))""" %sn
        cursor.execute(command)
        row = cursor.fetchone()
        if row:
            print('the row is:[%s]'%row,type(row))
            wippn = str(row[1])
            cursor.close()
            return wippn
        else :
            return False

    def Get_birthday(self,wipid):
        """
        return birthday
        :param wipid:
        :return:
        """
        cursor = self.odbc.cursor()
        command = """select min(lastupdated) birth_date from shasqlv01a.jems.dbo.wp_assemblyroutewip with(nolock) where wip_id = %s """ %wipid
        cursor.execute(command)
        rows = cursor.fetchall()
        cursor.close()
        if rows:
            if str(rows[0][0]) == "None":
                return False
            # print('row1 is:[%s]' % str(rows[0][0]), type(rows[0]))
            return datetime.strftime(rows[0][0],"%Y-%m-%d %H:%M:%S")
        else:
            return False


    def Get_Customer(self,sn):
        """
        :param sn:
        :return: str (Customer)
        """
        cursor = self.odbc.cursor()
        if not self.work_cell_dict:
            command = "Select DISTINCT a.Customer_ID, b.Translation from shasqlv01a.jems.dbo.CR_Customers a  with(nolock) left outer join shasqlv01a.jems.dbo.cr_text  b with(nolock) on b.text_id = a.Customer"
            cursor.execute(command)
            rows = cursor.fetchall()
            for row in rows:
                if str(row[0]) == "30":
                    row[1] = "BSC"
                if str(row[0]) == "73":
                    row[1] = "NihonKohden"
                self.work_cell_dict[str(row[0])] = str(row[1])
                # work_cell_dict[str(row[0])] = work_cell_dict[row[1]]
        command = '''Select  TOP 1 a.Customer_ID from shasqlv01a.jems.dbo.WP_wip a with (nolock) where SerialNumber='%s' ''' % sn
        cursor.execute(command)
        rows = cursor.fetchall()
        cursor.close()
        if rows:
            return self.work_cell_dict.get(str(rows[0][0]).strip())
        else:
            return False

    def Get_Customer_new(self, sn, wip_id):
        """
        :param sn:
        :return: str (Customer)
        """
        cursor = self.odbc.cursor()
        if not self.work_cell_dict:
            command = "Select DISTINCT a.Customer_ID, b.Translation from shasqlv01a.jems.dbo.CR_Customers a  with(nolock) left outer join shasqlv01a.jems.dbo.cr_text  b with(nolock) on b.text_id = a.Customer"
            cursor.execute(command)
            rows = cursor.fetchall()
            for row in rows:
                if str(row[0]) == "30":
                    row[1] = "BSC"
                if str(row[0]) == "73":
                    row[1] = "NihonKohden"
                self.work_cell_dict[str(row[0])] = str(row[1])
                # work_cell_dict[str(row[0])] = work_cell_dict[row[1]]
        command = '''Select  TOP 1 a.Customer_ID from shasqlv01a.jems.dbo.WP_wip a with (nolock) where SerialNumber='%s' and Wip_ID = '%s' ''' % (sn, wip_id)
        cursor.execute(command)
        rows = cursor.fetchall()
        cursor.close()
        if rows:
            return self.work_cell_dict.get(str(rows[0][0]).strip())
        else:
            return False



    def Get_analysis(self,wip):
        """
        :param wip: wip id
        :return: list
        """
        analysisList = []
        cursor = self.odbc.cursor()
        command = "Select c.translation, a.AnalysisDateTime, a.DefectLocation,d.StepText,e.UserID,e.LastName + ' ' + e.FirstName name from shasqlv01a.jems.dbo.QM_Analysis a with (nolock),shasqlv01a.jems.dbo.QM_Defects b with(nolock),shasqlv01a.jems.dbo.cr_text c with(nolock),shasqlv01a.jems.dbo.cr_fmrs_v d with (nolock),shasqlv01a.jems.dbo.SC_Users e with (nolock) where a.UserID_ID=e.UserID_ID and a.Wip_ID='%s' " %wip
        command += " and a.Defect_ID=b.Defect_ID and a.RouteStep_ID=d.RouteStep_ID and b.defect = c.text_id and c.language_id =0 and (d.StepText like '%FVT%' or d.StepText like '%ICT%' or d.StepText like '%FP%' or d.StepText like '%Beep%' or d.StepText like '%BURN%' or d.StepText like '%PCATS%' or d.StepText like '%OT%' or d.StepText like '%Programing%' or d.StepText like '%DL%' or d.StepText like '%Unlink Debug%' or d.StepText like '%RF%' or d.StepText like '%MACVERIFY%' or d.StepText like '%Rescreen%' or d.StepText like '%Assign CB%') order by a.AnalysisDateTime DESC"
        print(command)
        cursor.execute(command)
        rows = cursor.fetchall()
        for num,row in enumerate(rows):
            if 'Electrically defective' in row[0]:
                row[0] = 'ED'
            # for multiple crd case .
            if num >=1:
                # print(analysisList[num-1][1],type(analysisList[num-1][1]),row[1])
                d = (row[1] - datetime.strptime(analysisList[len(analysisList)-1][1],"%Y-%m-%d %H:%M:%S")).total_seconds()
                # print('sec',d)
                if d >-30 and d < 30:
                    analysisList[len(analysisList)-1][2] += ','+ row[2]
                    analysisList[len(analysisList)-1][0] += ',' + row[0]
                    continue
            temp = []
            temp.append(row[0])  # anaysis rec
            temp.append(datetime.strftime(row[1],"%Y-%m-%d %H:%M:%S"))
            temp.append(row[2])  # defect crd
            temp.append(row[3])  # step
            temp.append(row[4])  # user id
            temp.append(row[5])  # user name
            analysisList.append(temp)
        cursor.close()
        return analysisList

    def Get_material(self,wip_id,start_time):
        """_summary_

        Args:
            wip_id (_type_): _description_
            start_time (_type_): _description_
        """

        material_list = []
        material_list1 = []
        cursor = self.odbc.cursor()
        command = """ Select  a.[DefectLocation],a.[AnalysisDateTime],a.[Material_ID],a.[Defect_ID],a.[UserID_ID],c.[WindowsUserID],b.[Material],d.[Defect],e.[Translation] from shasqlv01a.jems.dbo.QM_Analysis a with (nolock) left outer join shasqlv01a.jems.dbo.cr_materials b with(nolock) on a.Material_ID = b.Material_ID,shasqlv01a.jems.dbo.SC_Users c with (nolock) ,shasqlv01a.jems.dbo.QM_Defects d with(nolock)  left outer join shasqlv01a.jems.dbo.cr_text e with(nolock) on d.[Defect] = e.[Text_ID]  where a.Defect_ID = d.Defect_ID and a.UserID_ID=c.UserID_ID and a.Wip_ID='{0}' and a.[AnalysisDateTime] >= '{1}'  order by AnalysisDateTime DESC """.format(wip_id,start_time)
        
        # print('command is:',command)
        cursor.execute(command)
        rows = cursor.fetchall()
        """ 'PCB', '2023-02-14 15:54:30', 12, 'weip', 'DRMU23373-R', 'Damaged' """
        

        

        [material_list.append([row[0],datetime.strftime(row[1],"%Y-%m-%d %H:%M:%S"),row[3],row[5],str(row[6]).strip(),row[8]]) for row in rows if row[0] not in material_list[-1][0] ]
        cursor.close()
        return material_list

    def to_dict_material(self,material_list):
        """
        board info to dict
        :return: dict
        """
        material_dict = {
            "Crd": material_list[0],
            "Analysis_dt":material_list[1],
            "AnalyzedCode":material_list[2],
            "mes_user": material_list[3],
            "Material": material_list[4],
            "Analysis_desc" : material_list[-1]

        }
        return material_dict




    # def Get_current_station(self,wipid,wipsn):
    #     """
    #     Get Current station
    #     :param wipid:
    #     :param wipsn:
    #     :return: list
    #     """
    #     current_status_list = []
    #     cursor = self.odbc.cursor()
    #     # sql command for get fail record.
    #     # return sample [120688073, 'F', '2019-08-27 13:46:01', 'RF1 RF1']
    #     command = """ select TOP 1 a.Wip_ID,a.TestStatus, a.StopDateTime,c.StepText,a.assembly_id from  shasqlv01a.jems.dbo.QM_TestData a  with (nolock)
    #     left outer join shasqlv01a.jems.dbo.cr_fmrs_v c with (nolock) on a.RouteStep_ID=c.RouteStep_ID
    #     where a.Wip_ID ='%s'order by a.StopDateTime DESC """ %wipid
    #     cursor.execute(command)
    #     rows = cursor.fetchall()
    #     for row in rows:
    #         if row[1] == 'A':
    #             row[1] = 'B'
    #         current_status_list.append(row[1]) # status
    #         current_status_list.append(row[2])  # Fail time
    #         current_status_list.append(row[3]) # Station
    #         # print('status time is:[%s]'%row[2])
    #     if current_status_list:
    #         # return sample "['Electrically defective', '2019-09-23 09:08:16', 'U14', 'DIAG Diag FVT2']"
    #         sql = '''Select TOP 1 c.translation, a.AnalysisDateTime, a.DefectLocation,d.StepText from shasqlv01a.jems.dbo.QM_Analysis a with (nolock),
    #                                          shasqlv01a.jems.dbo.QM_Defects b with(nolock),shasqlv01a.jems.dbo.cr_text c with(nolock),shasqlv01a.jems.dbo.cr_fmrs_v d with (nolock)
    #                                          where a.Wip_ID='''
    #         sql = sql + "'" + str(wipid) + "'" + " and a.Defect_ID=b.Defect_ID and a.RouteStep_ID=d.RouteStep_ID and b.defect = c.text_id and c.language_id =0 and (d.StepText like '%FVT%' or d.StepText like '%ICT%' or d.StepText like '%Fly%' or d.StepText like '%FP%' or d.StepText like '%PCATS%' or d.StepText like '%OT%' or d.StepText like '%Programing%' or d.StepText like '%DL%' or d.StepText like '%Unlink Debug%' or d.StepText like '%RF%' or d.StepText like '%Beep%' or d.StepText like '%BURN%' or d.StepText like '%MACVERIFY%' or d.StepText like '%Assign CB%') order by a.AnalysisDateTime DESC"
    #         # print('Mike Here ',sql)
    #         cursor.execute(sql)
    #         rows = cursor.fetchall()
    #         for row in rows:
    #             cal_sec = (current_status_list[1] - row[1]).total_seconds()
    #             # print("compare with analysis time ,calc result:[%s]"%cal_sec ,"analysis time is:",row[1])
    #             if cal_sec >0 : # Fail record greater than analysis record
    #                continue
    #             else :
    #                 # print(row[0],'analysis record !')
    #                 if row[0] == "No analysis" and (row[1]- current_status_list[1]).total_seconds() < 43200:
    #                     continue
    #                 else:
    #                     # print('current status is:',current_status_list[0])
    #                     if "FIXTURE" in row[0] or "RETEST" in row[0] or "Contact" in row[0] or "Not connected" in row[0] or "SCRIPT_PROBLEM" in row[0] or "NDF" in row[0] or "Operator" in row[0] or "Product" in row[0] or "NPF" in row[0] or "RETEST_NO_DEBUG" in row[0] or "Initialization Error" in row[0]:
    #                         current_status_list[0] = "T"
    #                         current_status_list[1] = row[1]
    #                         current_status_list[2] = row[3]
    #                     elif "Vendor Defect" in row[0] or "Open trace" in row[0]:
    #                         current_status_list[0] = "V"
    #                         current_status_list[1] = row[1]
    #                         current_status_list[2] = row[3]
    #                     else:
    #                         current_status_list[0] = "A"
    #                         current_status_list[1] = row[1]
    #                         current_status_list[2] = row[3]
    #     # sql command for get current station
    #     # return sample [120688073, 'N', '2019-09-17 14:06:10', 'DIAG Diag RF1']
    #
    #
    #     command1 = """Select Top 1 a.Wip_id,EndTime,b.StepText from shasqlv01a.jems.dbo.WP_WipRouteSteps a left outer join shasqlv01a.jems.dbo.cr_fmrs_v b
    #                   on a.RouteStep_ID=b.RouteStep_ID  where a.Wip_ID in
    #                   (Select Wip_ID from shasqlv01a.jems.dbo.WP_Wip with (nolock) where SerialNumber='%s') order by EndTime DESC""" %wipsn
    #
    #     cursor.execute(command1)
    #     rows = cursor.fetchall()
    #     # print('thinking',current_status_list[0],current_status_list[1],current_status_list[2])
    #     for row in rows:
    #         if not current_status_list: # 说明板子没有任何FAIL 记录
    #             current_status_list.append("N")
    #             current_status_list.append(row[1])
    #             current_status_list.append(row[2])
    #         else:
    #             if "DIAG" in str(row[2]):
    #                 continue
    #             cal_sec= (current_status_list[1] - row[1]).total_seconds()
    #             if current_status_list[2] == row[2] and (cal_sec >-200 and cal_sec < 200) :
    #                 continue
    #             # print ("compare with before time calc result is:",cal_sec)
    #             if cal_sec > -3:
    #                 continue
    #             else :
    #                 # print("current station time is: ",row[1])
    #                 current_status_list[0] = "N"
    #                 current_status_list[1] = row[1]
    #                 current_status_list[2] = row[2]
    #
    #     cursor.close()
    #     current_status_list[1] = datetime.strftime(current_status_list[1],"%Y-%m-%d %H:%M:%S")
    #     # print("current status list is:",current_status_list)
    #     # print(current_status_list,99999)
    #     return current_status_list

    def Get_current_station(self, wipid, wipsn):
        """
        Get Current station
        :param wipid:
        :param wipsn:
        :return: list
        """
        current_status_list = []
        cursor = self.odbc.cursor()
        # sql command for get fail record.
        # return sample [120688073, 'F', '2019-08-27 13:46:01', 'RF1 RF1']
        command = """ select TOP 1 a.Wip_ID,a.TestStatus, a.StopDateTime,c.StepText,a.assembly_id from  shasqlv01a.jems.dbo.QM_TestData a  with (nolock)
        left outer join shasqlv01a.jems.dbo.cr_fmrs_v c with (nolock) on a.RouteStep_ID=c.RouteStep_ID
        where a.Wip_ID ='%s'order by a.StopDateTime DESC """ % wipid
        print(command)
        cursor.execute(command)
        rows = cursor.fetchall()
        for row in rows:
            if row[1] == 'A':
                row[1] = 'B'
            current_status_list.append(row[1])  # status
            current_status_list.append(row[2])  # Fail time
            current_status_list.append(row[3])  # Station
            # print('status time is:[%s]'%row[2])
        if current_status_list:
            # return sample "['Electrically defective', '2019-09-23 09:08:16', 'U14', 'DIAG Diag FVT2']"
            sql = '''Select TOP 1 c.translation, a.AnalysisDateTime, a.DefectLocation,d.StepText from shasqlv01a.jems.dbo.QM_Analysis a with (nolock),
                                             shasqlv01a.jems.dbo.QM_Defects b with(nolock),shasqlv01a.jems.dbo.cr_text c with(nolock),shasqlv01a.jems.dbo.cr_fmrs_v d with (nolock)
                                             where a.Wip_ID='''
            sql = sql + "'" + str(
                wipid) + "'" + " and a.Defect_ID=b.Defect_ID and a.RouteStep_ID=d.RouteStep_ID and b.defect = c.text_id and c.language_id =0 and (d.StepText like '%FVT%' or d.StepText like '%ICT%' or d.StepText like '%Fly%' or d.StepText like '%FP%' or d.StepText like '%PCATS%' or d.StepText like '%OT%' or d.StepText like '%Programing%' or d.StepText like '%DL%' or d.StepText like '%Unlink Debug%' or d.StepText like '%RF%' or d.StepText like '%Beep%' or d.StepText like '%BURN%' or d.StepText like '%MACVERIFY%' or d.StepText like '%Assign CB%') order by a.AnalysisDateTime DESC"
            cursor.execute(sql)
            rows = cursor.fetchall()
            for row in rows:
                print(current_status_list[1], row[1], 'wqwqwwww')
                cal_sec = (current_status_list[1] - row[1]).total_seconds()
                print("compare with analysis time ,calc result:[%s]" % cal_sec, "analysis time is:", row[1])
                if cal_sec > 0:  # Fail record greater than analysis record
                    continue
                else:
                    print(row[0], 'analysis record !')
                    if row[0] == "No analysis" and (row[1] - current_status_list[1]).total_seconds() < 43200:
                        continue
                    else:
                        if "FIXTURE" in row[0] or "RETEST" in row[0] or "Contact" in row[0] or "Not connected" in row[0] or "SCRIPT_PROBLEM" in row[0] or "NDF" in row[0] or "Operator" in row[0] or "Product" in row[0] or "NPF" in row[0] or "RETEST_NO_DEBUG" in row[0] or "Initialization Error" in row[0]:
                            current_status_list[0] = "T"
                            current_status_list[1] = row[1]
                            current_status_list[2] = row[3]
                        elif "Vendor Defect" in row[0] or "Open trace" in row[0]:
                            current_status_list[0] = "V"
                            current_status_list[1] = row[1]
                            current_status_list[2] = row[3]
                        else:
                            current_status_list[0] = "A"
                            current_status_list[1] = row[1]
                            current_status_list[2] = row[3]
        # sql command for get current station
        # return sample [120688073, 'N', '2019-09-17 14:06:10', 'DIAG Diag RF1']
        command1 = """Select Top 1 a.Wip_id,EndTime,b.StepText from shasqlv01a.jems.dbo.WP_WipRouteSteps a left outer join shasqlv01a.jems.dbo.cr_fmrs_v b
                      on a.RouteStep_ID=b.RouteStep_ID  where a.Wip_ID in 
                      (Select Wip_ID from shasqlv01a.jems.dbo.WP_Wip with (nolock) where SerialNumber='%s') order by EndTime DESC""" % wipsn

        cursor.execute(command1)
        rows = cursor.fetchall()
        # print('thinking',current_status_list[0],current_status_list[1],current_status_list[2])
        for row in rows:
            if not current_status_list:  # 说明板子没有任何FAIL 记录
                current_status_list.append("N")
                current_status_list.append(row[1])
                current_status_list.append(row[2])
            else:
                if "DIAG" in str(row[2]):
                    continue
                cal_sec = (current_status_list[1] - row[1]).total_seconds()
                if current_status_list[2] == row[2] and (cal_sec > -200 and cal_sec < 200):
                    continue
                # print ("compare with before time calc result is:",cal_sec)
                if cal_sec > -3:
                    continue
                else:
                    pass
                    # print("current station time is: ",row[1])
                    # current_status_list[0] = "N"
                    # current_status_list[1] = row[1]
                    # current_status_list[2] = row[2]

        cursor.close()
        
        if current_status_list:
            current_status_list[1] = datetime.strftime(current_status_list[1], "%Y-%m-%d %H:%M:%S")

        return current_status_list

    def Get_Test_History(self,wipid):
        """
        :param wipid:str
        :return: History type: list
        """
        cursor = self.odbc.cursor()
        sql = '''
        select a.Wip_ID,a.TestStatus, a.StopDateTime,c.StepText,a.assembly_id from  shasqlv01a.jems.dbo.QM_TestData a  with (nolock)
        left outer join shasqlv01a.jems.dbo.cr_fmrs_v c with (nolock) on a.RouteStep_ID=c.RouteStep_ID
        where a.Wip_ID = '''
        sql = sql + str(wipid) + " and (c.StepText like '%FVT%' or c.StepText like '%PCATS%' or c.StepText like '%OT%' or c.StepText like '%ICT%' or c.StepText like '%FP%' or c.StepText like '%Fly%' or c.StepText like '%DL%' or c.StepText like '%Program%' or c.StepText like '%Unlink Debug%' or c.StepText like '%BURN%' or c.StepText like '%ROM%' or c.StepText like '%RF%' or c.StepText like '%Beep%' or c.StepText like '%MACVERIFY%' or c.StepText like '%Rescreen%' or c.StepText like '%Assign CB%') order by a.StopDateTime ASC"
        cursor.execute(sql)
        rows = cursor.fetchall()
        Test_History = []
        for row in rows:
            temp = []
            if row[1] =="F" or row[1] =="f":
                temp.append(row[0])
                temp.append(row[1])
                temp.append(datetime.strftime(row[2],"%Y-%m-%d %H:%M:%S"))
                temp.append(row[3])
                temp.append(row[4])
                print('temp data is:[%s]' %temp)
                Test_History.append(temp)
        cursor.close()
        return Test_History
    def Get_Test_History1(self,wipid):
        """
        Get all of test history
        :param wipid:str
        :return: History type: list
        """
        cursor = self.odbc.cursor()
        sql = '''
        select a.Wip_ID,a.TestStatus, a.StopDateTime,c.StepText,a.assembly_id from  shasqlv01a.jems.dbo.QM_TestData a  with (nolock)
        left outer join shasqlv01a.jems.dbo.cr_fmrs_v c with (nolock) on a.RouteStep_ID=c.RouteStep_ID
        where a.Wip_ID = '''
        sql = sql + str(wipid) + " and (c.StepText like '%FVT%' or c.StepText like '%PCATS%' or c.StepText like '%OT%' or c.StepText like '%ICT%' or c.StepText like '%FP%' or c.StepText like '%Fly%' or c.StepText like '%DL%' or c.StepText like '%Program%' or c.StepText like '%Unlink Debug%' or c.StepText like '%BURN%' or c.StepText like '%ROM%' or c.StepText like '%RF%' or c.StepText like '%Beep%' or c.StepText like '%Rescreen%' or c.StepText like '%MACVERIFY%' or c.StepText like '%Assign CB%' ) order by a.StopDateTime ASC"
        cursor.execute(sql)
        rows = cursor.fetchall()
        Test_History1 = []
        for row in rows:
            temp = []
            if row[1] == "P" or row[1] == "F":
                temp.append(row[0])
                temp.append(row[1])
                temp.append(datetime.strftime(row[2],"%Y-%m-%d %H:%M:%S"))
                temp.append(row[3])
                temp.append(row[4])
                print('temp data is:[%s]' %temp)
                Test_History1.append(temp)
        cursor.close()
        return Test_History1


    def Get_analysis_detail(self, wipid):
        """
        :param wipid:int ,program will convert this value to str .
        :return:Analysis history type:list
        """
        cursor = self.odbc.cursor()
        sql = '''Select c.translation, a.AnalysisDateTime, a.DefectLocation,d.StepText from shasqlv01a.jems.dbo.QM_Analysis a with (nolock),
                    shasqlv01a.jems.dbo.QM_Defects b with(nolock),shasqlv01a.jems.dbo.cr_text c with(nolock),shasqlv01a.jems.dbo.cr_fmrs_v d with (nolock)
                    where a.Wip_ID='''
        sql = sql + "'" + str(
            wipid) + "'" + " and a.Defect_ID=b.Defect_ID and a.RouteStep_ID=d.RouteStep_ID and b.defect = c.text_id and c.language_id =0 and (d.StepText like '%FVT%'or d.StepText like '%RF%' or d.StepText like '%FP%' or d.StepText like '%ICT%' or d.StepText like '%Fly%' or d.StepText like '%PCATS%' or d.StepText like '%OT%' or d.StepText like '%Programing%' or d.StepText like '%DL%' or d.StepText like '%Unlink Debug%' or d.StepText like '%Rescreen%' or d.StepText like '%Beep%' or d.StepText like '%BURN%' or d.StepText like '%ROM%' or d.StepText like '%MACVERIFY%' or d.StepText like '%Assign CB%')  order by a.AnalysisDateTime ASC"
        cursor.execute(sql)
        rows = cursor.fetchall()
        Analysis_History_FVT = []
        Analysis_History_ICT = []
        for index, row in enumerate(rows):
            if "DIAG Diag ICT" in row[3] or "FP" in row[3]:
                if len(Analysis_History_ICT) >= 1:
                    compare_result = self.__analysistime_judgement(row[1], Analysis_History_ICT)
                    if compare_result:
                        continue
                temp = []
                temp.append(row[0])
                temp.append(datetime.strftime(row[1], "%Y-%m-%d %H:%M:%S"))
                temp.append(str(row[2]))
                temp.append(row[3])
                Analysis_History_ICT.append(temp)
            elif  "ICT" not in row[3] and "FP" not in row[3]:
                if len(Analysis_History_FVT) >= 1:
                    compare_result = self.__analysistime_judgement(row[1], Analysis_History_FVT)
                    if compare_result:
                        continue
                temp = []
                temp.append(row[0])
                temp.append(datetime.strftime(row[1], "%Y-%m-%d %H:%M:%S"))
                temp.append(str(row[2]))
                temp.append(row[3])
                Analysis_History_FVT.append(temp)
        cursor.close()
        return (Analysis_History_ICT, Analysis_History_FVT)

    def Get_FAIL_History(self,wipid):
        """
        :param wipid:str
        :return: History type: list
        """
        cursor = self.odbc.cursor()
        sql = '''
        select a.Wip_ID,a.TestStatus, a.StopDateTime,c.StepText,a.assembly_id from  shasqlv01a.jems.dbo.QM_TestData a  with (nolock)
        left outer join shasqlv01a.jems.dbo.cr_fmrs_v c with (nolock) on a.RouteStep_ID=c.RouteStep_ID
        where a.Wip_ID = '''
        sql = sql + str(wipid) + " and (c.StepText like '%FVT%' or c.StepText like '%PCATS%' or c.StepText like '%OT%' or c.StepText like '%ICT%' or c.StepText like '%FP%' or c.StepText like '%Fly%' or c.StepText like '%DL%' or c.StepText like '%RF%' or c.StepText like '%Beep%' or c.StepText like '%Program%' or c.StepText like '%Unlink Debug%' or c.StepText like '%Rescreen%' or c.StepText like '%BURN%' or c.StepText like '%ROM%' or c.StepText like '%MACVERIFY%'  or c.StepText like '%Assign CB%') order by a.StopDateTime ASC"
        cursor.execute(sql)
        rows = cursor.fetchall()
        FAIL_History_ICT = []
        FAIL_History_FVT = []
        for row in rows:
            # print('row 3 value is:',row[3],row[1])
            if row[1] =="F" and ("ICT" in row[3] or "FP" in row[3]):
                if len(FAIL_History_ICT) >= 1:
                    compare_result = self.__analysistime_judgement(row[2], FAIL_History_ICT)
                    if compare_result:
                        continue
                temp = []
                temp.append(row[0])
                temp.append(row[1])
                temp.append(datetime.strftime(row[2],"%Y-%m-%d %H:%M:%S"))
                temp.append(row[3])
                temp.append(row[4])
                FAIL_History_ICT.append(temp)
            elif row[1] == "F":
                temp = []
                if len(FAIL_History_FVT) >= 1:
                    compare_result = self.__analysistime_judgement(row[2], FAIL_History_FVT)
                    if compare_result:
                        continue
                temp.append(row[0])
                temp.append(row[1])
                temp.append(datetime.strftime(row[2], "%Y-%m-%d %H:%M:%S"))
                temp.append(row[3])
                temp.append(row[4])
                FAIL_History_FVT.append(temp)
        cursor.close()
        return (FAIL_History_ICT,FAIL_History_FVT)

    def __analysistime_judgement(self, ana_time, analysis_list):
        """
        :param analysis_time:
        :param analysis_list:
        :return:
        """
        # for switch fail list  and analysis list time position .
        loop = 1
        if analysis_list[len(analysis_list) - 1][1] == "F":
            loop = 2
        d = (ana_time - datetime.strptime(analysis_list[len(analysis_list) - 1][loop],
                                          "%Y-%m-%d %H:%M:%S")).total_seconds()
        if d > -360 and d < 360:
            return True
        else:
            return False


    def Get_MRB_record(self,wipid,last_updatetime):
        """
        :param wipid:
        :param last_updatetime:
        :return:datatime (str)
        """
        cursor = self.odbc.cursor()
        command = '''select Top 1 EndTime from shasqlv01a.jems.dbo.WP_WipRouteSteps with (nolock) where Wip_ID= '%s'  '''%wipid
        print(command)
        command = command + '''and RouteStep_ID in (Select RouteStep_ID from shasqlv01a.jems.dbo.cr_fmrs_v with (nolock) where StepText like ('%MRB%')) order by EndTime DESC'''
        cursor.execute(command)
        sql_lastupdatetime = datetime.strptime(last_updatetime, '%Y-%m-%d %H:%M:%S')
        rows = cursor.fetchall()
        cursor.close()
        for row in rows:
            days = row[0] - sql_lastupdatetime
            if days.seconds >0 :
                return datetime.strftime(row[0],"%Y-%m-%d %H:%M:%S")
            else :
                return False
        else :
            return False

    def Get_OBA_record(self,wipid,last_updatetime):
        """
        :param wipid:
        :param last_updatetime:
        :return:datatime (str)
        """
        cursor = self.odbc.cursor()
        command = '''select Top 1 EndTime from shasqlv01a.jems.dbo.WP_WipRouteSteps with (nolock) where Wip_ID= '%s'  '''%wipid
        print(command)
        command = command + '''and RouteStep_ID in (Select RouteStep_ID from shasqlv01a.jems.dbo.cr_fmrs_v with (nolock) where StepText like ('%OBA%')) order by EndTime DESC'''
        cursor.execute(command)
        sql_lastupdatetime = datetime.strptime(last_updatetime, '%Y-%m-%d %H:%M:%S')
        rows = cursor.fetchall()
        cursor.close()
        for row in rows:
            days = row[0] - sql_lastupdatetime
            if days.seconds >0 :
                return datetime.strftime(row[0],"%Y-%m-%d %H:%M:%S")
            else :
                return False
        else :
            return False

    def Get_packout_record(self,wipid,last_updatetime):
        """
        :param wipid:
        :return: str
        """
        cursor = self.odbc.cursor()
        Get_date = (datetime.now() - timedelta(days = 1)).strftime("%Y-%m-%d")
        command = ''' select max(EndTime) from shasqlv01a.jems.dbo.WP_WipRouteSteps with (nolock) where Wip_ID='%s'  and RouteStep_ID in (Select RouteStep_ID from shasqlv01a.jems.dbo.cr_fmrs_v with (nolock) where StepText like'''%wipid
        command1 = ''' ('%PACKOUT%')) and EndTime >'''+"'" + Get_date + ''' 08:00:00.590'''+"'"
        command = command + command1
        print('The command is:', command)
        cursor.execute(command)
        sql_lastupdatetime = datetime.strptime(last_updatetime, '%Y-%m-%d %H:%M:%S')
        rows = cursor.fetchall()
        cursor.close()
        for row in rows:
            if 'None' in str(row[0]):
                return False
            else :
                days = row[0] - sql_lastupdatetime
                if days.seconds > 0:
                    return datetime.strftime(row[0], "%Y-%m-%d %H:%M:%S")
                else:
                    return False
        else :
            return False

    def Get_pass_result(self,wipid,last_updatetime):
        """
        :param wipid: num
        :param station: str
        :param last_updatetime:
        :return: list
        """
        passrecord =[]
        cursor = self.odbc.cursor()
        sql = '''
                select Top 1 a.Wip_ID,a.TestStatus, a.StopDateTime,c.StepText,a.assembly_id from  shasqlv01a.jems.dbo.QM_TestData a  with (nolock)
                left outer join shasqlv01a.jems.dbo.cr_fmrs_v c with (nolock) on a.RouteStep_ID=c.RouteStep_ID
                where a.Wip_ID = '''
        sql = sql + str(wipid) + "order by a.StopDateTime DESC"
        cursor.execute(sql)
        # 转成时间
        sql_lastupdatetime = datetime.strptime(last_updatetime,'%Y-%m-%d %H:%M:%S')
        rows = cursor.fetchall()
        cursor.close()
        for row in rows:
            temp = []
            days = row[2] - sql_lastupdatetime
            print('the seconds is:',days.seconds)
            if row[1] =="P" and days.seconds > 0:
                passrecord.append(row[0])
                passrecord.append(row[1])
                passrecord.append(datetime.strftime(row[2], "%Y-%m-%d %H:%M:%S"))
                passrecord.append(row[3])
                passrecord.append(row[4])
        return passrecord

    def Get_failed_snlist(self,cut_time):
        """
        :param start_time: str (start time)
        :param end_time:  str (end time)
        :return: list about SN detail(wip id ,sn ,customer id,failed time ,failed step name, assy id)
        """
        failedsnlist = []
        wipid_list = []
        cursor = self.odbc.cursor()
        sqlcommand = """
        SELECT  a.wip_id, b.serialnumber sn, b.customer_id,
        a.startdatetime ts, c.steptext step, a.assembly_id assy_id
        FROM shasqlv01a.jems.dbo.qm_testdata a WITH (NOLOCK)
        LEFT OUTER JOIN shasqlv01a.jems.dbo.wp_wip b WITH (NOLOCK)
        ON a.wip_id=b.wip_id
        LEFT OUTER JOIN shasqlv01a.jems.dbo.cr_fmrs_v c WITH (NOLOCK)
        ON a.routestep_id=c.routestep_id
        WHERE a.teststatus='F' """ + """ AND a.startdatetime >= '%s' """%cut_time  + """ AND a.lastupdated >= '%s' """%cut_time
        command = """and a.RouteStep_ID in (Select RouteStep_ID from shasqlv01a.jems.dbo.cr_fmrs_v with (nolock) where c.steptext like ('%FVT%') or c.steptext like ('%ICT%') or c.steptext like ('%Fly%')  or c.steptext like ('%FP%') or  c.steptext like ('%DL%') or c.steptext like ('%Program%') or c.steptext like ('%Unlink Debug%') or c.steptext like ('%RF%') or c.steptext like ('%PCATS%') or c.steptext like ('%OT%') or c.steptext like ('%Beep%') or c.steptext like ('%BURN%') or c.steptext like ('%MACVERIFY%')  or c.steptext like ('%Assign CB%'))and b.Customer_ID in ('30','39','41','54','55','59','73','77','84','90','95','103','122','83','88','22','142','131') """
        sqlcommand = sqlcommand + command
        cursor.execute(sqlcommand)
        rows = cursor.fetchall()
        cursor.close()
        for index,row in enumerate(rows):
            # print(index,row)
            temp = []
            if "RI" in row[4]:
                continue
            # 去除重复的WIP_id
            if str(row[0]).strip() not in wipid_list:
                wipid_list.append(str(row[0]).strip())
            else :
                continue
            temp.append(row[0]) # wip id
            temp.append(str(row[1])) # SN
            temp.append(row[2]) # customer id
            temp.append(datetime.strftime(row[3], "%Y-%m-%d %H:%M:%S"))   # failed time
            temp.append(row[4])  # failed step name
            temp.append(row[5])  # assy_id
            failedsnlist.append(temp)
        return failedsnlist

    def Get_NPF_record(self,wipid):
        """
        :param wipid:
        :return:Bool
        """
        cursor = self.odbc.cursor()
        command = """Select TOP 1 c.translation, a.AnalysisDateTime, a.DefectLocation,d.StepText from shasqlv01a.jems.dbo.QM_Analysis a with (nolock),
                     shasqlv01a.jems.dbo.QM_Defects b with(nolock),shasqlv01a.jems.dbo.cr_text c with(nolock),shasqlv01a.jems.dbo.cr_fmrs_v d with (nolock)
                     where a.Wip_ID= '%s' """%wipid + """and a.Defect_ID=b.Defect_ID and a.RouteStep_ID=d.RouteStep_ID and b.defect = c.text_id and c.language_id =0 and (d.StepText like ('%ICT%') or d.StepText like ('%Fly%')  or d.StepText like like ('%FP%') or d.StepText like '%FVT%'  or d.StepText like '%Programing%' or d.StepText like '%DL%' or d.StepText like '%Unlink Debug%' or d.StepText like '%RF%' or d.StepText like '%MACVERIFY%' or d.StepText like '%Rescreen%') order by a.AnalysisDateTime DESC"""
        cursor.execute(command)
        rows = cursor.fetchall()
        cursor.close()
        analysis_records = []
        for row in rows:
            print(row)
            analysis_records.append(row[0])
            analysis_records.append(row[1])
            analysis_records.append(str(row[2]))
            analysis_records.append(row[3])

        fail_records = self.Get_Test_History(wipid)
        for fail_record in fail_records:
            Get_last_fail_time = datetime.strptime(fail_record[2],"%Y-%m-%d %H:%M:%S")
        if analysis_records and ("RETEST_NO_DEBUG" in analysis_records[0] or "NDF_DEBUG" in analysis_records[0] or "Product retest" in analysis_records[0]):
            sec = (analysis_records[1] - Get_last_fail_time).total_seconds()
            if sec > 80 : # 如果大于80 秒
                return datetime.strftime(analysis_records[1],"%Y-%m-%d %H:%M:%S")
            else :
                return False
        else :
            return False

    def Get_RMA_info(self,wip_id):
        """
        :param :wip_id
        :return:bool
        """
        cursor = self.odbc.cursor()
        sql_command = """ select top 1 EndTime from shasqlv01a.jems.dbo.WP_WipRouteSteps with (nolock) where Wip_ID='%s' and RouteStep_ID in (Select RouteStep_ID from shasqlv01a.jems.dbo.cr_fmrs_v with (nolock) """%wip_id +""" where StepText like ('%VMI%')) order by EndTime DESC"""
        cursor.execute(sql_command)
        rows = cursor.fetchall()
        cursor.close()
        for row in rows:
            if len(str(row[0]))>10:
                return True
            else :
                return False
    def Get_packout_info(self,wip_id):
        """
        :param :wip_id
        :return:bool
        """
        cursor = self.odbc.cursor()
        sql_command = """ select top 1 EndTime from shasqlv01a.jems.dbo.WP_WipRouteSteps with (nolock) where Wip_ID='%s' and RouteStep_ID in (Select RouteStep_ID from shasqlv01a.jems.dbo.cr_fmrs_v with (nolock) """%wip_id +""" where StepText like ('%PACKOUT%')) order by EndTime DESC"""
        cursor.execute(sql_command)
        rows = cursor.fetchall()
        cursor.close()
        for row in rows:
            if len(str(row[0]))>10:
                return True
            else :
                return False

    def Get_steps_info(self,wip_id,rout_step):
        """
        :param wip_id: str
        :param rout_step: str
        :return: bool
        """
        cursor = self.odbc.cursor()
        sql_command = """ select top 1 EndTime from shasqlv01a.jems.dbo.WP_WipRouteSteps with (nolock) where Wip_ID='%s' and RouteStep_ID in (Select RouteStep_ID from shasqlv01a.jems.dbo.cr_fmrs_v with (nolock) """%wip_id +""" where StepText like ('%""" + rout_step + """%')) order by EndTime DESC"""
        cursor.execute(sql_command)
        rows = cursor.fetchall()
        cursor.close()
        for row in rows:
            if len(str(row[0]))>10:
                return True
            else :
                return False
    def Get_IRMA_info(self,wip_id):
        """
        :return bool
        """
        cursor = self.odbc.cursor()
        sql_command = """ select top 1 EndTime from shasqlv01a.jems.dbo.WP_WipRouteSteps with (nolock) where Wip_ID='%s' and RouteStep_ID in (Select RouteStep_ID from shasqlv01a.jems.dbo.cr_fmrs_v with (nolock) """ % wip_id + """ where StepText like ('%RMA%')) order by EndTime DESC"""
        cursor.execute(sql_command)
        rows = cursor.fetchall()
        cursor.close()
        for row in rows:
            if len(str(row[0])) > 10:
                return True
            else:
                return False


class BIG_DATA(object):
    """
    Query SN from database .
    :param N/A
    return : one obj
    """
    work_cell_dict = {}
    instance =None
    def __new__(cls):
        if cls.instance is None:
            obj = super(__class__,cls).__new__(cls)
            # 获取当前系统平台
            sys = platform.system()
            if sys == "Windows":
                sql_name = '{SQL Server}'
            elif sys == "Linux":
                sql_name = '{ODBC Driver 17 for SQL Server}'
            else:
                print("Can not running on an other system.")
            obj.odbc = pyodbc.connect('DRIVER=%s;SERVER=imedtedatabase;DATABASE=Bigdata_limitation;UID=sa;PWD=J!abil+12345;Mars_Connection=yes'%sql_name)
            cls.instance = obj
        return cls.instance
    
    def Get_group_names(self):
        """ 
            return: group names 
        """
        cursor = self.odbc.cursor()
        temp_list = []
        command = """ [Bigdata_limitation].[dbo].[GetGroupName] """
        # print(command)
        cursor.execute(command)
        rows = cursor.fetchall()
        cursor.close()
        if rows:
            temp_list = [row[0] for row in rows]
        return temp_list


        
    
    def Get_workcell_items(self,group_name):
        """
        :return: workcell list
        """
        cursor = self.odbc.cursor()
        temp_list = []
        command = """ [Bigdata_limitation].[dbo].[Get_customers] '%s' """%group_name
        # print(command)
        cursor.execute(command)
        rows = cursor.fetchall()
        cursor.close()
        if rows:
            temp_list = [[row[0],row[1]] for row in rows]
        return temp_list

    def Get_pn_items(self,workcell_id):
        """
        :param workcell_id: 83
        :return: pn list
        """
        cursor = self.odbc.cursor()
        temp_list = []
        # command = """ SELECT distinct(a.PN) FROM [AMS_Report].[dbo].[AMS_Limitation] a with(nolock) inner join  [AMS_Report].[dbo].[AMS_Test_Logs] b with (nolock) on a.Customer_ID = b.Customer_ID where a.Workcell = '%s' """ %workcell_name
        command = """ [Bigdata_limitation].[dbo].[get_partnumbers_by_customerid] '{}' """.format(workcell_id)
        # print(command)
        cursor.execute(command)
        rows = cursor.fetchall()
        cursor.close()
        if rows:
            temp_list = [row[0] for row in rows]
        return temp_list




    def Get_tester_names(self,customer_id,partnumber):

        """_summary_
            [Bigdata_limitation].[dbo].[query_testers] '83','MD7006063-006-A-R'
        """
        cursor = self.odbc.cursor()
        temp_list = []
        command = """ [Bigdata_limitation].[dbo].[query_testers] '{0}','{1}' """.format(customer_id,partnumber)
        print(command)
        cursor.execute(command)
        rows = cursor.fetchall()
        cursor.close()
        if rows:
            temp_list = [row[0] for row in rows]
        return temp_list


    def Get_table_names(self,group_name,customer_id,partnumber):
        """_summary_

        Args:
            group_name (_type_): _description_
            customer_id (_type_): _description_
            partnumber (_type_): _description_
        """
    
        cursor = self.odbc.cursor()
        temp_list = []
        command = """ [Bigdata_limitation].[dbo].[get_table_name] '{0}','{1}','{2}' """.format(group_name,customer_id,partnumber)
        # print(command)
        cursor.execute(command)
        rows = cursor.fetchall()
        cursor.close()
        if rows:
            temp_list = [[row[0],row[1]] for row in rows]
        return temp_list

   
    def Get_test_items(self,group_name,customer,partnumber):
        """_summary_

        Args:
            group_name (_type_): _description_
            customer_id (_type_): _description_
            partnumber (_type_): _description_
            exmple:[Bigdata_limitation].[dbo].[Get_test_items] 'IMED','Medtronic','MD7006076-008-A-R'
        """
        cursor = self.odbc.cursor()
        temp_list = []
        command = """ [Bigdata_limitation].[dbo].[Get_test_items] '{0}','{1}','{2}' """.format(group_name,customer,partnumber)
        print('command is:',command)
        cursor.execute(command)
        rows = cursor.fetchall()

        print('rows is:',rows)
        cursor.close()
        if rows:
            temp_list = [row[0] for row in rows]
        return temp_list
    

    def Get_test_data(self,group_name,wc_id,pn,item_name,start_time,end_time,tester):
        """
        :param item_name: item name
        :param start_time: start time
        :param end_time: end time
        command:[dbo].[Get_test_data] 'IMED','83','MD7006076-008-A-R','p1_dist','2023-03-07 01:00:32','2023-04-07 01:00:32','tester'
        :return: type (limit) ,example:[ [Tester],[Operator],[SN],[S0_Power_On_Current],[end_time - test_start_time]]
        """
        cursor = self.odbc.cursor()
        temp_list = []
        temp_list1 = []
        command = """ [Bigdata_limitation].[dbo].[Get_test_data] '{}','{}','{}','{}','{}','{}','{}' """.format(group_name,wc_id,pn,item_name,start_time,end_time,tester)
        cursor.execute(command)
        rows = cursor.fetchall()

        # print('command is:',command)

        [temp_list.append([datetime.strftime(row[4],'%Y-%m-%d %H:%M:%S'),float(row[3]),row[2]]) for row in rows]
            
        cursor.nextset()
        rows = cursor.fetchall()
        [temp_list1.append([float(row[0]),float(row[1])]) for row in rows ]

        cursor.close()

        return (temp_list, *temp_list1)
    
    def Get_out_limit_qty(self,item_name,start_time,end_time,wc,pn,tester):
        """
        :param item_name:
        :param start_time:
        :param end_time:
        :return: list
        """
        cursor = self.odbc.cursor()
        temp_list = []
        command = """[Bigdata_limitation].[dbo].[Get_out_limit_qty] '%s','%s','%s','%s','%s','%s' """ % (item_name, start_time, end_time,wc,pn,tester)
        cursor.execute(command)
        rows = cursor.fetchall()
        cursor.close()
        for row in rows:
            temp_list.append(row[0])
            temp_list.append(row[1])
            temp_list.append(row[2])
        print('temp list is:',temp_list)
        return temp_list
    


    def Get_test_default_data(self,group_name,wc_id,pn,item_name,start_time,end_time,tester):
        """
        :param item_name: item name
        :param start_time: start time
        :param end_time: end time
        command:[dbo].[Get_test_data] 'IMED','83','MD7006076-008-A-R','p1_dist','2023-03-07 01:00:32','2023-04-07 01:00:32','tester'
        :return: type (limit) ,example:[ [Tester],[Operator],[SN],[S0_Power_On_Current],[end_time - test_start_time]]
        """
        cursor = self.odbc.cursor()
        temp_list = []
        temp_list1 = []
        time_list = []
        command = """ [Bigdata_limitation].[dbo].[Get_test_data_dimm] '{}','{}','{}','{}','{}','{}','{}' """.format(group_name,wc_id,pn,item_name,start_time,end_time,tester)
        cursor.execute(command)

        print('command is:',command)
        rows = cursor.fetchall()

        # print('command is:',command)

        [temp_list.append([datetime.strftime(row[4],'%Y-%m-%d %H:%M:%S'),float(row[3]),row[2]]) for row in rows]
            
        cursor.nextset()
        rows = cursor.fetchall()
        [temp_list1.append([float(row[0]),float(row[1])]) for row in rows ]
        cursor.nextset()
        rows = cursor.fetchall()
        [time_list.append([row[0],row[1]]) for row in rows ]
        cursor.close()

        return (temp_list, *temp_list1,*time_list)
    
    def Get_out_limit_default_qty(self,item_name,start_time,end_time,wc,pn,tester):
        """
        :param item_name:
        :param start_time:
        :param end_time:
        :return: list
        """
        cursor = self.odbc.cursor()
        temp_list = []
        command = """[Bigdata_limitation].[dbo].[Get_out_dimm_limit_qty] '%s','%s','%s','%s','%s','%s' """ % (item_name, start_time, end_time,wc,pn,tester)
        cursor.execute(command)
        rows = cursor.fetchall()
        cursor.close()
        for row in rows:
            temp_list.append(row[0])
            temp_list.append(row[1])
            temp_list.append(row[2])
        print('temp list is:',temp_list)
        return temp_list



    def Get_bar_charts_qty(self,group_name,wc_name,family):
        """
        :param item_name:
        :param start_time:
        :param end_time:
        :return: list
        """
        cursor = self.odbc.cursor()
        temp_list = []
        command = """[Bigdata_limitation].[dbo].[get_last7_extracted] '%s','%s','%s' """ % (group_name,wc_name,family)
        cursor.execute(command)
        rows = cursor.fetchall()
        cursor.close()
        [temp_list.append([row[1],row[2]]) for row in rows]

        temp_list = sorted(temp_list,key=lambda x:x[0],reverse=False)


        return temp_list
    

    def Get_daily_cpk(self,test_item):
        """
        Args:
            [Bigdata_limitation].[dbo].[get_dimm_daily_cpk_by_pn] 'P1_dist_cpk','2023-04-10','2023-04-17'
        """

        cursor = self.odbc.cursor()

        start_time = datetime.strftime(datetime.now() + timedelta(days=-30),'%Y-%m-%d')
        end_time = datetime.strftime(datetime.now() + timedelta(days=-1),'%Y-%m-%d')
        temp_list = []
        command = """[Bigdata_limitation].[dbo].[get_dimm_daily_cpk_by_pn] '%s','%s','%s' """ % (test_item,start_time,end_time)

        print('command is wqllll',command)
        cursor.execute(command)
        rows = cursor.fetchall()
        cursor.close()
        [temp_list.append(list(row)) for row in rows]

        temp_list = sorted(temp_list,key=lambda x:x[0],reverse=False)


        return temp_list