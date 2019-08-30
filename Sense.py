import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class Sensor:

    def __init__(self, echo_l, echo_m, echo_r, trig_l, trig_m, trig_r):

        self.echo_l = echo_l
        self.echo_m = echo_m
        self.echo_r = echo_r

        self.trig_l = trig_l
        self.trig_m = trig_m
        self.trig_r = trig_r

        GPIO.setup(self.echo_l, GPIO.IN)
        GPIO.setup(self.echo_m, GPIO.IN)
        GPIO.setup(self.echo_r, GPIO.IN)

        GPIO.setup(self.trig_l, GPIO.OUT)
        GPIO.setup(self.trig_m, GPIO.OUT)
        GPIO.setup(self.trig_r, GPIO.OUT)


    def distance_us(self, l = True, m = True, r = True):

        '''
        :param l: disrance sensor l, default True
        :param m: disrance sensor m, default True
        :param r: disrance sensor r, default True

        :return: distance, aggregated as List and median from 6 measuremts: [l,m,r]
        '''

        count = 0
        output = [0, 1, 2]
        m_l = []
        m_m = []
        m_r = []

        #instructions to make 6 measurements per sensor

        while count <= 3:
            if l and m and r:

                m_l.append(self.d_measurement(self.trig_l, self.echo_l))

                m_m.append(self.d_measurement(self.trig_m, self.echo_m,))

                m_r.append(self.d_measurement(self.trig_r, self.echo_r))

            #in case you only want left and right
            elif l and not m and r:
                pass
                '''
                you get the idea, in case you only have a certain amount of sensors or more
                '''

            else:
                return "something is wrong"

            count += 1


        output[0] = m_l
        output[1] = m_m
        output[2] = m_r

        #takes the median of the six measurements

        for i in range(0, len(output)):
            output[i].sort()
            output[i] = output[i][3]

        return output


    def d_measurement(self,t,e):

        '''
        The measurement function itself

        :param t: triger pin
        :param e: echo pin
        :return: distance in cm
        '''

        #sends a signal on trig for 0.1 ms

        GPIO.output(t, True)
        time.sleep(0.0001)
        GPIO.output(t, False)

        #measures the time between sending the signal and receiving the signal on echo

        while GPIO.input(e) == False:
            start = time.time()

        while GPIO.input(e) == True:
            end = time.time()


        sig_time = end - start

        #time difference divided by constant is equal to distance in cm
        return sig_time / 0.000058



