#include "driver/adc.h"  // Include the ADC driver header

#define ANALOG_PIN 5  // Change this to your analog pin
#define BUTTON_PIN 12 // GPIO21 pin connected to button
#define HOLDPIN 17 // GPIO21 pin connected to button

int pstate, pstate2;     // the current reading from the input pin
int x = 0;
int h = 0;
void setup() {
  Serial.begin(115200);  // Start serial communication

  // Configure ADC for single read mode
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(HOLDPIN, INPUT_PULLUP);
  
  adc1_config_width(ADC_WIDTH_BIT_12);  // Set resolution to 12 bits
  adc1_config_channel_atten(ADC1_CHANNEL_5, ADC_ATTEN_DB_11);  // Set attenuation for channel 5
}

void loop() {
  int analog_value = adc1_get_raw(ADC1_CHANNEL_5);  // Read raw ADC value

  int currentState = digitalRead(BUTTON_PIN);
  if (currentState == LOW && currentState!=pstate){
    x = (x+1)%2;
  }
  pstate = currentState;

  int currentState2 = digitalRead(HOLDPIN);
  if (currentState2 == LOW && currentState2!=pstate2){
    h = (h+1)%2;
  }
  pstate2 = currentState2;

  Serial.print(analog_value);  // Send raw value to serial port
  Serial.print(",");  // Send raw value to serial port
  Serial.print(x);
  Serial.print(",");
  Serial.println(h);

  delay(1);  // Wait for 1ms
}