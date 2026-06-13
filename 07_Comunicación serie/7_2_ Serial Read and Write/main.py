# Proyecto 7.2 - Lectura y escritura serial con ESP32-S3 WROOM
# Comunicación bidireccional mediante MicroPython
# ====================================================

# Mostrar mensaje inicial indicando que el sistema está preparado
print("ESP32-S3 ready")

# Bucle infinito para mantener el programa ejecutándose
while True:
    
    # Esperar texto desde el ordenador mediante input()
    # El programa se detiene aquí hasta que el usuario escriba algo y pulse ENTER
    mensaje = input()
    
    # Mostrar el texto recibido usando print()
    # Confirmamos que hemos recibido el mensaje
    print("Recibido:", mensaje)
