#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <HTTPClient.h>
#include <ArduinoJson.h> // Dodaj bibliotekę ArduinoJson

const char* ssid = "Lumia";
const char* password = "alamakota";
const char* serverUrl = "https://paczkomat.pythonanywhere.com/paczkomaty";
const char* serverUr2 = "https://paczkomat.pythonanywhere.com/zamknij";

const int ledPin2 = 2;
const int ledPin3 = 3;
const int relay = 15;

WiFiClientSecure client;
HTTPClient http;

void setup() {
  Serial.begin(9600);
  pinMode(ledPin2, OUTPUT);
  pinMode(ledPin3, OUTPUT);

  pinMode(relay, OUTPUT);
  digitalWrite(relay, HIGH);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  client.setInsecure();
}

void loop() {
  
  if (WiFi.status() == WL_CONNECTED) {
    if (http.begin(client, serverUrl)) {
      int httpCode = http.GET();
      if (httpCode == HTTP_CODE_OK) {
        String payload = http.getString();
        Serial.println(payload);

        // Parsowanie JSON
        DynamicJsonDocument doc(1024);
        DeserializationError error = deserializeJson(doc, payload);
        if (error) {
          Serial.print("JSON parsing error: ");
          Serial.println(error.c_str());
        } else {
          bool otworz = doc[0]["otworz"]; // Pobierz wartość zmiennej "otworz"
          

          if (otworz) {
            digitalWrite(ledPin2, LOW);
            digitalWrite(relay, LOW);
            Serial.println("Unable to connect to serverUr2");
            digitalWrite(ledPin3, HIGH);
            delay(4000);  // Poczekaj 2 sekundy
            digitalWrite(relay, HIGH);
            if (http.begin(client, serverUr2)) {
              int httpCode2 = http.GET();
              if (httpCode2 == HTTP_CODE_OK) {
                String response = http.getString();
                Serial.println(response);
              } else {
                Serial.print("Error accessing serverUr2. Error code: ");
                Serial.println(httpCode2);
              }
              http.end();
            } else {
              Serial.println("Unable to connect to serverUr2");
            }
            Serial.println("LED3 turned ON");
          } else {
            digitalWrite(ledPin2, HIGH);
            digitalWrite(ledPin3, LOW);
            Serial.println("LED2 turned ON");
          }
        }
      } else {
        Serial.print("Error accessing server. Error code: ");
        Serial.println(httpCode);
      }

      http.end();
    } else {
      Serial.println("Unable to connect to server");
    }
  }
  
  delay(1000);  // Poczekaj 1 sekunde przed kolejnym sprawdzeniem
}
