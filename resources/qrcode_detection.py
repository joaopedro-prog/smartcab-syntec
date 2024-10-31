import cv2

cap = cv2.VideoCapture(0)
detector = cv2.QRCodeDetector()

def detectQRCode(showVideo=True):
    ret, frame = cap.read()
    
    if not ret:
        return

    data, bbox, _ = detector.detectAndDecode(frame)# Detectar e decodificar o QR code

    if bbox is not None:
        # Se um QR code for detectado
        cv2.putText(frame, data, (int(bbox[0][0][0]), int(bbox[0][0][1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        # Desenhar as linhas ao redor do QR code
        bbox = bbox.astype(int)  # Converter coordenadas para inteiros
        for i in range(len(bbox[0])):
            cv2.line(frame, tuple(bbox[0][i]), tuple(bbox[0][(i + 1) % len(bbox[0])]), (0, 255, 0), 2)

    # Mostrar o frame com a detecção
    if showVideo:
        cv2.imshow('QR Code Reader', frame)
        cv2.waitKey(1)
    
    if data == "":
        return None
    return data

def destroyCamera():
    cap.release()
    cv2.destroyAllWindows()
