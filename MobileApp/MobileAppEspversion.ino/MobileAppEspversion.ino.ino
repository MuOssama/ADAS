#include <BluetoothSerial.h>

BluetoothSerial SerialBT;

String Incoming_bytes;
int AnalogReading;
int AnalogDiff = 99;

int Accelerate_pin = 13; // PWM-capable pin
int Reverse_pin = 12;    // Digital pin
int pwmSpeedPin = 14;    // PWM-capable pin
int statusLedPin = 2;    //status led pin
int steeringRightPin = 32; //steering Right pin
int steeringLeftPin = 33; //steering left pin

unsigned char splitter(const char *text);
int steeringLeftTime = 0;
int steeringRightTime = 0;
int steeringLeftState = 0;
int steeringRightState = 0;

#define steeringTime 2000

void setup() {
  Serial.begin(500000);
  SerialBT.begin("ADAS");

  pinMode(Reverse_pin, OUTPUT);
  pinMode(Accelerate_pin, OUTPUT);
  pinMode(steeringRightPin, OUTPUT);
  pinMode(steeringLeftPin, OUTPUT);

  //moving logic high to turn off (not active at high logic) steering at beginning
  digitalWrite(steeringLeftPin,HIGH);
  digitalWrite(steeringRightPin,HIGH);
  digitalWrite(Reverse_pin,HIGH);
  digitalWrite(Accelerate_pin,HIGH);
  
  ledcSetup(0, 5000, 8);   // Setup PWM channel 0, 5000 Hz, 8-bit resolution
  ledcAttachPin(pwmSpeedPin, 0); // Attach channel 0 to pin pwmSpeedPin
}

void loop() {
  if (SerialBT.available()) {

    Incoming_bytes = SerialBT.readString();
    //AnalogReading = splitter(Incoming_bytes.c_str());
  }
   //moving forward
    if ( strcmp(Incoming_bytes.c_str() ,"U")==0) {
       //relay is active low
      digitalWrite(2, HIGH); // Turn the LED on
      digitalWrite(Accelerate_pin, LOW);
      digitalWrite(Reverse_pin, HIGH);
      ledStatusOFF();
    } 
       
    //moving backward
    else if (strcmp(Incoming_bytes.c_str() ,"r")==0) {
      //relay is active low
      ledStatusON();
      digitalWrite(Reverse_pin, LOW);
      digitalWrite(Accelerate_pin, HIGH);
      ledStatusOFF();
    }
     
    //Steer Right
    else if (strcmp(Incoming_bytes.c_str() ,"R")==0 ||steeringRightState == 1 ) {
      ledStatusON();
      if(steeringRightState == 0){
        steeringRightTime = millis();
      }
      steeringRightState = 1;
      digitalWrite(steeringLeftPin,HIGH);
      digitalWrite(steeringRightPin,LOW);
      
      int currTime = millis();
      if(currTime-steeringRightTime>steeringTime){
       ledStatusOFF();
       steeringRightState =0;
       digitalWrite(steeringRightPin,HIGH);
      }
      Serial.println(currTime-steeringRightTime);
      Incoming_bytes = 'k';
    }

    //Steer Left
    else if (strcmp(Incoming_bytes.c_str() ,"L")==0 ||steeringLeftState == 1 ) {
      ledStatusON();
      if(steeringLeftState == 0){
        steeringLeftTime = millis();
      }
      steeringLeftState = 1;
      digitalWrite(steeringRightPin,HIGH);
      digitalWrite(steeringLeftPin,LOW);
      
      int currTime = millis();
      if(currTime-steeringLeftTime>steeringTime){
       ledStatusOFF();
       steeringLeftState =0;
       digitalWrite(steeringLeftPin,HIGH);
      }
      Serial.println(currTime-steeringLeftTime);
      Incoming_bytes = 'k';
    }

    //brake
    else if (strcmp(Incoming_bytes.c_str() ,"B")==0) {
      ledStatusON();
      //relay is active low
      digitalWrite(Accelerate_pin, HIGH);
      digitalWrite(Reverse_pin, HIGH);
      digitalWrite(steeringLeftPin, HIGH);
      digitalWrite(steeringRightPin, HIGH);
      ledStatusOFF();
    }
  

  //stop all
  else {
    digitalWrite(Accelerate_pin, HIGH);
    digitalWrite(Reverse_pin, HIGH);
  }
}

void ledStatusON(){
    digitalWrite(statusLedPin, HIGH);
}
void ledStatusOFF(){
    digitalWrite(statusLedPin, LOW);
}
unsigned char splitter(const char *text) {
  char d[] = " ";
  char *token1 = strtok(const_cast<char *>(text), d);
  char *token2 = strtok(NULL, d);

  if (strcmp(token1, "Speed") == 0) {
    ledcWrite(0, atoi(token2) * 255 / 100); // Set PWM duty cycle on channel 0
    Serial.print(atoi(token2) * 255 / 100);
    Serial.print('\n');
    AnalogDiff = 1;
    return atoi(token2);
  } else if (strcmp(token1, "this") == 0) {
    AnalogDiff = 1;
    return atoi(token2);
  }

  return 0; // Add a default return value to avoid warning
}
