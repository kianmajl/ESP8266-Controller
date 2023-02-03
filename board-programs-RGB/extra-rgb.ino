#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>


const char* ssid = "xxx";
const char* password = "xxx";
WiFiClient clinet;

int ledPin = D4;
long req_counter = 5000;
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
  String payload;

  if ((delay_counter % req_counter) == 0) {
    unsigned long start_req_delay = millis();
    if (WiFi.status() == WL_CONNECTED) {  //Check WiFi connection status

      HTTPClient http;

      http.begin(clinet, "http://YOUR_IP_ADDRESS/device/max_rgb/");  //Specify request URL
      int httpCode = http.GET();                                    //Send the request

      if (httpCode > 0) {
        payload = http.getString();  //Get the request response payload
        Serial.println(payload);
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

  if (payload.charAt(0) == 'B')
    digitalWrite(ledPin, LOW);
  else
    digitalWrite(ledPin, HIGH);

  if (delay_counter == req_counter)
    delay_counter = 0;
  else
    delay_counter++;
}