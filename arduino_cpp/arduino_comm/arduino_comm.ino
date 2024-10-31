bool locked_Gate = true;
const char gate_sensor_port = 2;

const int numPins = 8;  // Defina o número de pinos que você deseja monitorar
int pins[numPins] = {3, 4, 5, 6, 7, 8, 9, 10};  // Array das portas digitais que você quer monitorar
bool pinStates[numPins];  // Array para armazenar os estados (HIGH ou LOW) das portas


void setup() {
  // Inicializa a comunicação serial a 9600 bps
  pinMode(gate_sensor_port, INPUT);

  for (int i = pins[0]; i < numPins; i++) {
    pinMode(pins[i], INPUT);  // Configura as portas como entradas
  }

  Serial.begin(9600);
}

void loop() {
  // Verifica se há dados disponíveis para leitura
  if (Serial.available() > 0) {
    // Lê o comando recebido
    String command = Serial.readStringUntil('\n');

    if (command == "open_gate") {
      Serial.println("Gate is now open");
    }

    if (command == "gate_state"){
      Serial.println(digitalRead(gate_sensor_port));
    }

    if (command == "tools_array"){
      // Atualiza o estado de cada porta e armazena no array
      for (int i = 0; i < numPins; i++) {
        pinStates[i] = digitalRead(pins[i]);
      }

      // Constrói uma string CSV com os estados das portas
      String output = "";
      for (int i = 0; i < numPins; i++) {
        output += (pinStates[i] ? "1" : "0");  // Usa '1' para HIGH e '0' para LOW
        if (i < numPins - 1) {
          output += ",";  // Adiciona uma vírgula entre os valores
        }
      }

      Serial.println(output);
    }
  }
}
