# coding: utf-8
"""
Train tickets query via command-line.

Usage:
    tickets [-gdtkz] <from> <to> <date>

Options:
    -h,--help   显示帮助菜单
    -g          高铁
    -d          动车
    -t          特快
    -k          快速
    -z          直达

Example:
    tickets beiging shanghai 2016-08-05
"""
from docopt import docopt
from stations import stations
import requests

def cli():
    arguments = docopt(__doc__)
    from_station = stations.get(arguments['<from>'].encode()).decode()
    print(from_station)
    to_station = stations.get(arguments['<to>'].encode()).decode()
    print(to_station)
    date = arguments['<date>']

    url = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'.format(date, from_station, to_station)

    r = requests.get(url, verify=False)
    rows = r.json()['data']['result']

if __name__ == '__main__':
    cli()
