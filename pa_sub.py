import paho.mqtt.client as mqtt
import mysql.connector
import json
import time
import pa_config as conf
import pa_packet
# $IME 下行, PABOX/$IME 上行
def on_connect(client, userdata, flags, rc):
    print("Connect MQTT: "+str(rc)+": Subscribe("+conf.SUB_TOPIC+"/#)")
    client.subscribe(conf.SUB_TOPIC+"/#")

def on_message(client, userdata, msg):
    pac = pa_packet.packet_obj()
    cursor = cnx.cursor()
    # pacobj={'NAME':__,'CODE':__,'SEQ':__,'TYPE':__,'DESC':__,'VALUE':[__]}
    pacobj=pac.parse_packet(msg.payload)
    topic=msg.topic
    topic_array=topic.split('/')
    iot_id=topic_array[1]
    now=time.strftime("%Y-%m-%d %X", time.localtime())
    print(now+':'+msg.topic+'='+json.dumps(pacobj,ensure_ascii=False,indent=None))
    pac=None
    # insert into mysql db
    r=(iot_id,pacobj['CODE'],pacobj['NAME'],pacobj['SEQ'],pacobj['TYPE'],pacobj['DESC'],str(pacobj['VALUE']))
    cursor.execute(add_info,r)
    cnx.commit()
    cursor.close()

#### Start Here
cnx = mysql.connector.connect(host=conf.MY_HOST,user=conf.MY_USER,passwd=conf.MY_PASS,database=conf.MY_DATABASE)
add_info=("INSERT INTO `pabox`.`trandata`(`iot_id`,`code`,`code_name`,`seq`,`attr01`,`desc`,`data`) VALUES (%s, %s, %s, %s, %s, %s, %s)")
client = mqtt.Client()
client.username_pw_set(conf.USER,conf.PASS)
client.on_connect = on_connect
client.on_message = on_message
client.connect(conf.HOST, conf.PORT, 60)
client.loop_forever()
cnx.close()

