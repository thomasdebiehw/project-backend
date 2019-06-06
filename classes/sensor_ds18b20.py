import time


class SensorDS18B20:
    def __init__(self, sensor_file_name = '/sys/bus/w1/devices/w1_bus_master1/28-0117b04414ff/w1_slave'):
        self.sensor_file_name = sensor_file_name

    def __read_raw(self):
        f = open(self.sensor_file_name, 'r')
        lines = f.readlines()
        f.close()
        return lines

    def read_temp(self):
        lines = self.__read_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self.__read_raw()
        temp_output = lines[1].find('t=')
        if temp_output != -1:
            temp_string = lines[1].strip()[temp_output+2:]
            temp_c = float(temp_string) / 1000
            return temp_c
