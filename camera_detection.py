import traceback
import cv2
import constants
import logic_control

detector = cv2.QRCodeDetector()
cap = cv2.VideoCapture(constants.CameraConstants.cameraIndex)

def generate_frames():
    while True:
        
        logic_control.run()

        if constants.logicFunctions.ACTIVATE_CAMERA_COMM:
            success, frame = cap.read()
        else:
            success = True
            frame = cv2.imread('resources\qr_code_img_simu.jpg')

        if success:
            try:
                data, bbox, _ = detector.detectAndDecode(frame)# Detectar e decodificar o QR code

                if bbox is not None:
                    cv2.putText(frame, data, (int(bbox[0][0][0]), int(bbox[0][0][1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                    bbox = bbox.astype(int)
                    for i in range(len(bbox[0])):
                        cv2.line(frame, tuple(bbox[0][i]), tuple(bbox[0][(i + 1) % len(bbox[0])]), (0, 255, 0), 2)

                # Codifica o frame como JPEG
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()

                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

            except Exception as e:
                print("Erro:", e)
                traceback.print_exc()  # Isso vai imprimir o stack trace


def get_video_code():
        if constants.logicFunctions.ACTIVATE_CAMERA_COMM:
            success, frame = cap.read()
        else:
            success = True
            frame = cv2.imread('resources\qr_code_img_simu.jpg')

        if success:
            data, bbox, _ = detector.detectAndDecode(frame)# Detectar e decodificar o QR code

            if not any(char.isalpha() for char in data):
                return data



