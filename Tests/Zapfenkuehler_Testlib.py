import time
import serial

class Zapfenkuehler_Testlib:

    def __init__(self):
        self.recv=-1

        #init serial connection to Arduino
        self.ser = serial.Serial(
            port='/dev/ttyUSB0',
            baudrate=9600,
            parity=serial.PARITY_ODD,
            stopbits=serial.STOPBITS_TWO,
            bytesize=serial.EIGHTBITS
        )

        #open serial connection
        if self.ser.isOpen():
            self.ser.close()
        self.ser.open()
        #check if connection is succesful
        if not self.ser.isOpen():
            print("Serial connection not succesful")
        time.sleep(2)

        #Handshake
        while self.ser.inWaiting() > 0:
            self.recv = self.ser.read()
        if not self.recv == b'A':
            print("Handshake not succesful")
        else:
            self.ser.write(b'a')
        #Arduino should now be ready to work
        # check functionality
        if self._checkserial() == -1:
            print("Arduino fucked up")
            return

        # init result buffer for use in later testcases
        self.result=[]
        print("Init successful")


    def set_temperature(self,temperature):
        # calculate PWM value matching set temperature
        temperature = 90 + int(temperature)

        # write 'T' to command PWM value
        self.ser.write(b'T')
        time.sleep(0.1)
        # write dummy 42 as commanded PWM
        self.ser.write(temperature.to_bytes(1, byteorder='big'))
        time.sleep(0.1)
        # Arduino should answer with a 'P'
        read = self.ser.read()
        if read != b'P':
            print(read)
            raise Exception("arduino did not respondcorrectly")

        # all finT
        print("temperature set to {}".format(temperature))
        return 1

    def get_cooler_output(self):
        self.recv=-1
        # write 'C' to request status of digital input
        self.ser.write(b'C')
        time.sleep(1)
        # Arduino should answer with '1' xor '0'
        self.recv = self.ser.read()
        if self.recv == b'1':
            self.result = '0' #cooler inactive
        elif self.recv == b'0':
            self.result =  '1' #cooler inactive
        else:
            return -1
        print("Cooler Signal = {}".format(self.recv))
    def get_error_messages(self):
        # not yet done
        return -1
    def wait_seconds(self,seconds):
        time.sleep(int(seconds))

    def Result_should_be(self,result):
        if  result.encode('utf-8') == self.recv:
            print("Result as expected")
        else:
            raise Exception("Result not as expected, aborting Test")
        return self.result

    def _checkserial(self):
        self.recv = 0
        #write 'T' to command PWM value
        self.ser.write(b'T')
        time.sleep(1)
        # write dummy 42 as commanded PWM
        self.ser.write(b'\x01')
        time.sleep(1)
        # Arduino should answer with a 'P'
        if self.ser.read() !=b'P':
            #print("no P")
            return -1
        #reset PWM to 0
        self.ser.write(b'\x00')

        # write 'C' to request status of digital input
        self.ser.write(b'C')
        time.sleep(1)
        # Arduino should answer with '1' xor '0'
        self.recv = self.ser.read()
        if (not(self.recv == b'1')) and (not(self.recv == b'0')):
            print("No digital")
            return -1

        # all fine
        return 1


if __name__ == '__main__':
    myTestlib = Zapfenkuehler_Testlib()

    myTestlib.set_temperature(10)
    time.sleep(300)
    myTestlib.set_temperature(-10)
    time.sleep(3)
    myTestlib.set_temperature(10)
    for t in range(3,150):
        myTestlib.get_cooler_output()
        print("time: {}; Cooler: {}".format(t,myTestlib.recv))
