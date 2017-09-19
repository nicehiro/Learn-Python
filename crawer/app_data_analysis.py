#!/usr/bin/python
# -*- coding:utf-8 -*-


import requests
import datetime


def get_right_time(time):
    if time < 10:
        return '0' + str(time)
    else:
        return time

def get_time():
    now = datetime.datetime.now()
    hour = get_right_time(now.hour)
    minute = get_right_time(now.minute)
    second = get_right_time(now.second)
    return hour, minute, second


class data_analysis():

    __Author__ = 'hiro'
    
    def __init__(self):
        self.da_session = requests.Session()
        self.host = 'http://stu.xinxi.zstu.edu.cn/WebReport/ReportServer'
        self.device = 'android'
        self.device_name = 'OnePlus+ONE+A2001'
        self.password = '181732'
        self.username = '2014332860054'
        self.macaddress = '97F9B86F0663598B9597B87C'
        self.lon = '120.359624'
        self.lat = '30.31706'
        self.login_home_title = ('%25E6%259A%2591%25E6%259C%259F%25E7%25AD'
                                 '%25BE%25E5%2588%25B0')
        self.login_class_title = ('%25E8%2580%2583%25E5%258B%25A4%25E7%25AD'
                                  '%25BE%25E5%2588%25B0')
        self.sign_in_home_id = '2724'
        self.sign_in_class_id = '2663'
        self.login()
        print('Login Success!')
        

    def login(self):
        login_param = ('__device__={}&__mobileapp__=true&'
                       'cmd=login&devname={}&'
                       'fr_password={}&fr_remember=true&'
                       'fr_username={}&fspassword={}'
                       '&fsremember=true&fsusername={}&'
                       'isMobile=yes&'
                       'macaddress={}&'
                       'op=fs_mobile_main'
                       .format(self.device, self.device_name,
                               self.password, self.username,
                               self.password, self.username,
                               self.macaddress))

        response = self.da_session.post(self.host+'?'+login_param)
        return response

    def get_session_cookie(self, response):
        return response.cookies

    def get_sign_session_id(self, sign_in_id):
        param = ('__device__={}&__mobileapp__=true&cmd=entry_report&'
                 'id={}&isMobile=yes&op=fs_main'.format(self.device,
                                                        sign_in_id))

        response = self.da_session.post(self.host+'?'+param)
        return response.json()['sessionid']

    def signin(self, title, sessionid, hour, minute, second):
        param = ('__device__={}&__mobileapp__=true&isMobile=yes&'
                 'op=closesessionid&sessionID={}'.format(self.device, sessionid))

        response = self.da_session.post(self.host+'?'+param)

        param2 = ('timetype={}&title={}&time={}%253A{}%253A{}&'
                  'jingdu={}&weidu={}&reportlet=2017%'
                  '252Fbaodaocheck_enter.cpt&op=write&__replaceview__=true'
                  '&__device__={}&__mobileapp__=true&isMobile=yes'
                  .format(0, title, hour, minute, second,
                          self.lon, self.lat, self.device))

        response2 = self.da_session.post(self.host+'?'+param2)
        return response2.json()['sessionid']

    def commit(self, sign_sessionid):
        param = ('__device__={}&__mobileapp__=true&cmd=write_verify&'
                 'isMobile=yes&op=fr_write&reportXML=%3C%3Fxml+version%3D'
                 '%221.0%22+encoding%3D%22UTF-8%22%3F%3E%3CWorkBook%3E%3CVersion'
                 '%3E6.5%3C%2FVersion%3E%3CReport+class%3D%22com.fr.report.'
                 'WorkSheet%22+name%3D%220%22%3E%3CCellElementList%3E%3C%2FC'
                 'ellElementList%3E%3C%2FReport%3E%3C%2FWorkBook%3E&'
                 'sessionID={}'.format(self.device, sign_sessionid))
        response = self.da_session.post(self.host+'?'+param)
        successp = response.json()[1]['fr_verifyinfo']['success']
        msg = self.get_err_msg(response, successp)
        return successp, msg

    def get_err_msg(self, response, successp):
        if successp is False:
            msg = response.json()[0]['message']
            msg = 'Log: ' + msg
        else:
            msg = ''
        return msg

    def close_session(self, sessionid):
        param = ('__device__={}&__mobileapp__=true&isMobile=yes&'
                 'op=closesessionid&sessionID={}'.format(self.device, sessionid))

        self.da_session.post(self.host+'?'+param)
        self.da_session.close()

    
    def sign_in(self, title, sign_in_id):
        # cookies = self.get_session_cookie(resp)
        # print('Get Cookies Success!')
        sessionid = da.get_sign_session_id(sign_in_id)
        print('Get Main SessionID Success!')
        hour, minute, second = get_time()
        print('Get Current Time Success!')
        sign_sessionid = da.signin(title, sessionid, hour, minute, second)
        print('Get SignIn SessionID Success!')
        successp, msg = da.commit(sign_sessionid)
        print('SignIn Statu: ' + str(successp))
        print(msg)
        da.close_session(sessionid)

    def sign_in_home(self):
        print('Sign in Home:')
        self.sign_in(self.login_home_title, self.sign_in_home_id)
        f = open('test', 'w')
        f.write('test sucess')

    def sign_in_class(self):
        print('Sign in Class:')
        self.sign_in(self.login_class_title, self.sign_in_class_id)
        f = open('test', 'w')
        f.write('test sucess')


if __name__ == '__main__':
    da = data_analysis()
    hour, minute, second = get_time()

    if hour > 21:
        da.sign_in_home()

    da.sign_in_class()
