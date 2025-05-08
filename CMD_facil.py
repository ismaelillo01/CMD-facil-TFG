import os
import json
import shutil
import requests
import re
import shutil
import subprocess
import zipfile
from dotenv import load_dotenv
load_dotenv()


HISTORIAL_RENOMBRADO = "historial.json"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = os.getenv("GEMINI_API_URL")


def guardar_historial(historial):
    """Guarda el historial de operaciones en un archivo JSON."""
    with open(HISTORIAL_RENOMBRADO, "w", encoding="utf-8") as f:
        json.dump(historial, f, indent=4, ensure_ascii=False)

def cargar_historial():
    """Carga el historial de operaciones desde un archivo JSON."""
    if os.path.exists(HISTORIAL_RENOMBRADO):
        with open(HISTORIAL_RENOMBRADO, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def extraer_numero(texto):
    # Busca el primer número en el texto 
    match = re.search(r'\d+', texto)
    return int(match.group()) if match else float('inf')  # 'inf' al final si no encuentra número

def seleccionar_archivos(directorio):
    """Permite seleccionar archivos específicos o todos los archivos en un directorio."""
    archivos = [f for f in os.listdir(directorio) if os.path.isfile(os.path.join(directorio, f))]
    if not archivos:
        print("No hay archivos en el directorio.")
        return []

    print("\nArchivos disponibles:")
    for i, archivo in enumerate(archivos, 1):
        print(f"{i}. {archivo}")

    seleccion = input("Introduce los números de los archivos separados por comas, o * para todos: ")

    if seleccion.strip() == "*":
        seleccionados = archivos
    else:
        try:
            indices = [int(i) - 1 for i in seleccion.split(",")]
            seleccionados = [archivos[i] for i in indices if 0 <= i < len(archivos)]
        except ValueError:
            print("Selección inválida.")
            return []

    # Ordenar por número extraído del nombre
    seleccionados.sort(key=lambda x: (extraer_numero(x), x.lower()))

    return seleccionados



def renombrar_archivos(directorio, prefijo):
    """Renombra archivos seleccionados en un directorio y guarda el historial."""
    if not os.path.exists(directorio):
        print("El directorio no existe.")
        return
    
    archivos = seleccionar_archivos(directorio)
    if not archivos:
        return

    usar_numeracion = input("¿Quieres añadir numeración automática al nombre? (s/n): ").strip().lower()
    if usar_numeracion == "s":
        try:
            inicio = int(input("Número inicial: "))
            incremento = int(input("Incremento entre archivos: "))
        except ValueError:
            print("Entrada inválida.")
            return
    else:
        inicio = None
        incremento = None

    historial = cargar_historial()
    if "operaciones" not in historial:
        historial["operaciones"] = []
    cambios = []

    for i, archivo in enumerate(archivos):
        ruta_antigua = os.path.join(directorio, archivo)
        extension = os.path.splitext(archivo)[1]

        if inicio is not None and incremento is not None:
            numero = inicio + i * incremento
            nuevo_nombre = f"{prefijo}{numero}{extension}"
        else:
            nuevo_nombre = f"{prefijo}{extension}"

        ruta_nueva = os.path.join(directorio, nuevo_nombre)

        os.rename(ruta_antigua, ruta_nueva)
        cambios.append((ruta_nueva, ruta_antigua))
        print(f"Renombrado: {archivo} → {nuevo_nombre}")
    
    if cambios:
        historial["operaciones"].append(cambios)
        guardar_historial(historial)

def copiar_archivos(origen, destino):
    """Copia archivos seleccionados de un directorio a otro con soporte para deshacer."""
    if not os.path.exists(origen):
        print("El directorio de origen no existe.")
        return
    if not os.path.exists(destino):
        os.makedirs(destino)
    
    archivos = seleccionar_archivos(origen)
    if not archivos:
        return

    historial = cargar_historial()
    if "operaciones" not in historial:
        historial["operaciones"] = []
    cambios = []

    for archivo in archivos:
        ruta_origen = os.path.join(origen, archivo)
        ruta_destino = os.path.join(destino, archivo)
        shutil.copy2(ruta_origen, ruta_destino)
        cambios.append((ruta_destino, "copiado"))
        print(f"Copiado: {archivo} → {destino}")

    if cambios:
        historial["operaciones"].append({
            "tipo": "copiar",
            "archivos": cambios
        })
        guardar_historial(historial)
        print("Operación de copia registrada en el historial.")


def mover_archivos(origen, destino):
    """Mueve archivos seleccionados de un directorio a otro con soporte para deshacer."""
    if not os.path.exists(origen):
        print("El directorio de origen no existe.")
        return
    if not os.path.exists(destino):
        os.makedirs(destino)
    
    archivos = seleccionar_archivos(origen)
    if not archivos:
        return

    historial = cargar_historial()
    if "operaciones" not in historial:
        historial["operaciones"] = []
    cambios = []

    for archivo in archivos:
        ruta_origen = os.path.join(origen, archivo)
        ruta_destino = os.path.join(destino, archivo)
        shutil.move(ruta_origen, ruta_destino)
        cambios.append((ruta_destino, ruta_origen))  # Registrar origen y destino para revertir
        print(f"Movido: {archivo} → {destino}")

    if cambios:
        historial["operaciones"].append({
            "tipo": "mover",
            "archivos": cambios
        })
        guardar_historial(historial)
        print("Operación de movimiento registrada en el historial.")


def eliminar_duplicados(directorio):
    """Elimina archivos duplicados en un directorio con soporte para deshacer."""
    if not os.path.exists(directorio):
        print("El directorio no existe.")
        return
    
    archivos_vistos = set()
    eliminados = []

    for archivo in os.listdir(directorio):
        ruta_archivo = os.path.join(directorio, archivo)
        if os.path.isfile(ruta_archivo):
            if archivo in archivos_vistos:
                os.remove(ruta_archivo)
                eliminados.append(ruta_archivo)  # Registrar archivo eliminado
                print(f"Eliminado duplicado: {archivo}")
            else:
                archivos_vistos.add(archivo)

    if eliminados:
        historial = cargar_historial()
        if "operaciones" not in historial:
            historial["operaciones"] = []
        historial["operaciones"].append({
            "tipo": "eliminar",
            "archivos": eliminados
        })
        guardar_historial(historial)
        print("Operación de eliminación registrada en el historial.")


def cargar_historial():
    """Carga el historial desde un archivo JSON si existe, sino devuelve un diccionario vacío."""
    if os.path.exists("historial.json"):
        with open("historial.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def seleccionar_carpetas(directorio):
    """Muestra las subcarpetas y permite seleccionar cuáles renombrar."""
    try:
        carpetas = [nombre for nombre in os.listdir(directorio) if os.path.isdir(os.path.join(directorio, nombre))]
        if not carpetas:
            print("No hay carpetas en el directorio.")
            return []

        print("\nCarpetas disponibles:")
        for i, carpeta in enumerate(carpetas, start=1):
            print(f"{i}. {carpeta}")

        seleccion = input("\nElige carpetas por número separadas por comas (ej: 1,3,5) o '*' para todas: ").strip()
        
        if seleccion == "*":
            return carpetas
        else:
            try:
                indices = [int(x.strip()) - 1 for x in seleccion.split(",")]
                return [carpetas[i] for i in indices if 0 <= i < len(carpetas)]
            except ValueError:
                print("Selección inválida.")
                return []
    
    except FileNotFoundError:
        print("El directorio no existe.")
        return []


def renombrar_carpetas(directorio, prefijo):
    carpetas = seleccionar_carpetas(directorio)
    carpetas.sort(key=lambda nombre: int(re.search(r'\d+', nombre).group()) if re.search(r'\d+', nombre) else float('inf'))
    if not carpetas:
        return

    usar_numeracion = input("¿Quieres añadir numeración automática al nombre? (s/n): ").strip().lower()
    if usar_numeracion == "s":
        try: 
            ancho = len(input("Formato de números (ejemplo: 001 → 3 dígitos): ").strip())  
            inicio = int(input("Número inicial (ejemplo: 001): "))           
            incremento = int(input("Incremento entre carpetas: "))
        except ValueError:
            print("Entrada inválida.")
            return
    else:
        inicio = None
        incremento = None
        ancho = 0

    historial = cargar_historial()
    if "operaciones" not in historial:
        historial["operaciones"] = []
    cambios = []

    for i, carpeta in enumerate(carpetas):
        ruta_antigua = os.path.join(directorio, carpeta)

        if inicio is not None and incremento is not None:
            numero = str(inicio + i * incremento).zfill(ancho)
            nuevo_nombre = f"{prefijo}{numero}"
        else:
            nuevo_nombre = f"{prefijo}"

        ruta_nueva = os.path.join(directorio, nuevo_nombre)

        os.rename(ruta_antigua, ruta_nueva)
        cambios.append((ruta_nueva, ruta_antigua))
        print(f"Renombrado: {carpeta} → {nuevo_nombre}")

    if cambios:
        historial["operaciones"].append({
            "tipo": "renombrar_carpetas",
            "cambios": cambios
        })
        guardar_historial(historial)


def comprimir_subcarpetas_a_rar(directorio):
    if not os.path.exists(directorio):
        print(f"❌ El directorio '{directorio}' no existe.")
        return

    if shutil.which("rar") is None:
        print("❌ El comando 'rar' no está disponible. Asegúrate de tenerlo instalado y añadido al PATH.")
        return

    subcarpetas = [carpeta for carpeta in os.listdir(directorio) if os.path.isdir(os.path.join(directorio, carpeta))]

    for carpeta in subcarpetas:
        ruta_carpeta = os.path.join(directorio, carpeta)
        archivo_rar = os.path.join(directorio, f"{carpeta}.rar")

        try:
            # Comprimir el contenido, no la carpeta
            subprocess.run(["rar", "a", "-r", archivo_rar, "."], cwd=ruta_carpeta, check=True)
            print(f"✅ Comprimida: {carpeta} → {archivo_rar}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error al comprimir '{carpeta}':", e)

def comprimir_subcarpetas_a_cbz(directorio):
    if not os.path.exists(directorio):
        print(f"❌ El directorio '{directorio}' no existe.")
        return

    subcarpetas = [carpeta for carpeta in os.listdir(directorio) if os.path.isdir(os.path.join(directorio, carpeta))]

    for carpeta in subcarpetas:
        ruta_carpeta = os.path.join(directorio, carpeta)
        archivo_cbz = os.path.join(directorio, f"{carpeta}.cbz")

        try:
            with zipfile.ZipFile(archivo_cbz, 'w', zipfile.ZIP_DEFLATED) as cbz:
                for root, _, files in os.walk(ruta_carpeta):
                    for file in files:
                        ruta_completa = os.path.join(root, file)
                        ruta_relativa = os.path.relpath(ruta_completa, ruta_carpeta)
                        cbz.write(ruta_completa, ruta_relativa)
            print(f"✅ Comprimida: {carpeta} → {archivo_cbz}")
        except Exception as e:
            print(f"❌ Error al crear el archivo CBZ para '{carpeta}': {e}")


def deshacer_ultima_operacion():
    """Revierte la última operación realizada."""
    historial = cargar_historial()

    if "operaciones" not in historial or not historial["operaciones"]:
        print("No hay operaciones para deshacer.")
        return

    ultima_operacion = historial["operaciones"].pop()  # Quitar la última operación del historial

    if ultima_operacion["tipo"] == "copiar":
        # Eliminar los archivos copiados
        for archivo, _ in ultima_operacion["archivos"]:
            if os.path.exists(archivo):
                os.remove(archivo)
                print(f"Eliminado archivo copiado: {archivo}")
    elif ultima_operacion["tipo"] == "mover":
        # Mover los archivos de vuelta a su origen
        for destino, origen in ultima_operacion["archivos"]:
            if os.path.exists(destino):
                shutil.move(destino, origen)
                print(f"Movido de vuelta: {destino} → {origen}")
    elif ultima_operacion["tipo"] == "eliminar":
        # Restaurar los archivos eliminados
        for archivo in ultima_operacion["archivos"]:
            print(f"Restaurar manualmente si es necesario: {archivo}")

    guardar_historial(historial)
    print("Deshacer completado.")


def interpretar_comando_gemini(comando_usuario):
    """Interpreta el comando en lenguaje natural usando la API de Gemini con directrices claras."""
    if not GEMINI_API_KEY or not GEMINI_API_URL:
        print("Error: La clave de API y la URL de Gemini deben configurarse como variables de entorno.")
        return None
    
    api_url = f"{GEMINI_API_URL}/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    
    prompt = f"Por favor, convierte el siguiente texto en un comando directo para la terminal, sin explicaciones adicionales. Si alguna información como rutas de archivos o parámetros necesarios no está establecida en el texto, indícalo claramente en tu respuesta junto con el comando para que pueda completarse correctamente: {comando_usuario}"

    payload = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }]
    }
    headers = {
        "Content-Type": "application/json"
    }

    try:
        respuesta = requests.post(api_url, json=payload, headers=headers)
        if respuesta.status_code == 200:
            respuesta_json = respuesta.json()
            contenido_generado = respuesta_json['candidates'][0]['content']['parts'][0]['text']
            return contenido_generado.strip()
        else:
            print("Error al comunicarse con la API:", respuesta.status_code)
            print("Detalles:", respuesta.json())
            return None
    except Exception as e:
        print("Excepción al usar la API de Gemini:", str(e))
        return None

def ejecutar_comando_personalizado():
    """Permite al usuario introducir comandos en lenguaje natural de forma dinámica."""
    while True:
        print("\nComando personalizado. Escribe 'salir' para volver al menú principal.")
        accion = input("Describe lo que quieres hacer (por ejemplo, 'mueve la carpeta' o 'renombra archivos'): ").lower()
        if accion == 'salir':
            print("Saliendo de la ejecución de comandos personalizados...")
            break

        # Detectar si la acción requiere rutas
        necesita_origen = "origen" in accion or "mueve" in accion or "copia" in accion
        necesita_destino = "destino" in accion or "mueve" in accion or "copia" in accion
        
        # Pedir rutas si es necesario
        if necesita_origen:
            origen = input("¿Dónde está la carpeta o archivo que quieres usar? Escribe la ruta completa: ")
        else:
            origen = None
        
        if necesita_destino:
            destino = input("¿A dónde quieres moverlo/copiarlo? Escribe la ruta completa: ")
        else:
            destino = None

        # Construir el prompt con la información obtenida
        comando_usuario = accion
        if origen and destino:
            comando_usuario += f" desde {origen} hacia {destino}"
        elif origen:
            comando_usuario += f" desde {origen}"
        elif destino:
            comando_usuario += f" hacia {destino}"

        # Interpretar el comando con Gemini
        resultado_gemini = interpretar_comando_gemini(comando_usuario)

        if resultado_gemini:
            print(f"Gemini interpretó: {resultado_gemini}")
            confirmar = input("¿Deseas ejecutar este comando? (s/n): ").strip().lower()
            if confirmar == 's':
                try:
                    os.system(resultado_gemini)
                    
                    # Registrar el comando en el historial si es necesario
                    historial = cargar_historial()
                    if "operaciones" not in historial:
                        historial["operaciones"] = []
                    historial["operaciones"].append({
                        "tipo": "gemini",
                        "comando": resultado_gemini,
                        "origen": origen,
                        "destino": destino
                    })
                    guardar_historial(historial)
                    print("Comando ejecutado y registrado en el historial.")
                except Exception as e:
                    print(f"Error al ejecutar el comando: {str(e)}")
            else:
                print("Ejecución cancelada.")
        else:
            print("No se pudo interpretar el comando.")


if __name__ == "__main__":
    while True:
        print("\nOpciones:")
        print("1. Renombrar archivos")
        print("2. Copiar archivos")
        print("3. Mover archivos")
        print("4. Eliminar archivos duplicados")
        print("5. Deshacer última operación")
        print("6. Ejecutar comandos personalizados (lenguaje natural)")
        print("7. Renombrar carpetas")
        print("8. Comprimir subcarpetas a .rar")
        print("9. Comprimir subcarpetas a .cbz")  
        print("10. Salir")  

        opcion = input("Elige una opción: ")

        if opcion == "1":
            carpeta = input("Introduce la ruta de la carpeta: ")
            prefijo = input("Introduce el prefijo para los archivos: ")
            renombrar_archivos(carpeta, prefijo)
        elif opcion == "2":
            origen = input("Introduce la ruta de la carpeta de origen: ")
            destino = input("Introduce la ruta de la carpeta de destino: ")
            copiar_archivos(origen, destino)
        elif opcion == "3":
            origen = input("Introduce la ruta de la carpeta de origen: ")
            destino = input("Introduce la ruta de la carpeta de destino: ")
            mover_archivos(origen, destino)
        elif opcion == "4":
            carpeta = input("Introduce la ruta de la carpeta para eliminar duplicados: ")
            eliminar_duplicados(carpeta)
        elif opcion == "5":
            deshacer_ultima_operacion()
        elif opcion == "6":
            ejecutar_comando_personalizado()
        elif opcion == "7":
            carpeta = input("Introduce la ruta del directorio donde están las carpetas a renombrar: ")
            prefijo = input("Introduce el prefijo para las carpetas: ")
            renombrar_carpetas(carpeta, prefijo)
        elif opcion == "8":
            directorio = input("Introduce la ruta del directorio con las subcarpetas a comprimir en .rar: ")
            comprimir_subcarpetas_a_rar(directorio)
        elif opcion == "9":
            directorio = input("Introduce la ruta del directorio con las subcarpetas a convertir en .cbz: ")
            comprimir_subcarpetas_a_cbz(directorio)
        elif opcion == "10":
            print("Saliendo del programa. ¡Hasta luego!")
            break
        else:
            print("Opción no válida, intenta de nuevo.")



