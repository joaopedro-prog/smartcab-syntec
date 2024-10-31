import serial
import time
import constants

class serial_comm():
    def __init__(self) -> None:
        print("Inicializando a conexão serial com o Arduino")
        # Configura a comunicação serial (porta e baud rate)
        if constants.logicFunctions.ACTIVATE_ARDUINO_COMM:
            self.arduino = serial.Serial(port='COM11', baudrate=9600, timeout=1)
            time.sleep(2)  # Espera 2 segundos após a conexão serial
            print("Conexão estabelecida com sucesso!")
        else:
            print("Conexão simulada estabelecida!")

    def send_command(self, command:str, show_command = False, printResponse = False)->str:
        """Send command and return the response"""
        response = ""
        if show_command:
            print(f"Enviando comando: {command}")
        if constants.logicFunctions.ACTIVATE_ARDUINO_COMM:
            self.arduino.write((command + '\n').encode('utf-8'))
            
            data = ''
            line = self.arduino.readline().decode('utf-8').strip()
            data += line + '\n'

            response = data.strip()
            self.arduino.flushInput()  # Limpa o buffer de entrada após a leitura
        else:
            response = "Arduino Commom Response"
        if printResponse:
            print(response)
        return response
    

# arduino = serial_comm()
# while True:
#     print(arduino.send_command("tools_array", show_command=False))
#     time.sleep(1)
