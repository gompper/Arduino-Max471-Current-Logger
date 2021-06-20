int analogPin = A3; 
int digitalPin = 2;
int led = 13;           
unsigned int val = 0;  
unsigned int val_avg = 0;

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
  pinMode(digitalPin, INPUT);
  pinMode(led, OUTPUT);
  Serial.begin(115200);           
}

void loop() {
  measure();
}
