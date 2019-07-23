# mqtt broker
這是一個由MQTT(mosquitto or any other MQTT brokers)訂閱(subscribe)特定的主題(topic),然後將得到的message.payload解析開來,insert into mysql的項目。

## INSTALL
1. Python 3<br>
  require:<br>
```
    aiohttp==3.5.4
    mysql-connector-python==8.0.17
    paho-mqtt==1.4.0
```
2. MySQL<br>
```
  $ brew install mysql or
  $ apt-get install mysql-server...
  $ mysql.server start
  $ sudo mysql
  mysql> create user 'iot'@localhost identified by 'iot';
  mysql> grant all on *.* to iot@localhost;
```
  執行 create_tables.sql 建立需要的TABLES
## 施行
3. pa_packet.py 負責解析或是拼湊 message.payload
4. pa_rest.py 在此是要將topic+message經過 RESTFUL，轉給MQTT，否則沒資料可測試,<br>
案例：<br>
http://localhost:9000/pub?topic=001&cmd=SETM&data=[7]<br>
5. pa_sub.py 無窮的循環，訂閱TOPIC<br>
解析message,insert到mysql pabox.trandata<br>
案例：<br>
2019-07-23 17:46:26:PABOX/001={"NAME": "SETM", "CODE": "00", "SEQ": 0, "TYPE": "1", "DESC": "工作模式转换", "VALUE": [7]}<br>
insert into trandata OK





  

