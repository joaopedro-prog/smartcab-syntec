import camera_detection
import constants
import db_connect
import arduino_comm


arduino = arduino_comm.serial_comm()

#Common use variables ------
#User Details
user = {}
#Lock_state_variable
locked_gate:bool = True
opened_gate:bool = False


def run():
    #Importa as variáveis globais
    global user, locked_gate, opened_gate

    #Lógica da porta
    gate_logic()

    #Lê os dados do QRCode do vídeo
    card_data = camera_detection.get_video_code()
    
    #Valida os dados lidos
    if card_data != "" and card_data != None and opened_gate == False and locked_gate == True:
        #Busca no banco de dados se existe esse id já salvo
        card_result = db_connect.db.query(f'SELECT * FROM users WHERE card_id = {card_data}')
        #Caso o resultado da busca seja maior que 0, significa que existe esse id
        if len(card_result) > 0:
            #Define o user
            user = card_result[0]
            tools = db_connect.db.query(f'SELECT * FROM tools WHERE location_id = {user["id"]};')
            user["tools"] = [tools[i]['name'] for i in range(len(tools))]
            print(user)

            #Feito isso, manda o arduino abrir a tranca
            arduino_response = arduino.send_command('open_gate',show_command=False, printResponse=False)
            if arduino_response == 'Gate is now open':
                #Define a variável locked_gate como falsa
                locked_gate = False

        #Caso o id do cartão não seja reconhecido
        else:
            print("Cartão não reconhecido")
            user = {
                'id' : 0,
                'name' : "Não reconhecido",
                'card_id' : card_data,
                'active' : False,
                'tools' :  None
            }


def gate_logic():
    global user, locked_gate, opened_gate
    if locked_gate == False and arduino.send_command("gate_state", show_command=False) == "0":
        opened_gate = True
    if opened_gate == True and locked_gate == False and arduino.send_command("gate_state", show_command=False) == "1":
        opened_gate = False
        locked_gate = True
        user = {
                'id' : 0,
                'name' : "Aguardando usuário",
                'card_id' : "",
                'active' : False,
                'tools' :  None
            }