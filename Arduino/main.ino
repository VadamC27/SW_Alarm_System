#include <Key.h>
#include <Keypad.h>

#define Pin 2

const byte ROWS = 4;
const byte COLS = 4; 

byte rowPins[ROWS] = {4, 5, 6, 7}; //piny wierszy
byte colPins[COLS] = {8, 9, 10, 11};

char keys[ROWS][COLS] = { //keypad map
  {'1','2','3','A'},
  {'4','5','6','B'},
  {'7','8','9','C'},
  {'*','0','#','D'}
};

char typedByUser[5] = {'\0', '\0', '\0', '\0', '\0'};
int length = 0;

Keypad keypad = Keypad( makeKeymap(keys), rowPins, colPins,  ROWS, COLS ); // init keypad

int isTriggered = 0; 
int armed = 1;

boolean lockLow = true;
boolean takeLowTime;
long unsigned int lowIn;         
long unsigned int pause = 5000;  

void clearPass(){
  for(int i = 0; i<5;i++){
    typedByUser[i]='\0';
  }
}

void triggerAlarm(int pin){
    if(armed){
      isTriggered = 1; 
      switch(pin){
      case 2:{      
        Serial.println("alrm2");
        break;
      }
      case 3:{
        Serial.println("alrm3");
        break;
      }
      default:{
        Serial.println("errn1");
        break;
      }
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
    clearPass();
  }else if(key == '*'){
    Serial.print("code");
    Serial.println(typedByUser);

    /*String input = Serial.readStringUntil('\n');
    if(input == 0) return; //nie sprawdził się
    if(input == 1) { //poprawny kod zmiana stanu?!
      
    }*/
  }else if(key){
    typedByUser[length] = key;
    length = length + 1;
    if(length >= 4 ) {
      length = 0; 
      clearPass();
    }
  }
}

void setup() {
  Serial.begin(9600);
  //TODO output dla diody
  pinMode(2, INPUT); 
  pinMode(3, INPUT); 
  attachInterrupt(digitalPinToInterrupt(2), detectionPIN2, RISING); 
  attachInterrupt(digitalPinToInterrupt(3), detectionPIN3, RISING); 

}

void loop() {
  chceckKeypad();
 /* char key = keypad.getKey();
  
  if (key){
    Serial.println(key);
  }*/
  /*if(isTriggered){
    
  } else{
    //TODO dioda ma byc zgaszona 
  }*/
 
}
