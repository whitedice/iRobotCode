# script.py
import sys

def main():
    print("Laufendes Python-Skript mit Python 3.7")
    print("Erhaltene Argumente:", sys.argv[1:])  # Druckt alle übergebenen Argumente außer dem Skriptnamen selbst
    
    # Einfache Berechnung, um die Funktionalität zu demonstrieren
    if len(sys.argv) > 1:
        numbers = map(int, sys.argv[1:])
        result = sum(numbers)
        print("Die Summe der Zahlen ist:", result)
    else:
        print("Keine Zahlen zum Addieren bereitgestellt.")

if __name__ == "__main__":
    main()
