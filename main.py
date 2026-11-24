import subprocess
import sys
from datetime import datetime

RESET   = "\033[0m"
BOLD    = "\033[1m"
ROJO    = "\033[91m"
VERDE   = "\033[92m"
AMARILLO = "\033[93m"
AZUL    = "\033[94m"
CIAN    = "\033[96m"
GRIS    = "\033[90m"

SINTOMAS = [
    ("pc_no_enciende",         "La PC no enciende"),
    ("pitidos_al_arrancar",    "Emite pitidos al arrancar"),
    ("luces_encendidas",       "Encienden luces/LEDs en la placa"),
    ("pantalla_negra",         "Pantalla negra (sin señal)"),
    ("pantalla_azul",          "Pantalla azul (BSOD)"),
    ("ruidos_mecanicos",       "Ruidos mecánicos / chasquidos en disco"),
    ("apagado_repentino",      "Se apaga repentinamente"),
    ("ventiladores_al_maximo", "Ventiladores al máximo de velocidad"),
    ("artefactos_en_pantalla", "Artefactos visuales o líneas en pantalla"),
    ("lentitud_extrema",       "Lentitud extrema del sistema"),
    ("alto_uso_disco",         "Uso de disco al 100% constante"),
    ("sin_internet",           "Sin acceso a internet"),
    ("icono_red_rojo",         "Icono de red con cruz roja"),
    ("hora_desconfigurada",    "Fecha y hora se reinician al apagar"),
]

historial_sesion = []


def registrar_historial(modulo, entrada, salida):
    marca = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    historial_sesion.append({
        "fecha": marca,
        "modulo": modulo,
        "entrada": entrada,
        "salida": salida,
    })


def probar_conexion():
    print(f"\n{AZUL}{BOLD}--- VERIFICACIÓN DE ENTORNOS ---{RESET}")
    for nombre, cmd in [("Prolog (swipl)", ["swipl", "--version"]),
                        ("Haskell (runghc)", ["runghc", "--version"])]:
        try:
            subprocess.run(cmd, capture_output=True, check=True)
            print(f"{VERDE}✅ {nombre} conectado correctamente.{RESET}")
        except Exception:
            print(f"{ROJO}❌ Error: No se encontró {nombre}.{RESET}")


def color_urgencia(nivel):
    return {
        "CRITICA": ROJO + BOLD,
        "ALTA":    AMARILLO + BOLD,
        "MEDIA":   CIAN + BOLD,
        "BAJA":    VERDE + BOLD,
    }.get(nivel, RESET)


def iniciar_sistema_experto():
    print(f"\n{CIAN}{BOLD}--- SISTEMA EXPERTO: DIAGNÓSTICO DE PC (PROLOG) ---{RESET}")
    for idx, (_, descripcion) in enumerate(SINTOMAS, start=1):
        print(f"  {AMARILLO}{idx:2d}.{RESET} {descripcion}")

    entrada = input(
        f"\n{BOLD}Ingresa los números de los síntomas separados por espacio (ej. 4 2 14): {RESET}"
    ).strip()

    if not entrada:
        print(f"{AMARILLO}⚠️ No seleccionaste ningún síntoma.{RESET}")
        return

    seleccionados = []
    for token in entrada.split():
        if token.isdigit() and 1 <= int(token) <= len(SINTOMAS):
            clave = SINTOMAS[int(token) - 1][0]
            if clave not in seleccionados:
                seleccionados.append(clave)
        else:
            print(f"{AMARILLO}⚠️ Número ignorado por inválido: '{token}'{RESET}")

    if not seleccionados:
        print(f"{ROJO}❌ No hubo síntomas válidos para diagnosticar.{RESET}")
        return

    comando = ["swipl", "-q", "-s", "experto.pl", "-g", "consultar", "--"] + seleccionados

    try:
        resultado = subprocess.run(comando, capture_output=True, text=True, check=True)
        salida = resultado.stdout.strip()
    except FileNotFoundError:
        print(f"{ROJO}❌ Error: 'swipl' no está instalado o no está en el PATH.{RESET}")
        return
    except Exception as e:
        print(f"{ROJO}❌ Error al ejecutar Prolog: {e}{RESET}")
        return

    print("\n" + "=" * 65)
    if salida == "SIN_COINCIDENCIA" or not salida:
        msg = "No se encontró una falla exacta para esa combinación de síntomas."
        print(f"{AMARILLO}DIAGNÓSTICO: {msg}{RESET}")
        registrar_historial("Prolog", ", ".join(seleccionados), msg)
    else:
        resumen_log = []
        for linea in salida.splitlines():
            partes = linea.split("|")
            if len(partes) == 3:
                falla, urgencia, solucion = partes
                falla_legible = falla.replace("_", " ").upper()
                c_urg = color_urgencia(urgencia)
                print(f"{BOLD}FALLA:{RESET}    {falla_legible}")
                print(f"{BOLD}URGENCIA:{RESET} {c_urg}{urgencia}{RESET}")
                print(f"{BOLD}SOLUCIÓN:{RESET} {solucion}")
                print(f"{GRIS}" + "-" * 65 + f"{RESET}")
                resumen_log.append(f"{falla_legible} [{urgencia}]: {solucion}")
            else:
                print(linea)
                resumen_log.append(linea)
        registrar_historial("Prolog", ", ".join(seleccionados), " || ".join(resumen_log))
    print("=" * 65)


def iniciar_calculadora():
    print(f"\n{CIAN}{BOLD}--- CALCULADORA ANALÍTICA (HASKELL) ---{RESET}")
    print(f"  {AMARILLO}1.{RESET} Factorial de un número (recursividad)")
    print(f"  {AMARILLO}2.{RESET} Serie de Fibonacci en posición n (evaluación perezosa)")
    print(f"  {AMARILLO}3.{RESET} Verificar si un número es primo")
    print(f"  {AMARILLO}4.{RESET} Listar todos los números primos hasta n (filter)")
    print(f"  {AMARILLO}5.{RESET} Máximo Común Divisor de dos números (Euclides)")
    print(f"  {AMARILLO}6.{RESET} Estadísticas de una lista de números (foldl)")

    op = input(f"\n{BOLD}Selecciona una operación (1-6): {RESET}").strip()

    operaciones = {
        "1": ("factorial",    "Ingresa un número entero (>= 0): "),
        "2": ("fibonacci",    "Ingresa la posición n (>= 0): "),
        "3": ("primo",        "Ingresa un número entero: "),
        "4": ("primos_hasta", "Ingresa el límite superior n (>= 2): "),
        "5": ("mcd",          "Ingresa DOS enteros separados por espacio (ej. 48 18): "),
        "6": ("estadisticas", "Ingresa una lista de números separados por espacio (ej. 10 25.5 30): "),
    }

    if op not in operaciones:
        print(f"{AMARILLO}⚠️ Operación inválida.{RESET}")
        return

    nombre_op, prompt = operaciones[op]
    entrada = input(prompt).strip()
    if not entrada:
        print(f"{AMARILLO}⚠️ No ingresaste valores.{RESET}")
        return

    argumentos = entrada.split()
    comando = ["runghc", "calculadora.hs", nombre_op] + argumentos

    try:
        resultado = subprocess.run(comando, capture_output=True, text=True)
        salida = resultado.stdout.strip()
        if not salida and resultado.stderr:
            print(f"{ROJO}❌ Error de Haskell: {resultado.stderr.strip()}{RESET}")
            return
    except FileNotFoundError:
        print(f"{ROJO}❌ Error: 'runghc' no está instalado o no está en el PATH.{RESET}")
        return
    except Exception as e:
        print(f"{ROJO}❌ Error al ejecutar Haskell: {e}{RESET}")
        return

    print("\n" + "=" * 65)
    color_res = ROJO if salida.startswith("Error:") else VERDE + BOLD
    print(f"{color_res}RESULTADO:{RESET} {salida}")
    print("=" * 65)
    registrar_historial("Haskell", f"{nombre_op} {entrada}", salida)


def ver_o_exportar_historial():
    print(f"\n{AZUL}{BOLD}--- HISTORIAL DE LA SESIÓN ---{RESET}")
    if not historial_sesion:
        print(f"{GRIS}Aún no se han realizado consultas en esta sesión.{RESET}")
        return

    for idx, item in enumerate(historial_sesion, start=1):
        print(f"{AMARILLO}{idx}.{RESET} [{item['fecha']}] ({item['modulo']}) "
              f"Entrada: {item['entrada']} -> {item['salida']}")

    exportar = input(f"\n¿Exportar historial a 'historial_sesion.txt'? (s/n): ").strip().lower()
    if exportar == "s":
        nombre_archivo = "historial_sesion.txt"
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            f.write("=== HISTORIAL DE SESIÓN - PROYECTO MULTIPARADIGMA ===\n\n")
            for idx, item in enumerate(historial_sesion, start=1):
                f.write(f"{idx}. [{item['fecha']}] [{item['modulo']}]\n")
                f.write(f"   Entrada:   {item['entrada']}\n")
                f.write(f"   Resultado: {item['salida']}\n\n")
        print(f"{VERDE}✅ Historial guardado en '{nombre_archivo}'.{RESET}")


def menu_principal():
    while True:
        print(f"\n{AZUL}{BOLD}=============================================={RESET}")
        print(f"{AZUL}{BOLD}   PROYECTO FINAL: LÓGICA Y FUNCIONAL         {RESET}")
        print(f"{AZUL}{BOLD}=============================================={RESET}")
        print(f"  {AMARILLO}1.{RESET} Probar conexión de lenguajes")
        print(f"  {AMARILLO}2.{RESET} Sistema Experto de Diagnóstico (Prolog)")
        print(f"  {AMARILLO}3.{RESET} Calculadora Analítica (Haskell)")
        print(f"  {AMARILLO}4.{RESET} Ver / Exportar historial de sesión")
        print(f"  {AMARILLO}5.{RESET} Salir")

        opcion = input(f"\n{BOLD}Selecciona una opción (1-5): {RESET}").strip()

        if opcion == "1":
            probar_conexion()
        elif opcion == "2":
            iniciar_sistema_experto()
        elif opcion == "3":
            iniciar_calculadora()
        elif opcion == "4":
            ver_o_exportar_historial()
        elif opcion == "5":
            print(f"{VERDE}Saliendo del programa. ¡Hasta luego!{RESET}")
            sys.exit()
        else:
            print(f"{ROJO}Opción no válida. Intenta de nuevo.{RESET}")


if __name__ == "__main__":
    menu_principal()