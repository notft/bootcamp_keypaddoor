import RPi.GPIO as GPIO
import time


keypad_rows = [2, 3, 4, 17]
keypad_cols = [27, 22, 10, 9]
servo_pin = 18
buzzer_pin = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(keypad_rows + keypad_cols, GPIO.OUT)
GPIO.setup(servo_pin, GPIO.OUT)
GPIO.setup(buzzer_pin, GPIO.OUT)


keypad_map = [
    ['1', '2', '3', 'A'],
    ['4', '5', '6', 'B'],
    ['7', '8', '9', 'C'],
    ['*', '0', '#', 'D']
]


servo = GPIO.PWM(servo_pin, 50)
servo.start(0)


correct_password = "1235"

def unlock_door():
    servo.ChangeDutyCycle(7.5)  
    time.sleep(1)
    servo.ChangeDutyCycle(0)     
def lock_door():
    servo.ChangeDutyCycle(2.5) 
    time.sleep(1)
    servo.ChangeDutyCycle(0)     
def buzz():
    GPIO.output(buzzer_pin, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(buzzer_pin, GPIO.LOW)
    time.sleep(0.5)


def get_key():
    key = None
    GPIO.setup(keypad_cols, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    for col_num, col_pin in enumerate(keypad_cols):
        GPIO.output(col_pin, GPIO.HIGH)
        for row_num, row_pin in enumerate(keypad_rows):
            if GPIO.input(row_pin):
                key = keypad_map[row_num][col_num]
                break
        GPIO.output(col_pin, GPIO.LOW)

    return key


def get_password():
    password_input = ""
    while len(password_input) < len(correct_password):
        key = get_key()
        if key and key.isdigit():
            password_input += key
            print("Password entered so far:", password_input)
            time.sleep(0.3)
    return password_input


try:
    while True:
        print("Enter password to unlock:")
        entered_password = get_password()
        if entered_password == correct_password:
            print("Password correct. Unlocking door...")
            unlock_door()
        else:
            print("Incorrect password. Please try again.")
            buzz() 
            time.sleep(1)  
        
except KeyboardInterrupt:
    servo.stop()
    GPIO.cleanup()
