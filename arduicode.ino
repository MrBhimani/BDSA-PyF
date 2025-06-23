#include <Servo.h>
#include <Ultrasonic.h>
Servo servo1;
Servo servo2;
Ultrasonic ultrasonic(11, 12);
int distance;
int buzzer = 13;

int incoming[2];

void setup(){
  Serial.begin(9600);
  Serial.setTimeout(1);
  servo1.attach(5);
  servo2.attach(6);
  pinMode(buzzer,OUTPUT);
}

void loop(){
  if(Serial.available() >= 2){
    for (int i = 0; i < 3; i++){
        incoming[i] = Serial.read();}
        servo1.write(incoming[0]);
        servo2.write(incoming[1]);}
        
   distance = ultrasonic.read();
   if(distance <= 20){
   digitalWrite(buzzer,HIGH);}
   else
   digitalWrite(buzzer,LOW);
}
