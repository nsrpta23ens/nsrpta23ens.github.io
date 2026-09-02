#2026july23thu tnhan@enersev MLw26mbrtuMs.py 2026au23su@MLw HN_MELI_NUOML1_20260716110000.txt
import os;import sys;import struct;import time;from datetime import datetime;import serial;from pathlib import Path #2026au23su@MLw
def i420ma2pv(b2): #2026au24mo@MLwTramBomRedRiver
    i=int.from_bytes(b2,byteorder='big');f=(float(i)-400)/1.6
    if f<0:f=0 #2026au31mo@e77
    return f 
def cdab2float(ab):
    cd=ab[2:4]+ab[0:2];return struct.unpack('>f',cd)[0]	#unpack as a32biFloat
def rs2pv(rs,i):
    j=3+i*4;return cdab2float(rs[j:j+4])
def dt2s(dt):
    return dt.strftime("%Y%m%d%H%M%S")#.%f");print(ts,end="")
def pmLogs(name,v,prec,unit,dt,sta):
    return name+"\t"+f"{v:.{prec}f}"+"\t"+unit+"\t"+dt2s(dt)+"\t"+sta
sPMname=["Flow in 1","TSS      ", "COD      ", "NH4+     ","DO       ","pH       ","Temp     "];   
sPMunit=["m3/h"     ,"mg/L"     ,"mg/L"      ,"mg/L"      , "mg/L"    ,"pH"       ,"°C"];     
fPMvalu=[0,0,0,0,0,0,0];fPMsum=[0,0,0,0,0,0,0];nPMcnt=[0,0,0,0,0,0,0];nPMtota=7
nPMprec=[0,2,2,2,2,2,1];fPMavg=[0,0,0,0,0,0,0];sCWD="";sFNprefix="HN_MELI_NUOML1";sFn2sv="";dt2sv=datetime.now()
def pmsHead():
    sh="DateTime"
    for i in range(nPMtota):sh+="\t"+sPMname[i]
    return sh
def pmsVals(dt,v):
    sv=dt2s(dt)
    for i in range(nPMtota):sv+="\t"+f"{v[i]:.{nPMprec[i]}f}"
    return sv
def upLf2sv(fn,dt):#192.168.1.149/X.%20PLANT%20DATA/7.MeLinhWater/MLwQlity  2026au27thu@e77
    c="curl -s -k --ftp-create-dirs -T "+fn;c+=" ftp://14.177.182.250/nuocmat/"+dt.strftime("%Y/")+dt.strftime("%m/")+dt.strftime("%d/")+' -u "250nmmelinh08980:Melinh@072026"'
    ec=os.system(c);print(c+"\t ec"+str(ec))
r1=bytes([1,3,0,0,0,2, 0xc4,0x0b]);rq=bytes([2,4,0,0,0,14,0x71,0xfd]) #([1,4,0,0,0,14,0x71,0xce]) #([1,4,0,0,0,10,0x70,0x0d])
while True:
    try:
        c="stty -F /dev/ttyS0 9600 cs8 -parenb -cstopb raw";ec=os.system(c)#;print(c+"\t ec"+str(ec))
        sp=serial.Serial("/dev/ttyS0",4800,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=0);time.sleep(1)
        #dt=datetime.now();print(dt2s(dt),end="");print("rq",end="");print(r1.hex())          
        sp.write(r1);time.sleep(1);n=sp.in_waiting   #FLOW
        rs=sp.read(n);sp.close();fPMvalu[0]=i420ma2pv(rs[5:7]);time.sleep(1)
        #dt=datetime.now();print(dt2s(dt),end="");print("fw",end="");print(rs.hex(),end="");print(" Len",end="");print(n)
        sp=serial.Serial("/dev/ttyS0",9600,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=0);time.sleep(1)
        #dt=datetime.now();print(dt2s(dt),end="");print("rq",end="");print(rq.hex())  
        sp.write(rq);time.sleep(1);n=sp.in_waiting  #k605  while True:time.sleep(0.1);n=sp.in_waiting;print(n,end="")if n<25:continue
        rs=sp.read(n);sp.close();np=(n-5)//4;#dt=datetime.now();print(dt2s(dt),end="");print("rs",end="");print(rs.hex(),end="");print(" Len",end="");print(n)
        dt=datetime.now();sCWD="/home/pi/"+sFNprefix+"/" #str(Path.cwd())+"/"
        for i in range(np-1):   fPMvalu[i+1]=rs2pv(rs,i+1)
        fn=sCWD+sFNprefix+"_"+dt.strftime("%Y%m%d%H")+"_PMsRecs.txt"
        if os.path.exists(fn)==False:
            with open(fn,"a") as f:f.write(pmsHead()+"\n")
        with open(fn,"a") as f:    f.write(pmsVals(dt,fPMvalu)+"\n")#
        fn=fc=sCWD+sFNprefix+"_";fn+=dt.strftime("%Y%m%d%H")+".txt";fc+="PMsCur.txt" #"0000.txt"
        if sFn2sv!="" and os.path.exists(fn)==False:
            upLf2sv(sFn2sv,dt2sv) #print(sFn2sv+" up2sv"+dt2sv.strftime("%Y%m%d%H%M%S"));
            for i in range(np):nPMcnt[i]=0;fPMsum[i]=0 #2026se2we@LvL
        sFn2sv=fn;dt2sv=dt;ss="";sc=""
        for i in range(np):
            nPMcnt[i]+=1;fPMsum[i]+=fPMvalu[i];fPMavg[i]=fPMsum[i]/nPMcnt[i]
            ss+=pmLogs(sPMname[i],fPMavg[i] ,nPMprec[i],sPMunit[i],dt,"01")+"\n"
            sc+=pmLogs(sPMname[i],fPMvalu[i],nPMprec[i],sPMunit[i],dt,"01")+"\n"
        with open(fn,"w") as f:f.write(ss)  #
        with open(fc,"w") as f:f.write(sc)
        #print(pmsHead());print(pmsVals(dt,fPMavg));print("cnt",end="");print(nPMcnt[0],end="");print(sFn2sv,end="");print(dt.strftime("%Y%m%d%H%M%S"))
        time.sleep(1)
    except Exception as e:  #2026au27thu@e77
    	sleep(5);continue   #except serial.SerialException as e:print(f"ERRopeningSP:{e}")    
    finally:sp.close()
