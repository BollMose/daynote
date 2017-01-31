#encoding=utf-8
import os
import sqlite3
import serial  
import time
from struct import *

print "Opening Serial Port...",
# ser = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=2.0)
ser = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=2.0)
print "Serial Connected"

def read_pm_line(_port):
    rv = b''
    while True:
        ch1 = _port.read()
        if ch1 == b'\x42':
            ch2 = _port.read()
            if ch2 == b'\x4d':
                rv += ch1 + ch2
                rv += _port.read(30)
                return rv

def main(): 
    cnt = 0
    conn = sqlite3.connect('pm25.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tpms
             (date integer, 
	     pmcf10 integer, pmcf25 integer, pm100cf integer, 
	     pm10 integer, pm25 integer, pm100 integer, 
	     r03 integer, r05 integer, r10 integer, 
	     r25 integer, r50 integer, r100 integer 
	     )''')
    while True:  
        recv = read_pm_line(ser)

        cnt = cnt + 1
        print "[%d]Recieve Data" % cnt,
        print len(recv), "Bytes:",
        tmp = recv[2:4]
        datas = unpack('>h', tmp)
	if datas[0] != 28:
	    print '\n====error====recv:', str(datas[0])
	    return
        tmp = recv[4:30]
        datas = unpack('>hhhhhhhhhhhhh', tmp)
        # print datas
        os.system('clear') 
        print('\n======= PMS7003 ========\n'
              'PM1.0(CF=1): {}\n'
              'PM2.5(CF=1): {}\n'
              'PM10 (CF=1): {}\n'
              'PM1.0 (STD): {}\n'
              'PM2.5 (STD): {}\n'
              'PM10  (STD): {}\n'
              '>0.3um     : {}\n'
              '>0.5um     : {}\n'
              '>1.0um     : {}\n'
              '>2.5um     : {}\n'
              '>5.0um     : {}\n'
              '>10um      : {}\n'
              .format(datas[0], datas[1], datas[2],
                                       datas[3], datas[4], datas[5],
                                       datas[6], datas[7], datas[8],
                                       datas[9], datas[10], datas[11]))
        ser.flushInput()
	datetime = round(time.time()*1000)

        c.execute("INSERT INTO tpms VALUES ({},{},{},{},{},{},{},{},{},{},{},{},{})".format(datetime, 
	datas[0],datas[1],datas[2],
	datas[3],datas[4],datas[5],
	datas[6],datas[7],datas[8],
	datas[9],datas[10],datas[11]))
        conn.commit()
        time.sleep(0.1)  
    #

if __name__ == '__main__':  
    try:  
        main()  
    except KeyboardInterrupt:  
        if ser != None:  
            ser.close()
