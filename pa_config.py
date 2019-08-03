HOST = "iothub.proadvancer.com" #139.198.19.224" 
PORT = 1883
USER = "pabox"
PASS = "1qaz2wsx3edc"
QoS  = 1
HTTP = 9000
SUB_TOPIC = "PABOX"
MY_HOST = "127.0.0.1"
MY_USER = "iot"
MY_PASS = "iot"
MY_DATABASE ="pabox"

# Subscribe 的 Topics
TOPICS = [SUB_TOPIC,]
# 订阅得到的msg.code ,设定发布回去的code及内容
MUST_REPLY_CODES = {
    '01':{"01" : -10},    # 原值
    '02':{"02" : -1},     # 空
    "05":{"05" :  1},     # item.attr02 (源自GET_SQL.item_attr)
    "13":{"13" :  2},     # item.attr03
    "14":{"14" :  3},     # item.attr04
    "15":{"15" :  4},     # item.attr05
    "0A":{"0A" :  5},     # item.attr06
    "0D":{"0D" :  6},     # item.attr07
    "0E":{"0E" :  7},     # item.attr08
    'F0':   {"02" : -1,"05" : 1,"13" : 2,"14" : 3,"15" : 4,"0A" : 5,"0D" : 6,"0E" : 7,},
    'DIRTY':{"02" : -1,"05" : 1,"13" : 2,"14" : 3,"15" : 4,"0A" : 5,"0D" : 6,"0E" : 7,},
    }

## mysql
GET_SQL={
    "add_trandata":("INSERT INTO `pabox`.`trandata`(`imei`,`code`,`code_name`,`seq`,`attr01`,`desc`,`data`) VALUES (%s, %s, %s, %s, %s, %s, %s)"),
    "trandata":("SELECT * from `pabox`.`trandata` order by `line_id` desc limit 100"),
    "item":("SELECT * from `pabox`.`item`"),
    "item_attr":("SELECT attr01,attr02,attr03,attr04,attr05,attr06,attr07,attr08 from `pabox`.`item` where imei= %s "),
    "item_clear":("Update `pabox`.`item` set `attr01`='' WHERE `imei`= %s "),
    "item_on":("Update `pabox`.`item` set `on_time`= now() WHERE `imei` = %s "),
    }

# accordin to GET_SQL['item_attr']
'''
861929041497593
attr01 DIRTY_FLAG
0x02 时间同步包                  []
0x05 设置温度上限和下限参数     attr02 = "[1,100,200]"
0x13 风扇最大的工作电流         attr03 = "[350]"
0x14 舱门开启告警时间设定       attr04 = "[60]"
0x15 温度通道告警设置           attr05 = "[1,200]"
0x0a 绑定风扇和温度控制         attr06 = "[1,1]"
0x0d 通信时间间隔              attr07 = [600]
0x0e 数据采集唤醒间隔           attr08 = [600]
'''

logo='''
 _______  __   __  ___   _  __   __  _______  __   __  ___  
|       ||  | |  ||   | | ||  | |  ||       ||  | |  ||   | 
|    ___||  | |  ||   |_| ||  | |  ||  _____||  |_|  ||   | 
|   |___ |  |_|  ||      _||  |_|  || |_____ |       ||   | 
|    ___||       ||     |_ |       ||_____  ||       ||   | 
|   |    |       ||    _  ||       | _____| ||   _   ||   | 
|___|    |_______||___| |_||_______||_______||__| |__||___| 
'''
