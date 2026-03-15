import cv2
import numpy as np

VIDEO_PATH = "video/videoTest.mp4"
cap = cv2.VideoCapture(VIDEO_PATH)

if not cap.isOpened():
    print("Error: no se pudo abrir el video.")
    exit()

FPS = cap.get(cv2.CAP_PROP_FPS)

# Sustraemos el fondo utilizando MOG2
back_sub = cv2.createBackgroundSubtractorMOG2(
    history=200,
    varThreshold=50,
    detectShadows=False
)

# Matriz para poder hacer las operaciones morfológicas
kernel = np.ones((5, 5), np.uint8)

AREA_MINIMA = 500

historial_centroides = []

# Definimos vistas para tener un mejor control sobre los diferentes procesos que hemos hecho
VISTAS = [
    "1. Original",
    "2. Escala de grises",
    "3. Mascara cruda",
    "4. Erosion",
    "5. Dilatacion",
    "6. Apertura",
    "7. Cierre",
    "8. Mascara limpia",
    "9. Contornos detectados",
    "10. Centroide y trayectoria",
]
vista_actual = 0

cv2.namedWindow("Segmentacion", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Segmentacion", 1280, 720)

while True:
    ret, frame = cap.read()
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        back_sub = cv2.createBackgroundSubtractorMOG2(
            history=200, varThreshold=50, detectShadows=False
        )
        historial_centroides.clear()
        continue

    frame_actual = cap.get(cv2.CAP_PROP_POS_FRAMES)
    segundo_actual = frame_actual / FPS

    # Escala de grises
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Sustracciónde fondo
    mask = back_sub.apply(gray)

    # Operaciones morfológicas que nos piden
    erosion     = cv2.erode(mask, kernel, iterations=1)
    dilatacion  = cv2.dilate(mask, kernel, iterations=1)
    apertura    = cv2.morphologyEx(mask, cv2.MORPH_OPEN,  kernel)
    cierre      = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask_limpia = cv2.morphologyEx(apertura, cv2.MORPH_CLOSE, kernel)

    # Contornos del vehículo
    contornos, _ = cv2.findContours(mask_limpia, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    contorno_vehiculo = None
    if contornos:
        contorno_mas_grande = max(contornos, key=cv2.contourArea)
        if cv2.contourArea(contorno_mas_grande) > AREA_MINIMA:
            contorno_vehiculo = contorno_mas_grande

    # Calculamos centroide con momentos
    cx, cy = None, None
    if contorno_vehiculo is not None:
        M = cv2.moments(contorno_vehiculo)
        if M["m00"] != 0:  # evitar división por cero
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            historial_centroides.append((cx, cy))

    # Dibujamos el contorno y lo delimitamos
    frame_contornos = frame.copy()
    if contorno_vehiculo is not None:
        cv2.drawContours(frame_contornos, [contorno_vehiculo], -1, (0, 255, 0), 2)
        x, y, w, h = cv2.boundingRect(contorno_vehiculo)
        cv2.rectangle(frame_contornos, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # Dibujamos la trayectoria y el centroide
    frame_centroide = frame.copy()
    for i in range(1, len(historial_centroides)):
        cv2.line(frame_centroide,
                 historial_centroides[i - 1],
                 historial_centroides[i],
                 (0, 255, 255), 2)  # línea amarilla

    if cx is not None and cy is not None:
        cv2.circle(frame_centroide, (cx, cy), 6, (0, 0, 255), -1)   # punto rojo
        cv2.putText(frame_centroide, f"({cx}, {cy})",
                    (cx + 10, cy - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    # Seleccionar display
    if vista_actual == 0:
        display = frame.copy()
    elif vista_actual == 1:
        display = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    elif vista_actual == 2:
        display = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    elif vista_actual == 3:
        display = cv2.cvtColor(erosion, cv2.COLOR_GRAY2BGR)
    elif vista_actual == 4:
        display = cv2.cvtColor(dilatacion, cv2.COLOR_GRAY2BGR)
    elif vista_actual == 5:
        display = cv2.cvtColor(apertura, cv2.COLOR_GRAY2BGR)
    elif vista_actual == 6:
        display = cv2.cvtColor(cierre, cv2.COLOR_GRAY2BGR)
    elif vista_actual == 7:
        display = cv2.cvtColor(mask_limpia, cv2.COLOR_GRAY2BGR)
    elif vista_actual == 8:
        display = frame_contornos
    elif vista_actual == 9:
        display = frame_centroide

    # HUD
    cv2.putText(display, VISTAS[vista_actual], (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)
    cv2.putText(display, f"Tiempo: {segundo_actual:.2f} s", (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
    cv2.putText(display, "[a] Anterior   [d] Siguiente   [q] Salir",
                (20, display.shape[0] - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)

    cv2.imshow("Segmentacion", display)

    key = cv2.waitKey(30) & 0xFF

    if key == ord('q'):
        break
    elif key == ord('a'):
        vista_actual = (vista_actual - 1) % len(VISTAS)
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        back_sub = cv2.createBackgroundSubtractorMOG2(
            history=200, varThreshold=50, detectShadows=False
        )
        historial_centroides.clear()
    elif key == ord('d'):
        vista_actual = (vista_actual + 1) % len(VISTAS)
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        back_sub = cv2.createBackgroundSubtractorMOG2(
            history=200, varThreshold=50, detectShadows=False
        )
        historial_centroides.clear()

    if cv2.getWindowProperty("Segmentacion", cv2.WND_PROP_VISIBLE) < 1:
        break

cap.release()
cv2.destroyAllWindows()