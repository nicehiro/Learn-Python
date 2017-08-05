from prettytable import PrettyTable

'''
网站数据分析：

请求：https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=2017-07-22&leftTicketDTO.from_station=HGH&leftTicketDTO.to_station=SHH&purpose_codes=ADULT

返回每条数据的 json 格式如下：
"5aNJxJ5gUK7eMjJilxZnTvo7N9xYmEwjHq2JflUlR4CO3Nc8K%2F9QEpmwm9dJ1gy%2BUFXf9fNsasN0%0AwpFqOx0gTr4y8jXrVOJR%2BatYIX%2B8zEXSAtbXHP7q5Cj6HFBPsvmR9srNZ%2Fgsv6A759z%2FmTyhclza%0AxINa0UIkog0P8RbePcRoZCOXJjGCNPweIYvpPvQ7XX9A19RDCbv93EkUiFPDB6SKkta4XFON%2F%2Bo2%0AhrOmVVtcJMMJ|预订|62000G236606|G2366|SYQ|AOH|HGH|AOH|22:00|22:52|00:52|Y|Aq0FnOzdxHAtMmPiKVLRJQU8CT6HB15ImXL8QbiU8kXyxsna|20170722|3|Q7|17|19|1|0|||||||||||有|10|9||O0M090|OM9"
根据'|'split之后：
['YQlSHJAe9Aebxf8dVFJ0GI3XKzcaapvvTP436ofFsqZRCf8YuFixVttAatRpeKVvKTNIYg79upy9%0AyR8CmFvCepw0%2FbN0ZgaY55ViBw6Bl%2BlPo10foXRVTZok9FD4O0lJNeDGFnywuFVkh8hQ4buaN60N%0AILiKx5BLdbXwdfcDL9ckOM4%2FirmZz3YOLCnqIHUqhq0bGEBrcN9wgQdugITZQg5TRmtIUQxafHCB%0A6f%2FeQtwIogD%2BbgK4Wg%3D%3D', '预订', '560000Z28212', 'Z282', 'HZH', 'BTC', 'HZH', 'SNH', '17:04', '18:54', '01:50', 'Y', '9bzgPFK%2BzaybDeEOM7%2Bo2moflh9fdhuXmUp1igiHPNKisLF3lBpP%2Boi7J%2FM%3D', '20170722', '3', 'H6', '01', '04', '0', '0', '', '', '', '12', '', '', '无', '', '有', '无', '', '', '', '', '10401030', '1413']

从 list 里拿我们需要的数据
| |高级软卧| |软卧| | |无座| |硬卧|硬座|二等座|一等座|商务座|动卧|

利用 dict 搞定 switch 的功能
'''

class TrainCollection(object):
    header = 'Train Station Time Duration ShangWu First Second SoftSleep HardSleep HardSit NoSit'.split()

    def __init__(self, rows, gao, dong, te, kuai, zhi):
        self.rows = rows
        self.gao = gao
        self.dong = dong
        self.te = te
        self.kuai = kuai
        self.zhi = zhi
        self.values = {
            'G': self.gao,
            'D': self.dong,
            'T': self.te,
            'K': self.kuai,
            'Z': self.zhi
        }
        print(self.values)

    def colored(self, color, text):
        table = {
            'red': '\033[91m',
            'green': '\033[92m',
            'nc': '\033[0'
        }
        cv = table.get(color)
        nc = table.get('nc')
        return ''.join([cv, text])

    '''
    得到车次类型
    '''
    def type(self, checi):
        return checi[0]

    '''
    是否有参数
    '''
    def hasparams(self):
        if not self.gao and not self.dong and not self.te and not self.kuai and not self.zhi:
            return False 
        else:
            return True

    @property
    def trains(self):
        for row in self.rows:
            rowlist = row.split('|')
            if self.hasparams() and not self.values.get(self.type(rowlist[3])):
                continue
            train = [
                rowlist[3],
                "\n".join([self.colored('green', rowlist[4]),
                           self.colored('red', rowlist[5])]),
                "\n".join([self.colored('green', rowlist[8]),
                           self.colored('red', rowlist[9])]),
                rowlist[10],
                rowlist[-4],
                rowlist[-5],
                rowlist[-6],
                rowlist[-13],
                rowlist[-8],
                rowlist[-7],
                rowlist[-10]
            ]
            yield train

    def pretty_print(self):
        pt = PrettyTable()
        pt._set_field_names(self.header)
        for train in self.trains:
            pt.add_row(train)
        print(pt)
