import struct
import time
import json
# $IME 下行, PABOX/$IME 上行
PACKET_HEAD=b'\x55\x8A'
PACKET_TAIL=b'\xFE\xAA'
cmdict={
    "SETM":{"CODE":'00',"TYPE":"1","DESC":"工作模式转换"}, # 1 自控 0, 外控 1
    "PING":{"CODE":'01',"TYPE":"2","DESC":"连接握手(sec)"}, # 2 秒数
    "TSYN":{"CODE":'02',"TYPE":"7","DESC":"时间同步"}, # 7 year_2+mon_1+mday_1+hour_1+min_1+sec_1, 7bytes
    "OFF_":{"CODE":'03',"TYPE":"0","DESC":"断开连接"}, # 0
    "GETT":{"CODE":'04',"TYPE":"1,2","DESC":"获取温度(°C)"}, # 1+2   通道+温度
    "SETT":{"CODE":'05',"TYPE":"1,2,2","DESC":"设置温度上限和下限参数(°C)"}, # 1+2+2 通道+温度上限和温度
    "GETF":{"CODE":'06',"TYPE":"1,2","DESC":"获取风扇状态(mA)"}, # 1+2 风扇电流
    "SETF":{"CODE":'07',"TYPE":"1,1","DESC":"控制风扇动作"}, # 1+1 控制风扇动作
    "GETL":{"CODE":'08',"TYPE":"1,1","DESC":"查询锁的状态"}, # 1+1 通道+锁状态
    "SETL":{"CODE":'09',"TYPE":"1,1","DESC":"控制开锁动作"}, # 1+1 通道+锁动作
    "BIND":{"CODE":'0A',"TYPE":"1,1","DESC":"绑定风扇和温度控制"}, # 1+1 风扇通道+温度通道
    "LOG_":{"CODE":'0B',"TYPE":"0,N","DESC":"终端日志获取"}, # 0 
    "GPS_":{"CODE":'0C',"TYPE":"0,N","DESC":"GPS定位经纬度信息"}, # 0 DDDDDddddNDDDDDddddE
    "TCOM":{"CODE":'0D',"TYPE":"2","DESC":"通信时间间隔(sec)"}, # 2 
    "TSEN":{"CODE":'0E',"TYPE":"2","DESC":"数据采集唤醒间隔(sec)"}, # 2 
    "VBAT":{"CODE":'0F',"TYPE":"2","DESC":"电池电压与电量(mV)"}, # 2 
    "VOUT":{"CODE":'10',"TYPE":"2","DESC":"外来电压(mV)"}, # 2
    "SIGN":{"CODE":'11',"TYPE":"1","DESC":"通信信号强度(0~31)"}, # 1
    "CIMI":{"CODE":'12',"TYPE":"0,N","DESC":"SIM卡CIMI码"}, # 0
    "FXMA":{"CODE":'13',"TYPE":"2","DESC":"风扇最大的工作电流(mA)"}, # 2
    "DOWA":{"CODE":'14',"TYPE":"2","DESC":"舱门开启告警时间设定(sec)"}, # 2
    "TWAR":{"CODE":'15',"TYPE":"1,2","DESC":"温度通道告警设置(°C)"}, # 1 + 2 通道+温度
    "VLOW":{"CODE":'80',"TYPE":"2","DESC":"电池过低(mV)"}, # 2 mV
    "FLOW":{"CODE":'81',"TYPE":"2","DESC":"风扇堵转或者故障(mA)"}, # 2 mA
    "DOAL":{"CODE":'82',"TYPE":"2","DESC":"舱门开启时间过长告警(sec)"}, # s
    "DOTI":{"CODE":'83',"TYPE":"2","DESC":"舱门开启动作(sec)"}, # 2 
    "VOVA":{"CODE":'84',"TYPE":"2","DESC":"外供电开始(mV)"}, # 2 mV
    "T_AL":{"CODE":'85',"TYPE":"1,2","DESC":"箱体温度告警(°C)"}, # 1+2 温度*10
    }

datdict={}
class packet_obj():
    def __init__(self,seq=0, head=PACKET_HEAD, tail=PACKET_TAIL):
        global datdict,cmdict
        self.seq, self.head, self.tail, self.packetdata = 0, head, tail, bytes()
        self.data =dict()
    def __str__(self):
        s = ["%02X"%b for b in self.packetdata]
        return self.codename+":"+(" ".join(s))
    def initdat(self):
        for k,v in cmdict.items():
            datdict[v['CODE']]={'NAME':k,'TYPE':v['TYPE'],'DESC':v['DESC']}
    def encode(self,code,seq,data=None):
        checksum , data_len = 0 , 0 if data is None else len(data)
        length = bytes([4+data_len])
        dummy = length + seq + code 
        if data_len>0: dummy = dummy + data
        for b in dummy: checksum ^= b
        return self.head+ dummy + bytes([checksum])+ self.tail
    def compose_cmd(self,codename,data=[]):
        global cmdict
        self.codename=codename
        p_seq = struct.pack("B", self.seq %256)
        p_code= struct.pack("B",int(cmdict[codename]["CODE"],16))
        p_type = cmdict[codename]["TYPE"]
        self.seq += 1
        if p_type=='2': # 2 bytes:
            p_data=struct.pack("<h",data[0]) # < 表示low byte在前
        elif p_type=='1': # 1
            p_data=struct.pack("B",data[0])
        elif p_type=='7':
            t = time.localtime(time.time())
            p_data=struct.pack("<h",t.tm_year)+struct.pack("B",t.tm_mon)+struct.pack("B",t.tm_mday)
            p_data=p_data+struct.pack("B",t.tm_hour)+struct.pack("B",t.tm_min)+struct.pack("B",t.tm_sec)
        elif p_type=='1,2': # 1 + 2
            p_data=struct.pack("B",data[0])+struct.pack("<h",data[1])
        elif p_type=='1,2,2': # 1 + 2 + 2
            p_data=struct.pack("B",data[0])+struct.pack("<h",data[1])+struct.pack("<h",data[2])
        elif p_type=='1,1':
            p_data=struct.pack("B",data[0])+struct.pack("B",data[1])
        elif p_type=='0' or p_type=='0,N':
            p_data=bytes()
        self.packetdata=self.encode(p_code,p_seq,p_data)
        return self.packetdata
    def parse_packet(self,pac): # length + seq + code + data
        self.data={}
        if pac[0:2]!=PACKET_HEAD or pac[-2:]!=PACKET_TAIL or len(pac)<8:
            return self.data
        length,seq,code=pac[2],pac[3],"%02X"%pac[4]
        desc, name, type= datdict[code]['DESC'],datdict[code]['NAME'],datdict[code]['TYPE']
        varr=[]
        if type=="2":
            if len(pac)!=10:
                return self.data
            else:
                varr.append(int.from_bytes(pac[5:7], byteorder='little', signed=True))
        elif type=="1,1":
            if len(pac)!=10:
                return self.data
            else:
                varr.append(pac[5])
                varr.append(pac[6])
        elif type=="1":
            if len(pac)!=9:
                return self.data
            else:
                varr.append(pac[5])
        elif type=="7":
            if len(pac)!=15:
                return self.data
            else:
                varr.append(int.from_bytes(pac[5:7], byteorder='little', signed=True))
                for i in range(0,5):
                    varr.append(pac[i+7])
        elif type=="0":
            pass
        elif type=="0,N":
            varr.append(''.join(chr(b) for b in pac[5:(length+1)]))
        elif type=="1,2":
            if len(pac)!=11:
                return self.data
            else:
                varr.append(pac[5])
                varr.append(int.from_bytes(pac[6:8], byteorder='little', signed=True))
        elif type=="1,2,2":
            if len(pac)!=13:
                return self.data
            else:
                varr.append(pac[5])
                varr.append(int.from_bytes(pac[6:8],  byteorder='little', signed=True))
                varr.append(int.from_bytes(pac[8:10], byteorder='little', signed=True))
        self.data={name:{'CODE':code,'SEQ':seq,'TYPE':type,'DESC':desc,'VALUE':varr}}
        return self.data

if __name__ == "__main__":
    k=packet_obj()
    k.initdat()
    pac=k.compose_cmd("VOUT",[120])
    print(k)
    pj=k.parse_packet(pac)
    print(json.dumps(pj, ensure_ascii=False,indent=1))

    pac=k.compose_cmd("SETF",[1,10])
    print(k)
    pj=k.parse_packet(pac)
    print(json.dumps(pj, ensure_ascii=False,indent=1))

    pac=k.compose_cmd("SETM",[1])
    print(k)
    pj=k.parse_packet(pac)
    print(json.dumps(pj, ensure_ascii=False,indent=1))

    pac=k.compose_cmd("TSYN",[])
    print(k)
    pj=k.parse_packet(pac)
    print(json.dumps(pj, ensure_ascii=False,indent=1))
    
    cc=b'\x55\x8A\x0B\x01\x0B\x41\x42\x61\x62\x63\x21\x39\xD5\xFE\xAA'
    pj=k.parse_packet(cc)
    print(json.dumps(pj, ensure_ascii=False,indent=1))

    pac=k.compose_cmd("GETT",[1,-230])
    print(k)
    pj=k.parse_packet(pac)
    print(json.dumps(pj, ensure_ascii=False,indent=1))

    pac=k.compose_cmd("SETT",[1,-230,300])
    print(k)
    pj=k.parse_packet(pac)
    print(json.dumps(pj, ensure_ascii=False,indent=1))
