import subprocess
import keyboard

scripts_paths = ("./controller.py", "./main.py",'./functions.py')

# Iniciar los procesos y almacenar los objetos Popen en una lista
ps = [subprocess.Popen(["python3", script]) for script in scripts_paths]

try:
    # Ciclo para esperar a que el usuario presione una tecla para detener los procesos
    while True:
        if keyboard.is_pressed("q"):  # Puedes cambiar la tecla según tu preferencia
            print("Deteniendo procesos...")
            # Terminar los procesos
            for p in ps:
                p.terminate()
            break
except KeyboardInterrupt:
    pass

# Esperar a que los procesos terminen y almacenar los códigos de salida
exit_codes = [p.wait() for p in ps]

if all(code == 0 for code in exit_codes):
    print("Todos los procesos terminaron con éxito")
else:
    print("Algunos procesos terminaron de forma inesperada.")
