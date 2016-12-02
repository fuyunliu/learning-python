# -*- coding: utf-8 -*-

import random
import requests
import pymysql.cursors
from bs4 import BeautifulSoup
from headers import agents


conn = pymysql.connect(
    host='localhost',
    user='root',
    password='root',
    db='test',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor)


class GatherXiCi(object):

    def __init__(self):
        self.conn = conn
        self.session = requests.Session()
        self.session.headers['user-agent'] = random.choice(agents)
        self.list_url = "http://www.xicidaili.com/nn/{page}"
        self.test_url = "http://httpbin.org/ip"
        self.insert_sql = """insert into proxy_ip (ip, port, area, type,
            protocol) values (%s, %s, %s, %s, %s)"""

    def parse_list(self):
        for p in range(1, 11):
            try:
                url = self.list_url.format(page=p)
                r = self.session.get(url)
                soup = BeautifulSoup(r.text, 'lxml')
                trs = soup.select('#ip_list tr')
                values = self.parse_detail(trs)
                self.save_data(values)
                print("解析第【%s】页完成！" % p)
            except Exception as e:
                print(str(e))
                print("解析第【%s】页出错..." % p)

    def parse_detail(self, trs):
        values = []
        del trs[0]
        for tr in trs:
            tds = tr('td')
            one = tuple(td.get_text(strip=True) for td in tds[1:6])
            if self.test_ip(one):
                values.append(one)
        return values

    def save_data(self, values):
        for one in values:
            try:
                with self.conn.cursor() as cursor:
                    cursor.execute(self.insert_sql, one)
                self.conn.commit()
                print("保存数据成功！")
            except Exception as e:
                print(str(e))

    def test_ip(self, one):
        ip, port = one[:2]
        proxies = {'http': 'http://{0}:{1}'.format(*one)}
        try:
            r = requests.get(self.test_url, proxies=proxies, timeout=5)
            origin_ip = r.json().get('origin')
            if origin_ip == ip:
                print("%s:%s is ok!" % (ip, port))
                return True
            else:
                print("%s:%s is not anonymous!" % (ip, port))
                return False
        except:
            print("connecting %s:%s failed!" % (ip, port))
            return False

    def control(self):
        self.parse_list()


if __name__ == '__main__':
    p = GatherXiCi()
    p.control()
