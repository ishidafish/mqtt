import paho.mqtt.publish as pahopublish
import asyncio
import json
from aiohttp import web
import pa_packet
import pa_config as conf
# $IME 下行, PABOX/$IME 上行
# http://localhost:9000/pub?topic=mytopic&cmd=SETM&data=[0]
# curl http://localhost:9000/pub?topic=mytopic&cmd=SETM&data=[0]

routes = web.RouteTableDef()
@routes.get('/')
async def index(request):
    return web.Response(text="Hello mosquitto restful Server")

@routes.get('/pub')
async def pub(request):
    pac = pa_packet.packet_obj()
    try:
        topic = request.query['topic'] 
        topic = topic.replace('.','/')
        cmd = request.query['cmd']
        data = request.query['data'] if request.query.__contains__('data') else []
        data_array=json.loads(data)
        message=pac.compose_cmd(cmd,data_array)
        pahopublish.single(
            topic=conf.SUB_TOPIC+'/'+topic, # prefix = conf.SUB_TOPIC
            payload=message, 
            qos = conf.QoS, 
            hostname=conf.HOST, 
            port=conf.PORT, 
            auth = {'username':conf.USER, 'password':conf.PASS})
        return web.Response(text=conf.SUB_TOPIC+'/'+topic+":"+cmd+", "+data)
    except:
        pac=None
        return web.Response(text="参数不对,ex: pub?topic=mytopic&cmd=SETM&data=[0]")

@routes.get('/info')
async def info(request):
    msg=json.dumps(pa_packet.cmdict, ensure_ascii=False,indent=2)
    return web.Response(text=msg)

app = web.Application()
app.add_routes(routes)
web.run_app(app, host='0.0.0.0', port=conf.HTTP)

