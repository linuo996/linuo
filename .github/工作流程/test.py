@@ -0,0 +1,95 @@
#!/usr/bin/python
# -*-coding: UTF-8 -*-//
# coding:utf-8
from selenium import webdriver
# 创建Firefox对象
# driver = webdriver.Firefox()
driver = webdriver.Chrome()
driver.get('https://cn.bing.com/')
driver.quit()


class Get_ES_Data(object):
    def __init__(self):
        self.headers = {'content-type': 'application/json'}
        self.payload2 = {
            "access_token": "xxxxxxxxxxxxxxxxxxxxxxxxxx",
            "request_body": {

            }
        }

        self.url = r"http://xxxxxxxxxxxxxxxxxxxxxxxxxx/xxxxxxxxxxx"
        self.re = requests.post(self.url, data=json.dumps(self.payload2), headers=self.headers)
        self.r = json.loads(self.re.text)

        self.db1 = MySQLdb.connect(
            host="localhost",
            db="",
            user="root",
            passwd="",
            port=3306,
            charset='utf8'
        )

        self.cur2 = self.db1.cursor()
        self.cur2.execute('drop table if exists table_deploy')

        self.sql1 = """create table table_deploy(id INT (11) UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT ,appid int not null
                                    ,timestamp VARCHAR(50)
                                  ,deploy_id INT
                                  )"""

        self.cur2.execute(self.sql1)
        self.db1.commit()

        self.insertTable = 'table_deploy'

    def inserttable(self, insertTable, insertId, insertTimestamp, insertDeploy_id):
        insertContentSql = "INSERT INTO " + insertTable + "(appid,timestamp,deploy_id)VALUES(%s,%s,%s)"
        DB_insert = self.db1
        cursor_insert = DB_insert.cursor()
        cursor_insert.execute(insertContentSql, (insertId, insertTimestamp, insertDeploy_id))
        DB_insert.commit()
        print 'inert contents to  ' + insertTable + ' successfully'

    def get_es(self):
        now_time = int(time.time())  # 当前时间的时间戳
        hoursAgo = (datetime.datetime.now() - datetime.timedelta(hours=8) - datetime.timedelta(hours=0.1))  # 0.1小时之前的时间
        hoursAgo_timeStamp = int(time.mktime(hoursAgo.timetuple()))  # 0.1小时之前的时间戳
        f = open('xxxxxxxxxx', 'w+')
        for i in range(len(self.r['hits']['hits'])):
            app_id = self.r['hits']['hits'][i]['_source']['app_id']
            timestamp = self.r['hits']['hits'][i]['_source']['@timestamp'].replace('Z', '').replace('T', ' ').replace(
                '.000', '')[:16]
            timeArray = time.strptime(timestamp, "%Y-%m-%d %H:%M")
            t = int(time.mktime(timeArray))  # 转化为时间戳
            if (t > hoursAgo_timeStamp and t < now_time):
                timeArray = time.strptime(timestamp, "%Y-%m-%d %H:%M")
                timestamp1 = \
                    self.r['hits']['hits'][i]['_source']['@timestamp'].replace('Z', '').replace('T', '').replace('.000',
                                                                                                                 '').replace(
                        '-', '').split(':')[0]
                temptime = time.strptime(timestamp1, "%Y%m%d%H")
                timeStamp_1 = int(time.mktime(temptime))
                dateArray_1 = datetime.datetime.utcfromtimestamp(timeStamp_1)
                timestamp1 = dateArray_1 + datetime.timedelta(hours=16)
                timestamp1 = timestamp1.strftime("%Y%m%d%H")
                timestamp2 = \
                    self.r['hits']['hits'][i]['_source']['@timestamp'].replace('Z', '').replace('T', '').replace('.000',
                                                                                                                 '').replace(
                        '-',
                        '').split(
                        ':')[1]
                timestamp3 = timestamp1 + timestamp2
                deploy_id = self.r['hits']['hits'][i]['_source']['deploy_id']
                self.inserttable(self.insertTable, app_id, timestamp1, deploy_id)
                f.write(str(app_id))
                f.write('\t')
                f.write(str(timestamp3))
                f.write('\t')
                f.write(str(deploy_id))
                f.write('\n')


a = Get_ES_Data()
a.get_es()

#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import json
import time
import xmltodict
import numpy
import MySQLdb
import time
import datetime


class RqAndRs(object):
    def __init__(self):
        self.hours = ["00", "01", "02", "03", "04", "05", "06", "07", "08",
                      "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
                      "21", "22", "23"]
        self.db2 = MySQLdb.connect(
            host="",
            db="",
            user="",
            passwd="",
            port=,
            charset='utf8'
        )
        self.cur2 = self.db2.cursor()

        self.insertTable = 'cat_respondse_time'

    def get_app1(self):
        sql3 = "select * from all_appids"
        cur3 = self.db2.cursor()
        cur3.execute(sql3)
        alldata = cur3.fetchall()
        app1 = []
        if alldata:
            for app in alldata:
                app1.append(app[0])
        return app1

    def inserttable(self, insertTable, insertId, insertDate, insertTime, insertCount, insertFail):
        insertContentSql = "INSERT INTO " + insertTable + "(appid1,time,respondse,request,failcount)VALUES(%s,%s,%s,%s,%s)"
        DB_insert = self.db2
        cursor_insert = DB_insert.cursor()
        cursor_insert.execute(insertContentSql, (insertId, insertDate, insertTime, insertCount, insertFail))
        DB_insert.commit()

    def get_daa(self):
            aaa = self.get_app1()
            timeStamp_1 = int(time.time())
            dateArray_1 = datetime.datetime.utcfromtimestamp(timeStamp_1)
            dayAgo1 = dateArray_1 + datetime.timedelta(hours =  8) - datetime.timedelta(days = 1)
            timeStamp1 = int(time.mktime(dayAgo1.timetuple()))
            otherStyleTime1 = dayAgo1.strftime("%Y%m%d%H%M%S")
            otherStyleTime = otherStyleTime1[:8]
            for a1 in set(aaa):
                print 'begin load' + str(a1)
                for q in self.hours:
                    url = r'http://xxx=%s&xx=%s%s&type=URL&forceDownload=xml' % (
                        str(a1), otherStyleTime, q)
                    try:
                        r = requests.get(url)
                        data = r.text
                        doc = xmltodict.parse(data)
                        appid = doc[u'transaction'][u'report'][u'@domain']
                        start = doc[u'transaction'][u'report'][u'@startTime']
                        start = start.replace('-', '').replace(' ', '').replace(':', '')
                        stime = start[:12]
                        for i in range(len(doc[u'transaction'][u'report'][u'machine'][u'type'][u'name'])):
                            if type(doc[u'transaction'][u'report'][u'machine'][u'type'][u'name']) == list:
                                adoc = doc[u'transaction'][u'report'][u'machine'][u'type'][u'name'][i][u'@id']
                            else:
                                adoc = doc[u'transaction'][u'report'][u'machine'][u'type'][u'name']
                            if adoc == u'All':
                                a = doc[u'transaction'][u'report'][u'machine'][u'type'][u'name'][i][u'range']
                                for j in range(len(a)):
                                    Appid = appid
                                    dtime = a[j][u'@avg']
                                    dateT = int(str(stime)) + int(a[j][u'@value'])
                                    dateT = str(dateT)
                                    timeArray = time.strptime(dateT, "%Y%m%d%H%M")
                                    timeStamp = int(time.mktime(timeArray))
                                    count = a[j][u'@count']
                                    fail = a[j][u'@fails']
                                    self.inserttable(self.insertTable, Appid, timeStamp, dtime, count, fail)
                    except:
                        pass
 9  cat_dep_zidong.py
@@ -0,0 +1,9 @@
#!/usr/bin/env python
# -*- coding:utf-8 -*-

from catdeppy import *

while True:
    if time.ctime()[11:19] == "00:05:00":
        a = catdeppy1()
        a.get_dependency()
 91  catdeppy.py
@@ -0,0 +1,91 @@
#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import time
import xmltodict
import MySQLdb
import datetime


class catdeppy1(object):
    def __init__(self):
        self.db2 = MySQLdb.connect(
            host="",
            db="",
            user="",
            passwd="",
            port=,
            charset='utf8'
        )
        self.hours = ["00", "01", "02", "03", "04", "05", "06", "07", "08",
                      "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
                      "21", "22", "23"]

        self.cur2 = self.db2.cursor()

        self.insertTable = 'cat_dependency_EveryMinute'

    def inserttable(self, insertTable, insertId1, insertId2, insertCount1, insertTime):
        insertContentSql = "REPLACE INTO " + insertTable + "(appid1,appid2,count,time)VALUES(%s,%s,%s,%s)"
        DB_insert = self.db2
        cursor_insert = DB_insert.cursor()
        cursor_insert.execute(insertContentSql, (insertId1, insertId2, insertCount1, insertTime))
        DB_insert.commit()

    def now_ti(self):
        now = int(time.time())
        loc_after = time.localtime(now)
        loc1_after = time.strftime('%Y-%m-%d %H:%M', loc_after)
        datetimeObj_After = datetime.datetime.strptime(loc1_after, "%Y-%m-%d %H:%M")
        now2 = datetimeObj_After - datetime.timedelta(days=1)
        now21 = now2.strftime("%Y%m%d%H%M")[:8]
        return now21

    def get_dependency(self):
        sql3 = "select * from all_appids"
        self.cur2.execute(sql3)
        alldata = self.cur2.fetchall()
        a_now = self.now_ti()
        for app in alldata:
            b = []
            print 'begin load dependency' + str(app)
            for hour in self.hours:
                url = 'http://xxxxxxxxxxdoxxx={}&date={}{}&forceDownload=xml'.format(
                    app[0], a_now, hour)
                try:
                    r = requests.get(url)
                    data = r.text
                    doc = xmltodict.parse(data)
                    for i in range(len(doc['dependency']['report']['segment'])):
                        for j in range(len(doc['dependency']['report']['segment'][i]['dependency'])):
                            time = doc['dependency']['report']['@startTime'].split(' ')[0]
                            if doc['dependency']['report']['segment'][i]['dependency'][j]['@type'] == 'Service':
                                appid2 = doc['dependency']['report']['@domain']
                                appid1 = doc['dependency']['report']['segment'][i]['dependency'][j]['@target']
                                count = doc['dependency']['report']['segment'][i]['dependency'][j]['@total-count']
                            elif 'Call' in doc['dependency']['report']['segment'][i]['dependency'][j]['@type']:
                                appid2 = doc['dependency']['report']['segment'][i]['dependency'][j]['@target']
                                appid1 = doc['dependency']['report']['@domain']
                                count = doc['dependency']['report']['segment'][i]['dependency'][j]['@total-count']
                            g = [appid1, appid2, count, time]
                            b.append(g)
                except:
                    pass
            try:
                c = [(0, 0, 0)]
                for n in b:
                    for i in range(0, len(c)):
                        if n[0] == c[i][0] and n[1] == c[i][1]:
                            c[i][2] = int(c[i][2]) + int(n[2])
                            break
                        elif i == len(c) - 1:
                            c.append(n)
                            break

                for i in range(1, len(c)):
                    self.inserttable(self.insertTable, c[i][0], c[i][1], c[i][2], c[i][3])
            except:
                pass
        self.cur2.close()
        self.db2.close()
 115  get_docker_message.py
@@ -0,0 +1,115 @@
# -*- coding: utf-8 -*-
import requests
import json
import traceback
import MySQLdb
import datetime
import time


class GETVERSION(object):
    def __init__(self):
        self.db2 = MySQLdb.connect(
            host="",
            db="",
            user="",
            passwd="",
            port=3306,
            charset='UTF8'
        )
        self.cur2 = self.db2.cursor()
        self.cur2.execute('drop table if exists vm_version_difference')

        self.sql2 = """create table vm_version_difference(id INT (11) UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,ci_c varchar(20) not null
                                 ,ip varchar(20)
                                ,env VARCHAR(20)
                              ,pd VARCHAR (20)
                              ,appid VARCHAR (20)
                              ,deploy_time VARCHAR (20)
                              ,prod_deploy_time VARCHAR (20)
                              ,version_name VARCHAR (500)
                              ,prod_version_name VARCHAR (500)
                              ,time_difference VARCHAR (20)
                              ,UNIQUE(appid)
                              )"""
        self.cur2.execute(self.sql2)
        self.db2.commit()
        self.insertTable = 'vm_version_difference'

    def inserttable(self, insertTable, insertci_c, insertip, insertenv, insertpd, insertappid, insertdeploy_time,
                    insertprod_deploy_time, insertversion_name, insertprod_version_name, inserttime_difference):
        insertContentSql = "REPLACE INTO " + insertTable + "(ci_c,ip,env,pd,appid,deploy_time,prod_deploy_time,version_name,prod_version_name,time_difference)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        DB_insert = self.db2
        cursor_insert = DB_insert.cursor()
        cursor_insert.execute(insertContentSql, (
        insertci_c, insertip, insertenv, insertpd, insertappid, insertdeploy_time, insertprod_deploy_time,
        insertversion_name, insertprod_version_name, inserttime_difference))
        DB_insert.commit()
        print 'inert contents to  ' + insertTable + ' successfully'

    def get_version_message(self):
        cur6 = self.db2.cursor()
        sql3 = "select * from vm_all_server WHERE role = 'DOCKER'"
        cur6.execute(sql3)
        alldata = cur6.fetchall()
        ci_list = []
        ci_tuple = (0, 0, 0, 0)
        if alldata:
            for ci in alldata:
                ci_tuple = (ci[2], ci[9], ci[1], ci[13])
                ci_list.append(ci_tuple)

        for ci in ci_list:
            url = 'http://xxxxxxx/{}/xxx/?xxx={}&page=1&page_size=8&searchs'.format(
                ci[0], ci[1].lower())
            a_content = requests.get(url)
            aa = a_content.content
            a_json = json.loads(aa)
            application = []
            if a_json.has_key('results'):
                for i in range(len(a_json['results'])):
                    application.append(a_json['results'][i]['id'])

                print 'application:' + str(application)

                for app in set(application):
                    url1 = 'http://xxxxxxxxxx/{}/groups/?env={}'.format(app, ci[1])
                    url2 = 'http://xxxxxxxxxxx/{}/tars_prod_groups/'.format(app)
                    a_content1 = requests.get(url1)
                    aa1 = a_content1.content
                    a_json1 = json.loads(aa1)
                    a_content2 = requests.get(url2) 
                    aa2 = a_content2.content
                    a_json2 = json.loads(aa2)
                    appid = app
                    ci_c = ci[0]
                    ip = ci[2]
                    pd = ci[3]
                    if a_json1[0]['latest_release'] != None:
                        version_name = a_json1[0]['latest_release']['package']['name']
                        env = a_json1[0]['latest_release']['package']['env']
                        deploy_time = a_json1[0]['latest_release']['created_at']
                    else:
                        version_name = None
                        env = None
                        deploy_time = None
                    if len(a_json2) != 0:
                        if a_json2[0]['groups'][0]['latest_deployment'].has_key('package'):
                            prod_version_name = a_json2[0]['groups'][0]['latest_deployment']['package']['name']
                            prod_deploy_time = a_json2[0]['groups'][0]['latest_deployment']['created_at']
                        else:
                            prod_version_name = None
                            prod_deploy_time = None
                    if prod_deploy_time and deploy_time != None:
                        time_difference = datetime.datetime.strptime(prod_deploy_time,
                                                                     '%Y-%m-%d %H:%M:%S') - datetime.datetime.strptime(
                            deploy_time, '%Y-%m-%d %H:%M:%S')
                    else:
                        time_difference = None
                    print prod_version_name
                    self.inserttable(self.insertTable, ci_c, ip, env, pd, appid, deploy_time, prod_deploy_time,
                                     version_name, prod_version_name, time_difference)
        self.db2.close()

a = GETVERSION(
            url = 'http://xxxxxxxxxxxxxxxxxx/{}/xxx/?xxx={}&page=1&page_size=8&searchs'.format(
                ci[0], ci[1].lower())
            cii = ci[0]
            a_content = requests.get(url)
            aa = a_content.content
            a_json = json.loads(aa)
            application = []
            if a_json.has_key('results'):
                for i in range(len(a_json['results'])):
                    application.append(a_json['results'][i]['id'])

                print 'application:' + str(application)

                d0 = []
                for app in set(application):
                    d1 = {}
                    url1 = 'http://xxxxxxx/{}/groups/?env={}'.format(app, ci[1])
                    url2 = 'http://xxxxxxxx/{}/tars_prod_groups/'.format(app)
                    a_content1 = reques
                        d1['pd'] = pd
                        d1['appid'] = appid
                        d1['deploy_time'] = deploy_time
                        d1['prod_deploy_time'] = prod_deploy_time
                        d1['version_name'] = version_name
                        d1['prod_version_name'] = prod_version_name
                        d1['time_difference'] = str(tiwme_difference)
                        d0.append(d1)
                d['content'] = d0
                dd0.append(d)
        dd['ci'] = cii
        dd['content'] = dd0
        print json.dumps(dd)

a = GETVERSION()
a.get_version_message()
 7  get_responsedate.py
@@ -0,0 +1,7 @@
# -*- coding: utf-8 -*-

from appid_response import *
while True:
    if time.ctime()[11:19]=="00:45:00":
        a = RqAndRs()   import
