import sys
from reset import Reset
from boom import Boom, Imu, Servo

imu = Imu()
servo = Servo()

try:
    boom = Boom(imu=imu, servo=servo)
    boom.run()
except KeyboardInterrupt as e:
    sys.print_exception(e)
except Exception as e:
    sys.print_exception(e)

Reset.start(imu=imu, servo=servo)
