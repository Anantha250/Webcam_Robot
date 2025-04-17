sudo apt update
sudo apt install python3-pip
pip3 install hiwonder-servo hiwonder-motor

import time
import hiwonder_servo

# สร้างอ็อบเจกต์สำหรับควบคุมเซอร์โว
servo = hiwonder_servo.Servo()

# ตั้งค่ามุมของเซอร์โวที่ช่อง 1 เป็น 90 องศา
servo.set_angle(1, 90)

# รอ 1 วินาที
time.sleep(1)

# ตั้งค่ามุมของเซอร์โวที่ช่อง 1 เป็น 0 องศา
servo.set_angle(1, 0)

import time
import hiwonder_motor

# สร้างอ็อบเจกต์สำหรับควบคุมมอเตอร์
motor = hiwonder_motor.Motor()

# ตั้งค่าความเร็วของมอเตอร์ที่ช่อง 1 เป็น 50%
motor.set_speed(1, 50)

# รอ 2 วินาที
time.sleep(2)

# หยุดมอเตอร์ที่ช่อง 1
motor.set_speed(1, 0)
