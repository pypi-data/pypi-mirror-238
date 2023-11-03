#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pymysql
from qianqiuyun.sdk import util

pooledDBDict = {}
dbhost = util.get_env('ENV_DB_HOST', 'mysql.' + util.get_env('ENV_QIANQIUYUN_NS', "qianqiuyun"))
dbport = int(util.get_env("ENV_DB_PORT", "3306"))
dbuser = util.get_env('ENV_DB_USERNAME', 'root')
dbpwd = util.get_env('ENV_DB_PASSWORD', 'qianqiu@#20222')
backenddb = 'ssms-iot-backend'
consoledb = 'ssms-iot-uam'

def connect(pooledDB):
   # 创建连接
   # conn = pymysql.connect(host='192.168.11.38', port=3306, user='root', passwd='apNXgF6RDitFtDQx', db='m2day03db')
   conn = pooledDB.connection()
   # 创建游标
   cursor = conn.cursor(pymysql.cursors.DictCursor)
   return conn,cursor
def close(conn,cursor):
   # 关闭游标
   cursor.close()
   # 关闭连接
   conn.close()
def fetch_one(pooledDB, sql, args=[]):
   conn,cursor = connect(pooledDB)
   # 执行SQL，并返回收影响行数
   effect_row = cursor.execute(sql,args)
   result = cursor.fetchone()
   close(conn,cursor)
   return result
def fetch_all(pooledDB, sql, args=[]):
   conn, cursor = connect(pooledDB)
   # 执行SQL，并返回收影响行数
   cursor.execute(sql,args)
   result = cursor.fetchall()
   close(conn, cursor)
   return result
def insert(pooledDB, sql, args):
   """
   创建数据
   :param sql: 含有占位符的SQL
   :return:
   """
   conn, cursor = connect(pooledDB)
   # 执行SQL，并返回收影响行数
   effect_row = cursor.execute(sql,args)
   conn.commit()
   close(conn, cursor)
def delete(pooledDB, sql, args=[]):
   """
   创建数据
   :param sql: 含有占位符的SQL
   :return:
   """
   conn, cursor = connect(pooledDB)
   # 执行SQL，并返回收影响行数
   effect_row = cursor.execute(sql,args)
   conn.commit()
   close(conn, cursor)
   return effect_row
def update(pooledDB, sql, args):
   conn, cursor = connect(pooledDB)
   # 执行SQL，并返回收影响行数
   effect_row = cursor.execute(sql, args)
   conn.commit()
   close(conn, cursor)
   return effect_row
def exec(pooledDB, sql, args=[]):
   conn, cursor = connect(pooledDB)
   # 执行SQL，并返回收影响行数
   effect_row = cursor.execute(sql, args)
   conn.commit()
   close(conn, cursor)
   return effect_row

# 初始化
pooledDBDict["console"] = util.create_pooleddb(dbhost, dbport, dbuser, dbpwd, consoledb)
pooledDBDict["backend"] = util.create_pooleddb(dbhost, dbport, dbuser, dbpwd, backenddb)
domains = fetch_all(pooledDBDict["backend"], "select * from sys_domain where del_flag = 0")
for domain in domains:
   domainstr = domain["domain"]
   datasource = domain["data_source"]

   pooledDB = pooledDBDict.get(domainstr)
   if pooledDB != None:
      continue
   pooledDBDict[domainstr] = util.create_pooleddb_by(datasource)