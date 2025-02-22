import cv2
import numpy as np
import concurrent.futures

def detect_golf_club_head_multiple_templates_optimized(video_path, template_paths):
    # Cargar el video
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: No se pudo abrir el video en la ruta '{video_path}'.")
        return

    # Cargar todas las plantillas (imagenes de la cabeza del palo de golf)
    templates = []
    for template_path in template_paths:
        template = cv2.imread(template_path, 0)  # Cargar la plantilla en escala de grises
        if template is None:
            print(f"Error: No se pudo cargar la plantilla en la ruta '{template_path}'.")
        else:
            templates.append(template)

    if not templates:
        print("Error: No se cargó ninguna plantilla correctamente.")
        return

    # Definir la ventana con tamaño escalable
    cv2.namedWindow('Detección de Cabeza de Palo de Golf', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Detección de Cabeza de Palo de Golf', 400, 700)  # Cambiar a tu preferencia

    # Parámetros de optimización
    scale_percent = 90  # Escalar el video al 50% para reducir el tiempo de procesamiento
    frame_skip = 5      # Procesar 1 de cada 3 fotogramas
    frame_count = 0

    while True:
        # Leer el frame del video
        ret, frame = cap.read()
        if not ret:
            break

        # Saltar algunos fotogramas
        if frame_count % frame_skip != 0:
            frame_count += 1
            continue

        # Reducir el tamaño del fotograma
        frame_resized = cv2.resize(frame, (frame.shape[1] * scale_percent // 100, 
                                           frame.shape[0] * scale_percent // 100))
        gray_frame = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2GRAY)

        # Variables para almacenar la mejor coincidencia
        best_match_value = 0
        best_match_location = None
        best_match_size = None

        # Función para aplicar el template matching
        def match_template(template):
            return cv2.matchTemplate(gray_frame, template, cv2.TM_CCOEFF_NORMED)

        # Aplicar template matching con todas las plantillas en paralelo
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(match_template, template) for template in templates]
            results = [future.result() for future in futures]

        # Verificar el resultado de cada plantilla
        for template, result in zip(templates, results):
            template_height, template_width = template.shape
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            if max_val > best_match_value:
                best_match_value = max_val
                best_match_location = max_loc
                best_match_size = (template_width, template_height)

        # Dibujar la mejor coincidencia si supera un umbral
        threshold = 0.2  # Ajustar este valor según sea necesario
        if best_match_value >= threshold:
            top_left = best_match_location
            # Volver a escalar las coordenadas a tamaño original
            top_left = (int(top_left[0] * 100 / scale_percent), int(top_left[1] * 100 / scale_percent))
            bottom_right = (top_left[0] + best_match_size[0] * 100 // scale_percent, 
                            top_left[1] + best_match_size[1] * 100 // scale_percent)
            cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)
            cv2.putText(frame, "Cabeza del palo", (top_left[0], top_left[1] - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Mostrar el frame con las detecciones
        cv2.imshow('Detección de Cabeza de Palo de Golf', frame)

        # Salir si se presiona la tecla 'q'
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

        frame_count += 1

    # Liberar el video y cerrar todas las ventanas
    cap.release()
    cv2.destroyAllWindows()

# Ruta del video y lista de plantillas
video_path = 'IMG_2652.MOV'  # Cambia a la ruta de tu video
template_paths = [
    'Tita1.jpg',  # Cambia a la ruta de tu primera plantilla
    'tita2.jpg',
    'tita3.jpg',
    'tita4.jpg',
    'tita5.jpg',
    'tita6.jpg',
    'tita7.jpg'  # Cambia a la ruta de tu segunda plantilla
    # Agrega más plantillas según sea necesario
]

detect_golf_club_head_multiple_templates_optimized(video_path, template_paths)
