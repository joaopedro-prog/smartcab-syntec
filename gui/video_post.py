from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

def generate_frames():
    cap = cv2.VideoCapture(0)  # Use 0 para câmera ou substitua por 'video.mp4' para um arquivo de vídeo
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            # Opcional: faça o processamento com OpenCV aqui
            # Exemplo: Convertendo para escala de cinza

            # Codifica o frame como JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Usa um gerador para criar o stream do vídeo
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
