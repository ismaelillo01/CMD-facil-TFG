# TFG-CMD

### Consola Avanzada con IA Integrada

## 1. Introducción
Este manual de usuario proporciona instrucciones detalladas sobre el uso de **TFG-CMD**, una consola avanzada con inteligencia artificial integrada. La aplicación permite realizar tareas como renombrar, copiar, mover archivos y ejecutar comandos personalizados mediante IA.

---

## 2. Requisitos del sistema
- **Sistema operativo:** Windows, Linux o macOS.
- **Python:** Versión 3.x instalada.
- **Conexión a Internet** (para el uso de la IA).

---

## 3. Instalación
1. Descarga el archivo del script principal.
2. Asegúrate de tener **Python** instalado en tu sistema.
3. Instala las dependencias necesarias ejecutando:
   ```bash
   pip install requests
   ```
4. Ejecuta el script desde la terminal con:
   ```bash
   python CMD_facil.py
   ```

---

## 4. Uso del Programa
Al iniciar el programa, se mostrará un menú con varias opciones:

### 📂 Renombrar archivos
1. Introduce la ruta del directorio donde se encuentran los archivos.
2. Especifica un prefijo para renombrar los archivos secuencialmente.
3. Los cambios se guardarán en el historial.

### 📄 Copiar archivos
1. Introduce la ruta del directorio de **origen**.
2. Introduce la ruta del directorio de **destino**.
3. Se copiarán los archivos seleccionados y se registrará la operación.

### 📦 Mover archivos
1. Introduce la ruta del directorio de **origen**.
2. Introduce la ruta del directorio de **destino**.
3. Se moverán los archivos y se registrará la operación.

### 🗑️ Eliminar archivos duplicados
1. Introduce la ruta del directorio.
2. Se eliminarán los archivos duplicados y la operación quedará registrada.

### 🔄 Deshacer última operación
- Revierte la última operación registrada en el historial (**copiar, mover o eliminar**).

### 🤖 Ejecutar comandos personalizados (lenguaje natural)
1. Introduce una acción en lenguaje natural (ejemplo: *"Mueve todos los archivos de la carpeta A a la carpeta B"*).
2. El sistema usará la **IA** para interpretar y generar el comando adecuado.
3. Se preguntará al usuario si desea ejecutarlo antes de proceder.

### ❌ Salir
- Termina la ejecución del programa.

---

## 5. Historial de operaciones
Todas las acciones realizadas quedan registradas en un archivo JSON (**historial.json**), permitiendo su consulta y reversión en caso de ser necesario.

**Notas adicionales:**
- La opción **"Deshacer última operación"** permite restaurar archivos eliminados, revertir movimientos y eliminar copias recientes.
- La funcionalidad de IA requiere acceso a Internet y una **clave de API** válida para interactuar con **Gemini**.
- Si la API de **Gemini** no responde, se mostrará un mensaje de error y se solicitará una nueva entrada al usuario.

---

## 6. Métodos Implementados
### 📌 Métodos de gestión de historial
- **`guardar_historial(historial)`**: Guarda el historial de operaciones en un archivo JSON.
- **`cargar_historial()`**: Carga el historial desde un archivo JSON (si existe) o devuelve un diccionario vacío.

### 📌 Métodos de manipulación de archivos
- **`seleccionar_archivos(directorio)`**: Lista los archivos de un directorio y permite seleccionarlos.
- **`renombrar_archivos(directorio, prefijo)`**: Renombra archivos con un prefijo personalizado.
- **`copiar_archivos(origen, destino)`**: Copia archivos entre directorios y los registra en el historial.
- **`mover_archivos(origen, destino)`**: Mueve archivos entre directorios y guarda el registro.
- **`eliminar_duplicados(directorio)`**: Elimina archivos duplicados y los registra en el historial.
- **`deshacer_ultima_operacion()`**: Revierte la última acción realizada (copia, movimiento o eliminación).

### 📌 Métodos de integración con IA
- **`interpretar_comando_gemini(comando_usuario)`**: Usa la API de **Gemini** para interpretar comandos en lenguaje natural.
- **`ejecutar_comando_personalizado()`**: Permite al usuario ingresar comandos en lenguaje natural, interpretarlos con **Gemini** y ejecutarlos en la consola.

---



⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⡀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠉⢻⠟⢹⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⡄⠀⠀⣼⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣄⣠⣤⣄⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⡿⠋⠀⣀⣀⠈⣿⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣇⠘⠋⠀⣿⠇⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡟⠀⢀⣾⠟⠻⠿⠿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀⣀⡀⠀⠀⣾⠋⢀⣀⠈⠻⢶⣄⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⠁⣰⡿⠁⠀⣀⣤⣶⣶⡶⢶⣤⣄⡀⢀⣠⠴⠚⠉⠉⠉⠉⠉⠙⢶⡄⠛⠒⠛⠙⢳⣦⡀⠹⣆⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⢠⣿⣠⣴⣿⡟⢉⣠⠤⠶⠶⠾⠯⣿⣿⣧⣀⣤⣶⣾⣿⡿⠿⠛⠋⢙⣛⡛⠳⣄⡀⠙⣷⡀⢹⡆
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⢸⣿⣿⣿⣿⠞⠉⠀⠀⠀⠀⣀⣤⣤⠬⠉⠛⠻⠿⠟⠉⢀⣠⢞⣭⣤⣤⣍⠙⠺⢷⡀⢸⡇⠀⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⢸⣿⣿⡟⠀⠀⠀⢀⣠⠞⣫⢗⣫⢽⣶⣤⣀⠉⠛⣶⠖⠛⠀⣾⡷⣾⠋⣻⡆⠀⠀⡇⣼⠇⠀⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀⣿⣿⡇⢠⡤⠔⣋⡤⠞⠁⢸⣷⣾⣯⣹⣿⡆⢀⣏⠀⠈⠈⣿⣷⣼⣿⠿⠷⣴⡞⠀⣿⠀⠀⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀⢿⣿⡇⠀⠀⠘⠻⠤⣀⡀⠸⣿⣯⣿⣿⡿⠷⠚⠉⠛⠛⠛⠛⠉⠉⠀⣠⡾⠛⣦⢸⡏⠀⠀⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀⢸⣿⡇⠀⣠⠶⠶⠶⠶⠿⣿⣭⣭⣁⣀⣠⣤⣤⣤⣤⣤⣤⡶⠶⠛⠋⢁⣀⣴⠟⣽⠇⠀⠀⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀⢸⣿⡇⢾⣅⠀⠀⠶⠶⢦⣤⣤⣀⣉⣉⣉⣉⣁⣡⣤⣤⣴⡶⠶⠶⠚⠉⢉⡿⣠⠟⠀⠀⣰⡟
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡀⠀⠀⢿⣇⠀⠈⠛⠳⠶⠤⠤⢤⣀⣉⣉⣉⣉⣉⣉⣁⣀⣠⣤⡤⠤⠤⠶⠞⢻⡟⠃⠀⠀⣰⠟⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣧⠀⠀⠘⣿⣦⣄⡀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠉⠉⠉⠁⠀⠀⠀⠀⠀⣠⣤⣶⣿⣧⣀⣴⠟⠃⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣆⠀⠀⠈⢻⣿⣿⣷⣶⣤⣄⣀⣀⣀⣠⣤⣶⣶⣶⣶⣶⣶⣶⣶⣿⣿⣿⣿⣿⣿⣟⡉⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣦⡄⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⣿⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡧⠀⠀⠀


### 🚀 *TFG desarrollado por Ismael Franco Yañez*

