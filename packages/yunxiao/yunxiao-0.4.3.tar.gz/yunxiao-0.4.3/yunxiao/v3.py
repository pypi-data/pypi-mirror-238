import logging

from .yunxiao import YunXiao, timestamp
# import requests
import httpx


class V3(YunXiao):
    def __init__(self, configfile: str = "yunxiao_config.ini", campus: tuple = ()):
        """
        初始化，输入用户账号密码，以及要操作的校区。
        :param campus: 校区
        :param configfile: 配置文件路径
        """
        super().__init__(configfile)
        self.campus = list(campus)
        self.client = httpx.Client(http2=True)

    def exit(self):
        self.client.close()

    def request(self, **kwargs) -> dict:
        response = self.client.request(
            method=kwargs.get("method"),
            url=kwargs.get("url"),
            json=kwargs.get("json"),
            params=kwargs.get("params"),
            headers={
                "x3-authentication": self.token,
                "Cookie": self.cookie,
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203",
                "Origin": "https://yunxiao.xiaogj.com",
                "Yunxiao-Version": "3.44"

            }
        )

        if response.status_code != 200:
            logging.error("无法到连接云校服务器。")
            return {"data": "无法到连接云校服务器。"}

        if response.json()["code"] == 401:
            logging.error(response.json()["msg"])
            self.renew_cookie()
            self.renew_token()
            response = self.client.request(
                method=kwargs.get("method"),
                url=kwargs.get("url"),
                json=kwargs.get("json"),
                params=kwargs.get("params"),
                headers={
                    "x3-authentication": self.token,
                    "Cookie": self.cookie,
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                  "Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43",
                    "Origin": "https://yunxiao.xiaogj.com",
                    "Referer": "https://yunxiao.xiaogj.com/app/teacher/"
                }
            )

        return response.json()

    # 翻页工具
    @staticmethod
    def loop_pages(KEY=None):
        """
        :param KEY: 实际数据所在的字段名
        :return:
        """

        def wrapper_func(func):
            def wrapper(*args, **kwargs):
                data_list = []  # 结果列表
                page = 1  # 设置起始页为 1
                size = kwargs.get("size")  # 设置每页数量为用户设置的数量

                page_count = 1  # 先假设总页数为 1
                while page <= page_count:  # 列表中数据行的数量不等于 1 时
                    kwargs["page"] = page
                    res = func(*args, **kwargs)
                    data = res["data"][KEY] if KEY else res["data"]
                    data_list.extend(data)

                    row_count = res["page"]["totalCount"]  # 取得实际的总行数
                    page_count = res["page"]["totalPage"]  # 取得实际的总页数
                    print(f"size: {size}, page: {page}/{page_count}, {page * size}/{row_count}")  # 汇报数量
                    page += 1  # 翻页
                return data_list

            return wrapper

        return wrapper_func

    # 查询机构指定日期范围业绩。
    def company_query_performance(self, startdate: str, enddate: str) -> list:
        """
        查询机构指定日期范围业绩。
        :param startdate: 起始日期
        :param enddate: 截止日期
        :return:
        """
        return self.request(
            method="post",
            url="https://yunxiao.xiaogj.com/api/cs-report/report/findDataReportList",
            json={
                "campusIds": self.campus,
                "startDate": startdate,
                "endDate": enddate,
                "orderByCampus": 1,
                "_t_": timestamp()
            }
        )["data"]

    # 查询校区（APP接口）
    def campus_query(self) -> list:
        """
        查询全部校区
        :return:
        """
        return self.request(
            method="get",
            url="https://yunxiao.xiaogj.com/api/cs-crm/campus/list?type=2"
        )["data"]

    # 查询指定日期范围业绩（APP接口）
    def campus_query_performance(self, start, end: str) -> list:
        """
        分校区列出指定日期的费用数据。
        :param start:
        :param end:
        :return:
        """
        data = self.request(
            method="post",
            url="https://yunxiao.xiaogj.com/api/cs-report/report/findDataReportList",
            json={
                "campusIds": self.campus,
                "startDate": start,
                "endDate": end,
                "orderByCampus": 1,
                "_t_": timestamp()
            }
        )["data"]
        data_list: list = data["dataReportVos"]
        data_list.append(
            {
                "campusId": 00000000,
                "campusName": "总计",
                "tuitionRevenue": data['totalTuitionRevenue'],
                "dayIncome": 0,
                "courseMoney": data['totalCourseMoney'],
                "courseStudentSize": 0,
                "newStudent": data['totalNewStudent'],
                "date": None,
                "dateStr": None,
                "refundMoney": data['totalRefundMoney'],
                "refundStudentSize": 0,
                "walletMoney": data['totalWalletMoney']
            }
        )
        return data_list

    # 查询老师
    @loop_pages()
    def teachers_query(self, page, size, name: str = "", status: tuple = (1,)):
        """
        查询老师。
        :param page:
        :param size: 查询数量，最大 200
        :param status: 老师状态。 **1** 在职 **0** 离职
        :param name: 查询教师的姓名
        :return: [{}...]
        """
        return self.request(
            method="post",
            url="https://yunxiao.xiaogj.com/api/cs-pc-crm/teacher/pageList",
            json={
                "_t_": timestamp(),
                "page": {"pageNum": page, "pageSize": size},
                "queryKey": name,
                "roleIds": [],
                "orgStructureId": "",
                "campusIds": self.campus,
                "statusList": list(status)
            }
        )

    # 查询意向（APP接口）
    @loop_pages()
    def intentions_query(self, page, size, distributeStatus: int = 1, keyWord: str = "", level: int = "",
                         nonFollowUpDays: int = "", startNextTime: str = "", endNextTime: str = "",
                         startLastCommunicateTime: str = "", endLastCommunicateTime: str = ""):
        """
        查询意向
        :param size: 分页查询，每页数量
        :param page: 分页查询，初始页码
        :param distributeStatus: 是否分配跟进人。 **0** 无跟进人 **1** 有跟进人
        :param level: 意向级别。 1-5
        :param keyWord: 查询关键字
        :param nonFollowUpDays: 未跟进天数
        :param startNextTime: 计划跟进时间（查询起点）
        :param endNextTime: 计划跟进时间（查询终点）
        :param startLastCommunicateTime: 最近跟进时间（查询起点）
        :param endLastCommunicateTime: 最近跟进时间（查询终点）
        :return:
        """
        return self.request(
            method="post",
            url="https://yunxiao.xiaogj.com/api/cs-crm/intention/clue/allPage",
            json={
                "_t_": timestamp(),
                "distributeStatus": distributeStatus,
                "campusIds": self.campus,
                "keyWord": keyWord,
                "nonFollowUpDays": nonFollowUpDays,
                "level": level,
                "startNextTime": startNextTime,
                "endNextTime": endNextTime,
                "startLastCommunicateTime": startLastCommunicateTime,
                "endLastCommunicateTime": endLastCommunicateTime,
                "status": [0],
                "page": {"pageNum": page, "pageSize": size}
            }
        )

    # 查询意向学员（APP接口）
    @loop_pages()
    def intentions_query_students(self, page, size, distributeStatus: int = 1, keyWord: str = "", level: int = "",
                                  nonFollowUpDays: int = "", startNextTime: str = "", endNextTime: str = "",
                                  startLastCommunicateTime: str = "", endLastCommunicateTime: str = ""):
        """
        查询意向学员
        :param size: 分页查询，每页数量
        :param page: 分页查询，初始页码
        :param distributeStatus: 是否分配跟进人。 **0** 无跟进人 **1** 有跟进人
        :param level: 意向级别。 1-5
        :param keyWord: 查询关键字
        :param nonFollowUpDays: 未跟进天数
        :param startNextTime: 计划跟进时间（查询起点）
        :param endNextTime: 计划跟进时间（查询终点）
        :param startLastCommunicateTime: 最近跟进时间（查询起点）
        :param endLastCommunicateTime: 最近跟进时间（查询终点）
        :return:https://yunxiao.xiaogj.com/app/teacher/#/cluedetails?id=7127357
        """
        return self.request(
            method="post",
            url="https://yunxiao.xiaogj.com/api/cs-crm/student/listForIntentionManage",
            json={
                "_t_": timestamp(),
                "distributeStatus": distributeStatus,
                "campusIds": self.campus,
                "keyWord": keyWord,
                "nonFollowUpDays": nonFollowUpDays,
                "level": level,
                "startNextTime": startNextTime,
                "endNextTime": endNextTime,
                "startLastCommunicateTime": startLastCommunicateTime,
                "endLastCommunicateTime": endLastCommunicateTime,
                "page": {"pageNum": page, "pageSize": size}
            }
        )

    # 查询学生
    @loop_pages()
    def students_query(self, page, size, curriculumids: tuple = (), classids: tuple = (), student_ids: tuple = (),
                       status: tuple = (1, 6, 7), class_student_status: int = 0, has_follow_teacher: int = None,
                       start_create_time: str = "", end_create_time: str = ""):
        """
        查询学生
        :param size: 分页查询，每页数量
        :param page: 分页查询，初始页码，应设为 0
        :param curriculumids: 课程筛选
        :param classids: 班级筛选
        :param student_ids: 查询学生
        :param status: 学员状态。 **0** 未收费 **1** 在读 **6** 曾就读 **7** 停课 **99** 无效学员
        :param class_student_status: **0** 不筛选 **1** 未入班 **2** 已入班
        :param has_follow_teacher: **0** 无跟进人 **1** 有跟进人
        :param start_create_time: 起始创建时间
        :param end_create_time: 截止创建时间
        :return:
        """
        return self.request(
            method="post",
            url="https://yunxiao.xiaogj.com/api/cs-pc-crm/student/extendList",
            json={
                "_t_": timestamp(),
                "campusIds": self.campus,
                "classIds": list(classids),
                "classStudentStatus": class_student_status,
                "curriculumIds": list(curriculumids),
                "customComeFromIds": [],
                "customGradeIds": [],
                "customFieldValueQueryDtoList": [],
                "startCreateTime": start_create_time,
                "endCreateTime": end_create_time,
                "followTeacherIdsMap": {"1": [], "2": []},
                "introducerIds": [],
                "hasFollowTeacher": has_follow_teacher,
                "onlyQueryRegisterCampus": False,
                "page": {"pageNum": page, "pageSize": size, "count": True},
                "sexList": [],
                "statusList": list(status),
                "studentIds": list(student_ids)
            }
        )

    # 查询学生课程卡
    @loop_pages()
    def students_query_cards(self, page: int, size: int, display_history: bool = True, fee_warn_status: int = 0,
                             remain_amount_min: str = "", remain_amount_max: str = "", student_name: str = ""):
        """
        列出所有课程卡
        :param size: 分页查询，每页数量
        :param page: 分页查询，起始页码
        :param fee_warn_status: **0** 不限
        :param display_history: 是否显示曾就读学生
        :param remain_amount_max: 限制查询剩余次数-最大
        :param remain_amount_min: 限制查询剩余次数-最小
        :param student_name: 查询学员名
        :return:
        """
        return self.request(
            method="post",
            url="https://yunxiao.xiaogj.com/api/cs-pc-report/cs-report/reports/studentCourseCard/report",
            json={
                "_t_": timestamp(),
                "page": {"pageNum": page, "pageSize": size},
                "campusIds": self.campus,
                "studentClassIds": [],
                "studentStatusList": [],
                "displayHistory": display_history,
                "cardType": "",
                "fee_warn_status": fee_warn_status,
                "curriculumIds": [],
                "cardInfoIds": [],
                "remainAmountMin": remain_amount_min,
                "remainAmountMax": remain_amount_max,
                "sort": "",
                "sortField": "",
                "studentName": student_name
            }
        )

    # 查询学生费用
    @loop_pages("cardCourseTradedList")
    def students_query_course_fee(self, page: int, size: int, displayHistory: bool = True,
                                  status: tuple = (1, 6, 7), studentName: str = ""):
        """
        学生数据费用报表。
        :param size: 分页查询，每页数量
        :param page: 分页查询，起始页码，应设为 0
        :param displayHistory: 是否显示曾就读学生
        :param status: 学生状态列表 **0** 未收费 **1** 在读 **7** 停课
        :param studentName: 学员姓名
        :return:
        """
        return self.request(
            method="post",
            url="https://yunxiao.xiaogj.com/api/cs-pc-report/cs-report/reports/findStudentCourseFee",
            json={
                "_t_": timestamp(),
                "page": {"pageNum": page, "pageSize": size},
                "campusIds": self.campus,
                "status": list(status),
                "displayHistory": displayHistory,
                "curriculumIds": [],
                "studentClassIds": [],
                "sort": "",
                "sortField": "",
                "studentName": studentName
            }
        )

    # 查询学生课时
    @loop_pages("studentCourseAmountList")
    def students_query_course_amount(self, page: int, size: int, displayHistory: bool = True,
                                     status: tuple = (1, 7), studentName: str = ""):
        """
        学生数据的课次报表。
        :param size: 分页查询，每页数量
        :param page: 分页查询，起始页码，应设为 0
        :param displayHistory: 是否显示曾就读学生
        :param status: 学生状态列表 **0** 未收费 **1** 在读 **7** 停课
        :param studentName: 学员姓名
        :return:
        """
        return self.request(
            method="post",
            url="https://yunxiao.xiaogj.com/api/cs-pc-report/cs-report/reports/findStudentCourseAmount",
            json={
                "_t_": timestamp(),
                "page": {"pageNum": page, "pageSize": size},
                "campusIds": self.campus,
                "status": list(status),
                "displayHistory": displayHistory,
                "curriculumIds": [],
                "studentClassIds": [],
                "sort": "",
                "sortField": "",
                "studentName": studentName
            }
        )

    # 查询学生基本信息
    def student_query_info(self, student_id: int):
        """
        查询学生基本信息
        :param student_id: 学员ID
        :return:
        """
        return self.request(
            method="get",
            url="https://yunxiao.xiaogj.com/api/cs-pc-crm/student/detail",
            params={
                "_t_": timestamp(),
                "id": student_id,
                "queryMember": True,
                "queryWallet": True
            }
        )["data"]

    # 查询学生课程卡包
    def student_query_cards(self, studentid: int) -> list:
        """
        查看学员的课程卡包
        :param studentid: 学生ID
        :return: json数据
        """
        return self.request(
            method="post",
            url="https://yunxiao.xiaogj.com/api/cs-pc-edu/studentCard/list",
            json={
                "_t_": timestamp(),
                "studentId": studentid
            }
        )["data"]

    # 查询学生就读课程
    def student_query_course(self, studentid: int) -> list:
        """
        查看学员的课程卡包
        :param studentid: 学生ID
        :return: json数据
        """
        return self.request(
            method="post",
            url="https://yunxiao.xiaogj.com/api/cs-pc-edu/courseStudent/findStudentAttendCourse",
            json={
                "_t_": timestamp(),
                "studentId": studentid,
                "page": {"pageNum": 1, "pageSize": 1000}
            }
        )["data"]["studentAttendCourseList"]

    # 设置在读学生状态为曾就读
    def student_operation_become_history(self, studentlist: tuple):
        """
        设置学生为曾就读。
        :param studentlist: 学生ID
        :return:
        """
        return self.request(
            method="post",
            url="https://yunxiao.xiaogj.com/api/cs-pc-edu/student/becomeHistory",
            json={"_t_": timestamp(), "studentIds": list(studentlist)}
        )

    # 设置曾就读学生状态为在读
    def student_operation_become_study(self, studentlist: tuple):
        """
        设置学生为曾就读。
        :param studentlist: 学生ID
        :return:
        """
        return self.request(
            method="post",
            url="https://yunxiao.xiaogj.com/api/cs-pc-edu/student/becomeStudy",
            json={"_t_": timestamp(), "studentIds": list(studentlist)}
        )

    # 查询课程
    @loop_pages()
    def curriculums_query(self, page: int, size: int, searchname: str = None):
        """
        查询课程
        :param page:
        :param size:
        :param searchname: 查找课程名
        :return:
        """
        return self.request(
            method="post",
            url="https://yunxiao.xiaogj.com/api/cs-pc-edu/curriculum/page",
            json={
                "_t_": timestamp(),
                "page": {"pageNum": page, "pageSize": size},
                "curriculumName": searchname,
                "dimensionDetailIdList": []
            }
        )

    # 查排课
    @loop_pages()
    def arranges_query(self, page, size, starttime: str, endtime: str, classid: int = "", teacherids: tuple = (),
                       studentids: tuple = (), display_completed_class: bool = False, courseStatusList: tuple = (0, 1)):
        """
        查询某日到某日的排课。
        :param classid: 班级
        :param size: 分页查询，每页数量
        :param page: 分页查询，起始页码
        :param studentids: 查询的学生列表
        :param teacherids: 查询的教师列表
        :param display_completed_class: 是否已结班排课
        :param courseStatusList: 排课状态。 **0** 未点名 **1** 已点名 **2** 已取消
        :param starttime: 查询起始时间 **2020-02-20**
        :param endtime: 查询截止时间 **2020-03-20**
        :return:
        """

        data = {
            "_t_": timestamp(),
            "page": {"pageNum": page, "pageSize": size},
            "campusIds": self.campus,
            "startDate": starttime,
            "endDate": endtime,
            "curriculumIds": [],
            "teacherIds": list(teacherids),
            "assistantTeacherIds": [],
            "classRoomIds": [],
            "studentIds": list(studentids),
            "reserve": 0,
            "displayCompletedClass": display_completed_class,
            "courseStatusList": list(courseStatusList),
            "sortType": 1
        }

        if classid:
            data["classId"] = classid
            data["sortType"] = 2

        return self.request(
            method="post",
            url="https://yunxiao.xiaogj.com/api/cs-pc-edu/arrange/page",
            json=data
        )

    # 查询班级
    @loop_pages()
    def classes_query(self, page, size, teacherids: tuple = (), class_ids: tuple = (), class_status: tuple = ()):
        """
        查询班级
        :param size: 分页查询，每页数量
        :param page: 分页查询，起始页码
        :param class_ids: 班级ID
        :param class_status: 班级状态。 **0** 未结班 **1** 已结班
        :param teacherids: 老师ID
        :return:
        """
        return self.request(
            method="post",
            url="https://yunxiao.xiaogj.com/api/cs-pc-edu/classInfo/page",
            json={
                "_t_": timestamp(),
                "queryClassTime": 1,
                "campusIds": self.campus,
                "classIds": list(class_ids),
                "curriculumIds": [],
                "assistantIds": [],
                "page": {"pageNum": page, "pageSize": size, "count": True},
                "classStatusList": list(class_status),
                "nowTeacherIds": list(teacherids)
            }
        )

    # 查询班级信息
    def class_query_info(self, classid: int = None) -> dict:
        """
        查询指定班级信息
        :param classid: 班级id
        :return:
        """
        return self.request(
            method="get",
            url="https://yunxiao.xiaogj.com/api/cs-pc-edu/classInfo/getClassInfoVo",
            params={
                "_t_": timestamp(),
                "classId": classid
            }
        )["data"]

    # 查询班级学生
    def class_query_student(self, classid: int, inout: int = 1) -> list:
        """
        查询班级学生
        :param inout: **[1]** 当前在班学员 **[2]** 历史学员
        :param classid: 班级ID
        :return:
        """
        return self.request(
            method="get",
            url="https://yunxiao.xiaogj.com/api/cs-pc-edu/classStudent/queryClassStudentList",

            params={
                "_t_": timestamp(),
                "nameOrPhone": "",
                "classId": classid,
                "page": {"pageNum": 1, "pageSize": 100, "count": True},
                "inOut": inout
            }
        )["data"]

    # 查询课消记录
    @loop_pages("courseConsumeList")
    def charges_query_record(self, page, size, startdate: str, enddate: str, class_id: int = None,
                             student_id: int = None, curriculum_ids: tuple = (), teacher_ids: tuple = ()):
        """
        列出指定上课日期范围的所有课消记录
        :param teacher_ids:
        :param curriculum_ids:
        :param student_id: 学生ID
        :param class_id: 班级ID
        :param size: 每次取数据的分片量
        :param page: 从第几页开始取数据。应设为 0
        :param startdate: YY-MM-DD
        :param enddate: YY-MM-DD
        :return:
        """

        return self.request(
            method="post",
            url="https://yunxiao.xiaogj.com/api/cs-pc-report/cs-report/reports/findCourseSignCharge",
            json={
                "_t_": timestamp(),
                "page": {"pageNum": page, "pageSize": size},
                "campusIds": self.campus,
                "teacherIds": list(teacher_ids),
                "courseStartTime": startdate,
                "courseEndTime": enddate,
                "sourceTypeList": [],
                "courseStudentStatusList": [],
                "assistantTeacherIds": [],
                "sort": 1,
                "sortField": "operationTime",
                "curriculumIds": list(curriculum_ids),
                "classId": class_id,
                "studentId": student_id
            }
        )

    # 查询订单明细
    @loop_pages("orderItemAllList")
    def orders_query_items(self, page, size, start_date: str = "", end_date: str = "", order_types: tuple = (),
                           order_status: tuple = ()):
        """
        查询指定操作日期范围的所有订单子项
        :param order_status: **0** 待付款 **1** 已付款 **2** 已取消 **3** 已失效 **4** 已作废 **6** 已退费 **7** 已结转
        :param order_types: **0** 收费 **1** 转课 **2** 退费 **3** 结转
        :param size: 每次取数据的分片量
        :param page: 从第几页开始取数据
        :param end_date: YY-MM-DD
        :param start_date: YY-MM-DD
        :return:
        """
        return self.request(
            method="post",
            url="https://yunxiao.xiaogj.com/api/cs-pc-report/cs-report/reports/findOrderItemAll/page",
            json={
                "_t_": timestamp(),
                "page": {"pageNum": page, "pageSize": size},
                "campusIds": self.campus,
                "studentIds": [],
                "cardName": "",
                "productTypeList": [],
                "productName": "",
                "orderFlagIds": [],
                "orderTypeAllList": list(order_types),
                "orderStatusAllList": list(order_status),
                "orderNo": "",
                "startTime": start_date,
                "endTime": end_date,
                "creatorIds": [],
                "comeFroms": [],
                "phone": ""
            }
        )

    # 查询收支明细-支出
    @loop_pages("paymentRefundDtos")
    def payments_query_refund(self, page, size, startdate: str = "", enddate: str = ""):
        """
        列出指定操作日期范围的所有订单记录
        :param size: 每次取数据的分片量
        :param page: 从第几页开始取数据
        :param enddate: YY-MM-DD
        :param startdate: YY-MM-DD
        :return:
        """
        return self.request(
            method="post",
            url="https://yunxiao.xiaogj.com/api/cs-pc-report/cs-report/reports/findPaymentRefundList",
            json={
                "_t_": timestamp(),
                "page": {"pageNum": page, "pageSize": size},
                "campusIds": self.campus,
                "refundFinishStartTime": startdate,
                "refundFinishEndTime": enddate,
                "orderNo": "",
                "paymentAccountCustomIds": [],
                "cardName": "",
                "refundMethodList": [],
                "confirmStatusList": [],
                "phone": ""
            }
        )

    # 查询收支明细-收入
    @loop_pages("paymentDetailDtos")
    def payments_query(self, page, size, startdate: str = "", enddate: str = "", revenue_type: int = "",
                       order_status: int = ""):
        """
        查询指定操作日期范围的所有收入
        :param order_status: 订单状态： **1** 已付款 **4** 已作废
        :param revenue_type: 收入类型： **0** 收费 **1** 转课
        :param size: 分页查询，每页数量
        :param page: 分页查询，起始页码，应设为 0
        :param enddate: YY-MM-DD
        :param startdate: YY-MM-DD
        :return:
        """
        return self.request(
            method="post",
            url="https://yunxiao.xiaogj.com/api/cs-pc-report/cs-report/reports/findPaymentList",
            json={
                "_t_": timestamp(),
                "page": {"pageNum": page, "pageSize": size},
                "campusIds": self.campus,
                "payStartTime": startdate,
                "payEndTime": enddate,
                "revenueType": revenue_type,
                "payType": "",
                "groupNo": "",
                "btransactionId": "",
                "cardName": "",
                "orderNo": "",
                "orderStatus": order_status,
                "orderStartTime": "",
                "orderEndTime": "",
                "paymentAccountCustomIds": [],
                "confirmStatusList": [],
                "phone": ""
            }
        )

    # 查询收支明细-账户明细
    @loop_pages()
    def payments_query_record(self, page, size, startdate: str = "", enddate: str = "",
                              display_invalid_order: bool = True, types: tuple = ()):
        """
        列出指定操作日期范围的所有订单记录
        :param size: 分页查询，每页数量
        :param page: 分页查询，起始页码
        :param types: 收支类型：**0** 收费 **1** 转课 **2** 退费
        :param display_invalid_order: 是否展示已作废订单
        :param enddate: YY-MM-DD
        :param startdate: YY-MM-DD
        :return:
        """

        return self.request(
            method="post",
            url="https://yunxiao.xiaogj.com/api/cs-pc-report/cs-report/reports/findPaymentAccountCustomRecord",
            json={
                "_t_": timestamp(),
                "paymentAccountCustomIds": [],
                "page": {"pageNum": page, "pageSize": size},
                "campusIds": self.campus,
                "startTime": startdate,
                "endTime": enddate,
                "displayInvalidOrder": display_invalid_order,
                "typeList": list(types)
            }
        )

    # 取得收据信息
    def payments_query_receipt(self, orderinfo_id: int, payment_groupid: int) -> dict:
        """
        取得收据信息。
        :param orderinfo_id: 订单 ID
        :param payment_groupid: 支付 ID
        :return:
        """
        return self.request(
            method="get",
            url="https://yunxiao.xiaogj.com/api/cs-pc-edu/public/receipt/findReceipt",
            params={
                "orderInfoId": orderinfo_id,
                "paymentGroupId": payment_groupid,
                "_t_": timestamp()
            }
        )["data"]

    # 查询签单业绩
    @loop_pages("achievementBelongerDetailItems")
    def payments_query_achievements_datarange(self, page, size, startdate: str = "", enddate: str = "",
                                              teacher_ids: tuple = (), order_types: tuple = ()):
        """
        查询业绩归属，根据日期
        :param order_types: **0** 收费 **1** 转课 **2** 退费 **3** 结转
        :param teacher_ids:
        :param size: 分页查询，每页数量
        :param page: 分页查询，起始页码
        :param enddate: YY-MM-DD
        :param startdate: YY-MM-DD
        :return:
        """

        return self.request(
            method="post",
            url="https://yunxiao.xiaogj.com/api/cs-pc-report/cs-report/reports/findAchievementBelongerDetail",
            json={
                "_t_": timestamp(),
                "page": {"pageNum": page, "pageSize": size},
                "campusIds": self.campus,
                "startDate": startdate,
                "endDate": enddate,
                "orderFlagIds": [],
                "orderTypes": list(order_types),
                "productTypes": [],
                "orderNo": "",
                "productName": "",
                "studentId": "",
                "teacherIds": list(teacher_ids)
            }
        )

    # 查询招生来源
    def comefroms_query(self):
        return self.request(
            method="get",
            url=f"https://yunxiao.xiaogj.com/api/cs-crm/customField/get",
            params={"_t_": timestamp(), "customFieldId": "26118419"}
        )["data"]["selectItemList"]
