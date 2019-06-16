const int ledPin = 13;
volatile byte state = LOW;
byte bandera = LOW;

void setup() {
   pinMode(ledPin, OUTPUT);
   TIMSK2 = (TIMSK2 & B11111110) | 0x01;
   TCCR2B = (TCCR2B & B11111000) | 0x03;
   //TCCR2B = (TCCR2B & B11111000) | 0x07;
   Serial.begin(115200); // start serial for output
}
  
void loop() {
   if (Serial.available()) { //Si está disponible
      char c = Serial.read(); //Guardamos la lectura en una variable char
      if (c == 'H') { //Si es una 'H', enciendo el LED
         bandera = HIGH;
      } else if (c == 'L') { //Si es una 'L', apago el LED
         bandera = LOW;
      }
   }

   if(bandera == LOW){
      digitalWrite(ledPin, LOW);
   }else{
      digitalWrite(ledPin, state);
   }
}

ISR(TIMER2_OVF_vect){
   state = !state; 
   Serial.println("1");
}
