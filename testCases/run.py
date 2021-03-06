#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'BIN'
import os,sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import unittest,requests,ddt
from common import read_excel,config,write_excel,login
from common.send_requests import *
from common import new_report,send_mail
if os.path.exists(config.TEST_RESULT):  # 如果文件存在
    os.remove(config.TEST_RESULT)
else:
    print("测试结果文件不存在")
if os.path.exists(config.TEST_TOKEN):  # 如果文件存在
    os.remove(config.TEST_TOKEN)
else:
    print("测试token文件不存在")
login.Login().adminlogin()
testDATA =read_excel.ReadExcel(config.TEST_CONFIG,"Sheet1").read_Excel()
@ddt.ddt
class API_demo(unittest.TestCase):
    def setUp(self):
        self.s = requests.session()
    @ddt.data(*testDATA)
    def test_api(self,data):
        rowNum = int(data['ID'].split("_")[1])
        print("******* 正在执行用例 ->{0} *********".format(data['模块']))
        print("请求方式: {0}，请求URL: {1}".format(data['method'],data['url']))
        print("请求头信息: {0}".format(data['headers']))
        print("请求参数: {0}".format(data['body']))
        print("post请求body类型为：{0} ,body内容为：{1}".format(data['type'], data['body']))
        # 发送请求
        re = SendRequests.sendRequests(self,self.s,data)
        fail = "测试没有通过，报错了"
        try:
            re.json()["message"] == "成功"
        except AttributeError as e:
            write_excel.WriteExcel(config.TEST_RESULT).write_data(rowNum+1,"fail")
        # # 获取服务端返回的值
        else:
            write_excel.WriteExcel(config.TEST_RESULT).write_data(rowNum + 1, "pass")
        # print(self.result)
    def tearDown(self):
        pass
if __name__=='__main__':
    API_demo().test_api()
    send_mail.SEND_MAIL().send_mail('2514095967@qq.com', new_report.new_report(config.TEST_REPORT))
