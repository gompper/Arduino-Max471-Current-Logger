int analogPin = A3;            
unsigned int val = 0;  
unsigned int val_avg = 0;
#define AVG 64

void setup() {
  Serial.begin(115200);           
}

void loop() {
  for(int i=0;i<AVG;i++){
    val = analogRead(analogPin);  
    val_avg += val;
  }
  val_avg /= AVG;
  Serial.println(val_avg);      
  val_avg = 0;
}
