#!/usr/local/bin/python3
import paho.mqtt.publish as pahopublish
import asyncio
import json, time
from aiohttp import web
import pa_packet
import pa_config as conf
import mysql.connector
# $IME 下行, PABOX/$IME 上行
# http://localhost:9000/pub?topic=[_]mytopic&cmd=SETM&data=[0]
# http://localhost:9000/cmd
# http://localhost:9000/query/trandata[item]
# curl -v --globoff http://localhost:9000/pub?topic=[_]mytopic\&cmd=SETM\&data=[0]

routes = web.RouteTableDef()
@routes.get('/')
async def index(request):
    return web.Response(text="Welcome to mosquitto restful Server")

@routes.get('/pub')
async def pub(request):
    global seq
    seq += 1
    pac = pa_packet.packet_obj(seq=seq)
    try:
        topic = request.query['topic'] 
        topic = topic.replace('.','/')
        cmd = request.query['cmd']
        if request.query.__contains__('data'):
            data_array = json.loads(request.query['data'])
        else:
            data_array = []
        message = pac.compose_cmd(cmd,-1,data_array)
        if topic[0:1]=='_': # conf.SUB_TOPIC
            topic = conf.SUB_TOPIC+'/' + topic[1:]            
        pahopublish.single(topic= topic, payload=message, qos = conf.QoS, hostname=conf.HOST, port=conf.PORT, auth = {'username':conf.USER, 'password':conf.PASS})
    except:
        pac=None
        return web.Response(text="参数不对,ex: pub?topic=[_]mytopic&cmd=SETM&data=[0]")
    else:
        pac=None
        now=time.strftime("%Y-%m-%d %X", time.localtime())
        print(now+":Publish:"+topic+' message:'+cmd+"+"+str(data_array))
        return web.Response(text='('+str(seq)+')'+topic+":"+cmd+", "+ str(data_array))

@routes.get('/cmd')
async def cmd(request):
    msg="COMMAND:\n"+json.dumps(pa_packet.cmdict, ensure_ascii=False,indent=2) + "\n---\n"
    msg= msg + "QUERY:\n" + json.dumps(conf.GET_SQL, ensure_ascii=False,indent=2) + "\n---\n"
    return web.Response(text=msg)

@routes.get('/query/{sqlname}')
#@routes.get('/query/{sqlname}/{param}')
async def query(request):
    try:
        print(request.match_info)
        q=request.match_info.get('sqlname', "")
        sql=conf.GET_SQL[q]
        cursor = cnx.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        result_array=[]
        for row in results:  # 也许要加 csv的方式
            result_array.append(mapdict(cursor.column_names, row))
        cursor.close()
        return web.Response(text=json.dumps(result_array, ensure_ascii=False,indent=2))
    except:
        return web.Response(text="参数不对,ex: query/trandata")

def mapdict(keys,vals):
    try:
        i ,dummy=0, {}
        for key in keys:
            dummy[key]=str(vals[i])
            i += 1
        return dummy
    except:
        return {}     

seq=0
cnx = mysql.connector.connect(host=conf.MY_HOST,user=conf.MY_USER,passwd=conf.MY_PASS,database=conf.MY_DATABASE)
app = web.Application()
app.add_routes(routes)
web.run_app(app, host='0.0.0.0', port=conf.HTTP)
cnx.close()

