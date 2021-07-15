/*
* Uncomment one of the following three
*/
// #define CONTINUOUS_SAMPLE
#define STOP_SAMPLE_WITH_FALLING_EDGE 
// #define STOP_SAMPLE_WITH_TIMER

const int digitalPin = 2;
const int ledPin = 13;
const int analogPin = A3;

volatile int measure = 0;

typedef enum{
  IDLE,
  MEASURE
} State;

State state = IDLE;
State nextState = IDLE;

#ifdef STOP_SAMPLE_WITH_TIMER
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
  OCR1A = 3*1563; 
  // Output Compare Match A Interrupt Enable
  TIMSK1 |= (1 << OCIE1A);
  // activate interrupts
  interrupts();
}

ISR(TIMER1_COMPA_vect) {
  //stop timer
  TCCR1B = 0; 
  //clear timer counts
  TCNT1 = 0;

  nextState = IDLE;
}
#endif

void rising(){
  nextState = MEASURE;
  #ifdef STOP_SAMPLE_WITH_TIMER
  // CTC (clear timer on compare)
  TCCR1B |= (1 << WGM12);
  // Prescaler 1024
  TCCR1B |= (1 << CS12) | (1 << CS10);
  #endif
}
void falling(){
  #ifdef STOP_SAMPLE_WITH_FALLING_EDGE
  nextState = IDLE;
  #endif
}

void trigger(){
  if(digitalRead(digitalPin)) rising();
  else falling();
}

void setup()
{
  attachInterrupt (digitalPinToInterrupt (digitalPin), trigger, CHANGE);  // attach interrupt handler

  // set ADC prescaler to 16
  ADCSRA |= (1 << ADPS2); 

  Serial.begin(115200);

  pinMode(digitalPin,INPUT);
  pinMode(ledPin,OUTPUT);
  pinMode(analogPin,INPUT);

  Serial.println("Start");
  
  #ifdef STOP_SAMPLE_WITH_TIMER
  setupTimer1();
  #endif
}

void loop()
{
  switch (state)
  {
    case IDLE:
      if (nextState != state) {
        state = nextState;
        Serial.println("B");
      }
      break;
    case MEASURE:
      Serial.println(analogRead(analogPin));
      if (nextState != state) {
        state = nextState;
        Serial.println("E");
      }
      break;
    default:
      break;
  }
}
