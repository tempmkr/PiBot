import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


class Move:

    def __init__(self, pwm_l, pwm_r, dir_l1, dir_l2, dir_r1, dir_r2, servo1, f = 1000):

        '''
        engine gpio pins are set and initialized.
        Pass in the pins:
        pwm_l(ENA), pwm_r(ENB), dir_l1(IN1), dir_l2(IN2), dir_r1(IN3), dir_r2(IN4), pwm frequency default = 1000Hz

        '''

        self.pwm_l = pwm_l
        self.pwm_r = pwm_r

        self.dir_l1 = dir_l1
        self.dir_l2 = dir_l2
        self.dir_r1 = dir_r1
        self.dir_r2 = dir_r2

        self.servo1 = servo1

        self.f = f

        GPIO.setup(pwm_l, GPIO.OUT)
        GPIO.setup(pwm_r, GPIO.OUT)

        GPIO.setup(dir_l1, GPIO.OUT)
        GPIO.setup(dir_l2, GPIO.OUT)

        GPIO.setup(dir_r1, GPIO.OUT)
        GPIO.setup(dir_r2, GPIO.OUT)

        GPIO.setup(servo1, GPIO.OUT)

        self.p_r = GPIO.PWM(self.pwm_l, self.f)
        self.p_l = GPIO.PWM(self.pwm_r, self.f)

        self.s_1 = GPIO.PWM(self.servo1, 50)

        self.s_1.start(7.5)


    def straight(self,speed = 50, forward = True):

        '''

        :param speed: Speed in percent
        :param forward: default = forward, enter False for backwards

        '''

        GPIO.output(self.dir_r1, forward)
        GPIO.output(self.dir_r2, not forward)

        GPIO.output(self.dir_l1, forward)
        GPIO.output(self.dir_l2, not forward)



        if forward:
            self.p_l.start(speed+20)
            self.p_r.start(speed)

        else:
            self.p_l.start(speed)
            self.p_r.start(speed)


    def rotate(self, speed = 60, right = True):
        '''

        :param speed: Speed in percent
        :param right: default = right, enter False for left
        '''

        GPIO.output(self.dir_l1, right)
        GPIO.output(self.dir_l2, not right)

        GPIO.output(self.dir_r1, not right)
        GPIO.output(self.dir_r2, right)

        self.p_l.start(speed)
        self.p_r.start(speed)


    def turn(self, speed_diff = 60, right = True):

        '''

        :param speed__diff: Speed difference between left and right
        Speeddiff: The idea here is that when bot is on trajectory turn can be implemented upon existing movement without stoping one of the engines.

        '''

        GPIO.output(self.dir_r1, True)
        GPIO.output(self.dir_r2, False)

        GPIO.output(self.dir_l1, True)
        GPIO.output(self.dir_l2, False)

        if right:

            self.p_l.start(speed_diff)
            self.p_r.stop()

        elif not right:
            self.p_l.stop()
            self.p_r.start(speed_diff)


    def stop(self):
        self.p_r.stop()
        self.p_l.stop()

        '''
        Enter servo position in degrees; PWM will varry from 2%-10%
        '''
    def servo(self, pos):

        self.s_1.ChangeDutyCycle(pos)

