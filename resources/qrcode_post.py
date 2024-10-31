from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

detector = cv2.QRCodeDetector()
def generate_frames():
    cap = cv2.VideoCapture(0)  # Use 0 para câmera ou substitua por 'video.mp4' para um arquivo de vídeo
    while True:
        try:
            success, frame = cap.read()
            if not success:
                break
            else:

                data, bbox, _ = detector.detectAndDecode(frame)# Detectar e decodificar o QR code

                if bbox is not None:
                    # Se um QR code for detectado
                    cv2.putText(frame, data, (int(bbox[0][0][0]), int(bbox[0][0][1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                    # Desenhar as linhas ao redor do QR code
                    bbox = bbox.astype(int)  # Converter coordenadas para inteiros
                    for i in range(len(bbox[0])):
                        cv2.line(frame, tuple(bbox[0][i]), tuple(bbox[0][(i + 1) % len(bbox[0])]), (0, 255, 0), 2)
                # Opcional: faça o processamento com OpenCV aqui
                # Exemplo: Convertendo para escala de cinza

                # Codifica o frame como JPEG
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()

                # Usa um gerador para criar o stream do vídeo
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        except:
            continue

@app.route('/')
def index():
    return render_template('gui/index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
