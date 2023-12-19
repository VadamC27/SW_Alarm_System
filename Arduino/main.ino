#include <Key.h>
#include <Keypad.h>

#define Pin

const byte ROWS = 4;
const byte COLS = 4; 

byte rowPins[ROWS] = {7, 6, 5, 4}; //piny wierszy
byte colPins[COLS] = {8, 9, 10, 11};

char keys[ROWS][COLS] = { //keypad map
  {'*','0','#','D'},
  {'7','8','9','C'},
  {'4','5','6','B'},
  {'1','2','3','A'}
};

char typedByUser[5] = {'\0', '\0', '\0', '\0', '\0'};
int length = 0;

Keypad keypad = Keypad( makeKeymap(keys), rowPins, colPins, ROWS, COLS ); // init keypad

int isTriggered = 0; 


void triggerAlarm(int pin){
  switch(pin){
    case 2:{

      brake;
    }
    case 3:{

      brake;
    }
    default:{

      brake;
    }
  }
}

void detectionPIN2(){
  triggerAlarm(2);
}

void detectionPIN3(){
  triggerAlarm(3);
}

void chceckKeypad(){
  char key = keypad.getKey();
  if(key == '#'){
    length = 0;
  }else if(key == '*'){
    Serial.print("code ");
    Serial.println(typedByUser);

    String input = Serial.readStringUntil('\n');
    if(input == 0) return; //niesprawdził się
    if(input == 1) { //poprawny kod zmiana stanu?!
      
    }
  }else{
    typedByUser[length] = key;
    length = length + 1;
    if(length => 4 ) {lenght = 0; typedByUser[5] = {'\0', '\0', '\0', '\0', '\0'};}
  }
}

void setup() {
  Serial.begin(9600);
  Serial.println("This is setup code");
  //TODO output dla diody
  pinMode(2, INPUT_PULLUP); 
  pinMode(3, INPUT_PULLUP); 
  attachInterrupt(digitalPinToInterrupt(2), detectionPIN2, FALLING); 
  attachInterrupt(digitalPinToInterrupt(3), detectionPIN3, FALLING); 
}

void loop() {
  chceckKeypad();
  
  if(isTriggered){
    
  } else{
    //TODO dioda ma byc zgaszona 
  }

}