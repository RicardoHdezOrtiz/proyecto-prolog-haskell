import subprocess
import sys

def ejecutar_comando(comando):
    """Ejecuta un comando en la terminal y devuelve la salida."""
    try:
        resultado = subprocess.run(comando, shell=True, text=True, capture_output=True)
        if resultado.returncode == 0:
            return resultado.stdout.strip()
        else:
            return f"Error: {resultado.stderr.strip()}"
    except Exception as e:
        return f"Error de ejecución: {e}"

def probar_conexiones():
    print("--- Verificando Conexiones ---")
    
    # Prueba Haskell (GHC)
    # GHCi es el modo interactivo, le pasamos un comando simple
    print("Probando Haskell...")
    res_haskell = ejecutar_comando('ghc -e "putStrLn \\"Haskell conectado correctamente\\""')
    print(f"Respuesta de Haskell: {res_haskell}")

    # Prueba Prolog (SWI-Prolog)
    # Ejecutamos una consulta sencilla (1+1=:=2) para ver si responde
    print("\nProbando Prolog...")
    res_prolog = ejecutar_comando('swipl -q -t "writeln(\'Prolog conectado correctamente\')."')
    print(f"Respuesta de Prolog: {res_prolog}")
    print("------------------------------\n")

def menu_principal():
    while True:
        print("\n=== PROYECTO FINAL: LÓGICA Y FUNCIONAL ===")
        print("1. Probar conexión de lenguajes")
        print("2. Iniciar Sistema Experto (Prolog)")
        print("3. Iniciar Calculadora Analítica (Haskell)")
        print("4. Salir")
        
        opcion = input("Selecciona una opción (1-4): ")
        
        if opcion == '1':
            probar_conexiones()
        elif opcion == '2':
            print("Llamando al archivo experto.pl... (Pronto)")
            # Aquí irá la lógica para llamar a experto.pl
        elif opcion == '3':
            print("Llamando al archivo calculadora.hs... (Pronto)")
            # Aquí irá la lógica para llamar a calculadora.hs
        elif opcion == '4':
            print("Saliendo del sistema...")
            sys.exit()
        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    menu_principal()
    # Prueba de conexion Git