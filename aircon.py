import sys
import json
import os


class ac_get:
    def __init__(self, file):
        self.status = {
            'CurrentTemperature': 0,
            # Minimum Value 0
            # Maximum Value 100
            # Step Value 0.1

            'SwingMode': 1,
            # 0 - "Swing disabled"
            # 1 - "Swing enabled"

            'RotationSpeed': 2,
            # Minimum Value: 0
            # Maximum Value: 100
            # Step Value: 1
            # Unit: percentage

            'TargetHeaterCoolerState': 3,
            # Valid Values
            # 0 - AUTO
            # 1 - HEAT
            # 2 - COOL

            'LockPhysicalControls': 4,
            # 0 - "Control lock disabled"
            # 1 - "Control lock enabled"

            'HeatingThresholdTemperature': 5,
            # Minimum Value: 0
            # Maximum Value: 25
            # Step Value: 0.1
            # Unit: celcius

            'CurrentHeaterCoolerState': 'COOLING',
            # 0 - INACTIVE
            # 1 - IDLE
            # 2 - HEATING
            # 3 - COOLING

            'CoolingThresholdTemperature': 7,
            # Minimum Value: 10
            # Maximum Value: 35
            # Step Value: 0.1
            # Unit: celcius

            'Active': 8,
            # 0 - "Inactive"
            # 1 - "Active"

            'TemperatureDisplayUnits': 0  # 0 - Celcius
        }

        contents = file.read()
        if contents == '':
            self.Save(file)
        else:
            self.ConvertFromJson(file)

    def ConvertFromJson(self, file):
        self.status = json.load(file)

    def Save(self, file):
        json.dump(self.status, file, ensure_ascii=False, indent=4,
                  sort_keys=True, separators=(',', ': '))

    def getValue(self, args):
        try:
            return self.status[args]
        except KeyError:
            raise ValueError('Invalid Value: {}'.format(args))


if __name__ == "__main__":

    # if os.path.exists("./acVariableHolder") == False:
    #     f = open('./acVariableHolder', 'w')
    #     f.close()

        # with open('/tmp/acVariableHolder', 'r+') as file:
    with open('./acVariableHolder', 'w+') as file:

        # if len(sys.argv) != 4:
        #    sys.exit(1)

        if sys.argv[1] == 'Get':
            get = ac_get(file)
            get.getValue(sys.argv[3])
            get.Save(file)
            print(get.getValue(sys.argv[3]))
            sys.exit(get.getValue(sys.argv[3]))

        sys.exit()
