# BMX055.py
from machine import I2C, Pin
import time

class BMX055:
    def __init__(self, sda=4, scl=5, id=0, freq=400000, *, addr_accel=0x19, addr_gyro=0x69, addr_mag=0x13, debug=False):
        self.sda_pin = Pin(sda, Pin.IN, Pin.PULL_UP)
        self.scl_pin = Pin(scl, Pin.IN, Pin.PULL_UP)
        self.i2c = I2C(id, sda=self.sda_pin, scl=self.scl_pin, freq=freq)

        self.addr_accel = addr_accel
        self.addr_gyro = addr_gyro
        self.addr_mag = addr_mag
        self.debug = debug

        self._init_accel()
        self._init_gyro()
        self._init_mag()
        self._delay(300)

    # ----- Public API -----

    @property
    def accel(self):
        data = [self._read1(self.addr_accel, 2 + i) for i in range(6)]

        if self.debug:
            print("accel raw:", [hex(x) for x in data])

        x = ((data[1] << 8) | (data[0] & 0xF0)) >> 4
        y = ((data[3] << 8) | (data[2] & 0xF0)) >> 4
        z = ((data[5] << 8) | (data[4] & 0xF0)) >> 4

        if x > 2047: x -= 4096
        if y > 2047: y -= 4096
        if z > 2047: z -= 4096

        return x * 0.0098, y * 0.0098, z * 0.0098

    @property
    def gyro(self):
        data = [self._read1(self.addr_gyro, 2 + i) for i in range(6)]

        if self.debug:
            print("gyro raw:", [hex(x) for x in data])

        x = (data[1] << 8) | data[0]
        y = (data[3] << 8) | data[2]
        z = (data[5] << 8) | data[4]

        if x > 32767: x -= 65536
        if y > 32767: y -= 65536
        if z > 32767: z -= 65536

        return x * 0.0038, y * 0.0038, z * 0.0038

    @property
    def mag(self):
        data = [self._read1(self.addr_mag, 0x42 + i) for i in range(8)]

        if self.debug:
            print("mag raw:", [hex(x) for x in data])

        x = ((data[1] << 8) | (data[0] >> 3))
        if x > 4095: x -= 8192

        y = ((data[3] << 8) | (data[2] >> 3))
        if y > 4095: y -= 8192

        z = ((data[5] << 8) | (data[4] >> 3))
        if z > 16383: z -= 32768

        return x, y, z

    # ----- Internal helpers -----

    def _write1(self, addr, reg, val):
        self.i2c.writeto_mem(addr, reg, bytes([val]))

    def _read1(self, addr, reg):
        return int.from_bytes(self.i2c.readfrom_mem(addr, reg, 1), "big")

    def _delay(self, ms):
        time.sleep_ms(ms)

    # ----- Init sequences -----

    def _init_accel(self):
        self._write1(self.addr_accel, 0x0F, 0x03)  # ±2g
        self._delay(100)
        self._write1(self.addr_accel, 0x10, 0x08)  # BW = 7.81Hz
        self._delay(100)
        self._write1(self.addr_accel, 0x11, 0x00)  # Normal mode
        self._delay(100)

    def _init_gyro(self):
        self._write1(self.addr_gyro, 0x0F, 0x04)  # ±125 deg/s
        self._delay(100)
        self._write1(self.addr_gyro, 0x10, 0x07)  # ODR = 100Hz
        self._delay(100)
        self._write1(self.addr_gyro, 0x11, 0x00)  # Normal mode
        self._delay(100)

    def _init_mag(self):
        self._write1(self.addr_mag, 0x4B, 0x83)
        self._delay(100)
        self._write1(self.addr_mag, 0x4B, 0x01)
        self._delay(100)
        self._write1(self.addr_mag, 0x4C, 0x00)
        self._delay(100)
        self._write1(self.addr_mag, 0x4E, 0x84)
        self._delay(100)
        self._write1(self.addr_mag, 0x51, 0x04)
        self._delay(100)
        self._write1(self.addr_mag, 0x52, 0x16)
        self._delay(100)
