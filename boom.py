import utime
import _thread
from machine import I2C, Pin, PWM
from mpu9250 import MPU9250


class Servo:
    """ The servo class to control the servo motor via PWM.
    """
    MIN_DEG = 0
    MID_DEG = 90
    MAX_DEG = 180
    DEG_TIMES = 10
    MIN_DUTY = 1000
    MAX_DUTY = 9000
    DEG_RANGE = MAX_DEG * DEG_TIMES
    DEG_STEP = int(DEG_RANGE / int((MAX_DUTY - MIN_DUTY)) *  DEG_TIMES)
    SLEEP_US = 10000
    SPN = Pin(13)

    def __init__(self):
        print("Servo Starting")
        self.pwm = PWM(Servo.SPN)
        self.degree = None
        self.pwm.freq(50)

    def duty(self, duty: int) -> None:
        """Set the duty cycle of the PWM

        Args:
            duty (int): Duty cycle of the PWM
        """
        self.pwm.duty_u16(duty)

    def degree_to_duty(self, degree: int) -> int:
        """Convert the degree to the duty cycle

        Args:
            degree (int): degree of the servo, usually between 0 and 180

        Returns:
            int: PWM duty cycle
        """
        return int(Servo.MIN_DUTY + (Servo.MAX_DUTY-Servo.MIN_DUTY) * (degree / Servo.MAX_DEG))

    def to_degree(self, degree: int) -> None:
        """Set the servo to a specific degree

        Args:
            degree (int): degree of the servo, usually between 0 and 180
        """
        if degree < Servo.MIN_DEG: degree = Servo.MIN_DEG
        if degree > Servo.MAX_DEG: degree = Servo.MAX_DEG
        self.degree = degree
        self.duty(self.degree_to_duty(degree))

    def stop(self):
        """Stop the servo
        """
        #self.pwm.deinit()
        print("Servo Stopped")


class Imu:
    """ The IMU class to read the accelerometer data from the MPU9250.
    """

    SCL = Pin(1)
    SDA = Pin(0)
    FRQ = 400000

    def __init__(self):
        self.ax = 0.0
        self.ay = 0.0
        self.az = 0.0
        i2c = I2C(0, scl=Imu.SCL, sda=Imu.SDA, freq=Imu.FRQ)
        self.sensor = MPU9250(i2c)
        self.running = True
        self.thread = _thread.start_new_thread(self._read, ())


    def sleep(self):
        """Sleep for 100us"""
        utime.sleep_us(100)

    def stop(self):
        """Stop the IMU
        """
        print("Stopping IMU")
        self.running = False
        self.sleep()
        print("IMU Stopped")


    def add_callback(self, callback):
        """ Add a callback function to be called when the IMU data is read.

        Args:
            callback (function): The callback function to be called when the IMU data is read.
        """
        self._callback = callback


    def _read(self):
        print("Starting IMU Read")
        while self.running:
            self.sleep()
            self.ax = round(self.sensor.acceleration[0], 3)
            self.ay = round(self.sensor.acceleration[1], 3)
            self.az = round(self.sensor.acceleration[2], 3)
            if self._callback:
                self._callback()
        print("IMU Read Stopped")



class Boom:
    """ The Boom class to control the servo motor via the IMU.

    Raises:
        RuntimeError: _description_
    """

    GRV = 9.80665
    def __init__(self, imu: Imu, servo: Servo):
        self.servo = servo
        self.imu = imu
        self.g = 0.0
        self.imu.add_callback(self.moved)
        have_g = False
        for i in range(1000000):
            if self.g != 0.0:
                have_g = True
                break
            utime.sleep_us(100)
        if not have_g:
            raise RuntimeError("No IMU Detected")
        self.servo.to_degree(90)
        utime.sleep_us(Servo.SLEEP_US * 100)


    def run(self):
        """Run the boom. The servo will move according to the accelerometer data.
        """
        tolerance = 0.1
        while self.imu.running:
            g = abs(self.g)
            if g < tolerance:
                continue
            
            g = round(g / Boom.GRV, 3)
            step_size = Servo.DEG_STEP * g
            step_sleep = Servo.SLEEP_US
            degree = self.servo.degree

            if self.g < 0:
                degree = self.servo.degree - step_size
            else:
                degree = self.servo.degree + step_size

            print("G: {0:<8} DG: {1:<8} FrDeg: {2:<8} ToDeg: {3:<8}".format(
                self.g, g, round(self.servo.degree, 2), round(degree, 2)
            ))
            self.servo.to_degree(degree)
            utime.sleep_us(step_sleep)


    def moved(self):
        """Callback function to be called when the IMU data is read.
        """
        if self.imu.ax != self.g:
            self.g = self.imu.ax