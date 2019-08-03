#!/usr/local/bin/python3
import paho.mqtt.client as mqtt
import mysql.connector
import json
import time
import threading
import pa_config as conf
import pa_packet

def on_connect(client, userdata, flags, rc):
    print("Connect %s MQTT: %s"%(conf.HOST,str(rc)))
    for t in conf.TOPICS:
        client.subscribe( t+"/#" )
        print("订阅:%s/#"%(t,))

def on_message(client, userdata, msg):
    t=threading.Thread(target=my_on_message, args=(msg,))
    t.start()

def my_on_message(msg):
    pac = pa_packet.packet_obj()
    cursor = cnx.cursor()
    now=time.strftime("%Y-%m-%d %X", time.localtime())
    # pacobj={'NAME':__,'CODE':__,'SEQ':__,'TYPE':__,'DESC':__,'VALUE':[__]}
    pacobj = pac.parse_packet(msg.payload)
    topic = msg.topic
    topic_array = topic.split('/')
    iid = topic_array[1]  # 假設 iid 為 IMEI
    print(now +':'+msg.topic+'='+str(pacobj)) 
    r = (iid, pacobj['CODE'], pacobj['NAME'], pacobj['SEQ'],  pacobj['TYPE'], pacobj['DESC'], str(pacobj['VALUE']))
    cursor.execute(conf.GET_SQL['add_trandata'], r)  # DB
    cnx.commit()
    cursor.execute(conf.GET_SQL['item_attr'], (iid,)) # 每次收到message 都检查 item dirty, item.attr01
    item_row = cursor.fetchone()
    now = time.strftime("%Y-%m-%d %X", time.localtime())
    try:
        org_code = pacobj['CODE']
        rA=conf.MUST_REPLY_CODES[org_code]
    except:
        rA = {}
    if item_row[0] == "Y":
        cursor.execute(conf.GET_SQL['item_clear'], (iid,))
        cnx.commit()
        rB=conf.MUST_REPLY_CODES["DIRTY"] if org_code !="F0" else {}
    else:
        rB = {}
    reply_codes = joindict(rA,rB)
    try:
        i=0
        for k,v in reply_codes.items():
            if i>0:
                time.sleep(1)  # ***
            t = pa_packet.datdict[k]
            pacobj['CODE'] = k
            pacobj['NAME'] = t['NAME'] 
            pacobj['TYPE'] = t['TYPE'] 
            pacobj['DESC'] = t['DESC']
            if v > 0:
                val_arr = json.loads(item_row[v])   # item_row[position]
                v_str = str(val_arr)
            elif v == -1:
                val_arr, v_str = [] , now
            elif v == -10:
                val_arr, v_str =  pacobj['VALUE'],str(pacobj['VALUE'])
            tdata(cursor, pac, iid, pacobj, val_arr, v_str)
            i += 1
    except:
        pass
    pac = None
    cursor.close()

def tdata(cursor, pac, iid, pacobj, val_arr, v_str):
    msg_back = pac.compose_cmd(pacobj['NAME'], pacobj['SEQ'], val_arr)
    r1 = (iid, pacobj['CODE'], pacobj['NAME'], pacobj['SEQ'], pacobj['TYPE'], '[R]:'+pacobj['DESC'], v_str)
    client.publish(iid, msg_back, conf.QoS)
    cursor.execute(conf.GET_SQL['add_trandata'], r1)
    cnx.commit()
    print(time.strftime("%Y-%m-%d %X", time.localtime()) + ":Reply_Publish:"+iid+'/'+pacobj['CODE']+"+"+v_str)

def joindict(dict1, dict2):
    dictX=dict1
    for k,v in dict2.items():
        try:
            c = dict1[k]
        except:
            dictX[k]=v
    return dictX


# Start Here
cnx = mysql.connector.connect(host=conf.MY_HOST, user=conf.MY_USER, passwd=conf.MY_PASS, database=conf.MY_DATABASE)
cnx.ping(True)
add_info = conf.GET_SQL['add_trandata']
client = mqtt.Client()
client.username_pw_set(conf.USER, conf.PASS)
client.on_connect = on_connect
client.on_message = on_message
client.connect(conf.HOST, conf.PORT, 60)
print(conf.logo)
client.loop_forever()
cnx.close()


# "[b'123']" ::: bytes.decode(eval(b)[0])  ::: '123'
# $IME 下行, PABOX/$IME 上行