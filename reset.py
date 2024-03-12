""" The Pico and uPython seem to get stuck with threading.
    This class is here as a reset method. Otherwise the 
    flash has to be wiped and all files reloaded.
"""

import os
import sys
import utime
import machine
from boom import Imu, Servo

class Reset:
    TMP_MAIN = "_rst_main_.py"
    MAIN = "main.py"

    @staticmethod
    def end():
        """Reset ended. Put main.py back in its rightful place.
           If there is no tmp_main, then the reset was not start.
        """
        try:
            with open(Reset.TMP_MAIN, 'r'):
                pass  
            os.remove(Reset.MAIN)
            os.rename(Reset.TMP_MAIN, Reset.MAIN)
            sys.stdin.read(1)
        except Exception:
            pass

    @staticmethod
    def start(imu: Imu, servo: Servo):
        """Stop all components running and reset the Pico.

        Args:
            imu (Imu): IMU
            servo (Servo): Servo
        """
        imu.stop()
        servo.stop()
        utime.sleep(1)
        os.rename(Reset.MAIN, Reset.TMP_MAIN)
        with open(Reset.MAIN, 'w') as f:
            f.write(Reset._tmp_main())

        print("####################################")
        print("# Resetting")
        print("####################################")
        print("#")
        print("# After the reset either ...")
        print("#")
        print("# Press Ctrl-D to restart, or, Upload")
        print("# new files including main.py and restart")
        print("#")
        print("# Pres any key to continue")
        print("####################################")
        sys.stdin.read(1)
        machine.reset()


    @staticmethod
    def _tmp_main():
        """Write out a main.py file to be used after the reset.

        Returns:
            str: main.py content
        """
        return "from reset import Reset\nReset.end()\n"
