// controla motor pedreirão


#define dirPin 2   // pino 2 arduino no DIR+ do driver
#define stepPin 3  // pino 3 arduino no STEP+ do driver

struct CFG {
  unsigned int delay;
};
CFG config;

void default_config(){
  config.delay = 200;
}

void setup() {


  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);

  // escolhe direção, acho que HIGH é anti-horário
  digitalWrite(dirPin, HIGH);

  default_config();

  Serial.begin(9600);
}

void cfg(){
  long del = Serial.parseInt();
  config.delay = del > 0 ? del : -del;
  Serial.println(config.delay);
}

void passo() {
  digitalWrite(stepPin, HIGH);
  delayMicroseconds(config.delay);
  digitalWrite(stepPin, LOW);
  delayMicroseconds(config.delay);
}

void passos(){
  bool dir = 0;

  long passos = Serial.parseInt();
  if (passos != 0) {
    if (passos > 0) {
      dir = HIGH;
    } else {
      dir = LOW;
      passos = -passos;
    }
    Serial.println(passos);
    digitalWrite(dirPin, dir);
    for (unsigned int i = 0; i < passos; i++)
      passo();
  }
}

void loop() {
  char cmd;
   while (Serial.available() > 0) {
      cmd = Serial.read();
      switch (cmd){
        case 'p':
          passos();
          break;
        case 'c':
          cfg();
          break;
        default:
          break;
      }
   }


}