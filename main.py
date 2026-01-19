# main.py
from machine import I2C, Pin
import time
from BMX055 import BMX055

# # ピンを個別に設定（プルアップを指定）
# sda_pin = Pin(4, Pin.IN, Pin.PULL_UP)
# scl_pin = Pin(5, Pin.IN, Pin.PULL_UP)

# # I2Cを初期化
# i2c = I2C(0, sda=sda_pin, scl=scl_pin, freq=400000)

bmx = BMX055(sda=4, scl=5)

while True:
    ax, ay, az = bmx.accel
    gx, gy, gz = bmx.gyro
    mx, my, mz = bmx.mag

    print("Accel: %+8.3f %+8.3f %+8.3f" % (ax, ay, az))
    print("Gyro : %+8.3f %+8.3f %+8.3f" % (gx, gy, gz))
    print("Mag  : %+8.3f %+8.3f %+8.3f" % (mx, my, mz))
    print("-" * 40)

    time.sleep_ms(100)
