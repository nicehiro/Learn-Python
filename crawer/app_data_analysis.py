#!/usr/bin/python
# -*- coding:utf-8 -*-


import requests

class data_analysis():

    __Author__ = 'hiro'
    
    def __init__(self):
        self.da_session = requests.Session()
        self.host = 'http://stu.xinxi.zstu.edu.cn/WebReport/ReportServer'

    def login(self):
        login_param = ('__device__=android&__mobileapp__=true&'
                       'cmd=login&devname=OnePlus+ONE+A2001&'
                       'fr_password=181732&fr_remember=true&'
                       'fr_username=2014332860054&fspassword=181732'
                       '&fsremember=true&fsusername=2014332860054&'
                       'isMobile=yes&'
                       'macaddress=97F9B86F0663598B9597B87C&'
                       'op=fs_mobile_main')

        response = self.da_session.post(self.host+'?'+login_param)
        return response

    def get_session_cookie(self, response):
        return response.cookies

    def get_sign_session_id(self):
        param = ('__device__=android&__mobileapp__=true&cmd=entry_report&'
                 'id=2724&isMobile=yes&op=fs_main')

        response = self.da_session.post(self.host+'?'+param)
        return response.json()['sessionid']

    def signin(self, sessionid, hour, minute, second):
        param = ('__device__=android&__mobileapp__=true&isMobile=yes&'
                 'op=closesessionid&sessionID={}'.format(sessionid))

        response = self.da_session.post(self.host+'?'+param)

        param2 = ('timetype=1&title=%25E6%259A%2591%25E6%259C%259F%25E7%25AD'
                  '%25BE%25E5%2588%25B0&time={}%253A{}%253A{}&'
                  'jingdu=120.359624&weidu=30.31706&reportlet=2017%'
                  '252Fbaodaocheck_enter.cpt&op=write&__replaceview__=true'
                  .format(hour, minute, second))

        response2 = self.da_session.post(self.host+'?'+param2)
        return response2

    def close_session(self, sessionid):
        param = ('__device__=android&__mobileapp__=true&isMobile=yes&'
                 'op=closesessionid&sessionID={}'.format(sessionid))

        self.da_session.post(self.host+'?'+param)
        self.da_session.close()


if __name__ == '__main__':
    da = data_analysis()
    resp = da.login()
    cookies = da.get_session_cookie(resp)
    sessionid = da.get_sign_session_id()
    da.signin(sessionid, 21, 40, 34)
    da.close_session(sessionid)
