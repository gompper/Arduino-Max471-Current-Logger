// #define CONTINUOUS_SAMPLE

const unsigned int numReadings = 1;
const int analogPin = A3;
const int digitalPin = 2;
bool stopMeasure = true;
unsigned int analogVals[numReadings];

void setupTimer1() {
  // Deactivate Interrupts
  noInterrupts();
  // Normal Port Operation
  TCCR1A = 0; 
  // stop timer
  TCCR1B = 0; 
  // set timer counter
  TCNT1 = 0;  
  // output compare // 400 ms = 2.5 Hz
  OCR1A = 2*1563; 
  // Output Compare Match A Interrupt Enable
  TIMSK1 |= (1 << OCIE1A);
  // activate interrupts
  interrupts();
}

void startTimer(){
  stopMeasure = false;
  // CTC (clear timer on compare)
  TCCR1B |= (1 << WGM12);
  // Prescaler 1024
  TCCR1B |= (1 << CS12) | (1 << CS10);
}

void stopTimer(){
  stopMeasure = true;
  //stop timer
  TCCR1B = 0; 
  //clear timer counts
  TCNT1 = 0;  
}

void setup()
{
  // connect interrupt service routine
  attachInterrupt (digitalPinToInterrupt (digitalPin), startTimer, RISING);  // attach interrupt handler
  Serial.begin(115200);
  // set ADC prescaler to 16
  ADCSRA |= (1 << ADPS2); 
  pinMode(digitalPin,INPUT);
  pinMode(led,OUTPUT);
  pinMode(analogPin,INPUT);
  setupTimer1();
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
    if (digitalRead(digitalPin) && stopMeasure){
      startTimer();
    }else{
      while (!stopMeasure) measureAndSend();
    }
  #endif
}

ISR(TIMER1_COMPA_vect) {
  stopTimer();
}
