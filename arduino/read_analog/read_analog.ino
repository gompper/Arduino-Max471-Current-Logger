// #define CONTINUOUS_SAMPLE

const unsigned int numReadings = 12;
const int analogPin = A3;
const int digitalPin = 2;
const int led = 13;
unsigned int analogVals[numReadings];

void setup()
{
  Serial.begin(115200);
  ADCSRA |= (1 << ADPS2); // 16 Prescaler
  pinMode(digitalPin,INPUT);
  pinMode(led,OUTPUT);
  pinMode(analogPin,INPUT);
}

void measureAndSend(){
  for (int i=0; i< numReadings;i++){
    analogVals[i] = analogRead(analogPin);
  }
  for (int i=0; i< numReadings;i++){
    Serial.println(analogVals[i]);
  }
}

void loop()
{
  #ifdef CONTINUOUS_SAMPLE
    measureAndSend();
  #else
    if (digitalRead(digitalPin)){
      measureAndSend();
      digitalWrite(led, HIGH);
    }else{
      digitalWrite(led, LOW);
    }
  #endif
}
