import sht21
with sht21.SHT21(1) as sht21:
    print "temp: %s"%sht21.read_temperature()
    print "humi: %s"%sht21.read_humidity()
