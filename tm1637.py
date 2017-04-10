import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

HEXDIGITS = [0x3f, 0x06, 0x5b, 0x4f, 0x66, 0x6d, 0x7d, 0x07, 0x7f, 0x6f]

HEXLETTERS = {
    'A': 0x77,
    'B': 0x7f,
    'b': 0x7C,
    'C': 0x39,
    'c': 0x58,
    'D': 0x3f,
    'd': 0x5E,
    'E': 0x79,
    'F': 0x71,
    'G': 0x7d,
    'H': 0x76,
    'h': 0x74,
    'I': 0x06,
    'J': 0x1f,
    'K': 0x76,
    'L': 0x38,
    'l': 0x06,
    'n': 0x54,
    'O': 0x3f,
    'o': 0x5c,
    'P': 0x73,
    'r': 0x50,
    'S': 0x6d,
    'U': 0x3e,
    'Y': 0x66,
    'Z': 0x5b,
    ' ': 0x00,
    'T1': 0x07,
    'T2': 0x31,
}

ADDR_AUTO = 0x40
ADDR_FIXED = 0x44
STARTADDR = 0xC0
BRIGHT_DARKEST = 0
BRIGHT_DEFAULT = 2
BRIGHT_HIGHEST = 7
OUTPUT = GPIO.OUT
INPUT = GPIO.IN
LOW = GPIO.LOW
HIGH = GPIO.HIGH


class TM1637:
    __double_point = False
    __clk_pin = 0
    __data_pin = 0
    __brightness = BRIGHT_DEFAULT
    __current_data = [' ', ' ', ' ', ' ']

    def __init__(self, clock_pin, data_pin, brightness=BRIGHT_DEFAULT):
        self.__clk_pin = clock_pin
        self.__data_pin = data_pin
        self.__brightness = brightness
        GPIO.setup(self.__clk_pin, OUTPUT)
        GPIO.setup(self.__data_pin, OUTPUT)

    def clear(self):
        b = self.__brightness
        point = self.__double_point
        self.__brightness = 0
        self.__double_point = False
        data = [' ', ' ', ' ', ' ']
        self.set_values(data)
        self.__brightness = b
        self.__double_point = point

    def set_values(self, data):
        for i in range(4):
            self.__current_data[i] = data[i]

        self.start()
        self.write_byte(ADDR_AUTO)
        self.stop()
        self.start()
        self.write_byte(STARTADDR)
        for i in range(4):
            self.write_byte(self.encode(data[i]))
        self.stop()
        self.start()
        self.write_byte(0x88 + self.__brightness)
        self.stop()

    def encode(self, data):
        point = 0x80 if self.__double_point else 0x00;

        if data == 0x7F:
            data = 0
        elif HEXLETTERS.has_key(data):
            data = HEXLETTERS[data] + point
        else:
            data = HEXDIGITS[data] + point
        return data

    def write_byte(self, data):
        for i in range(8):
            GPIO.output(self.__clk_pin, LOW)
            if data & 0x01:
                GPIO.output(self.__data_pin, HIGH)
            else:
                GPIO.output(self.__data_pin, LOW)
            data >>= 1
            GPIO.output(self.__clk_pin, HIGH)

        GPIO.output(self.__clk_pin, LOW)
        GPIO.output(self.__data_pin, HIGH)
        GPIO.output(self.__clk_pin, HIGH)
        GPIO.setup(self.__data_pin, INPUT)

        while GPIO.input(self.__data_pin):
            time.sleep(0.001)
            if GPIO.input(self.__data_pin):
                GPIO.setup(self.__data_pin, OUTPUT)
                GPIO.output(self.__data_pin, LOW)
                GPIO.setup(self.__data_pin, INPUT)
        GPIO.setup(self.__data_pin, OUTPUT)

    def start(self):
        GPIO.output(self.__clk_pin, HIGH)
        GPIO.output(self.__data_pin, HIGH)
        GPIO.output(self.__data_pin, LOW)
        GPIO.output(self.__clk_pin, LOW)

    def stop(self):
        GPIO.output(self.__clk_pin, LOW)
        GPIO.output(self.__data_pin, LOW)
        GPIO.output(self.__clk_pin, HIGH)
        GPIO.output(self.__data_pin, HIGH)