import sys
import json
import os
import subprocess
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN
import math


def my_round(x, d=0):
    p = 10 ** d
    return int(float(math.floor((x * p) + math.copysign(0.5, x)))/p)


class ac_get:
    CurrentTemperature = 26

    def __init__(self, file):
        self.status = {
            "CurrentTemperature": self.CurrentTemperature,
            # Minimum Value 0
            # Maximum Value 100
            # Step Value 0.1

            "SwingMode": 0,
            # 0 - "Swing disabled"
            # 1 - "Swing enabled"

            "RotationSpeed": 2,
            # Minimum Value: 0
            # Maximum Value: 100
            # Step Value: 1
            # Unit: percentage

            "TargetHeaterCoolerState": 2,
            # Valid Values
            # 0 - AUTO
            # 1 - HEAT
            # 2 - COOL

            "LockPhysicalControls": 0,
            # 0 - "Control lock disabled"
            # 1 - "Control lock enabled"

            "HeatingThresholdTemperature": 25,
            # Minimum Value: 0
            # Maximum Value: 25
            # Step Value: 0.1
            # Unit: celcius

            "CurrentHeaterCoolerState": 3,
            # 0 - INACTIVE
            # 1 - IDLE
            # 2 - HEATING
            # 3 - COOLING

            "CoolingThresholdTemperature": 26,
            # Minimum Value: 10
            # Maximum Value: 35
            # Step Value: 0.1
            # Unit: celcius

            "Active": 0,
            # 0 - "Inactive"
            # 1 - "Active"

            "TemperatureDisplayUnits": 0  # 0 - Celcius
        }

        self.contents = file.read()

        if self.contents == '':
            pass

        else:
            self.ConvertFromJson(file)

    def ConvertFromJson(self, file):
        self.status = json.loads(self.contents)

    def Save(self, file):
        print(self.status)
        file.seek(0)
        file.write('')
        json.dump(self.status, file, ensure_ascii=False, indent=4)

    def getValue(self, args):
        try:
            return self.status[args]
        except KeyError:
            raise ValueError('Invalid Value: {}'.format(args))


class cool_set(ac_get):
    def __init__(self, file):
        super(cool_set, self).__init__(file)
        self.__STATUS = 'Cool'

    def SetValue(self, arg3, arg4):
        if arg3 == '{}ingThresholdTemperature'.format(self.__STATUS):
            self.ChangeTenperature(arg4)
        elif arg3 == 'Active':
            self.ChangeActive(arg4)

    def ChangeTenperature(self, temp):
        rounded = my_round(float(temp))
        cmd = 'python3 ~/pigpio/irrp2.py -p -g17 -f ~/pigpio/aircon_{0} ac:{1}'.format(self.__STATUS,
                                                                                       rounded)
        res = subprocess.run(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # print(f'{i},{res.stdout.decode("utf8")}')
        self.status['{}ingThresholdTemperature'.format(
            self.__STATUS)] = rounded
        self.CurrentTemperature = rounded
        print(rounded)
        self.Save(file)

    def ChangeActive(self, value):
        if value == '0':
            onoff = 'off'
        else:
            onoff = 'on'

        cmd = 'python3 ~/pigpio/irrp2.py -p -g17 -f ~/pigpio/aircon_{0} ac:{1}'.format(self.__STATUS,
                                                                                       onoff)
        res = subprocess.run(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.status['Active'] = value
        print(value)
        self.Save(file)


if __name__ == "__main__":
    with open('./test.txt', 'r+') as file:
        f = open('./test.txt', "a")

    for i in sys.argv:
        text = i + ' '
        f.write(text)

    f.write('\n')

    if os.path.exists('/tmp/acVariableHolder') == False:
        cmd = 'touch /tmp/acVariableHolder'
        res = subprocess.run(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    with open('/tmp/acVariableHolder', 'r+') as file:
        # with open('./acVariableHolder', 'w+') as file:

        # if len(sys.argv) != 5:
        #    sys.exit(1)

        if sys.argv[1] == 'Get':
            get = ac_get(file)
            print(get.getValue(sys.argv[3]))
            # get.Save(file)
            sys.exit(0)

        if sys.argv[1] == 'Set':
            set = cool_set(file)
            set.SetValue(sys.argv[3], sys.argv[4])
            sys.exit()

        sys.exit()
