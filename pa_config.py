## MQTT
HOST = "iothub.proadvancer.com" #139.198.19.224" 
PORT = 1883
USER = "pabox"
PASS = "1qaz2wsx3edc"
QoS  = 1
HTTP = 9000
SUB_TOPIC = "PABOX"
# Subscribe 的 Topics
TOPICS = [SUB_TOPIC]
# 订阅得到的msg.code ,设定发布回去的code及内容
MUST_REPLY_CODES = {
    '01':{"01" : -10},    # 原值
    '02':{"02" : -1},     # 空
    "05":{"05" :  1},     # item.attr02 (源自GET_SQL.item_attr)
    "13":{"13" :  2},     # item.attr03
    "14":{"14" :  3},     # item.attr04
    "15":{"15" :  4},     # item.attr05
    "09":{"09" :  5},     # item.attr06
    "0D":{"0D" :  6},     # item.attr07
    "0E":{"0E" :  7},     # item.attr08
    'F0':   {"02" : -1,"05" : 1,"13" : 2,"14" : 3,"15" : 4,"09" : 5,"0D" : 6,"0E" : 7,},
    'DIRTY':{"02" : -1,"05" : 1,"13" : 2,"14" : 3,"15" : 4,"09" : 5,"0D" : 6,"0E" : 7,},
    }

## mysql
MY_HOST = "127.0.0.1"
MY_USER = "iot"
MY_PASS = "iot"
MY_DATABASE ="pabox"
GET_SQL={
    "add_trandata":("INSERT INTO `pabox`.`trandata`(`imei`,`code`,`code_name`,`seq`,`attr01`,`desc`,`data`) VALUES (%s, %s, %s, %s, %s, %s, %s)"),
    "trandata":("SELECT * from `pabox`.`trandata` order by `line_id` desc limit 100"),
    "item":("SELECT * from `pabox`.`item`"),
    "item_attr":("SELECT attr01,attr02,attr03,attr04,attr05,attr06,attr07,attr08 from `pabox`.`item` where `imei`= %s"),
    "item_clear":("Update `pabox`.`item` set `attr01`='' WHERE `imei`= %s "),
    "item_on":("Update `pabox`.`item` set `on_time`= now() WHERE `imei` = %s "),
    }


## postgresql
PG_HOST    = "host=127.0.0.1"
PG_PORT    = "port=5432"
PG_DBNAME  = "dbname=pabox"
PG_USER    = "user=iot password=iot"
PG_GET_SQL={
    "add_trandata":("INSERT INTO pabox.trandata(imei,code,code_name,seq,attr01,desc,data) VALUES (%s, %s, %s, %s, %s, %s, %s)"),
    "trandata":("SELECT * from pabox.trandata order by line_id desc limit 100"),
    "item":("SELECT * from pabox.item"),
    "item_attr":("SELECT attr01,attr02,attr03,attr04,attr05,attr06,attr07,attr08 from pabox.item where imei= %s"),
    "item_clear":("Update pabox.item set attr01='' WHERE imei= %s "),
    "item_on":("Update pabox.item set on_time= now() WHERE imei = %s "),
    }

logo='''
___________________________________________________________
 _______  __   __  ___   _  __   __  _______  __   __  ___  
|       ||  | |  ||   | | ||  | |  ||       ||  | |  ||   | 
|    ___||  | |  ||   |_| ||  | |  ||  _____||  |_|  ||   | 
|   |___ |  |_|  ||      _||  |_|  || |_____ |       ||   | 
|    ___||       ||     |_ |       ||_____  ||       ||   | 
|   |    |       ||    _  ||       | _____| ||   _   ||   | 
|___|    |_______||___| |_||_______||_______||__| |__||___| 
-----------------------------------------------------------
'''
