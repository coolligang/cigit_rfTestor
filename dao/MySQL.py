# encoding:utf-8

import MySQLdb
import sys

reload(sys)
sys.setdefaultencoding("utf-8")  # 解决mysql中午乱吗


class MySQL:
    def __init__(self, str_host, int_port, str_user, str_pwd, str_db):
        self.host = str_host
        self.port = int_port
        self.user = str_user
        self.pwd = str_pwd
        self.db = str_db

    def __open(self):
        try:
            connect = MySQLdb.connect(host=self.host, port=self.port, user=self.user, passwd=self.pwd, db=self.db,
                                      charset="utf8")
        except Exception as e:
            raise self.failureException("%s,%s  %s" % (self.type, self.db, repr(e)))
        cursor = connect.cursor()
        cursor.execute("SET NAMES UTF8")
        return connect, cursor

    def __close(self, con, cur):
        try:
            if cur is not None:
                cur.close()
            if con is not None:
                con.close()
        except Exception as e:
            print("*ERROR*" + repr(e))


    def save_date_by_sql(self, str_sql):
        """
        通过sql插入数据
        :param str_sql:
        :return:
        """
        conn, cur = self.__open()
        try:
            cur.execute(str_sql)
            conn.commit()
        except Exception, e:
            print " *ERROR* " + repr(e)
        finally:
            self.__close(conn, cur)


if __name__ == "__main__":
    host = "172.16.31.36"
    port = 3306
    user = "root"
    pwd = "123456"
    db = "inspurface"
    mysql = MySQL(host, port, user, pwd, db)
    sql = 'insert into facedata (create_time,feature,http_stauts,u_id,update_time,face_img,city_region,sex) VALUES ("2018-04-18 12:11:11","testeature",0,"testuid001","2018-04-18 12:11:11","testface","testcity",1)'
    mysql.save_date_by_sql(sql)
