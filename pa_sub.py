import paho.mqtt.client as mqtt
import json
import pa_config as conf
import pa_packet
# $IME 下行, PABOX/$IME 上行
def on_connect(client, userdata, flags, rc):
    print("连接MQTT "+str(rc)+":"+conf.SUB_TOPIC)
    client.subscribe(conf.SUB_TOPIC+"/#")

def on_message(client, userdata, msg):
    pac = pa_packet.packet_obj()
    pac.initdat()
    #{$KEY:{'CODE':__,'SEQ':__,'TYPE':__,'DESC':__,'VALUE':[__]}}
    pacobj=pac.parse_packet(msg.payload) 
    print(msg.topic)
    print(json.dumps(pacobj, ensure_ascii=False,indent=1))
    pac=None
    # insert into mysql db

client = mqtt.Client()
client.username_pw_set(conf.USER,conf.PASS)
client.on_connect = on_connect
client.on_message = on_message

client.connect(conf.HOST, conf.PORT, 60)
client.loop_forever()
'''
pip install mysql-connector-python
import mysql.connector
cnx = mysql.connector.connect(user='scott', database='employees')
cursor = cnx.cursor()
tomorrow = datetime.now().date() + timedelta(days=1)
add_employee = ("INSERT INTO employees "
               "(first_name, last_name, hire_date, gender, birth_date) "
               "VALUES (%s, %s, %s, %s, %s)")
add_salary = ("INSERT INTO salaries "
              "(emp_no, salary, from_date, to_date) "
              "VALUES (%(emp_no)s, %(salary)s, %(from_date)s, %(to_date)s)")
data_employee = ('Geert', 'Vanderkelen', tomorrow, 'M', date(1977, 6, 14))
cursor.execute(add_employee, data_employee)
emp_no = cursor.lastrowid
data_salary = {
  'emp_no': emp_no,
  'salary': 50000,
  'from_date': tomorrow,
  'to_date': date(9999, 1, 1),
}
cursor.execute(add_salary, data_salary)
cnx.commit()
cursor.close()
cnx.close()
'''
