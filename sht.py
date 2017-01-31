    def _get_humidity_from_buffer(data):
        """This function reads the first two bytes of data and returns
        the relative humidity in percent by using the following function:
        RH = -6 + (125 * (SRH / 2 ^16))
        where SRH is the value read from the sensor
        """
        unadjusted = (ord(data[0]) << 8) + ord(data[1])
        unadjusted &= SHT21._STATUS_BITS_MASK  # zero the status bits
        unadjusted *= 125.0
        unadjusted /= 1 << 16  # divide by 2^16
        unadjusted -= 6
        return unadjusted


class SHT21Test(unittest.TestCase):
    """simple sanity test.  Run from the command line with
    python -m unittest sht21 to check they are still good"""

    def test_temperature(self):
        """Unit test to check the checksum method"""
        calc_temp = SHT21._get_temperature_from_buffer([chr(99), chr(172)])
        self.failUnless(abs(calc_temp - 21.5653979492) < 0.1)

    def test_humidity(self):
        """Unit test to check the humidity computation using example
        from the v4 datasheet"""
        calc_temp = SHT21._get_humidity_from_buffer([chr(99), chr(82)])
        self.failUnless(abs(calc_temp - 42.4924) < 0.001)

    def test_checksum(self):
        """Unit test to check the checksum method.  Uses values read"""
        self.failUnless(SHT21._calculate_checksum([chr(99), chr(172)], 2) == 249)
        self.failUnless(SHT21._calculate_checksum([chr(99), chr(160)], 2) == 132)

if __name__ == "__main__":
    try:
        with SHT21(0) as sht21:
            print "Temperature: %s" % sht21.read_temperature()
            print "Humidity: %s" % sht21.read_humidity()
    except IOError, e:
        print e
        print "Error creating connection to i2c.  This must be run as root"
