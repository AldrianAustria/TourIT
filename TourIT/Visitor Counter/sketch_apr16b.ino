#include <LiquidCrystal_I2C.h>
#include <WiFi.h>
#include <HTTPClient.h>

HTTPClient http;
WiFiClient client;

const char* ssid = "";  //Enter SSID
const char* password = "";   //Enter Password
const char* address = "http://192.168.1.x/TourIT/web_server/php/counter.php";

#define trig_left 32
#define echo_left 33

#define trig_right 25
#define echo_right 26

int trig_distance = 10;

int lcdColumns = 16;
int lcdRows = 2;

LiquidCrystal_I2C lcd(0x27, lcdColumns, lcdRows);

int people_count = 0;
int timeout_counter = 0;
int prev_people_count = 0;

String seq = "";

unsigned long current_time;
unsigned long prev_time_client = 0;
unsigned long prev_time_us_sensor = 0;
int us_sensor_delay = 50;

void setup() {
  Serial.begin(115200);

  lcd.init();
  lcd.backlight();

  pinMode(echo_left, INPUT);
  pinMode(trig_left, OUTPUT);

  pinMode(echo_right, INPUT);
  pinMode(trig_right, OUTPUT);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("***");
  }
  Serial.println("");
  Serial.println("WiFi connection Successful");
  Serial.print("The IP Address of ESP32 Module is: ");
  Serial.println(WiFi.localIP());  // Print the IP address

  http.begin(client, address);
  http.addHeader("Content-Type", "application/x-www-form-urlencoded");
  http.POST("input=0");  // Send an initial POST request to the server to set up the data variable
  http.end();
}

void call_http(String counter_value);
int us_sensor_left(int trig, int echo);

void loop() {
  int res_distance_left = us_sensor(trig_left, echo_left);
  int res_distance_right = us_sensor(trig_right, echo_right);
  current_time = millis();

  lcd.setCursor(0, 0);
  lcd.print("People Inside:");

  if ((res_distance_right < trig_distance) && (seq.charAt(0) != '1')) {
    seq += "1";
  }
  if ((res_distance_left < trig_distance) && (seq.charAt(0) != '2')) {
    seq += "2";
  }

  if (seq.equals("12")) {
    if (current_time - prev_time_us_sensor >= us_sensor_delay) {
      people_count++;
      seq = "";
      delay(500);
    }
  } else if (seq.equals("21") && people_count > 0) {
    if (current_time - prev_time_us_sensor >= us_sensor_delay) {
      people_count--;
      seq = "";
      delay(500);
    }
  }

  if (seq.length() > 2 || seq.equals("11") || seq.equals("22") || timeout_counter > 10) {
    seq = "";
  }

  if (seq.length() == 1) {
    timeout_counter++;
  } else {
    timeout_counter = 0;
  }

  Serial.println(people_count);

  if (prev_people_count != people_count) {
    call_http(String(people_count));
    prev_people_count = people_count;
  }

  if (people_count < 10) {
    lcd.setCursor(0, 1);
    lcd.print(people_count);
    lcd.print(" ");
  } else if (people_count >= 10) {
    lcd.setCursor(0, 1);
    lcd.print(people_count);
  }
}

int us_sensor(int trig, int echo) {
  digitalWrite(trig, LOW);
  delayMicroseconds(2);
  digitalWrite(trig, HIGH);
  delayMicroseconds(10);
  digitalWrite(trig, LOW);
  int duration = pulseIn(echo, HIGH);
  int distance = (duration * 0.0343 / 2);
  return distance;
}

void call_http(String counter_value) {
  http.begin(client, address);
  http.addHeader("Content-Type", "application/x-www-form-urlencoded");
  int httpCode = http.POST("input=" + counter_value);
  if (httpCode > 0) {
    Serial.printf("HTTP status code: %d\n", httpCode);
    String response = http.getString();
    Serial.println(response);
  } else {
    Serial.println("HTTP request failed");
    delay(500);
  }
  http.end();
  counter_value.clear();
}
