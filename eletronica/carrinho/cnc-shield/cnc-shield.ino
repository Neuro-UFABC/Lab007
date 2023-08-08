#define dirZPin 7
#define dirYPin 6
#define dirXPin 5
#define stepZPin 4  // isso tudo vem da imagem Grbl_Pin_Layout.png
#define stepYPin 3
#define stepXPin 2
#define enablePin 8

class Driver {
private:
  unsigned int dirPin;
  unsigned int stepPin;
public:
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

  void passos(unsigned long quantos, int dir) {
    digitalWrite(dirPin, dir);
    for (unsigned int i = 0; i < quantos; i++) {
      passo();
    }
  }
};

Driver x = Driver('x');
Driver y = Driver('y');

void setup() {

  pinMode(enablePin, OUTPUT);
  x.setup();
  y.setup();

  desabilita_motor();

  Serial.begin(9600);
}

void habilita_motor() {
  digitalWrite(enablePin, LOW);
  delayMicroseconds(2);
}
void desabilita_motor() {
  digitalWrite(enablePin, HIGH);
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
      case 'h':
        habilita_motor();
        break;
      case 'd':
        desabilita_motor();
        break;
      default:
        break;
    }
  }
}
