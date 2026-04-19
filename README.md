# 🚗 SeguimientoVehicular-VC

Proyecto de visión por computador que detecta y sigue el movimiento de un vehículo en un video. El sistema separa el vehículo del fondo, limpia la imagen para reducir el ruido y calcula la posición del vehículo en cada fotograma para analizar su trayectoria.

---

## 🛠️ Tecnologías utilizadas

- **Python**
- **OpenCV** `4.13.0` — captura de video, procesamiento de imagen y visualización
- **NumPy** `2.4.3` — operaciones matriciales sobre los fotogramas
- **Matplotlib** `3.10.8` — visualización de resultados y gráficas de movimiento

---

## ▶️ ¿Cómo ejecutarlo?

1. Clona el repositorio:
   ```bash
   git clone https://github.com/OswaldGutierrez/SeguimientoVehicular-VisionPorComputadora.git
   ```

2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Abre el archivo principal en tu editor (VS Code, PyCharm, etc.) y ejecútalo con el botón **Run** o:
   ```bash
   python main.py
   ```

4. Se abrirá una ventana de visualización. Usa las siguientes teclas para navegar entre los pasos del procesamiento:

   | Tecla | Acción |
   |-------|--------|
   | `D`   | Siguiente paso |
   | `A`   | Paso anterior  |

---

## 📸 Vista previa

![Vista previa del proyecto](https://github.com/OswaldGutierrez/SeguimientoVehicular-VisionPorComputadora/blob/22acd9d89c577705f6a0adfbb7ef146a005f8770/MascaraLimpia.png)

---

## 📚 Lo que aprendí

Durante el desarrollo de este proyecto trabajé por primera vez con visión por computador aplicada a video en tiempo real. Aprendí a separar el fondo de un objeto en movimiento usando sustracción de fondo, técnica fundamental en análisis de video. También comprendí la importancia del preprocesamiento de imagen: aplicar filtros para eliminar ruido antes de detectar contornos mejora considerablemente la precisión del seguimiento. Finalmente, entendí cómo representar la posición de un objeto a lo largo del tiempo para construir una trayectoria visual.

---

## 👤 Autores

**Oswald David Gutiérrez Cortina**  
Estudiante de Ingeniería — Universidad  
[LinkedIn](www.linkedin.com/in/oswald-david-gutierrez-1a452939a) · [GitHub]([https://github.com/tu-usuario](https://github.com/OswaldGutierrez))

**Miguel Puerta**

**Juan Andraus**
