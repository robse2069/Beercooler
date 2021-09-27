/*
 Stimulator to automatically test the Zapfenkuehler with Robot Framework
 
   The circuit:
 * RC-Lowpass at PWM output to emulate DAC 
 * Digital Input to check if cooler is activated
 
 Created by RoSch

 */

int PWM_setpoint = 0;    // PWM to be converted into temperature stimulus
int cooler = 0;   // state of digital input
int PWM_pin = 3;
int cooler_pin = 2;

int inByte=0;

void setup()
{
  // start serial port at 9600 bps:
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for Leonardo only
  }

  pinMode(2, INPUT);   // digital sensor is on digital pin 2
  establishContact();  // send a byte to establish contact until receiver responds 
}

void loop()
{
  if (Serial.available() > 0) {
    // get incoming byte:
    inByte = Serial.read();
    switch (inByte){
      case 'T':
        while (Serial.available() <= 0) {
        }
        PWM_setpoint = Serial.read();
        analogWrite(PWM_pin,PWM_setpoint);
        Serial.write('P');
        break;
      case 'C':
        if (digitalRead(cooler_pin)){
          Serial.write('1');
        }else{
          Serial.write('0');          
        }
        break;
    }
  }
}

void establishContact() {
  while (Serial.available() <= 0) {
    Serial.print('A');   // send a capital A
    delay(300);
  }
}

