int steerL = 10;
int steerR = 11;
int lp = 13;
void setup() {
 
  Serial.begin(9600);  // Initialize serial communication at 9600 baud rate
  while (!Serial) {
    ; // Wait for the serial port to connect. Needed for native USB port only
  }
  Serial.println("Ready to receive data");
  pinMode(steerL,OUTPUT);
  pinMode(steerR,OUTPUT);

}

void loop() {
  if (Serial.available() > 0) {
    // Read the incoming byte
    int incomingByte = Serial.parseInt();
    // Print the received value to the Serial Monitor
    if(incomingByte>=0){
      digitalWrite(steerL,HIGH);
      digitalWrite(steerR,LOW);
      delay(abs(incomingByte)*20);
    }
    else if (incomingByte < 0){
      digitalWrite(steerR,HIGH);
      digitalWrite(steerL,LOW);
      delay(abs(incomingByte)*20);

    }
    Serial.print("Received: ");
    Serial.println(incomingByte);
  }
}
