#define dirZPin 7
#define dirYPin 6
#define dirXPin 5
#define stepZPin 4  // isso tudo vem da imagem Grbl_Pin_Layout.png
#define stepYPin 3
#define stepXPin 2
#define enablePin 8

class Driver {
public:
  unsigned int dirPin;
  unsigned int stepPin;
  unsigned int delay = 200;

  Driver(char qualMotor) {
    switch (qualMotor) {
      case 'x':
      case 'X':
        dirPin = dirXPin;
        stepPin = stepXPin;
        break;
      case 'y':
      case 'Y':
        dirPin = dirYPin;
        stepPin = stepYPin;
        break;
      case 'z':
      case 'Z':
        dirPin = dirZPin;
        stepPin = stepZPin;
        break;
      default:
        break;
    }
  }

  void setup() {
    pinMode(stepPin, OUTPUT);
    pinMode(dirPin, OUTPUT);
  }

  void passo() {
    digitalWrite(stepPin, HIGH);
    //delayMicroseconds(delay);
    delayMicroseconds(10);

    digitalWrite(stepPin, LOW);
    delayMicroseconds(delay);
  }

  void direcao(int dir){
    digitalWrite(dirPin, dir);
  }

  void passos(unsigned long quantos, int dir) {
    direcao(dir);
    for (unsigned int i = 0; i < quantos; i++) {
      passo();
    }
  }
};

Driver x = Driver('x');
Driver y = Driver('y');
Driver z = Driver('z');


void setup() {

  pinMode(enablePin, OUTPUT);
  x.setup();
  y.setup();
  z.setup();

  desabilita_motores();

  Serial.begin(9600);
}

void habilita_motores() {
  digitalWrite(enablePin, LOW);
  delayMicroseconds(2);
}
void desabilita_motores() {
  digitalWrite(enablePin, HIGH);
}

void passo_duplo(){
   digitalWrite(x.stepPin, HIGH);
   digitalWrite(y.stepPin, HIGH);
    //delayMicroseconds(delay);
    delayMicroseconds(10);

    digitalWrite(x.stepPin, LOW);
    digitalWrite(y.stepPin, LOW);

    delayMicroseconds(delay);
}

void passos2eixos(){
  int dirx;
  int diry;

  long px = Serial.parseInt();
  if (px > 0) {
    x.direcao(HIGH);
  } else {
    x.direcao(LOW);
  }
  px = abs(px);


  long py = Serial.parseInt();
  if (py > 0) {
    y.direcao(HIGH);
  } else {
    y.direcao(LOW);
  }
  py = abs(py);


  Serial.print(px);   Serial.print(" ");   Serial.println(py);

  while(px + py > 0){
    if(px > 0){
      if(py > 0){
        passo_duplo();
        px -= 1;
        py -= 1;
      }
      else {
        x.passo();
        px -= 1;
      }
    }
    else {
      y.passo();
      py -=1 ;
    }
  }
  
}

void passos() {
  int dir = 0;
  delay(2);  // serial é lerda
  char qualMotor = Serial.read();
  long passos = Serial.parseInt();


  Serial.println(passos);
  if (passos > 0) {
    dir = HIGH;
  } else {
    dir = LOW;
    passos = -passos;
  }

  switch (qualMotor) {
    case 'x':
      x.passos(passos, dir);
      break;
    case 'y':
      y.passos(passos, dir);
      break;
    case 'z':
      z.passos(passos, dir);
      break;
    default:
      break;
  }
}

void loop() {
  char cmd;
  while (Serial.available() > 0) {
    cmd = Serial.read();
    switch (cmd) {
      case 'p':
        passos();
        break;
      case 'P':
        passos2eixos();
        break;
      case 'h':
        habilita_motores();
        break;
      case 'd':
        desabilita_motores();
        break;
      default:
        break;
    }
  }
}
