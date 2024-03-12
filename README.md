# Pico Horizon

A demonstration project showing how to keep a level horizontal platform using a GY91 9DoF sensor, a servo and Raspberry Pi Pico running MicroPython.

## MicroPython Install

For installing MicroPython onto a Pico see...

* [Raspberry Pi docs](https://www.raspberrypi.com/documentation/microcontrollers/)
* or, [MicroPython docs](https://micropython.org/download/RPI_PICO/)

## Install this Demo

Clone this and IMU repo

```bash
$ git clone https://github.com/tgu-ltd/pico-horizon.git
$ cd pico-horizon
$ git clone https://github.com/tuupola/micropython-mpu9250.git
```

Create a virtual environment and install rshell

```bash
$ pipenv install
$ pipenv shell
$ pip install rshell
```

Upload files to the Pico

```bash
$ rshell -p /dev/ttyACM0 --baud 115200 -f ./upload_files.rshell
```

Start the program

```bash
$ minicom -o -D /dev/ttyACM0 # And press Ctrl-D
```


## Demo video

There is a [Youtube video](https://www.youtube.com/watch?v=0rjBdKVnOcw) of this working.

## Pinout

```bash
                     --------------
                     | Pi Pico    |
                     |------------|
                     |  Pin . GP  |
--------------       |      .     |
|        3v3-|-------|- 36  . n/a |
| GY91   Gnd-|-------|- 38  . n/a |
|  IMU   SCL-|-------|-  2  . 2   |
|        SDA-|-------|-  1  . 0   |
--------------       |      .     |
                     |      .     |
--------------       |      .     |
|         5v-|-------|- 40  . n/a |
|  SG90  Gnd-|-------|- 18  . n/a |
|  Servo PWM-|-------|- 17  . 13  |
--------------       --------------

```

## AK8963 Note

A dud AK8963 class is used in this code to bypass any AK8963 errors
