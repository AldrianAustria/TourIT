//Libraries
#include <SPI.h>
#include <RFID.h>
#include <SparkFun_TB6612.h>
#include <Servo.h>

//Front Wheel Pins
#define A1_1 22
#define A1_2 23
#define B1_1 24
#define B1_2 25

//Rear Wheel Pins
#define A2_1 26
#define A2_2 27
#define B2_1 28
#define B2_2 29

//Front Wheel Config
#define PWMA1 2
#define PWMB1 3
#define STBY1 4

//Rear Wheel Config
#define PWMA2 5
#define PWMB2 6
#define STBY2 7

//Motor Constants
const int offset1A = 1;
const int offset1B = 1;
const int offset2A = 1;
const int offset2B = 1;

//Motor Initializations
Motor motor1A = Motor(A1_1, A1_2, PWMA1, offset1A, STBY1);
Motor motor1B = Motor(B1_1, B1_2, PWMB1, offset1B, STBY1);
Motor motor2A = Motor(A2_1, A2_2, PWMA2, offset2A, STBY2);
Motor motor2B = Motor(B2_1, B2_2, PWMB2, offset2B, STBY2);

//Battery Pins
#define bar4 39
#define bar3 38
#define bar2 37
#define bar1 36

//Battery Variables
int var4;
int var3;
int var2;
int var1;
unsigned long battery_prev_time = 0;
unsigned long battery_delay_time = 5000;

//Ultrasonic Sensor Pins
#define trig_pin 40
#define echo_pin 41

//Servo Motor Pins
#define servo 10

String prev_rfid = "";

//Servo Motor Variables
Servo myservo;
int pos = 85;
bool servo_change = false;
int duration = 0;
int distance = 100;
bool distance_clear = true;
bool event_trig_us = false;

//Ultrasonic & Servo Motor Delays
unsigned long current_time = 0;
unsigned long servo_prev_time = 0;
unsigned long servo_delay_time = 100;
unsigned long ultrasonic_prev_time = 0;
unsigned long ultrasonic_delay_time = 300;

//RFID Pins
#define RESET_DIO 8
#define SDA_DIO 9

//RFID Object Init
RFID RC522(SDA_DIO, RESET_DIO);

//RFID Variables
String serNum = "";
String tempSerNum = "";
bool rfid_active = true;
bool rfid_read = false;
String card_id[] = { "163231282335", "812232487149", "24314722416144", "365671716", "17923520877197",
                     "35618017158", "35301031775", "1312316577104", "359717117248", "17950204770",
                     "16316725477183" };

//IR Sensor
#define IR_PINS 5
int IR_sensor[] = { 43, 44, 45, 46, 49 };
int position = 0;
int setpoint = 0;

void setup() {
  Serial.begin(9600);
  Serial1.begin(115200);
  myservo.attach(servo);
  pinMode(trig_pin, OUTPUT);
  pinMode(echo_pin, INPUT);
  SPI.begin();
  RC522.init();
  for (int i = 0; i < IR_PINS; i++) {
    pinMode(IR_sensor[i], INPUT);
  }
  pinMode(bar4, INPUT);
  pinMode(bar3, INPUT);
  pinMode(bar2, INPUT);
  pinMode(bar1, INPUT);
}

void ir_position();

void battery_indicator();

void motor_forward(int speed);
void motor_backward(int speed);
void motor_left(int speed);
void motor_right(int speed);
void motor_rotate180(int speed);
void motor_brake();

void ultrasonic_sensor(int trig, int echo);
void servo_motor_sweep();

void loop() {
  current_time = millis();

  ir_position();
  //servo_motor_sweep();
  char incomingByte = Serial.read();
  if (current_time - battery_prev_time >= battery_delay_time) {
    battery_prev_time = current_time;
    battery_indicator();
  }
  if (current_time - ultrasonic_prev_time >= ultrasonic_delay_time) {
    ultrasonic_prev_time = current_time;
    ultrasonic_sensor(trig_pin, echo_pin);
  }
  if (distance < 20) {
    if (event_trig_us == false) {
      Serial.println(100);
      event_trig_us = true;
      distance_clear = false;
    } else {
      if (incomingByte == '0') {
        distance_clear = true;
        event_trig_us = false;
      }
    }
  } else {
    if (incomingByte == '0') {
      distance_clear = true;
      event_trig_us = false;
    }
  }

  if (distance_clear == true) {
    if (rfid_active == true) {
      if (RC522.isCard()) {
        rfid_read = true;
        RC522.readCardSerial();
        for (int i = 0; i < 5; i++) {
          serNum += RC522.serNum[i];
        }
        for (int i = 0; i < 11; i++) {
          if (serNum == card_id[i]) {
            if (serNum != tempSerNum) {
              Serial.println(i);
              Serial1.println(serNum + ",");
              //prev_rfid = serNum;
              tempSerNum = serNum;
              rfid_active = false;
            }
          }
        }
        serNum = "";
      }
      //Motor Go, Ultrasonic, IR Sensor
      if (rfid_read == true) {
        //IR Sensor and Motor functions
        if (position == -2) {
          motor_left(160);
        } else if (position == -1) {
          motor_left(150);
        } else if (position == 0) {
          motor_forward(110);
        } else if (position == 1) {
          motor_right(150);
        } else if (position == 2) {
          motor_right(160);
        }
      } else {
        motor_brake();
      }
    } else {
      //Motor stop & Wait
      motor_brake();
      if (incomingByte == '1') {
        rfid_active = true;
        //Comment these both if conditions
        // if (prev_rfid == "163231282335") {
        //   motor_rotate180(150);
        //   delay(2000);
        // }
        // else if (prev_rfid == "16316725477183") {
        //   motor_rotate180(150);
        //   delay(2000);
        // }
      }
    }
  } else {
    motor_brake();
  }
}

void ir_position() {
  int IR_VALUES[] = {
    digitalRead(43),
    !digitalRead(44),
    !digitalRead(45),
    !digitalRead(46),
    digitalRead(49)
  };
  //Set point value
  if (IR_VALUES[2] == 1) {
    position = 0;
  }

  //LEFT
  //1 value left away from set point
  else if (IR_VALUES[1] == 1) {
    position = -1;
  }
  //2 value left away from set point
  else if (IR_VALUES[0] == 1) {
    position = -2;
  }

  //RIGHT
  //1 value right away from set point
  else if (IR_VALUES[3] == 1) {
    position = 1;
  }
  //2 value left away from set point
  else if (IR_VALUES[4] == 1) {
    position = 2;
  }
  //Rotate Value
  // else {
  //   position = -5;
  // }
}

void motor_forward(int speed) {
  forward(motor1A, motor1B, speed);
  forward(motor2A, motor2B, speed);
}

void motor_backward(int speed) {
  back(motor1A, motor1B, speed);
  back(motor2A, motor2B, speed);
}

void motor_left(int speed) {
  motor1A.drive(speed);
  motor1B.brake();
  motor2A.drive(speed);
  motor2B.drive(-speed);
  /*motor1A.drive(speed);
  motor1B.drive(-speed);
  motor2A.drive(speed);
  motor2B.drive(-speed);*/
}

void motor_right(int speed) {
  motor1A.brake();
  motor1B.drive(speed);
  motor2A.drive(-speed);
  motor2B.drive(speed);
  /*motor1A.drive(-speed);
  motor1B.drive(speed);
  motor2A.drive(-speed);
  motor2B.drive(speed);*/
}

void motor_rotate180(int speed) {
  motor1A.drive(-speed);
  motor1B.drive(speed);
  motor2A.drive(-speed);
  motor2B.drive(speed);
}

void motor_brake() {
  motor1A.brake();
  motor1B.brake();
  motor2A.brake();
  motor2B.brake();
}

void ultrasonic_sensor(int trig, int echo) {
  digitalWrite(trig, LOW);
  //delayMicroseconds(2);
  digitalWrite(trig, HIGH);
  //delayMicroseconds(10);
  digitalWrite(trig, LOW);
  duration = pulseIn(echo, HIGH);
  distance = duration * 0.034 / 2;
  //Serial.println(distance);
}

void servo_motor_sweep() {
  if (current_time - servo_prev_time >= servo_delay_time) {
    servo_prev_time = current_time;
    if (servo_change == false) {
      if (pos == 95) {
        servo_change = true;
      } else {
        pos++;
      }
    }
    if (servo_change == true) {
      if (pos == 85) {
        servo_change = false;
      } else {
        pos--;
      }
    }
    myservo.write(pos);
  }
}

void battery_indicator() {
  var1 = digitalRead(bar1);
  var2 = digitalRead(bar2);
  var3 = digitalRead(bar3);
  var4 = digitalRead(bar4);

  if (var4 && var3 && var2 && var1) {
    Serial1.println(",4");
  } else if (var3 && var2 && var1) {
    Serial1.println(",3");
  } else if (var2 && var1) {
    Serial1.println(",2");
  } else if (var1 == 1) {
    Serial1.println(",1");
  } else {
    Serial1.println(",0");
  }
}
