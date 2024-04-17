#include <Keypad.h>
#include <Servo.h>
#include <string.h>

const byte ROWS = 4; 
const byte COLS = 4; 
char keys[ROWS][COLS] = {
  {'1','2','3','A'},
  {'4','5','6','B'},
  {'7','8','9','C'},
  {'*','0','#','D'}
};

byte rowPins[ROWS] = {9, 8, 7, 6}; 
byte colPins[COLS] = {5, 4, 3, 2}; 

Keypad keypad = Keypad( makeKeymap(keys), rowPins, colPins, ROWS, COLS );

Servo lockServo;
const int unlockAngle = 90; 
const int lockAngle = 0;    

char keycode[3];
int digit = 0;
int isLocked = 0;
const uint8_t RESET = 11;

void setup() {
  Serial.begin(9600);
  lockServo.attach(10); 
}

void loop() {
  char key = keypad.getKey();
  if(key){
    keycode[digit] = key;
    Serial.println(digit);
    if(strcmp(keycode, "0987") == 0){   //edit this code to enter the password u want, dont try, our password isnt 0987 :) 
      if(isLocked){
        unlockDoor();
        isLocked = 0;
      }else{
        lockDoor();
        isLocked = 1;
      }
      digitalWrite(RESET, LOW);
    }
    digit++;
  }
}

void resetVariables(){
  digit = 0;
  strcpy(keycode, "");
  Serial.println("Board has been resetted");
  Serial.println(keycode);
}

void unlockDoor() {
  lockServo.write(unlockAngle);
  delay(1000); 
  Serial.println("Door unlocked");
}

void lockDoor() {
  lockServo.write(lockAngle);
  delay(1000); 
  Serial.println("Door locked");
}
