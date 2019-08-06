import struct
import time
# $IME 下行, PABOX/$IME 上行
PACKET_HEAD=b'\x55\x8A'
PACKET_TAIL=b'\xFE\xAA'
codeDict={
    '00':{"NAME":"SETM","TYPE":"1","DESC":"工作模式转换"}, # 1 自控 0, 外控 1
    '01':{"NAME":"PING","TYPE":"2","DESC":"连接握手(sec)"}, # 2 秒数
    '02':{"NAME":"TSYN","TYPE":"7","DESC":"时间同步"}, # 7 year_2+mon_1+mday_1+hour_1+min_1+sec_1, 7bytes
    '03':{"NAME":"OFF_","TYPE":"0","DESC":"断开连接"}, # 0
    '04':{"NAME":"GETT","TYPE":"1,2","DESC":"获取温度(°C)"}, # 1+2   通道+温度
    '05':{"NAME":"SETT","TYPE":"1,2,2","DESC":"设置温度上限和下限参数(°C)"}, # 1+2+2 通道+温度上限和温度
    '06':{"NAME":"GETF","TYPE":"1,2","DESC":"获取风扇状态(mA)"}, # 1+2 风扇电流
    '07':{"NAME":"SETF","TYPE":"1,1","DESC":"控制风扇动作"}, # 1+1 控制风扇动作
    '08':{"NAME":"GETL","TYPE":"1,1","DESC":"查询锁的状态"}, # 1+1 通道+锁状态
    '09':{"NAME":"SETL","TYPE":"1,1","DESC":"控制开锁动作"}, # 1+1 通道+锁动作
    '0A':{"NAME":"BIND","TYPE":"1,1","DESC":"绑定风扇和温度控制"}, # 1+1 风扇通道+温度通道
    '0B':{"NAME":"LOG_","TYPE":"0,-1","DESC":"终端日志获取"}, # 0 
    '0C':{"NAME":"GPS_","TYPE":"0,-1","DESC":"GPS定位经纬度信息"}, # 0 DDDDDddddNDDDDDddddE
    '0D':{"NAME":"TCOM","TYPE":"2","DESC":"通信时间间隔(sec)"}, # 2 
    '0E':{"NAME":"TSEN","TYPE":"2","DESC":"数据采集唤醒间隔(sec)"}, # 2 
    '0F':{"NAME":"VBAT","TYPE":"2","DESC":"电池电压与电量(mV)"}, # 2 
    '10':{"NAME":"VOUT","TYPE":"2","DESC":"外来电压(mV)"}, # 2
    '11':{"NAME":"SIGN","TYPE":"1","DESC":"通信信号强度(0~31)"}, # 1
    '12':{"NAME":"CIMI","TYPE":"0,-1","DESC":"SIM卡CIMI码"}, # 0
    '13':{"NAME":"FXMA","TYPE":"2","DESC":"风扇最大的工作电流(mA)"}, # 2
    '14':{"NAME":"DOWA","TYPE":"2","DESC":"舱门开启告警时间设定(sec)"}, # 2
    '15':{"NAME":"TWAR","TYPE":"1,2","DESC":"温度通道告警设置(°C)"}, # 1 + 2 通道+温度
    '80':{"NAME":"VLOW","TYPE":"2","DESC":"电池过低(mV)"}, # 2 mV
    '81':{"NAME":"FLOW","TYPE":"2","DESC":"风扇堵转或者故障(mA)"}, # 2 mA
    '82':{"NAME":"DOAL","TYPE":"2","DESC":"舱门开启时间过长告警(sec)"}, # s
    '83':{"NAME":"DOTI","TYPE":"2","DESC":"舱门开启动作(sec)"}, # 2 
    '84':{"NAME":"VOVA","TYPE":"2","DESC":"外供电开始(mV)"}, # 2 mV
    '85':{"NAME":"T_AL","TYPE":"1,2","DESC":"箱体温度告警(°C)"}, # 1+2 温度*10
    'F0':{"NAME":"_ON_","TYPE":"7","DESC":"数控启动"},  # 7 year_2+mon_1+mday_1+hour_1+min_1+sec_1, 7bytes
    }

class Tpacket():
    def __init__(self,seq=0, head=PACKET_HEAD, tail=PACKET_TAIL):
        global codeDict
        self.seq, self.head, self.tail, self.bindata = 0, head, tail, bytes()
        self.data =dict()
    def __str__(self):
        s = ["%02X"%b for b in self.bindata]
        return (" ".join(s))
    def compose(self,code,seq=-1, data=[]):
        global codeDict
        _seq = self.seq if seq == -1 else seq
        p_seq_code = struct.pack("2B", _seq % 256, int(code,16))
        p_type = codeDict[code]["TYPE"]
        self.seq += 1
        if p_type=='2': 
            p_data=struct.pack("h",data[0]) # < 表示low byte在前
        elif p_type=='1':
            p_data=struct.pack("B",data[0])
        elif p_type=='7':
            t = time.localtime(time.time())
            p_data=struct.pack("h",t.tm_year)+ struct.pack("5B",t.tm_mon,t.tm_mday,t.tm_hour,t.tm_min,t.tm_sec)
        elif p_type=='1,2':
            p_data=struct.pack("B",data[0]) + struct.pack("h",data[1])
        elif p_type=='1,2,2':
            p_data=struct.pack("B",data[0]) + struct.pack("2h",data[1],data[2])
        elif p_type=='1,1':
            p_data=struct.pack("2B",data[0],data[1])
        elif p_type=='0':
            p_data=bytes()
        elif p_type=='0,-1':
            p_data=data[0].encode('utf8')
        checksum , p_data_len = 0 , 0 if data is None else len(p_data)
        dummy = bytes([4+p_data_len]) + p_seq_code + p_data if p_data_len>0 else bytes([])
        for b in dummy: checksum ^= b
        self.bindata=self.head+ dummy + bytes([checksum])+ self.tail
        return self.bindata
    def parse(self,pac): # length + seq + code + data
        self.data={}
        if pac[0:2]!=PACKET_HEAD or pac[-2:]!=PACKET_TAIL or len(pac)<8:
            return self.data
        length,seq,code = pac[2],pac[3],"%02X"%pac[4]
        cr=codeDict[code]
        lsum=sum([int(x) for x in cr['TYPE'].split(',')])
        self.data={'NAME':cr['NAME'],'CODE':code,'SEQ':seq,'TYPE':cr['TYPE'],'DESC':cr['DESC'],'VALUE':[]}
        if lsum+8 != len(pac) and lsum >0:
            return self.data
        try:
            tt=cr['TYPE']
            varr=[]
            if tt=="2":
                varr.append(int.from_bytes(pac[5:7], byteorder='little', signed=True))
            elif tt=="1,1":
                varr.append(pac[5])
                varr.append(pac[6])
            elif tt=="1":
                varr.append(pac[5])
            elif tt=="7":
                varr.append(int.from_bytes(pac[5:7], byteorder='little', signed=True))
                for i in range(0,5):
                    varr.append(pac[i+7])
            elif tt=="0":
                pass
            elif tt=="0,-1":
                varr.append(pac[5:(length+1)])
            elif tt=="1,2":
                varr.append(pac[5])
                varr.append(int.from_bytes(pac[6:8], byteorder='little', signed=True))
            elif tt=="1,2,2":
                varr.append(pac[5])
                varr.append(int.from_bytes(pac[6:8],  byteorder='little', signed=True))
                varr.append(int.from_bytes(pac[8:10], byteorder='little', signed=True))
        except:
            pass
        self.data['VALUE']=varr
        return self.data

if __name__ == "__main__":
    import json
    pac=Tpacket()
    bindata = pac.compose("02",-1,[])
    print(pac)
    pac.parse(bindata)
    print(pac.data)

    bindata = pac.compose("05",-1,[1,-200,300])
    print(pac)
    pac.parse(bindata)
    print(pac.data)
    bindata = pac.compose("07",-1,[1,2])
    print(pac)
    pac.parse(bindata)
    print(pac.data)
    '''
    pj=k.parse_packet(pac)
    print(json.dumps(pj, ensure_ascii=False,indent=1))
'''
