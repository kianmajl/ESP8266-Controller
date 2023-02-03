#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>


const char* ssid = "xxx";
const char* password = "xxx";
WiFiClient client;

int ledPin = D4;
long req_counter = 5000;
long on_time = 0;
long off_time = 0;
long delay_counter = 0;


void setup() {

  Serial.begin(115200);
  while (!Serial)
    ;

  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);

  // Connect to WiFi network
  Serial.print("Connecting to: ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
    digitalWrite(ledPin, !digitalRead(ledPin));
  }

  Serial.print("\nWiFi connected");
  Serial.print(" (");
  Serial.print(ssid);
  Serial.println(")");

  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);

  long rssi = WiFi.RSSI();
  Serial.print("signal strength (RSSI):");
  Serial.print(rssi);
  Serial.println(" dBm");

  Serial.println("-----------------------------");
}


void loop() {

  delay(1);

  if ((delay_counter % req_counter) == 0) {
    unsigned long start_req_delay = millis();
    if (WiFi.status() == WL_CONNECTED) {  //Check WiFi connection status

      HTTPClient http;

      http.begin(client, "http://YOUR_IP_ADDRESS/device/get/");  //Specify request URL
      int httpCode = http.GET();                                    //Send the request

      if (httpCode > 0) {
        String payload = http.getString();  //Get the request response payload

        char delimiter = ';';
        int del_index = payload.indexOf(';');
        on_time = payload.substring(0, del_index).toInt();
        off_time = payload.substring(del_index + 1, payload.length()).toInt();

        Serial.print("On Time: ");
        Serial.print(on_time);
        Serial.println(" ms");
        Serial.print("Off Time: ");
        Serial.print(off_time);
        Serial.println(" ms");
      }

      else {
        Serial.println("Error Code: ");
        Serial.println(httpCode);
      }

      http.end();  //Close connection
    } else {
      Serial.println("ESP8266 didn't connect to WiFi!");
    }

    Serial.print("Network delay: ");
    Serial.print(millis() - start_req_delay);
    Serial.println(" ms");
    Serial.println("--------------------------------");
  }

  if ((on_time == 0) & (off_time == 0)) {
    digitalWrite(ledPin, HIGH);
  }

  else if ((on_time != 0) & (off_time == 0)) {
    digitalWrite(ledPin, LOW);
  }

  else if ((off_time != 0) & (on_time == 0)) {
    digitalWrite(ledPin, HIGH);
  }

  else if (!digitalRead(ledPin) & ((delay_counter % on_time) == 0)) {
    digitalWrite(ledPin, HIGH);
  }

  else if ((delay_counter % off_time) == 0) {
    digitalWrite(ledPin, LOW);
  }

  if (delay_counter == (off_time * on_time * req_counter))
    delay_counter = 0;
  else
    delay_counter++;
}