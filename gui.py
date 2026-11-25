import subprocess
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime

ARCHIVO_PROLOG = "experto.pl"
ARCHIVO_HASKELL = "calculadora.hs"

SINTOMAS = [
    ("pc_no_enciende", "La PC no enciende"),
    ("luces_encendidas", "Luces / LEDs encendidos"),
    ("pitidos_al_arrancar", "Pitidos al arrancar"),
    ("pantalla_negra", "Pantalla negra sin video"),
    ("pantalla_azul", "Pantalla azul (BSOD)"),
    ("ruidos_mecanicos", "Ruidos mecánicos en disco"),
    ("apagado_repentino", "Apagado repentino"),
    ("ventiladores_al_maximo", "Ventiladores al máximo"),
    ("artefactos_en_pantalla", "Artefactos / líneas en pantalla"),
    ("lentitud_extrema", "Lentitud extrema"),
    ("alto_uso_disco", "Alto uso de disco (100%)"),
    ("sin_internet", "Sin conexión a Internet"),
    ("icono_red_rojo", "Icono de red en rojo / desconectado"),
    ("hora_desconfigurada", "Hora y fecha desconfiguradas"),
]

# Sincronizado 100% con calculadora.hs
OPERACIONES_HASKELL = {
    "Factorial (n)": ("factorial", "Número entero >= 0 (ej. 6):"),
    "Fibonacci en posición (n)": ("fibonacci", "Posición entera >= 0 (ej. 10):"),
    "Verificar si es primo (n)": ("primo", "Número entero (ej. 17):"),
    "Listar primos hasta (n)": ("primos_hasta", "Límite entero >= 2 (ej. 30):"),
    "MCD Euclides (a b)": ("mcd", "Dos enteros separados por espacio (ej. 48 18):"),
    "Estadísticas de lista": ("estadisticas", "Números separados por espacio (ej. 8.5 9.0 10 4.5):"),
}


class AppMultiparadigma:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Multiparadigma — Python + Prolog + Haskell")
        self.root.geometry("840x640")
        self.root.configure(bg="#1e1e2e")

        self.historial = []
        self._configurar_estilos()
        self._construir_interfaz()

    def _configurar_estilos(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook", background="#1e1e2e", borderwidth=0)
        style.configure("TNotebook.Tab", background="#313244", foreground="#cdd6f4", padding=[14, 8], font=("Helvetica", 11, "bold"))
        style.map("TNotebook.Tab", background=[("selected", "#89b4fa")], foreground=[("selected", "#11111b")])
        style.configure("TFrame", background="#1e1e2e")
        style.configure("TLabel", background="#1e1e2e", foreground="#cdd6f4", font=("Helvetica", 11))
        style.configure("Header.TLabel", font=("Helvetica", 15, "bold"), foreground="#89b4fa")
        style.configure("Accent.TButton", font=("Helvetica", 11, "bold"), padding=8)

    def _construir_interfaz(self):
        header = ttk.Label(
            self.root,
            text="Proyecto Final: Programación Lógica y Funcional",
            style="Header.TLabel",
        )
        header.pack(pady=(15, 5))

        sub = ttk.Label(
            self.root,
            text="Orquestador Gráfico (Python) • Motor Lógico (SWI-Prolog) • Cálculo Puro (Haskell)",
        )
        sub.pack(pady=(0, 12))

        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        tab_prolog = ttk.Frame(notebook)
        tab_haskell = ttk.Frame(notebook)
        tab_historial = ttk.Frame(notebook)

        notebook.add(tab_prolog, text="  Sistema Experto (Prolog)  ")
        notebook.add(tab_haskell, text="  Calculadora Funcional (Haskell)  ")
        notebook.add(tab_historial, text="  Historial y Entorno  ")

        self._construir_tab_prolog(tab_prolog)
        self._construir_tab_haskell(tab_haskell)
        self._construir_tab_historial(tab_historial)

    def _construir_tab_prolog(self, parent):
        ttk.Label(parent, text="Selecciona los síntomas observados en el equipo:").pack(anchor="w", padx=15, pady=(12, 8))

        grid_frame = ttk.Frame(parent)
        grid_frame.pack(fill="x", padx=15)

        self.vars_sintomas = {}
        for idx, (clave, etiqueta) in enumerate(SINTOMAS):
            var = tk.BooleanVar()
            self.vars_sintomas[clave] = var
            chk = tk.Checkbutton(
                grid_frame,
                text=etiqueta,
                variable=var,
                bg="#1e1e2e",
                fg="#cdd6f4",
                selectcolor="#313244",
                activebackground="#1e1e2e",
                activeforeground="#89b4fa",
                font=("Helvetica", 11),
            )
            chk.grid(row=idx // 2, column=idx % 2, sticky="w", padx=8, pady=3)

        btn_frame = ttk.Frame(parent)
        btn_frame.pack(fill="x", padx=15, pady=12)

        ttk.Button(btn_frame, text="Ejecutar Diagnóstico en Prolog", style="Accent.TButton", command=self.ejecutar_prolog).pack(side="left", padx=(0, 10))
        ttk.Button(btn_frame, text="Limpiar Selección", command=self.limpiar_prolog).pack(side="left")

        self.txt_prolog = tk.Text(parent, height=11, bg="#11111b", fg="#a6e3a1", font=("Menlo", 11), relief="flat", padx=10, pady=10)
        self.txt_prolog.pack(fill="both", expand=True, padx=15, pady=(0, 15))

    def _construir_tab_haskell(self, parent):
        ttk.Label(parent, text="Selecciona la función pura en Haskell:").pack(anchor="w", padx=15, pady=(15, 6))

        self.combo_op = ttk.Combobox(parent, values=list(OPERACIONES_HASKELL.keys()), state="readonly", font=("Helvetica", 11), width=40)
        self.combo_op.current(0)
        self.combo_op.pack(anchor="w", padx=15)
        self.combo_op.bind("<<ComboboxSelected>>", self._actualizar_ayuda_haskell)

        self.lbl_ayuda_hs = ttk.Label(parent, text="Número entero >= 0 (ej. 6):")
        self.lbl_ayuda_hs.pack(anchor="w", padx=15, pady=(12, 4))

        self.entry_hs = tk.Entry(parent, font=("Menlo", 12), bg="#313244", fg="#cdd6f4", insertbackground="white", relief="flat", width=42)
        self.entry_hs.pack(anchor="w", padx=15, ipady=6)

        ttk.Button(parent, text="Evaluar en Haskell (GHC)", style="Accent.TButton", command=self.ejecutar_haskell).pack(anchor="w", padx=15, pady=14)

        self.txt_haskell = tk.Text(parent, height=12, bg="#11111b", fg="#89dceb", font=("Menlo", 11), relief="flat", padx=10, pady=10)
        self.txt_haskell.pack(fill="both", expand=True, padx=15, pady=(0, 15))

    def _construir_tab_historial(self, parent):
        top = ttk.Frame(parent)
        top.pack(fill="x", padx=15, pady=12)

        ttk.Button(top, text="Verificar Entornos (swipl / runghc)", command=self.verificar_entornos).pack(side="left", padx=(0, 10))
        ttk.Button(top, text="Exportar Historial (.txt)", style="Accent.TButton", command=self.exportar_historial).pack(side="left")

        self.txt_historial = tk.Text(parent, bg="#11111b", fg="#f9e2af", font=("Menlo", 11), relief="flat", padx=10, pady=10)
        self.txt_historial.pack(fill="both", expand=True, padx=15, pady=(0, 15))

    def _actualizar_ayuda_haskell(self, _event=None):
        seleccion = self.combo_op.get()
        _, ayuda = OPERACIONES_HASKELL[seleccion]
        self.lbl_ayuda_hs.config(text=ayuda)

    def _registrar_historial(self, modulo, entrada, salida):
        marca = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        registro = f"[{marca}] ({modulo}) Entrada: {entrada}\n{salida}\n{'-'*55}\n"
        self.historial.append(registro)
        self.txt_historial.insert("end", registro)
        self.txt_historial.see("end")

    def limpiar_prolog(self):
        for var in self.vars_sintomas.values():
            var.set(False)
        self.txt_prolog.delete("1.0", "end")

    def _formatear_salida_prolog(self, crudo):
        if crudo == "SIN_COINCIDENCIA":
            return (
                "No se encontró una regla exacta para esa combinación de síntomas.\n"
                "Sugerencia: Selecciona síntomas complementarios (ej. pantalla negra + pitidos)."
            )

        lineas_formateadas = []
        for idx, linea in enumerate(crudo.splitlines(), start=1):
            partes = linea.split("|")
            if len(partes) == 3:
                falla = partes[0].replace("_", " ").upper()
                urgencia = partes[1]
                solucion = partes[2]
                lineas_formateadas.append(
                    f"{idx}. [{urgencia}] {falla}\n   Solución: {solucion}"
                )
            else:
                lineas_formateadas.append(linea)
        return "\n\n".join(lineas_formateadas)

    def ejecutar_prolog(self):
        seleccionados = [k for k, v in self.vars_sintomas.items() if v.get()]
        if not seleccionados:
            messagebox.showwarning("Sin síntomas", "Selecciona al menos un síntoma para diagnosticar.")
            return

        # === [1. ORQUESTADOR PYTHON -> PROLOG] ===
        # Envia sintomas por terminal (subprocess) y atrapa la respuesta (stdout)
        try:
            comando = ["swipl", "-q", "-s", ARCHIVO_PROLOG, "-g", "consultar", "--"] + seleccionados
            res = subprocess.run(
                comando,
                capture_output=True,
                text=True,
                check=False,
            )
            crudo = res.stdout.strip() or res.stderr.strip() or "Sin respuesta de Prolog."
            salida = self._formatear_salida_prolog(crudo)
            self.txt_prolog.delete("1.0", "end")
            self.txt_prolog.insert("end", salida)
            self._registrar_historial("Prolog", ", ".join(seleccionados), salida)
        except FileNotFoundError:
            messagebox.showerror("Error", "No se encontró 'swipl' en el PATH del sistema.")

    def ejecutar_haskell(self):
        seleccion = self.combo_op.get()
        comando, _ = OPERACIONES_HASKELL[seleccion]
        parametro = self.entry_hs.get().strip()
        if not parametro:
            messagebox.showwarning("Dato faltante", "Ingresa un valor antes de evaluar.")
            return

        try:
            # === [2. ORQUESTADOR PYTHON -> HASKELL] ===
            # Separa los parametros y ejecuta el calculo puro en GHC
            argumentos = parametro.replace(",", " ").split()
            res = subprocess.run(
                ["runghc", ARCHIVO_HASKELL, comando] + argumentos,
                capture_output=True,
                text=True,
                check=False,
            )
            salida = res.stdout.strip() or res.stderr.strip() or "Sin respuesta de Haskell."
            self.txt_haskell.delete("1.0", "end")
            self.txt_haskell.insert("end", salida)
            self._registrar_historial("Haskell", f"{comando} {' '.join(argumentos)}", salida)
        except FileNotFoundError:
            messagebox.showerror("Error", "No se encontró 'runghc' en el PATH del sistema.")

    def verificar_entornos(self):
        self.txt_historial.delete("1.0", "end")
        for herramienta in ["python3", "swipl", "runghc"]:
            try:
                res = subprocess.run([herramienta, "--version"], capture_output=True, text=True)
                linea = (res.stdout or res.stderr).splitlines()[0]
                self.txt_historial.insert("end", f"[OK] {herramienta}: {linea}\n")
            except Exception as exc:
                self.txt_historial.insert("end", f"[ERROR] {herramienta}: {exc}\n")

    def exportar_historial(self):
        if not self.historial:
            messagebox.showinfo("Historial vacío", "Aún no hay consultas registradas en esta sesión.")
            return
        ruta = filedialog.asksaveasfilename(
            defaultextension=".txt",
            initialfile="historial_gui.txt",
            filetypes=[("Archivos de texto", "*.txt")],
        )
        if ruta:
            with open(ruta, "w", encoding="utf-8") as f:
                f.writelines(self.historial)
            messagebox.showinfo("Exportado", f"Historial guardado en:\n{ruta}")


if __name__ == "__main__":
    root = tk.Tk()
    app = AppMultiparadigma(root)
    root.mainloop()