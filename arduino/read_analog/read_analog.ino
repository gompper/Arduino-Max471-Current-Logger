/*
So looks like using a prescale of 16 as above would give an ADC clock of 1 MHz and a sample rate of ~77KHz without much loss of resolution.
*/
// defines for setting and clearing register bits
#ifndef cbi
#define cbi(sfr, bit) (_SFR_BYTE(sfr) &= ~_BV(bit))
#endif
#ifndef sbi
#define sbi(sfr, bit) (_SFR_BYTE(sfr) |= _BV(bit))
#endif

int analogPin = A3; 
int digitalPin = 2;
int led = 13;           
unsigned int val = 0;  
unsigned int val_avg = 0;

// #define CONTINUOUS_SAMPLE

/*
Averaging over 64 samples.
integer on arduiono is 16 bit, so it can store ~64.06 samples with a max value of 1023 each.
--> 2^16/1032 
*/
#define AVG 64 

void measure(){
    for(int i=0;i<AVG;i++){
    val = analogRead(analogPin);  
    val_avg += val;
  }
  val_avg /= AVG;
  Serial.println(val_avg);      
  val_avg = 0;
}

void setup() {
  // set prescale to 16
  sbi(ADCSRA,ADPS2) ;
  cbi(ADCSRA,ADPS1) ;
  cbi(ADCSRA,ADPS0) ;
  
  pinMode(digitalPin, INPUT);
  pinMode(led, OUTPUT);
  digitalWrite(led,LOW);
  Serial.begin(115200);     
        
}

void loop() {
  #ifdef CONTINUOUS_SAMPLE
    measure();
  #else
    if (digitalRead(digitalPin)){
      measure();
      digitalWrite(led, HIGH);
    }else{
      digitalWrite(led, LOW);
    }
  #endif
}
