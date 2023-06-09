#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);

//Push Button
#define btn 2

//IR Sensor Pins
#define right_ir 3
#define left_ir 4

//Photo Interrupter
#define ruptPin 5

//US Sensor Pins
#define echo 6
#define trig 7

//Motor Pins
#define enA 9
#define enB 10
#define in1 8
#define in2 11
#define in3 12
#define in4 13

//Speaker
#define spk A0

//LED
#define grn A1
#define ylw A2
#define red A3
#define blu A4

//Variables
int duration = 0;
int distance = 0;
int us_value = 0;
int r_ir = 0;
int l_ir = 0;
char ir_value;
char dir;
int interrupt = 0;
int toggle = 0;
int event = 0;
int old_event = 1;

//Exhibits
int trig_count = 0;

//Functions
int us_distance();
int btn_toggle(int btn_input);
char ir_sensor();
void motor_control(char command);

void setup() {
  lcd.init();
  lcd.backlight();
  //US Sensor
  pinMode(echo, INPUT);
  pinMode(trig, OUTPUT);
  //IR Sensor
  pinMode(right_ir, INPUT);
  pinMode(left_ir, INPUT);
  pinMode(ruptPin, INPUT);
  //Motor
  pinMode(enA, OUTPUT);
  pinMode(enB, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
  //Speaker
  pinMode(spk, OUTPUT);
  //LED
  pinMode(grn, OUTPUT);
  pinMode(ylw, OUTPUT);
  pinMode(red, OUTPUT);
  pinMode(blu, OUTPUT);
  //Serial
  Serial.begin(9600);
}

void loop() {
  lcd.setCursor(0,0);
  lcd.print("Prototype 1");
  event = digitalRead(btn);
  btn_toggle(event);
  us_value = us_distance();
  interrupt = digitalRead(ruptPin);
  //Serial.println(us_value);
  if(toggle == 1){
    lcd.setCursor(0,1);
    lcd.print("ON");
    if(us_value >= 15){
      /*digitalWrite(red, LOW);
      digitalWrite(ylw, LOW);
      digitalWrite(grn, HIGH);
      digitalWrite(blu, LOW);*/
      if(interrupt == HIGH){
        motor_control('s');
        trig_count = trig_count + 1;
        if(trig_count == 4){
          motor_control('g');
          delay(500);
          toggle = 0;
          trig_count = 0;
          motor_control('s');
          lcd.setCursor(0,1);
          lcd.print("Push the button again!");
          delay(5000);
        }
        else{
          digitalWrite(red, LOW);
          digitalWrite(ylw, LOW);
          digitalWrite(grn, LOW);
          digitalWrite(blu, HIGH);
          lcd.setCursor(0,1);
          lcd.print("Exhibit No.");
          lcd.print(trig_count);
          for(int i = 500; i<= 800; i++){
            tone(spk, i);
            delay(10);
          }
          for(int i = 800; i>= 500; i--){
            tone(spk, i);
            delay(10);
          }
          noTone(spk);
          delay(3000);
          motor_control('g');
          delay(300);
        }
      }
      else{
        ir_value = ir_sensor();
        motor_control(ir_value);
        lcd.setCursor(6,1);
        lcd.print(ir_value);
        digitalWrite(red, LOW);
        digitalWrite(ylw, LOW);
        digitalWrite(grn, HIGH);
        digitalWrite(blu, LOW);
      }
    }
    else{
      motor_control('s');
      lcd.setCursor(0,1);
      lcd.print("Oject Detected");
      digitalWrite(red, LOW);
      digitalWrite(ylw, HIGH);
      digitalWrite(grn, LOW);
      digitalWrite(blu, LOW);
    }
  }
 else {
    digitalWrite(red, HIGH);
    digitalWrite(ylw, LOW);
    digitalWrite(grn, LOW);
    digitalWrite(blu, LOW);
    motor_control('s');
    lcd.setCursor(0,1);
    lcd.print("OFF");
  }
  delay(1);
  lcd.clear();
}

int btn_toggle(int event){
  if(event == HIGH && old_event == 0){
    if(toggle == 0){
      toggle = 1;
    }
    else {
      toggle = 0;
    }
  }
  old_event = event;
}

int us_distance(){
  digitalWrite(trig, LOW);
  delayMicroseconds(2);
  digitalWrite(trig, HIGH);
  delayMicroseconds(10);
  digitalWrite(trig, LOW);
  duration = pulseIn(echo, HIGH);
  distance = (duration*0.0343)/2;
  return distance;
}

char ir_sensor(){
  r_ir = digitalRead(right_ir);
  l_ir = digitalRead(left_ir);
  if(r_ir == HIGH && l_ir == LOW){
    //Serial.println("GOING RIGHT");
    dir = 'r';
  }
  else if(r_ir == LOW && l_ir == HIGH){
    //Serial.println("GOING LEFT");
    dir = 'l';
  }
  else if(r_ir == HIGH && l_ir == HIGH){
    //Serial.println("STOP");
    dir = 'b';
  }
  else if(r_ir == LOW && l_ir == LOW){
    //Serial.println("GO");
    dir = 'g';
  }
  return dir;
}

void motor_control(char command){
  if(command == 'g'){
    analogWrite(enA, 55);
    analogWrite(enB, 65);
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
    digitalWrite(in3, HIGH);
    digitalWrite(in4, LOW);
  }
  else if(command == 's'){
    analogWrite(enA, 0);
    analogWrite(enB, 0);
    digitalWrite(in1, LOW);
    digitalWrite(in2, LOW);
    digitalWrite(in3, LOW);
    digitalWrite(in4, LOW);
  }
  else if(command == 'r'){
    analogWrite(enA, 0);
    analogWrite(enB, 65);
    digitalWrite(in1, LOW);
    digitalWrite(in2, LOW);
    digitalWrite(in3, HIGH);
    digitalWrite(in4, LOW);
  }
  else if(command == 'l'){
    analogWrite(enA, 55);
    analogWrite(enB, 0);
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
    digitalWrite(in3, LOW);
    digitalWrite(in4, LOW);
  }
  /*else if(command == 'b'){
    analogWrite(enA, 90);
    analogWrite(enB, 50);
    digitalWrite(in1, LOW);
    digitalWrite(in2, HIGH);
    digitalWrite(in3, LOW);
    digitalWrite(in4, HIGH);
  }*/
  return;
}
