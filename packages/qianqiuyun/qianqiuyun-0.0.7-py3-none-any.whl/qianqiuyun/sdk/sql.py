#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pymysql
from qianqiuyun.sdk import sqlhelper
from qianqiuyun.sdk.util import get_env_ns

def get_db(ns=None):
    ns = get_env_ns(ns)
    db = pymysql.connect(host='mysql.%s.svc.cluster.local' % ns, port=3306, user='root', passwd='qianqiu@#20222', db='oadb_cvxa3663')
    return db

class DB:
   def __init__(self, domain='cvxa3663'):
      self.pooleddb = sqlhelper.pooledDBDict[domain]
   
   def exec(self, sql, args=[]):
      if sql.lower().strip().index("select") >= 0:
         return sqlhelper.fetch_all(self.pooleddb, sql, args)
      else:
         return sqlhelper.exec(self.pooleddb, sql, args)