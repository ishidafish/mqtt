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
    pac = pa_packet.Tpacket()
    cursor = cnx.cursor()
    now=time.strftime("%Y-%m-%d %X", time.localtime())
    pdata = pac.parse(msg.payload) # pdata={'NAME':__,'CODE':__,'SEQ':__,'TYPE':__,'DESC':__,'VALUE':[__]}
    topic = msg.topic
    topic_array = topic.split('/')
    iid = topic_array[1]  # 假設 iid 為 IMEI
    print(now +':'+msg.topic+'='+str(pdata)) 
    r = (iid, pdata['CODE'], pdata['NAME'], pdata['SEQ'],  pdata['TYPE'], pdata['DESC'], str(pdata['VALUE']))
    cursor.execute(conf.GET_SQL['add_trandata'], r)  # DB
    cnx.commit()
    cursor.execute(conf.GET_SQL['item_attr'], (iid,)) # 每次收到message 都检查 item dirty, item.attr01
    item_row = cursor.fetchone()
    try:
        org_code = pdata['CODE']
        rA=conf.MUST_REPLY_CODES[org_code]
    except:
        rA = {}
    if item_row[0] == "Y":
        cursor.execute(conf.GET_SQL['item_clear'], (iid,))
        cnx.commit()
        rB=conf.MUST_REPLY_CODES["DIRTY"] if org_code !="F0" else {}
    else:
        rB = {}
    reply_codes = joindict(rA,rB) #{"02" : -1,"05" : 1,"13" : 2,"14" : 3,"15" : 4,"09" : 5,"0D" : 6,"0E" : 7,}
    try:
        i, _data, _vstr = 0, bytes(), ''
        for k,v in reply_codes.items():
            t = pa_packet.codeDict[k]
            if v > 0:
                val_arr = json.loads(item_row[v])   # item_row[position]
                v_str = str(val_arr)
            elif v == -1:
                val_arr, v_str = [] , "['"+now+"']"
            elif v == -10:
                val_arr, v_str =  pdata['VALUE'],str(pdata['VALUE'])        
            msg_back = pac.compose(k, pdata['SEQ'], val_arr)
            _data = _data + pac.p_data # binary data 
            _vstr = _vstr + ('' if i==0 else ',') + v_str
            i += 1
        msg_back = pac.join( k ,pdata['SEQ'] , _data)
        r1 = (iid, org_code, pdata['NAME'], pdata['SEQ'], pdata['TYPE'], '[R]:'+pdata['DESC'], _vstr)
        client.publish(iid, msg_back, conf.QoS)
        cursor.execute(conf.GET_SQL['add_trandata'], r1)
        cnx.commit()
        print(time.strftime("%Y-%m-%d %X", time.localtime()) + ":Reply_Publish:"+iid+'/'+ org_code +"+"+ _vstr)
        i += 1
    except:
        pass
    pac = None
    cursor.close()

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
client = mqtt.Client()
client.username_pw_set(conf.USER, conf.PASS)
client.on_connect = on_connect
client.on_message = on_message
client.connect(conf.HOST, conf.PORT, 60)
print(conf.logo)
client.loop_forever()
cnx.close()
