#include <string.h>
//variables
String Incoming_bytes; 
int AnalogReading; 
int AnalogDiff = 99; //this is used to differntiate analog incoming bytes from mob app


//Pins
int Accelerate_pin = 3;
int Reverse_pin = 4;
int pwmSpeedPin = 5;


//functions
unsigned char splitter (char text[]);
long microsecondsToCentimeters(long microseconds);
long microsecondsToInches(long microseconds);

void setup()
{
  Serial.begin(9600);         //Sets the data rate in bits per second (baud) for serial data transmission
  pinMode(Reverse_pin, OUTPUT);        //Sets digital pin 13 as output pin
  pinMode(Accelerate_pin, OUTPUT);

}

void loop()
{
  if (Serial.available() > 0)
  {
    Incoming_bytes = Serial.readString();
    AnalogReading = splitter(Incoming_bytes.c_str());
      
    
      if (strcmp(Incoming_bytes.c_str() , "LightOn") == 0) {
        //digitalWrite(LightPin, HIGH);
      }
      else if (strcmp(Incoming_bytes.c_str(), "r") == 0){
        //the car moves forward for 2 sec
        digitalWrite(Accelerate_pin, HIGH);
      delay(1000);
      digitalWrite(Accelerate_pin, LOW);
    }
    
    else if (strcmp(Incoming_bytes.c_str(), "U") == 0)  {
      //the car moves backward for 2 sec
      digitalWrite(Reverse_pin, HIGH);
      delay(1000);
      digitalWrite(Reverse_pin, LOW);
    }
    
    else if (strcmp(Incoming_bytes.c_str(), "B") == 0){
      // the car stops
      digitalWrite(Accelerate_pin, LOW);
    digitalWrite(Reverse_pin, LOW);
    }
    
    /*
      //Readings output
      Serial.print(Emergency);
      Serial.print('|');
      Serial.print(VisitorKnocking);
      Serial.print('|');
      Serial.print(VisitorCame);
      Serial.print('|');
      Serial.print(TempSensor);
      Serial.print('|');
      Serial.print(GasSensor);
      Serial.print('\n');
      delay(500);
      */
      }
   else{
    // the car stops
    digitalWrite(Accelerate_pin, LOW);
    digitalWrite(Reverse_pin, LOW);
   }
}


unsigned char splitter (char text[]) {
  // this function checks the input string
  // if the input string like "Speed 140"
  // this algorithm takes token 2 wich is 140
  // and converts it to integer which is the speed of the vehicle
  char d[] = " ";
  char *token1 = strtok(text, d);
  char *token2 = strtok(NULL, d);

  if (strcmp(token1, "Speed") == 0) {
    analogWrite(pwmSpeedPin, atoi(token2) * 255 / 100);
    Serial.print(atoi(token2) * 255 / 100);
    Serial.print('\n');
    AnalogDiff = 1;
    return atoi(token2);
  }
  else if (strcmp(token1, "this") == 0) {
    AnalogDiff = 1;
    return atoi(token2);
  }

}
