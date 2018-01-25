import sqlite3

class MySqlite():

    def __init__(self):
        self.connect_cookie_and_three_args_db = sqlite3.connect("cache_sql/cookie_and_three_args.db",check_same_thread=False)  # 用来储存QQ帐号、cookie、
        self.connect_undone_shuoshuo_key_db = sqlite3.connect('cache_sql/undone_shuoshuo.db',check_same_thread=False)  # 用来储存未爬取的说说id的临时数据库
        self.connect_completed_shuoshuo_key_db = sqlite3.connect("cache_sql/completed_shuoshuo.db",check_same_thread=False)  # 用来储存已爬取完成的说说id的临时数据库
        self.connect_undone_summary_db = sqlite3.connect("cache_sql/undone_summary.db",check_same_thread=False)  # 用来储存未爬取的说说id内容的临时数据库
        self.connect_completed_summary_db = sqlite3.connect("cache_sql/completed_summary.db",check_same_thread=False)  # 用来储存已爬取完成的说说id内容的临时数据库
        self.connect_undone_qq_number_db = sqlite3.connect('cache_sql/undone_qq_number.db', check_same_thread=False)  # 用来储存未爬取的QQ号的临时数据库
        self.connect_completed_qq_number_db = sqlite3.connect("cache_sql/completed_qq_number.db",check_same_thread=False)  # 用来储存已爬取完成的QQ号的临时数据库
        self.connect_information_qq_number_db = sqlite3.connect("cache_sql/information_qq_number.db",check_same_thread=False)  # 用来储存爬取QQ好友信息的临时数据库
        self.connect_completed_information_qq_db = sqlite3.connect("cache_sql/completed_information_qq.db",check_same_thread=False)  # 用来储存爬取完成的QQ好友信息的临时数据库
        self.connect_beijing_undone_qq_number_db = sqlite3.connect("cache_sql/beijing_undone_qq_number.db",check_same_thread=False)  # 用来储存未完成爬取到的北京城市的QQ号的临时数据库
        self.connect_beijing_complteted_qq_number_db = sqlite3.connect("cache_sql/beijing_completed_qq_number.db",check_same_thread=False)  # 用来储存已完成爬取到的北京城市的QQ号的临时数据库
        self.cursor_cookie_and_three_args_db = self.connect_cookie_and_three_args_db.cursor()
        self.cursor_undone_shuoshuo_key_db = self.connect_undone_shuoshuo_key_db.cursor()
        self.cursor_undone_summary_db = self.connect_undone_summary_db.cursor()
        self.cursor_completed_summary_db = self.connect_completed_summary_db.cursor()
        self.cursor_completed_shuoshuo_key_db = self.connect_completed_shuoshuo_key_db.cursor()
        self.cursor_undone_qq_number_db = self.connect_undone_qq_number_db.cursor()
        self.cursor_completed_qq_number_db = self.connect_completed_qq_number_db.cursor()
        self.cursor_information_qq_number_db = self.connect_information_qq_number_db.cursor()
        self.cursor_completed_information_qq_db = self.connect_completed_information_qq_db.cursor()
        self.cursor_beijing_undone_qq_number_db = self.connect_beijing_undone_qq_number_db.cursor()
        self.cursor_beijing_completed_qq_number_db = self.connect_beijing_complteted_qq_number_db.cursor()

        cookie_and_three_args = """
                CREATE TABLE IF NOT EXISTS cookie_and_args(
                    qq VARCHAR(11),
                    cookie VARCHAR(255),
                    gtk VARCHAR(11),
                    sid VARCHAR(88),
                    token VARCHAR(88)
                );
        """

        undone_shuoshuo_key_sql = """
                CREATE TABLE IF NOT EXISTS undone_shuoshuo(
                    qq_number VARCHAR(11),
                    appid VARCHAR(5),
                    feedkey VARCHAR(30) UNIQUE
                );
                """

        undone_summary_sql = """
                CREATE TABLE IF NOT EXISTS undone_summary(
                    qq_number VARCHAR(11),
                    feedkey VARCHAR(30) UNIQUE
                );
        """

        completed_summary_sql = """
                CREATE TABLE IF NOT EXISTS completed_summary(
                    qq_number VARCHAR(11),
                    feedkey VARCHAR(30) UNIQUE
                );
        """

        completed_shuoshuo_key_sql = """
                CREATE TABLE IF NOT EXISTS completed_shuoshuo(
                    qq_number VARCHAR(11),
                    feedkey VARCHAR(30) UNIQUE
                );
                """

        undone_qq_number_sql = """
                CREATE TABLE IF NOT EXISTS undone_qq_number(
                    u_qq_number VARCHAR(11) UNIQUE
                );
                """

        completed_qq_number_sql = """
                CREATE TABLE IF NOT EXISTS completed_qq_number(
                    c_qq_number VARCHAR(11) UNIQUE
                );
                """

        information_qq_number_sql = """
                CREATE TABLE IF NOT EXISTS information_qq_number(
                    i_qq_number VARCHAR(11) UNIQUE
                );
                """
        completed_information_sql = """
                CREATE TABLE IF NOT EXISTS completed_information_qq(
                    ci_qq_number VARCHAR(11) UNIQUE
                );
                """

        beijing_undone_qq_number_sql = """
                CREATE TABLE IF NOT EXISTS beijing_qq_number(
                    bj_u_qq_number VARCHAR(11) UNIQUE
                );
                """

        beijing_completed_qq_number_sql = """
                CREATE TABLE IF NOT EXISTS beijing_qq_number(
                    bj_c_qq_number VARCHAR(11) UNIQUE
                
                );
                """

        try:
            self.cursor_cookie_and_three_args_db.execute(cookie_and_three_args)
            self.cursor_undone_shuoshuo_key_db.execute(undone_shuoshuo_key_sql)
            self.cursor_completed_shuoshuo_key_db.execute(completed_shuoshuo_key_sql)
            self.cursor_undone_summary_db.execute(undone_summary_sql)
            self.cursor_completed_summary_db.execute(completed_summary_sql)
            self.cursor_undone_qq_number_db.execute(undone_qq_number_sql)
            self.cursor_completed_qq_number_db.execute(completed_qq_number_sql)
            self.cursor_information_qq_number_db.execute(information_qq_number_sql)
            self.cursor_completed_information_qq_db.execute(completed_information_sql)
            self.cursor_beijing_undone_qq_number_db.execute(beijing_undone_qq_number_sql)
            self.cursor_beijing_completed_qq_number_db.execute(beijing_completed_qq_number_sql)
            self.connect_cookie_and_three_args_db.commit()
            self.connect_undone_shuoshuo_key_db.commit()
            self.connect_completed_shuoshuo_key_db.commit()
            self.connect_undone_summary_db.commit()
            self.connect_completed_summary_db.commit()
            self.connect_undone_qq_number_db.commit()
            self.connect_completed_qq_number_db.commit()
            self.connect_information_qq_number_db.commit()
            self.connect_completed_information_qq_db.commit()
            self.connect_beijing_undone_qq_number_db.commit()
            self.connect_beijing_complteted_qq_number_db.commit()
        except sqlite3.OperationalError:
            pass

    def sava_cookie_and_args(self,qq,cookie,gtk,sid,token):
        sql = "INSERT OR IGNORE INTO cookie_and_args (qq,cookie,gtk,sid,token) VALUES ('{}','{}','{}','{}','{}')".format(qq,cookie,gtk,sid,token)
        self.cursor_cookie_and_three_args_db.execute(sql)
        self.connect_cookie_and_three_args_db.commit()

    def sava_undone_shuoshuo_key(self,qq,appid,feedkey):
        try:
            check_sql = "SELECT qq_number,feedkey FROM completed_shuoshuo WHERE qq_number='{}' and feedkey='{}'".format(qq, feedkey)
            check_fetchall = self.cursor_completed_shuoshuo_key_db.execute(check_sql)
            if check_fetchall.fetchall() == []:
                sql = "INSERT OR IGNORE INTO undone_shuoshuo (qq_number,appid,feedkey) VALUES ('{}','{}','{}')".format(qq,appid,feedkey)
                self.cursor_undone_shuoshuo_key_db.execute(sql)
                self.connect_undone_shuoshuo_key_db.commit()
                print("已保存到临时数据库中......")
            else:
                print("这条说说已经爬过了~pass")
        except sqlite3.OperationalError:
            pass

    def sava_undone_summary_key(self,qq,feedkey):
        try:
            check_sql = "SELECT qq_number,feedkey FROM completed_summary WHERE qq_number='{}' and feedkey='{}'".format(qq, feedkey)
            check_fetchall = self.cursor_completed_summary_db.execute(check_sql)
            if check_fetchall.fetchall() == []:
                sql = "INSERT OR IGNORE INTO undone_summary (qq_number,feedkey) VALUES ('{}','{}')".format(qq,feedkey)
                self.cursor_undone_summary_db.execute(sql)
                self.connect_undone_summary_db.commit()
                print("已保存到临时数据库中......")
            else:
                print("这条说说已经爬过了~pass")
        except sqlite3.OperationalError:
            pass

    def del_undone_shuoshuo_key_and_sava_completed_shuoshuo_key(self,qq,feedkey):
        try:
            del_sql = "DELETE FROM undone_shuoshuo WHERE qq_number='{}' and feedkey='{}'".format(qq, feedkey)
            insert_sql = "INSERT OR IGNORE INTO completed_shuoshuo (qq_number,feedkey) VALUES ('{}','{}')".format(qq,feedkey)
            self.cursor_undone_shuoshuo_key_db.execute(del_sql)
            self.cursor_completed_shuoshuo_key_db.execute(insert_sql)
            self.connect_undone_shuoshuo_key_db.commit()
            self.connect_completed_shuoshuo_key_db.commit()
        except sqlite3.OperationalError:
            pass

    def del_undone_summary_key_and_sava_completed_summary_key(self,qq,feedkey):
        del_sql = "DELETE FROM undone_summary WHERE qq_number='{}' and feedkey='{}'".format(qq, feedkey)
        insert_sql = "INSERT OR IGNORE INTO completed_summary (qq_number,feedkey) VALUES ('{}','{}')".format(qq,feedkey)
        self.cursor_undone_summary_db.execute(del_sql)
        self.cursor_completed_summary_db.execute(insert_sql)
        self.connect_undone_summary_db.commit()
        self.connect_completed_summary_db.commit()

    def sava_undone_qq_number_and_sava_information_qq_number(self,qq):
        check_qq = "SELECT c_qq_number FROM completed_qq_number WHERE c_qq_number='{}'".format(qq)
        check_fetchall = self.cursor_completed_qq_number_db.execute(check_qq)
        if check_fetchall.fetchall() == []:
            sql = "INSERT OR IGNORE INTO undone_qq_number (u_qq_number) VALUES ('{}')".format(qq)
            sql2 = "INSERT OR IGNORE INTO information_qq_number (i_qq_number) VALUES ('{}')".format(qq)
            self.cursor_undone_qq_number_db.execute(sql)
            self.cursor_information_qq_number_db.execute(sql2)
            self.connect_undone_qq_number_db.commit()
            self.connect_information_qq_number_db.commit()
        else:
            print("QQ '{}' 已经爬过了~pass".format(qq))

    def sava_beijing_undone_qq_number_and_sava_information_qq_number(self,qq):
        check_qq = "SELECT c_qq_number FROM completed_qq_number WHERE c_qq_number='{}'".format(qq)
        check_fetchall = self.cursor_completed_qq_number_db.execute(check_qq)
        if check_fetchall.fetchall() == []:
            sql = "INSERT OR IGNORE INTO beijing_qq_number (bj_u_qq_number) VALUES ('{}')".format(qq)
            sql2 = "INSERT OR IGNORE INTO information_qq_number (i_qq_number) VALUES ('{}')".format(qq)
            self.cursor_beijing_undone_qq_number_db.execute(sql)
            self.cursor_information_qq_number_db.execute(sql2)
            self.connect_beijing_undone_qq_number_db.commit()
            self.connect_information_qq_number_db.commit()
        else:
            print("QQ '{}' 已经爬过了~pass".format(qq))

    def del_undone_qq_number_and_del_beijing_qq_number_and_sava_completed_qq_number(self,qq):
        del_sql = "DELETE FROM undone_qq_number WHERE u_qq_number='{}'".format(qq)
        del_sql1 = "DELETE FROM beijing_qq_number WHERE bj_u_qq_number='{}'".format(qq)
        sava_sql = "INSERT OR IGNORE INTO completed_qq_number (c_qq_number) VALUES ('{}')".format(qq)
        self.cursor_undone_qq_number_db.execute(del_sql)
        self.cursor_beijing_undone_qq_number_db.execute(del_sql1)
        self.cursor_completed_qq_number_db.execute(sava_sql)
        self.connect_undone_qq_number_db.commit()
        self.connect_beijing_undone_qq_number_db.commit()
        self.connect_completed_qq_number_db.commit()

    def del_information_qq_number(self,qq):
        del_sql = "DELETE FROM information_qq_number WHERE i_qq_number='{}'".format(qq)
        sava_sql = "INSERT OR IGNORE INTO completed_information_qq (ci_qq_number) VALUES ('{}')".format(qq)
        self.cursor_information_qq_number_db.execute(del_sql)
        self.cursor_completed_information_qq_db.execute(sava_sql)
        self.connect_information_qq_number_db.commit()
        self.connect_completed_information_qq_db.commit()

    def read_cookie(self):
        sql = "SELECT * FROM cookie_and_args"
        data = self.cursor_cookie_and_three_args_db.execute(sql)
        for cookie in data:
            return cookie

    def del_cookie(self,qq):
        sql = "DELETE FROM cookie_and_args WHERE qq='{}'".format(qq)
        sava_sql = "INSERT OR IGNORE INTO "
        self.cursor_cookie_and_three_args_db.execute(sql)
        self.connect_cookie_and_three_args_db.commit()

    def read_20_shuoshuo_key(self):
        try:
            sql = "SELECT * FROM undone_shuoshuo;"
            data = self.cursor_undone_shuoshuo_key_db.execute(sql)
            # for i in s:
            #     print(i)
            data_list = []
            num = 0
            for x in data:
                if num == 20:
                    break
                data_list.append(x)
                num +=1
            return data_list
        except sqlite3.OperationalError:
            print("因为锁(Lock)....请重新运行.....")

    def read_10_summary_key(self):
        try:
            sql = "SELECT * FROM undone_summary;"
            data = self.cursor_undone_summary_db.execute(sql)
            # for i in s:
            #     print(i)
            data_list = []
            num = 0
            for x in data:
                if num == 10:
                    break
                data_list.append(x)
                num +=1
            return data_list
        except sqlite3.OperationalError:
            print("因为锁(Lock)....请重新运行.....")

    def read_5_duilie(self):
        beijing_check_sql = "SELECT bj_u_qq_number FROM beijing_qq_number"
        beijing_fetchall = self.cursor_beijing_undone_qq_number_db.execute(beijing_check_sql)
        data_list = []
        if beijing_fetchall.fetchall() == []:
            sql = "SELECT u_qq_number FROM undone_qq_number"
            data = self.cursor_undone_qq_number_db.execute(sql)
            num = 0
            for x in data:
                # return x[0]
                if num == 5:
                    break
                data_list.append(x[0])
                num += 1
        else:
            sql = "SELECT bj_u_qq_number FROM beijing_qq_number"
            data = self.cursor_beijing_undone_qq_number_db.execute(sql)
            num = 0
            for x in data:
                # return x[0]
                if num == 5:
                    break
                data_list.append(x[0])
                num += 1
        return data_list

    def read_information_number(self):
        sql = "SELECT i_qq_number FROM information_qq_number"
        data = self.cursor_information_qq_number_db.execute(sql)
        data_list = []
        num = 0
        for x in data:
            # return x[0]
            if num == 10:
                break
            data_list.append(x)
            num += 1
        return data_list

    def read_10_shuoshuokey_summary(self):
        sql = "SELECT "

    def read_10_numbers(self,qq):
        sql = "SELECT qq_number FROM undone_shuoshuo WHERE qq_number=qq_number"
        data = self.cursor_undone_shuoshuo_key_db.execute(sql).fetchall()
        print(data)
        # data_list = []
        # set_data
        # num = 0
        # for x in data:
        #     # return x[0]
        #     if num == 20:
        #         break
        #     data_list.append(x)
        #     num += 1

        # return data_list

    def read_qq_number(self,qq):
        # self.cursor_qq_number_db.execute('INSERT INTO undone_qq_number (u_qq_number) VALUES ("123456")')
        # self.connect_qq_number_db.commit()
        sql = "SELECT * FROM undone_qq_number"
        da = self.cursor_undone_qq_number_db.execute(sql)
        num = 1
        for i in da:
            print(num,i)
            num+=1

if __name__ == '__main__':
    s = MySqlite()
#     # print(s.read_10_numbers(1390540743))
    s.read_qq_number("")
    # print(s.read_cookie())
#     # print(s.read_10_duilie())
