// controla caixinha apontadora com motor de passo e potenciômetro


#define dirPin 2   // pino dig 2 arduino no DIR+ do driver
#define stepPin 3  // pino dig 3 arduino no STEP+ do driver
#define enablePin 4  // pino dig 4 arduino no EN+ do driver
#define botaoPin 5  // pino dig 4 arduino no EN+ do driver

struct CFG {
  unsigned int delay;
};
CFG config;

void default_config(){
  config.delay = 5000;
}

void habilita_motor(){
    digitalWrite(enablePin, LOW);
}
void desabilita_motor(){
    digitalWrite(enablePin, HIGH);
}


void setup() {
  
  pinMode(enablePin, OUTPUT);
  desabilita_motor();

  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);


  pinMode(botaoPin, INPUT_PULLUP);


  // escolhe direção, depende do motor pra saber se HIGH é anti ou horário
  digitalWrite(dirPin, HIGH);

  default_config();

  Serial.begin(9600);
}


void passo() {
  habilita_motor();
  digitalWrite(stepPin, HIGH);
  delayMicroseconds(config.delay);
  digitalWrite(stepPin, LOW);
  delayMicroseconds(config.delay);
  desabilita_motor();

}

void pot(){
  Serial.println(analogRead(A0));
}

void cfg(){
  long del = Serial.parseInt();
  config.delay = del > 0 ? del : -del;
  Serial.println(config.delay);
}

void passos(){
  int dir = 0;

  long passos = Serial.parseInt();
  if (passos != 0) {
    Serial.println(passos);
    if (passos > 0) {
      dir = HIGH;
    } else {
      dir = LOW;
      passos = -passos;
    }

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
        case 'a':
          pot();
          break;
        case 'c':
          cfg();
          break;
        case 'b':
          Serial.println(!digitalRead(botaoPin));
          break;  
        default:
          break;
      }
   }
}