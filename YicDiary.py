# 予定管理アプリ

# ユーザ名 tomato202

import tkinter as tk
import tkinter.ttk as ttk
import datetime as da
import calendar as ca
import pymysql

WEEK = ['日', '月', '火', '水', '木', '金', '土']
WEEK_COLOUR = ['red', 'black', 'black', 'black','black', 'black', 'blue']
actions = ('学校','試験', '課題', '行事', '就活', 'アルバイト','旅行')

class Yic:

  def __init__(self, root, login_name, login_id):
    root.title('予定管理アプリ ({}さんがログイン中)'.format(login_name))
    root.geometry('520x280')
    root.resizable(0, 0)
    root.grid_columnconfigure((0, 1), weight=1)
    self.sub_win = None

    self.year  = da.date.today().year
    self.mon = da.date.today().month
    self.today = da.date.today().day

    self.title = None
    self.plan = None

    self.login_name = login_name
    self.login_id = login_id
    self.now_id = login_id

    # 左側のカレンダー部分
    leftFrame = tk.Frame(root)
    leftFrame.grid(row=0, column=0)
    self.leftBuild(leftFrame)

    # 右側の予定管理部分
    rightFrame = tk.Frame(root)
    rightFrame.grid(row=0, column=1)
    self.rightBuild(rightFrame)



  #-----------------------------------------------------------------
  # アプリの左側の領域を作成する
  #
  # leftFrame: 左側のフレーム
  def leftBuild(self, leftFrame):
    self.viewLabel = tk.Label(leftFrame, font=('', 10))
    beforButton = tk.Button(leftFrame, text='＜', font=('', 10), command=lambda:self.disp(-1))
    nextButton = tk.Button(leftFrame, text='＞', font=('', 10), command=lambda:self.disp(1))

    self.viewLabel.grid(row=0, column=1, pady=10, padx=10)
    beforButton.grid(row=0, column=0, pady=10, padx=10)
    nextButton.grid(row=0, column=2, pady=10, padx=10)

    self.calendar = tk.Frame(leftFrame)
    self.calendar.grid(row=1, column=0, columnspan=3)
    self.disp(0)


  #-----------------------------------------------------------------
  # アプリの右側の領域を作成する
  #
  # rightFrame: 右側のフレーム
  def rightBuild(self, rightFrame):
    
    # マルチユーザー
    self.max_user = self.max_user()
    temp = self.user(0)
    print(temp)
    self.viewLabel2 = tk.Label(rightFrame,text=temp, font=('', 10))
    beforButton = tk.Button(rightFrame, text='＜', font=('', 10),command=lambda:self.user(-1))
    nextButton = tk.Button(rightFrame, text='＞', font=('', 10),command=lambda:self.user(1))

    self.viewLabel2.grid(row=70, column=1, pady=10, padx=10)
    beforButton.grid(row=70, column=0, pady=50, padx=10)
    nextButton.grid(row=70, column=2, pady=10, padx=10)  
    
    # 日付
    r1_frame = tk.Frame(rightFrame)
    r1_frame.grid(row=0, column=0, pady=10)

    temp2 = '{}年{}月{}日の予定'.format(self.year, self.mon, self.today)
    self.title = tk.Label(r1_frame, text=temp2, font=('', 12))
    self.title.grid(row=0, column=0, padx=20)

    button = tk.Button(rightFrame, text='追加', command=lambda:self.add())
    button.grid(row=0, column=1)

    # 予定
    self.r2_frame = tk.Frame(rightFrame)
    self.r2_frame.grid(row=50, column=0, padx=10)

    """
    temp = self.getplan()
    self.plan = tk.Label(self.r2_frame, text=temp, font=("", 12))
    self.plan.grid(row=0, column=0, padx=40)
    """

    self.schedule()



  #-----------------------------------------------------------------
  # アプリの右側の領域に予定を表示する
  #
  def schedule(self):

    # ウィジットを廃棄
    for widget in self.r2_frame.winfo_children():
      widget.destroy()

    # データベースに予定の問い合わせを行う
    temp = self.getplan()



    # 予定がない場合
    if not temp:
      temp = "予定がありません"
      self.plan = tk.Label(self.r2_frame, text=temp, font=("", 12))
      self.plan.grid(row=1, column=0, padx=0)

    # 予定ありの場合
    else:
      for idx in range(len(temp)):
        print(temp[idx])
        self.plan = tk.Label(self.r2_frame, text=temp[idx], font=("", 12))
        self.plan.grid(row=idx+1, column=0, padx=0)

  # ユーザの最大数
  def max_user(self):
    # データベースに接続
    #---------------------------------------------------------------------------------------------------------------------------------------
    connection = pymysql.connect(host = '127.0.0.1',
                                 user = 'root',
                                 password = '',
                                 db = 'apr02',
                                 charset = 'utf8mb4',
                                 cursorclass = pymysql.cursors.DictCursor)

    try:
     # トランザクション開始
       connection.begin()

       with connection.cursor() as cursor:

        cursor = connection.cursor()

         # Create a new record

        # plan_codeの取り出し
        sql = "select count(user) from user_table;;"
        # print("{}を実行".format(sql))
        cursor.execute(sql)
        results = cursor.fetchone()
        # print(results)

        # 数値を抽出
        idx = results["count(user)"]

        # print(idx)
        return idx

    except Exception as e:
      print("error:", e)
      connection.rollback()
    finally:
      connection.close()

# マルチユーザー
  def user(self, argv):
    connection = pymysql.connect(host = '127.0.0.1',
                                 user = 'root',
                                 password = '',
                                 db = 'apr02',
                                 charset = 'utf8mb4',
                                 cursorclass = pymysql.cursors.DictCursor)


        
    try:
        # トランザクション開始
            if self.now_id > 1 and self.now_id < self.max_user or self.now_id == 1 and argv == 1 or self.now_id == self.max_user and argv == -1:
              self.now_id = self.now_id + argv
              print(self.now_id)
              connection.begin()
            
              with connection.cursor() as cursor:

                cursor = connection.cursor()

                # Create a new record
                
                # plan_codeの取り出し
                sql = "SELECT user FROM user_table WHERE user_id = {};".format(self.now_id)
                print(sql)
                cursor.execute(sql)
                results = cursor.fetchone()
                # 数値を抽出
                print(results)

                user = results["user"]
                self.viewLabel2['text'] = '{}'.format(user)

                self.schedule()
                print(user)

            else:
              pass
                
                

    except Exception as e:
            if self.now_id >= 1:
              pass
              return user
              connection.rollback()
            else:
              pass
              connection.rollback()
                
    finally:
            connection.close()




  #-----------------------------------------------------------------
  # カレンダーを表示する
  #
  # argv: -1 = 前月
  #        0 = 今月（起動時のみ）
  #        1 = 次月
  def disp(self, argv):
    self.mon = self.mon + argv
    if self.mon < 1:
      self.mon, self.year = 12, self.year - 1
    elif self.mon > 12:
      self.mon, self.year = 1, self.year + 1

    self.viewLabel['text'] = '{}年{}月'.format(self.year, self.mon)

    cal = ca.Calendar(firstweekday=6)
    cal = cal.monthdayscalendar(self.year, self.mon)

    # ウィジットを廃棄
    for widget in self.calendar.winfo_children():
      widget.destroy()

    # 見出し行
    r = 0
    for i, x in enumerate(WEEK):
      label_day = tk.Label(self.calendar, text=x, font=('', 10), width=3, fg=WEEK_COLOUR[i])
      label_day.grid(row=r, column=i, pady=1)

    # カレンダー本体
    r = 1
    for week in cal:
      for i, day in enumerate(week):
        if day == 0: day = ' ' 
        label_day = tk.Label(self.calendar, text=day, font=('', 10), fg=WEEK_COLOUR[i], borderwidth=1)
        if (da.date.today().year, da.date.today().month, da.date.today().day) == (self.year, self.mon, day):
          label_day['relief'] = 'solid'
        label_day.bind('<Button-1>', self.click)
        label_day.grid(row=r, column=i, padx=2, pady=1)
      r = r + 1

    # 画面右側の表示を変更
    if self.title is not None:
      self.today = 1
      self.title['text'] = '{}年{}月{}日の予定'.format(self.year, self.mon, self.today)

  def getplan(self):
    # データベースに接続
    #---------------------------------------------------------------------------------------------------------------------------------------
    connection = pymysql.connect(host = '127.0.0.1',
                                 user = 'root',
                                 password = '',
                                 db = 'apr02',
                                 charset = 'utf8mb4',
                                 cursorclass = pymysql.cursors.DictCursor)

    try:
     # トランザクション開始
       connection.begin()

       with connection.cursor() as cursor:

        cursor = connection.cursor()

         # Create a new record
        
        # planの取り出し
        print("{}{}{}".format(self.year, self.mon, self.today))
        sql = "SELECT kinds, plan FROM plan_table inner join kinds_table on plan_table.kinds_code = kinds_table.kinds_code where day = '{}-{}-{}' and user_id = {};".format(self.year, self.mon, self.today, self.now_id)
        # 
        # print("{}を実行".format(sql))
        cursor.execute(sql)
        results = cursor.fetchall()
        print(results)
        display = []
          
        # 予定がある
        if len(results) != 0:
          # 文字を抽出
          for i in range(len(results)):
            kinds = results[i]["kinds"]
            plan = results[i]["plan"]
            box = "{} : {}".format(kinds, plan)
            display.append(box)
      


        #print(idx)
        return display

        connection.commit()

    except Exception as e:
      print("error:", e)
      connection.rollback()
    finally:
      connection.close()



  #-----------------------------------------------------------------
  # 予定を追加したときに呼び出されるメソッド
  #
  def add(self):
    if self.sub_win == None or not self.sub_win.winfo_exists():
      self.sub_win = tk.Toplevel()
      self.sub_win.geometry("300x300")
      self.sub_win.resizable(0, 0)

      # ラベル
      sb1_frame = tk.Frame(self.sub_win)
      sb1_frame.grid(row=0, column=0)
      temp = '{}年{}月{}日　追加する予定'.format(self.year, self.mon, self.today)
      title = tk.Label(sb1_frame, text=temp, font=('', 12))
      title.grid(row=0, column=0)

      # 予定種別（コンボボックス）
      sb2_frame = tk.Frame(self.sub_win)
      sb2_frame.grid(row=1, column=0)
      label_1 = tk.Label(sb2_frame, text='種別 : ', font=('', 10))
      label_1.grid(row=0, column=0, sticky=tk.W)
      self.combo = ttk.Combobox(sb2_frame, state='readonly', values=actions)
      self.combo.current(0)
      self.combo.grid(row=0, column=1)
      

      # テキストエリア（垂直スクロール付）
      sb3_frame = tk.Frame(self.sub_win)
      sb3_frame.grid(row=2, column=0)
      self.text = tk.Text(sb3_frame, width=40, height=15)
      self.text.grid(row=0, column=0)
      scroll_v = tk.Scrollbar(sb3_frame, orient = tk.VERTICAL, command = self.text.yview)
      scroll_v.grid(row=0, column=1, sticky=tk.N+tk.S)
      self.text["yscrollcommand"] = scroll_v.set

      # 保存ボタン
      sb4_frame = tk.Frame(self.sub_win)
      sb4_frame.grid(row=3, column=0, sticky=tk.NE)
      button = tk.Button(sb4_frame, text='保存', command=lambda:self.done())
      button.pack(padx=10, pady=10)
    elif self.sub_win != None and self.sub_win.winfo_exists():
      self.sub_win.lift()

  def getKey(self, my_kinds):
    # データベースに接続
    #---------------------------------------------------------------------------------------------------------------------------------------
    connection = pymysql.connect(host = '127.0.0.1',
                                 user = 'root',
                                 password = '',
                                 db = 'apr02',
                                 charset = 'utf8mb4',
                                 cursorclass = pymysql.cursors.DictCursor)

    try:
     # トランザクション開始
       connection.begin()

       with connection.cursor() as cursor:

        cursor = connection.cursor()

         # Create a new record
        sql = "select kinds_code from kinds_table where kinds = '{}';".format(my_kinds)
        cursor.execute(sql)

        results = cursor.fetchone()
        idx = results["kinds_code"]
        return idx

    except Exception as e:
      print("error:", e)
      connection.rollback()
    finally:
      connection.close()

# 現在の計画数
  def getnow(self):
    # データベースに接続
    #---------------------------------------------------------------------------------------------------------------------------------------
    connection = pymysql.connect(host = '127.0.0.1',
                                 user = 'root',
                                 password = '',
                                 db = 'apr02',
                                 charset = 'utf8mb4',
                                 cursorclass = pymysql.cursors.DictCursor)

    try:
     # トランザクション開始
       connection.begin()

       with connection.cursor() as cursor:

        cursor = connection.cursor()

         # Create a new record

        # plan_codeの取り出し
        sql = "select count(plan_code) from plan_table;"
        # print("{}を実行".format(sql))
        cursor.execute(sql)
        results = cursor.fetchone()
        # print(results)

        # 数値を抽出
        idx = results["count(plan_code)"]

        # print(idx)
        return idx

    except Exception as e:
      print("error:", e)
      connection.rollback()
    finally:
      connection.close()


  #-----------------------------------------------------------------
  # 予定追加ウィンドウで「保存」を押したときに呼び出されるメソッド
  #
  def done(self):

    # 日付
    days = "{}-{}-{}".format(self.year, self.mon, self.today)
    print(days)

    # 種別
    kinds = self.combo.get()
    # print(kinds)

    # ----------------------------------------------------------------------------------------------------------------------------------------------------------
    kinds_id = self.getKey(kinds)
    #self.getKey(kinds)
    print(kinds_id)

    # 予定詳細
    plan = self.text.get("1.0", "end")
    print(plan)

    # 数値
    now_num = self.getnow()
    #self.getnow()

    # データベースに新規予定を挿入する
    pass

    # データベースに接続
    connection = pymysql.connect(host = '127.0.0.1',
                                 user = 'root',
                                 password = '',
                                 db = 'apr02',
                                 charset = 'utf8mb4',
                                 cursorclass = pymysql.cursors.DictCursor)
    ######################################

    user_id = self.login_id

    try:
     # トランザクション開始
       connection.begin()

       with connection.cursor() as cursor:

         cursor = connection.cursor()

         # SQLに追加
         sql = "insert into plan_table(plan_code, day, plan, kinds_code, user_id) values({}, '{}', '{}', {}, {}); ".format(now_num + 1, days, plan, kinds_id, user_id)

         # SQLの実行
         cursor.execute(sql)

       connection.commit()

    except Exception as e:
      print("error:", e)
      connection.rollback()
    finally:
      connection.close()

    self.sub_win.destroy()


  #-----------------------------------------------------------------
  # 日付をクリックした際に呼びだされるメソッド（コールバック関数）
  #
  # event: 左クリックイベント <Button-1>
  def click(self, event):
    day = event.widget['text']
    if day != ' ':
      self.title['text'] = '{}年{}月{}日の予定'.format(self.year, self.mon, day)
      self.today = day
    self.schedule()


def Main():
  root = tk.Tk()
  Yic(root)
  root.mainloop()

if __name__ == '__main__':
  Main()
