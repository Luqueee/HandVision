import subprocess
import keyboard
import json

with open("./app/data/commands.json", "w", encoding="UTF-8") as file:
    json.dump({
    "scroll": [False, 0, 0],
    "drag": [False, 0, 0],
    "click": [False],
    "straight": [False]
}, file, indent=4)

with open("./app/data/positions.json", "w", encoding="UTF-8") as file:
    json.dump([], file, indent=4)


scripts_paths = ("./app/controller.py", "./app/main.py",'./app/mouse.py','./app/scroll.py')

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
