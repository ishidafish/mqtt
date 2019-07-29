#!/usr/local/bin/python3
import paho.mqtt.client as mqtt
import mysql.connector
import json
import time
import pa_config as conf
import pa_packet

# "[b'123']" ::: bytes.decode(eval(b)[0])  ::: '123'

# $IME 下行, PABOX/$IME 上行
def on_connect(client, userdata, flags, rc):
    print("Connect MQTT: "+str(rc)+": Subscribe("+conf.SUB_TOPIC+"/#)")
    client.subscribe(conf.SUB_TOPIC+"/#")

def on_message(client, userdata, msg):
    pac = pa_packet.packet_obj()
    cursor = cnx.cursor()
    # pacobj={'NAME':__,'CODE':__,'SEQ':__,'TYPE':__,'DESC':__,'VALUE':[__]}
    pacobj = pac.parse_packet(msg.payload)
    topic = msg.topic
    topic_array = topic.split('/')
    iid = topic_array[1]  # 假設 iid 為 IMEI
    now = time.strftime("%Y-%m-%d %X", time.localtime())
    print(now+':'+msg.topic+'='+str(pacobj))  #json.dumps(pacobj, ensure_ascii=False, indent=None))
    # insert into mysql db
    r = (iid, pacobj['CODE'], pacobj['NAME'], pacobj['SEQ'],  pacobj['TYPE'], pacobj['DESC'], str(pacobj['VALUE']))
    cursor.execute(conf.GET_SQL['add_trandata'], r)  # DB
    cnx.commit()
    # 需要自動回覆的指令
    if pacobj['CODE'] in conf.MUST_REPLY_CODES:
        if pacobj['NAME'] == 'TSYN':
            (r1, msg_back), v = tdata(pac, iid, pacobj, []), now
        elif pacobj['NAME'] == 'PING':
            (r1, msg_back), v = tdata(pac, iid, pacobj, pacobj['VALUE']), str(pacobj['VALUE'])
        client.publish(iid, msg_back, conf.QoS)
        cursor.execute(conf.GET_SQL['add_trandata'], r1)
        cnx.commit()
        print(now+":Reply_Publish:"+iid+'/'+pacobj['CODE']+"+"+v)
    pac = None
    cursor.close()

def tdata(pac, iid, pacobj, val):
    msg_back = pac.compose_cmd(pacobj['NAME'], pacobj['SEQ'], val)
    r1 = (iid, pacobj['CODE'], pacobj['NAME'], pacobj['SEQ'], pacobj['TYPE'], '[R]:'+pacobj['DESC'], str(val))
    return (r1, msg_back)

# Start Here
cnx = mysql.connector.connect(host=conf.MY_HOST, user=conf.MY_USER, passwd=conf.MY_PASS, database=conf.MY_DATABASE)
add_info = conf.GET_SQL['add_trandata']
client = mqtt.Client()
client.username_pw_set(conf.USER, conf.PASS)
client.on_connect = on_connect
client.on_message = on_message
client.connect(conf.HOST, conf.PORT, 60)
client.loop_forever()
cnx.close()
