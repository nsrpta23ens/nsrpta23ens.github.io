# 2026au31mo@e77-MLw26mbTCPsvr.py tnhan@enersev
import threading;import time;from pyModbusTCP.server import ModbusServer #,DataBank from datetime import datetime;
MBtcpSvr=ModbusServer(host="0.0.0.0",port=5022,no_block=True)
def updRegs():#print("BackgroundThread started.modifying inRegs..")
    while True:#generate some randomized SensorReadings temp=random.randint(0,999);#humi=random.randint(45,65)
        m3h=0 #dt=datetime.now()    # DataBank.set_List_words(addr,[List_of_16bit_ints]) #sets inRegs starting@aGivenAddress offset
        #DataBank.set_list_words(0,[dt.second]) #,humi]) #print(f"[SvrStatus]updRegs:Temp={temp}°C,Humid={humi}%")
        with open("/home/pi/HN_MELI_NUOML1/HN_MELI_NUOML1_PMsCur.txt","r") as f: #HN_MELI_NUOML1_PMsCur.txt
            Line=f.readline();m3h=int(Line.split("\t")[1])
            MBtcpSvr.data_bank.set_input_registers(0,[m3h]);time.sleep(3)
if __name__ == "__main__":
    try:
        updThread=threading.Thread(target=updRegs,daemon=True);updThread.start()
        MBtcpSvr.start() #print(f"startingModbusTCPsvr on{SVR_HOST}:{SVR_PORT}..ctrlC2exit")
        while True:#keepMainProcess alive
            time.sleep(0.5)
    except:print(" anException occurred ") #KeyboardInterrupt:print("\nshuttingDown-ModbusTCPsvr..");server.stop();print("SVRoffline")
    finally:MBtcpSvr.stop() 
