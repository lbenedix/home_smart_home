void setup() {
    Serial.begin(9600);
}

void loop(){
  int sensorVal = analogRead(A0);
  float voltage = (sensorVal*5.0)/1024.0;
  float pressure_bar = 1.358 * voltage - 0.7042;
  Serial.println(pressure_bar);
  delay(1000);
}