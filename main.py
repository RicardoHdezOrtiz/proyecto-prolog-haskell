import subprocess
import sys

def probar_conexion():
    print("\nProbando conexiones...")
    try:
        subprocess.run(["swipl", "--version"], capture_output=True, check=True)
        print("✅ Prolog (swipl) conectado correctamente.")
    except Exception:
        print("❌ Error: No se encontró Prolog (swipl).")
        
    try:
        subprocess.run(["runghc", "--version"], capture_output=True, check=True)
        print("✅ Haskell (runghc) conectado correctamente.")
    except Exception:
        print("❌ Error: No se encontró Haskell (runghc).")

def iniciar_sistema_experto():
    print("\n--- SISTEMA EXPERTO: DIAGNÓSTICO DE PC ---")
    print("Síntomas disponibles:")
    print("- pc_no_enciende         - pantalla_negra")
    print("- pitidos_al_arrancar    - luces_encendidas")
    print("- apagado_repentino      - ventiladores_al_maximo")
    print("- pantalla_azul          - ruidos_mecanicos")
    
    entrada = input("\nIngresa los síntomas que presenta tu equipo (separados por espacio): ").strip()
    
    if not entrada:
        print("⚠️ No ingresaste ningún síntoma. Cancelando diagnóstico.")
        return

    sintomas = entrada.split()
    
    # Preparamos el comando para llamar a Prolog. 
    # El "--" al final le indica a Prolog que lo que sigue son argumentos del usuario.
    comando = ["swipl", "-q", "-s", "experto.pl", "-g", "consultar", "--"] + sintomas
    
    try:
        resultado = subprocess.run(comando, capture_output=True, text=True)
        print("\n" + "="*50)
        print(resultado.stdout.strip())
        print("="*50)
    except Exception as e:
        print(f"❌ Error al ejecutar Prolog: {e}")

def menu_principal():
    while True:
        print("\n=== PROYECTO FINAL: LÓGICA Y FUNCIONAL ===")
        print("1. Probar conexión de lenguajes")
        print("2. Iniciar Sistema Experto (Prolog)")
        print("3. Iniciar Calculadora Analítica (Haskell)")
        print("4. Salir")
        
        opcion = input("Selecciona una opción (1-4): ").strip()
        
        if opcion == '1':
            probar_conexion()
        elif opcion == '2':
            iniciar_sistema_experto()
        elif opcion == '3':
            print("\n⚙️ Opción en desarrollo... (Falta conectar Haskell)")
        elif opcion == '4':
            print("Saliendo del programa. ¡Adiós!")
            sys.exit()
        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    menu_principal()