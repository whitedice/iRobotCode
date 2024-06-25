# run_script.py
import subprocess

def run_script(script_name, *args):
    # Pfad zum Python 3.7 Interpreter (angepasst für Ihr spezielles Setup)
    python37_path = 'C:\\Users\\eisen\\AppData\\Local\\Microsoft\\WindowsApps\\python3.7.exe' 

    # Bauen des Befehls
    command = [python37_path, script_name] + list(args)
    
    # Subprozess starten und Ausgabe erfassen
    result = subprocess.run(command, text=True, capture_output=True)

    if result.returncode == 0:
        print("Erfolg! Ausgabe:")
        print(result.stdout)
    else:
        print("Fehler bei der Ausführung des Skripts:")
        print(result.stderr)

    return result.stdout

# Aufrufen des Skripts, das sich im gleichen Ordner befindet
output = run_script("script.py", "10", "20", "30")
print("Erhaltene Ausgabe vom Skript:", output)
