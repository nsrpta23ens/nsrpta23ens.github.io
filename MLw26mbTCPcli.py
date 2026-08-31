# 2026au31mo@e77-MLw26mbTCPcli.py tnhan@enersv
from pyModbusTCP.client import ModbusClient #initialize ModbusTCPcli # auto_open=True automatically connects/reconnects4eachRequest
MBtcpCli=ModbusClient(host="127.0.0.1",port=5022,unit_id=1,auto_open=True)
#startAddr=0;nRegs=4 #sefine StartingRegisterAddr &how manyRegisters2r #r_inRegs(MBfc04)returns aList of integers|None ifRequest fails
Reg=MBtcpCli.read_input_registers(0,1)
if Reg:print(Reg)  #outputs aListLike [124,0,4522,12]
else:print("ERR:failed2r-inReg")
