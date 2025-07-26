import tkinter as tk
from tkinter import font, messagebox, Toplevel, Radiobutton, StringVar
import pandas as pd
from datetime import datetime, timedelta
import os

# --- ARCHIVOS DE CONFIGURACIÓN ---
# Se han cambiado los nombres de los archivos para forzar la creación de nuevos archivos limpios
ARCHIVO_REGISTRO = 'registro_personal_nuevo.xlsx'
ARCHIVO_EMPLEADOS = 'empleados_nuevo.xlsx'
DURACION_ALMUERZO_MINUTOS = 60 # Duración fija del almuerzo en minutos

# --- LÓGICA DE DATOS (EXCEL) ---

def inicializar_archivos():
    """Asegura que ambos archivos Excel existan con las columnas correctas.
    Crea los archivos si no existen y añade columnas faltantes si es necesario."""
    print("Inicializando archivos...")
    
    # Columnas esperadas para empleados.xlsx
    columnas_empleados_esperadas = ['id empleado', 'nombre completo', 'edad', 'cargo', 'jornada horas']
    
    # Inicializar ARCHIVO_EMPLEADOS
    if not os.path.exists(ARCHIVO_EMPLEADOS):
        print(f"'{ARCHIVO_EMPLEADOS}' no encontrado, creando...")
        df_empleados = pd.DataFrame(columns=columnas_empleados_esperadas)
        try:
            df_empleados.to_excel(ARCHIVO_EMPLEADOS, index=False)
            messagebox.showinfo("Información", f"El archivo '{ARCHIVO_EMPLEADOS}' ha sido creado con las columnas requeridas.")
            print(f"'{ARCHIVO_EMPLEADOS}' creado exitosamente.")
        except Exception as e:
            messagebox.showerror("Error de Creación", f"No se pudo crear '{ARCHIVO_EMPLEADOS}'. Error: {e}")
            print(f"Error al crear '{ARCHIVO_EMPLEADOS}': {e}")
            return False
    else:
        # Si el archivo existe, verificar y normalizar columnas, y añadir si faltan
        print(f"'{ARCHIVO_EMPLEADOS}' encontrado, verificando y normalizando...")
        try:
            df_empleados = pd.read_excel(ARCHIVO_EMPLEADOS)
            
            # Normalizar nombres de columnas existentes y eliminar duplicados
            df_empleados.columns = df_empleados.columns.str.lower().str.strip()
            df_empleados = df_empleados.loc[:, ~df_empleados.columns.duplicated(keep='first')]

            columna_mapping_empleados = {
                'id_empleado': 'id empleado',
                'nombre_completo': 'nombre completo',
                'jornada_laboral_horas': 'jornada horas' # Por si venía de una versión anterior
            }
            actual_rename_map_empleados = {old_name: new_name for old_name, new_name in columna_mapping_empleados.items() 
                                        if old_name in df_empleados.columns}
            df_empleados.rename(columns=actual_rename_map_empleados, inplace=True)
            
            # Añadir columnas faltantes
            for col in columnas_empleados_esperadas:
                if col not in df_empleados.columns:
                    df_empleados[col] = pd.NA
                    messagebox.showinfo("Actualización", f"La columna '{col}' ha sido añadida a '{ARCHIVO_EMPLEADOS}'.")
                    print(f"Columna '{col}' añadida a '{ARCHIVO_EMPLEADOS}'.")
            
            df_empleados = df_empleados.reindex(columns=columnas_empleados_esperadas)
            df_empleados.to_excel(ARCHIVO_EMPLEADOS, index=False)
            print(f"'{ARCHIVO_EMPLEADOS}' normalizado y guardado.")
        except Exception as e:
            messagebox.showerror("Error al normalizar/actualizar", f"Error al normalizar o actualizar '{ARCHIVO_EMPLEADOS}': {e}")
            print(f"Error al normalizar/actualizar '{ARCHIVO_EMPLEADOS}': {e}")
            return False
            
    # Columnas esperadas para registro_personal.xlsx
    columnas_registro_esperadas = ['id empleado', 'nombre completo', 'cargo', 'fecha', 'hora entrada', 
                                   'jornada horas', 'hora inicio almuerzo', 'hora fin almuerzo', 
                                   'hora salida', 'horas trabajadas', 'tiempo extra minutos', 
                                   'tiempo almuerzo minutos']
    
    # Inicializar ARCHIVO_REGISTRO
    if not os.path.exists(ARCHIVO_REGISTRO):
        print(f"'{ARCHIVO_REGISTRO}' no encontrado, creando...")
        df_registro = pd.DataFrame(columns=columnas_registro_esperadas)
        try:
            df_registro.to_excel(ARCHIVO_REGISTRO, index=False)
            messagebox.showinfo("Información", f"El archivo '{ARCHIVO_REGISTRO}' ha sido creado con las columnas requeridas.")
            print(f"'{ARCHIVO_REGISTRO}' creado exitosamente.")
        except Exception as e:
            messagebox.showerror("Error de Creación", f"No se pudo crear '{ARCHIVO_REGISTRO}'. Error: {e}")
            print(f"Error al crear '{ARCHIVO_REGISTRO}': {e}")
            return False
    else:
        # Si el archivo existe, verificar y normalizar columnas, y añadir si faltan
        print(f"'{ARCHIVO_REGISTRO}' encontrado, verificando y normalizando...")
        try:
            df_registro = pd.read_excel(ARCHIVO_REGISTRO)
            
            # Normalizar nombres de columnas existentes y eliminar duplicados
            df_registro.columns = df_registro.columns.str.lower().str.strip()
            df_registro = df_registro.loc[:, ~df_registro.columns.duplicated(keep='first')]

            columna_mapping_registro = {
                'id_empleado': 'id empleado',
                'nombre_completo': 'nombre completo',
                'hora_entrada': 'hora entrada',
                'jornada_laboral_horas': 'jornada horas',
                'hora_inicio_almuerzo': 'hora inicio almuerzo',
                'hora_fin_almuerzo': 'hora fin almuerzo',
                'hora_salida': 'hora salida',
                'horas_trabajadas': 'horas trabajadas',
                'tiempo_extra_minutos': 'tiempo extra minutos',
                'tiempo_almuerzo_minutos': 'tiempo almuerzo minutos'
            }
            actual_rename_map_registro = {old_name: new_name for old_name, new_name in columna_mapping_registro.items() 
                                        if old_name in df_registro.columns}
            df_registro.rename(columns=actual_rename_map_registro, inplace=True)

            # Añadir columnas faltantes
            for col in columnas_registro_esperadas:
                if col not in df_registro.columns:
                    df_registro[col] = pd.NA
                    messagebox.showinfo("Actualización", f"La columna '{col}' ha sido añadida a '{ARCHIVO_REGISTRO}'.")
                    print(f"Columna '{col}' añadida a '{ARCHIVO_REGISTRO}'.")
            
            df_registro = df_registro.reindex(columns=columnas_registro_esperadas)
            df_registro.to_excel(ARCHIVO_REGISTRO, index=False)
            print(f"'{ARCHIVO_REGISTRO}' normalizado y guardado.")
        except Exception as e:
            messagebox.showerror("Error de Actualización", f"No se pudo verificar/actualizar '{ARCHIVO_REGISTRO}'. Error: {e}")
            print(f"Error de actualización en '{ARCHIVO_REGISTRO}': {e}")
            return False
    print("Inicialización de archivos completada.")
    return True

def obtener_datos_empleado(id_empleado):
    """Busca un empleado en empleados.xlsx y devuelve sus datos."""
    print(f"Obteniendo datos para ID: {id_empleado}")
    try:
        df_empleados = pd.read_excel(ARCHIVO_EMPLEADOS)
        df_empleados.columns = df_empleados.columns.str.lower().str.strip()
        
        if 'id empleado' in df_empleados.columns:
            df_empleados['id empleado'] = df_empleados['id empleado'].astype(str).str.upper().str.strip()
        else:
            messagebox.showerror("Error de Columna", "La columna 'id empleado' no se encontró en 'empleados.xlsx'.")
            print("Error: Columna 'id empleado' no encontrada en empleados.xlsx.")
            return None

        id_empleado_normalizado = str(id_empleado).upper().strip()
        
        datos = df_empleados[df_empleados['id empleado'] == id_empleado_normalizado]
        if not datos.empty:
            print(f"Datos de empleado encontrados: {datos.iloc[0].to_dict()}")
            return datos.iloc[0].to_dict()
        else:
            print(f"ID de empleado '{id_empleado_normalizado}' no encontrado.")
            return None
    except FileNotFoundError:
        messagebox.showerror("Error de Archivo", f"El archivo '{ARCHIVO_EMPLEADOS}' no se encontró.")
        print(f"Error: Archivo '{ARCHIVO_EMPLEADOS}' no encontrado.")
        return None
    except Exception as e:
        messagebox.showerror("Error de Lectura", f"Error al leer '{ARCHIVO_EMPLEADOS}': {e}")
        print(f"Error al leer '{ARCHIVO_EMPLEADOS}': {e}")
        return None

def verificar_registro_hoy(id_empleado):
    """Verifica el estado del registro del empleado para hoy.
    Retorna: 'completo' si ya marcó salida, 'parcial' si solo tiene entrada, False si no tiene registro."""
    print(f"Verificando registro de hoy para ID: {id_empleado}")
    try:
        df = pd.read_excel(ARCHIVO_REGISTRO)
        df.columns = df.columns.str.lower().str.strip() # Normalizar columnas
    except FileNotFoundError:
        print(f"'{ARCHIVO_REGISTRO}' no encontrado para verificación.")
        return False
    except Exception as e:
        print(f"Error al leer '{ARCHIVO_REGISTRO}' para verificación: {e}")
        return False

    hoy = datetime.now().strftime('%Y-%m-%d')
    id_empleado_normalizado = str(id_empleado).upper().strip()
    
    if 'id empleado' in df.columns and 'fecha' in df.columns:
        df['id empleado'] = df['id empleado'].astype(str).str.upper().str.strip()
        registro_hoy = df[(df['id empleado'] == id_empleado_normalizado) & 
                          (df['fecha'] == hoy)]
        
        if not registro_hoy.empty:
            salida_marcada = pd.notna(registro_hoy.iloc[0]['hora salida'])
            if salida_marcada:
                print(f"Registro completo para hoy (salida marcada).")
                return 'completo'
            else:
                print(f"Registro parcial para hoy (solo entrada).")
                return 'parcial'
    print("No hay registro para hoy.")
    return False

def obtener_registro_actual(id_empleado):
    """Obtiene el registro actual del empleado para hoy."""
    print(f"Obteniendo registro actual para ID: {id_empleado}")
    try:
        df = pd.read_excel(ARCHIVO_REGISTRO)
        df.columns = df.columns.str.lower().str.strip()
    except FileNotFoundError:
        print(f"'{ARCHIVO_REGISTRO}' no encontrado.")
        return None
    except Exception as e:
        print(f"Error al leer '{ARCHIVO_REGISTRO}': {e}")
        return None

    hoy = datetime.now().strftime('%Y-%m-%d')
    id_empleado_normalizado = str(id_empleado).upper().strip()
    
    if 'id empleado' in df.columns and 'fecha' in df.columns:
        df['id empleado'] = df['id empleado'].astype(str).str.upper().str.strip()
        registro_hoy = df[(df['id empleado'] == id_empleado_normalizado) & 
                          (df['fecha'] == hoy)]
        
        if not registro_hoy.empty:
            print(f"Registro actual encontrado: {registro_hoy.iloc[0].to_dict()}")
            return registro_hoy.iloc[0].to_dict()
    
    print("No hay registro actual.")
    return None

def registrar_evento(id_empleado, evento, jornada_horas=None):
    """Registra un evento (entrada, almuerzo, salida) en el archivo de registro."""
    print(f"Registrando evento '{evento}' para ID: {id_empleado}")
    try:
        df = pd.read_excel(ARCHIVO_REGISTRO)
        df.columns = df.columns.str.lower().str.strip()
        print(f"'{ARCHIVO_REGISTRO}' leído exitosamente.")
    except FileNotFoundError:
        messagebox.showerror("Error", "El archivo de registro no existe. Por favor, reinicie la aplicación.")
        print(f"Error: '{ARCHIVO_REGISTRO}' no encontrado en registrar_evento.")
        return None
    except Exception as e:
        messagebox.showerror("Error de Lectura", f"Error al leer '{ARCHIVO_REGISTRO}': {e}")
        print(f"Error al leer '{ARCHIVO_REGISTRO}' en registrar_evento: {e}")
        return None

    hoy = datetime.now().strftime('%Y-%m-%d')
    hora_actual = datetime.now().strftime('%H:%M:%S')

    id_empleado_normalizado = str(id_empleado).upper().strip()

    idx = df[(df['id empleado'] == id_empleado_normalizado) & (df['fecha'] == hoy)].index

    if evento == "entrada":
        if not idx.empty:
            messagebox.showinfo("Información", "Ya se ha registrado una entrada para este empleado hoy.")
            print("Entrada ya registrada para hoy.")
            return df.loc[idx[0]].to_dict()
        
        if jornada_horas is None:
            messagebox.showerror("Error", "Las horas de jornada son requeridas para el registro de entrada.")
            print("Error: Horas de jornada no proporcionadas para la entrada.")
            return None

        datos_empleado = obtener_datos_empleado(id_empleado_normalizado)
        if datos_empleado is None:
            messagebox.showerror("Error", "ID de empleado no encontrado en el archivo de empleados.")
            print("Error: ID de empleado no encontrado en empleados.xlsx.")
            return None

        nuevo_registro = {
            'id empleado': id_empleado_normalizado,
            'nombre completo': datos_empleado.get('nombre completo', 'N/A'),
            'cargo': datos_empleado.get('cargo', 'N/A'),
            'fecha': hoy,
            'hora entrada': hora_actual,
            'jornada horas': jornada_horas,
            'hora inicio almuerzo': pd.NA,
            'hora fin almuerzo': pd.NA,
            'hora salida': pd.NA,
            'horas trabajadas': pd.NA,
            'tiempo extra minutos': pd.NA,
            'tiempo almuerzo minutos': pd.NA
        }
        df = pd.concat([df, pd.DataFrame([nuevo_registro])], ignore_index=True)
        print(f"Intentando guardar el registro de entrada en '{ARCHIVO_REGISTRO}'...")
        try:
            df.to_excel(ARCHIVO_REGISTRO, index=False)
            print(f"Registro de entrada guardado en '{ARCHIVO_REGISTRO}'.")
        except Exception as e:
            messagebox.showerror("Error de Escritura", f"No se pudo guardar el registro de entrada en '{ARCHIVO_REGISTRO}'. Error: {e}")
            print(f"Error al guardar registro de entrada: {e}")
            return None
        return nuevo_registro

    elif idx.empty:
        messagebox.showerror("Error", "Debe registrar la entrada antes de cualquier otro evento.")
        print("Error: Entrada no registrada para el evento actual.")
        return None
    
    idx_row = idx[0]

    if evento == "inicio_almuerzo":
        df.loc[idx_row, 'hora inicio almuerzo'] = hora_actual
    elif evento == "fin_almuerzo":
        df.loc[idx_row, 'hora fin almuerzo'] = hora_actual
        try:
            inicio_alm_str = str(df.loc[idx_row, 'hora inicio almuerzo'])
            fin_alm_str = hora_actual
            
            inicio_alm = datetime.strptime(inicio_alm_str, '%H:%M:%S')
            fin_alm = datetime.strptime(fin_alm_str, '%H:%M:%S')
            
            tiempo_almuerzo = fin_alm - inicio_alm
            df.loc[idx_row, 'tiempo almuerzo minutos'] = round(tiempo_almuerzo.total_seconds() / 60)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo calcular el tiempo de almuerzo: {e}")
            print(f"Error al calcular tiempo de almuerzo: {e}")
            
    elif evento == "salida":
        df.loc[idx_row, 'hora salida'] = hora_actual
        try:
            entrada_str = str(df.loc[idx_row, 'hora entrada'])
            salida_str = hora_actual
            jornada_horas = float(df.loc[idx_row, 'jornada horas']) 
            
            entrada = datetime.strptime(entrada_str, '%H:%M:%S')
            salida = datetime.strptime(salida_str, '%H:%M:%S')
            
            tiempo_almuerzo = timedelta(0)
            inicio_alm_str = df.loc[idx_row, 'hora inicio almuerzo']
            fin_alm_str = df.loc[idx_row, 'hora fin almuerzo']

            if pd.notna(inicio_alm_str) and pd.notna(fin_alm_str):
                inicio_alm = datetime.strptime(str(inicio_alm_str), '%H:%M:%S')
                fin_alm = datetime.strptime(str(fin_alm_str), '%H:%M:%S')
                tiempo_almuerzo = fin_alm - inicio_alm

            tiempo_trabajado = (salida - entrada) - tiempo_almuerzo
            horas_trabajadas_decimal = round(tiempo_trabajado.total_seconds() / 3600, 2)
            df.loc[idx_row, 'horas trabajadas'] = horas_trabajadas_decimal
            
            tiempo_extra_segundos = max(0, tiempo_trabajado.total_seconds() - (jornada_horas * 3600))
            df.loc[idx_row, 'tiempo extra minutos'] = round(tiempo_extra_segundos / 60)

        except Exception as e:
            messagebox.showerror("Error de Cálculo", f"No se pudieron calcular las horas. Error: {e}")
            print(f"Error de cálculo en salida: {e}")

    print(f"Intentando guardar el evento '{evento}' en '{ARCHIVO_REGISTRO}'...")
    try:
        df.to_excel(ARCHIVO_REGISTRO, index=False)
        print(f"Evento '{evento}' guardado en '{ARCHIVO_REGISTRO}'.")
    except Exception as e:
        messagebox.showerror("Error de Escritura", f"No se pudo guardar el evento '{evento}' en '{ARCHIVO_REGISTRO}'. Error: {e}")
        print(f"Error al guardar evento '{evento}': {e}")
        return None
    return df.loc[idx_row].to_dict()

# --- INTERFAZ GRÁFICA (GUI) ---

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Registro de Personal v3.0")
        self.geometry("900x700")
        self.configure(bg="#2c3e50")

        container = tk.Frame(self, bg="#2c3e50")
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (LoginPage, DashboardPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginPage")

    def show_frame(self, page_name, data=None):
        frame = self.frames[page_name]
        if data:
            frame.set_data(data)
        frame.tkraise()

    def handle_login_and_jornada(self, id_empleado, selected_jornada_horas):
        print(f"handle_login_and_jornada llamado con ID: {id_empleado}, Jornada: {selected_jornada_horas}")
        
        try:
            # Verificar que el empleado aún existe
            datos_empleado = obtener_datos_empleado(id_empleado)
            if not datos_empleado:
                messagebox.showerror("Error", "ID de empleado no encontrado.")
                print("Error: ID de empleado no encontrado en handle_login_and_jornada.")
                return
                
            print("Datos de empleado obtenidos en handle_login_and_jornada.")
            
            # Intentar registrar la entrada
            registro_actual = registrar_evento(id_empleado, "entrada", jornada_horas=selected_jornada_horas)
            
            if registro_actual:
                print("Registro de entrada exitoso. Mostrando Dashboard.")
                # Combinar datos del empleado con el registro
                datos_completos = {**datos_empleado, **registro_actual}
                
                # Forzar la actualización de la ventana principal
                self.update()
                
                # Mostrar el dashboard
                self.show_frame("DashboardPage", data=datos_completos)
                
                # Mensaje de confirmación
                messagebox.showinfo("Entrada Registrada", 
                                  f"¡Bienvenido {datos_empleado.get('nombre completo', '')}!\n"
                                  f"Entrada registrada exitosamente para jornada de {selected_jornada_horas} horas.")
            else:
                print("Fallo al registrar evento de entrada.")
                messagebox.showerror("Error", "No se pudo registrar la entrada. Intente nuevamente.")
                
        except Exception as e:
            print(f"Error en handle_login_and_jornada: {e}")
            messagebox.showerror("Error de Sistema", f"Ocurrió un error inesperado: {e}")
        
        print("Fin de handle_login_and_jornada.")


class JornadaSelectionDialog(Toplevel):
    def __init__(self, parent, id_empleado, callback):
        super().__init__(parent)
        self.id_empleado = id_empleado
        self.callback = callback
        self.transient(parent)
        self.grab_set() # Captura todos los eventos hasta que se destruya
        self.title("Seleccionar Jornada Laboral")
        self.geometry("350x300")  # Aumenté la altura
        self.resizable(False, False)
        self.configure(bg="#34495e")

        self.jornada_var = StringVar(self)
        self.jornada_var.set("7")

        label_font = font.Font(family="Helvetica", size=12, weight="bold")
        button_font = font.Font(family="Helvetica", size=10, weight="bold")

        # Título y texto explicativo
        title_label = tk.Label(self, text=f"ID: {id_empleado}", 
                              font=label_font, fg="#ecf0f1", bg="#34495e")
        title_label.pack(pady=(15, 5))
        
        instruction_label = tk.Label(self, text="Seleccione su jornada laboral:", 
                                    font=label_font, fg="#ecf0f1", bg="#34495e")
        instruction_label.pack(pady=(0, 15))

        # Frame para los radio buttons
        radio_frame = tk.Frame(self, bg="#34495e")
        radio_frame.pack(pady=10)

        jornadas = [4, 5, 6, 7]
        for jornada in jornadas:
            radio_btn = Radiobutton(radio_frame, text=f"{jornada} horas", 
                                   variable=self.jornada_var, value=str(jornada),
                                   font=label_font, bg="#34495e", fg="#ecf0f1", 
                                   selectcolor="#2c3e50", activebackground="#34495e",
                                   activeforeground="#ecf0f1")
            radio_btn.pack(anchor="w", padx=20, pady=5)

        # Botón "Confirmar Jornada" - ASEGURAR QUE SE MUESTRE
        button_frame = tk.Frame(self, bg="#34495e")
        button_frame.pack(pady=20)
        
        confirm_button = tk.Button(button_frame, text="Confirmar Jornada", 
                                  font=button_font, bg="#27ae60", fg="white", 
                                  command=self.on_confirm,
                                  width=15, height=2)
        confirm_button.pack()

        # Centrar la ventana
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (self.winfo_width() // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")

        # Permitir cerrar con Enter
        self.bind('<Return>', lambda event: self.on_confirm())
        self.focus_set()

    def on_confirm(self):
        print("DEBUG: Entrando a JornadaSelectionDialog.on_confirm")
        selected_jornada = float(self.jornada_var.get())
        print(f"Jornada seleccionada: {selected_jornada}")
        
        # Liberar el grab antes de cualquier operación
        self.grab_release()
        print("Grab released.")
        
        try:
            # Llamar al callback con los parámetros correctos
            self.callback(self.id_empleado, selected_jornada)
            print("Callback (handle_login_and_jornada) llamado exitosamente.")
        except Exception as e:
            print(f"Error llamando al callback: {e}")
            messagebox.showerror("Error de Aplicación", f"Ocurrió un error al procesar la jornada: {e}")
        finally:
            # Asegurar que la ventana se cierre
            self.destroy()
            print("JornadaSelectionDialog destruida.")

    def on_closing(self):
        """Maneja el cierre de la ventana con la X"""
        self.grab_release()
        self.destroy()

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#2c3e50")
        self.controller = controller

        title_font = font.Font(family="Helvetica", size=24, weight="bold")
        label_font = font.Font(family="Helvetica", size=14)
        button_font = font.Font(family="Helvetica", size=12, weight="bold")

        main_frame = tk.Frame(self, bg="#34495e", bd=5, relief=tk.GROOVE)
        main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        tk.Label(main_frame, text="Control de Acceso", font=title_font, fg="#ecf0f1", bg="#34495e").pack(pady=(20, 10), padx=50)
        tk.Label(main_frame, text="Ingrese su ID de Empleado", font=label_font, fg="#ecf0f1", bg="#34495e").pack(pady=10, padx=50)

        self.id_entry = tk.Entry(main_frame, font=label_font, width=20, justify='center')
        self.id_entry.pack(pady=10, padx=50)
        self.id_entry.focus()
        
        self.id_entry.bind("<Return>", self.login)

        login_button = tk.Button(main_frame, text="Ingresar", font=button_font, bg="#2980b9", fg="#ecf0f1", command=self.login)
        login_button.pack(pady=20, padx=50, ipadx=10, ipady=5)

    def login(self, event=None):
        id_empleado = self.id_entry.get().strip().upper()
        print(f"Intento de login para ID: {id_empleado}")
        
        if not id_empleado:
            messagebox.showwarning("Entrada Inválida", "Por favor, ingrese un ID.")
            print("Advertencia: ID de empleado vacío.")
            return
        
        # Verificar el estado del registro del empleado
        estado_registro = verificar_registro_hoy(id_empleado)
        
        if estado_registro == 'completo':
            messagebox.showinfo("Registro Completo", "Este empleado ya completó su registro para hoy.")
            print("Info: Empleado ya completó registro hoy.")
            self.id_entry.delete(0, tk.END)
            return
        
        # Verificar que el empleado existe
        datos_empleado = obtener_datos_empleado(id_empleado)
        if not datos_empleado:
            messagebox.showerror("Error", "ID de empleado no encontrado.")
            print("Error: ID de empleado no encontrado en la base de datos.")
            self.id_entry.delete(0, tk.END)
            return
        
        if estado_registro == 'parcial':
            # El empleado ya tiene entrada registrada, ir directo al dashboard
            print("Empleado ya registrado hoy. Cargando dashboard directamente.")
            registro_actual = obtener_registro_actual(id_empleado)
            if registro_actual:
                # Combinar datos del empleado con el registro actual
                datos_completos = {**datos_empleado, **registro_actual}
                self.controller.show_frame("DashboardPage", data=datos_completos)
                messagebox.showinfo("Bienvenido de Nuevo", 
                                f"¡Hola {datos_empleado.get('nombre completo', '')}!\n"
                                f"Continuando con tu jornada laboral.")
            else:
                messagebox.showerror("Error", "No se pudo cargar el registro actual.")
        else:
            # Empleado nuevo del día, pedir jornada laboral
            print("Empleado nuevo del día. Abriendo diálogo de jornada.")
            try:
                # Crear y mostrar el diálogo de jornada
                dialog = JornadaSelectionDialog(self.controller, id_empleado, 
                                            self.controller.handle_login_and_jornada)
                
                # Configurar el protocolo de cierre
                dialog.protocol("WM_DELETE_WINDOW", dialog.on_closing)
                
                # Esperar a que el diálogo se muestre completamente
                dialog.wait_window()
                
            except Exception as e:
                print(f"Error al crear diálogo de jornada: {e}")
                messagebox.showerror("Error", f"Error al mostrar selección de jornada: {e}")
        
        # Limpiar el campo de entrada
        self.id_entry.delete(0, tk.END)

class DashboardPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#ecf0f1")
        self.controller = controller
        self.datos_empleado = {}
        self.tiempo_almuerzo_restante = timedelta(minutes=DURACION_ALMUERZO_MINUTOS)
        self.almuerzo_activo = False
        self.alarma_almuerzo_on = False
        self.mensaje_almuerzo_mostrado = False
        self.inicio_almuerzo_time = None
        self.timer_id = None
        
        self.crear_widgets()
        
    def crear_widgets(self):
        header_font = font.Font(family="Arial", size=24, weight="bold")
        info_font = font.Font(family="Arial", size=14)
        timer_font = font.Font(family="Consolas", size=18, weight="bold")
        status_font = font.Font(family="Arial", size=14, weight="bold")
        button_font = font.Font(family="Helvetica", size=12, weight="bold")
        
        header_frame = tk.Frame(self, bg="#34495e", height=80)
        header_frame.pack(fill="x")
        
        btn_volver = tk.Button(header_frame, text="← Volver", font=("Arial", 12), bg="#e74c3c", fg="white", 
                            command=self.volver_login, relief=tk.RAISED, bd=2)
        btn_volver.pack(side="left", padx=10, pady=10)
        
        self.nombre_label = tk.Label(header_frame, text="", font=header_font, fg="white", bg="#34495e")
        self.nombre_label.pack(pady=20)

        info_panel = tk.Frame(self, bg="#ecf0f1")
        info_panel.pack(fill="x", pady=15, padx=50)
        
        self.cargo_label = tk.Label(info_panel, text="", font=info_font, bg="#ecf0f1")
        self.cargo_label.grid(row=0, column=0, sticky="w", padx=10)
        self.edad_label = tk.Label(info_panel, text="", font=info_font, bg="#ecf0f1")
        self.edad_label.grid(row=0, column=1, sticky="w", padx=10)
        self.jornada_label = tk.Label(info_panel, text="", font=info_font, bg="#ecf0f1", fg="#27ae60")
        self.jornada_label.grid(row=0, column=2, sticky="w", padx=10)
        self.entrada_label = tk.Label(info_panel, text="", font=info_font, bg="#ecf0f1")
        self.entrada_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)

        timers_panel = tk.Frame(self, bg="white", bd=2, relief=tk.SOLID)
        timers_panel.pack(fill="both", expand=True, padx=50, pady=10)

        tk.Label(timers_panel, text="Jornada Restante", font=status_font, bg="white").grid(row=0, column=0, pady=10, padx=20)
        self.jornada_timer_label = tk.Label(timers_panel, text="00:00:00", font=timer_font, fg="#27ae60", bg="white")
        self.jornada_timer_label.grid(row=1, column=0, pady=5, padx=20)

        tk.Label(timers_panel, text="Tiempo en Almuerzo", font=status_font, bg="white").grid(row=0, column=1, pady=10, padx=20)
        self.almuerzo_timer_label = tk.Label(timers_panel, text="01:00:00", font=timer_font, fg="#2980b9", bg="white")
        self.almuerzo_timer_label.grid(row=1, column=1, pady=5, padx=20)
        
        tk.Label(timers_panel, text="Tiempo Laborado Hoy", font=status_font, bg="white").grid(row=0, column=2, pady=10, padx=20)
        self.total_timer_label = tk.Label(timers_panel, text="00:00:00", font=timer_font, fg="#8e44ad", bg="white")
        self.total_timer_label.grid(row=1, column=2, pady=5, padx=20)

        timers_panel.grid_columnconfigure((0, 1, 2), weight=1)

        buttons_panel = tk.Frame(self, bg="#ecf0f1")
        buttons_panel.pack(pady=20)

        self.btn_almuerzo_inicio = tk.Button(buttons_panel, text="Iniciar Almuerzo", font=button_font, bg="#f39c12", fg="white", command=self.iniciar_almuerzo)
        self.btn_almuerzo_inicio.grid(row=0, column=0, padx=10, ipadx=10, ipady=5)
        
        self.btn_almuerzo_fin = tk.Button(buttons_panel, text="Finalizar Almuerzo", font=button_font, bg="#e67e22", fg="white", command=self.finalizar_almuerzo, state="disabled")
        self.btn_almuerzo_fin.grid(row=0, column=1, padx=10, ipadx=10, ipady=5)

        self.btn_salida = tk.Button(buttons_panel, text="Marcar Salida", font=button_font, bg="#c0392b", fg="white", command=self.marcar_salida)
        self.btn_salida.grid(row=0, column=2, padx=10, ipadx=10, ipady=5)

        self.mensaje_panel = tk.Frame(self, bg="#ecf0f1")
        self.mensaje_panel.pack(pady=10)
        
        self.mensaje_label = tk.Label(self.mensaje_panel, text="", font=("Arial", 12), bg="#ecf0f1", fg="#e74c3c", wraplength=600)
        self.mensaje_label.pack()

    def volver_login(self):
        respuesta = messagebox.askyesno("Volver al Login", 
                                    "¿Está seguro de que desea volver al login?\n"
                                    "Esto permitirá que otro empleado se registre.")
        if respuesta:
            if self.timer_id:
                self.after_cancel(self.timer_id)
                self.timer_id = None
            self.controller.show_frame("LoginPage")

    def set_data(self, data):
        print(f"DashboardPage: set_data llamado con datos: {data}")
        self.datos_empleado = data
        self.nombre_label.config(text=f"Bienvenido, {data.get('nombre completo', 'N/A')}")
        self.cargo_label.config(text=f"Cargo: {data.get('cargo', 'N/A')}")
        self.edad_label.config(text=f"Edad: {data.get('edad', 'N/A')} años")
        self.jornada_label.config(text=f"Jornada: {int(data.get('jornada horas', 7))} horas")
        self.entrada_label.config(text=f"Entrada: {data.get('hora entrada', 'N/A')}")
        
        # Configurar botones según el estado actual del registro
        inicio_almuerzo = data.get('hora inicio almuerzo')
        fin_almuerzo = data.get('hora fin almuerzo')
        
        if pd.notna(inicio_almuerzo) and pd.isna(fin_almuerzo):
            # Está en almuerzo actualmente
            self.btn_almuerzo_inicio.config(state="disabled")
            self.btn_almuerzo_fin.config(state="normal")
            self.almuerzo_activo = True
            self.mensaje_almuerzo_mostrado = True
            
            # Calcular tiempo restante de almuerzo
            inicio_alm = datetime.strptime(str(inicio_almuerzo), '%H:%M:%S')
            tiempo_transcurrido = datetime.now() - inicio_alm
            self.tiempo_almuerzo_restante = timedelta(minutes=DURACION_ALMUERZO_MINUTOS) - tiempo_transcurrido
            
            if self.tiempo_almuerzo_restante.total_seconds() <= 0:
                self.tiempo_almuerzo_restante = timedelta(0)
                self.alarma_almuerzo_on = True
            
            self.mensaje_label.config(text="Almuerzo en progreso. Recuerde finalizar cuando termine.", 
                                    fg="#f39c12")
        elif pd.notna(fin_almuerzo):
            # Ya terminó el almuerzo
            self.btn_almuerzo_inicio.config(state="disabled")
            self.btn_almuerzo_fin.config(state="disabled")
            self.almuerzo_activo = False
            self.mensaje_label.config(text="Almuerzo completado para hoy.", fg="#27ae60")
        else:
            # No ha iniciado almuerzo
            self.btn_almuerzo_inicio.config(state="normal")
            self.btn_almuerzo_fin.config(state="disabled")
            self.almuerzo_activo = False
            
        if not self.almuerzo_activo:
            self.almuerzo_timer_label.config(text=f"{DURACION_ALMUERZO_MINUTOS:02d}:00:00", fg="#2980b9")
            self.tiempo_almuerzo_restante = timedelta(minutes=DURACION_ALMUERZO_MINUTOS)
        
        self.alarma_almuerzo_on = False
        self.inicio_almuerzo_time = None

        if self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None
        self.actualizar_timers()
        print("DashboardPage: set_data completado. Timers actualizándose.")


    def actualizar_timers(self):
        if 'hora entrada' not in self.datos_empleado or self.datos_empleado['hora entrada'] is None:
            self.timer_id = self.after(1000, self.actualizar_timers)
            return

        hora_entrada = datetime.strptime(self.datos_empleado['hora entrada'], '%H:%M:%S')
        jornada_horas = float(self.datos_empleado.get('jornada horas', 7))

        tiempo_laborado = datetime.now() - hora_entrada
        
        # Calcular tiempo de almuerzo ya tomado
        tiempo_almuerzo_tomado = timedelta(0)
        inicio_alm_str = self.datos_empleado.get('hora inicio almuerzo')
        fin_alm_str = self.datos_empleado.get('hora fin almuerzo')
        
        if pd.notna(inicio_alm_str):
            inicio_alm = datetime.strptime(str(inicio_alm_str), '%H:%M:%S')
            if pd.notna(fin_alm_str):
                # Almuerzo completado
                fin_alm = datetime.strptime(str(fin_alm_str), '%H:%M:%S')
                tiempo_almuerzo_tomado = fin_alm - inicio_alm
            elif self.almuerzo_activo:
                # Almuerzo en progreso
                tiempo_almuerzo_tomado = datetime.now() - inicio_alm
                
                # Actualizar tiempo restante de almuerzo
                self.tiempo_almuerzo_restante = timedelta(minutes=DURACION_ALMUERZO_MINUTOS) - tiempo_almuerzo_tomado
                
                if not self.mensaje_almuerzo_mostrado:
                    self.mensaje_label.config(text="¡Ha comenzado su hora de almuerzo! Recuerde que tiene 60 minutos.", 
                                            fg="#f39c12")
                    self.mensaje_almuerzo_mostrado = True
                
                if self.tiempo_almuerzo_restante.total_seconds() <= 0:
                    self.tiempo_almuerzo_restante = timedelta(0)
                    if not self.alarma_almuerzo_on:
                        self.activar_alarma_almuerzo()

        # Calcular tiempo laborado neto
        tiempo_laborado_neto = tiempo_laborado - tiempo_almuerzo_tomado

        jornada_total = timedelta(hours=jornada_horas)
        jornada_restante = jornada_total - tiempo_laborado_neto
        if jornada_restante.total_seconds() < 0:
            jornada_restante = timedelta(0)

        self.total_timer_label.config(text=str(tiempo_laborado_neto).split('.')[0])
        self.jornada_timer_label.config(text=str(jornada_restante).split('.')[0])
        
        # Actualizar timer de almuerzo
        if self.almuerzo_activo and not self.alarma_almuerzo_on:
            total_seconds = int(self.tiempo_almuerzo_restante.total_seconds())
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            self.almuerzo_timer_label.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
        elif not self.almuerzo_activo and pd.isna(self.datos_empleado.get('hora fin almuerzo')):
            # No ha iniciado almuerzo
            self.almuerzo_timer_label.config(text=f"{DURACION_ALMUERZO_MINUTOS:02d}:00:00", fg="#2980b9")
        elif pd.notna(self.datos_empleado.get('hora fin almuerzo')):
            # Almuerzo completado
            tiempo_tomado = self.datos_empleado.get('tiempo almuerzo minutos', 0)
            if pd.notna(tiempo_tomado):
                horas_alm = int(tiempo_tomado // 60)
                mins_alm = int(tiempo_tomado % 60)
                self.almuerzo_timer_label.config(text=f"{horas_alm:02d}:{mins_alm:02d}:00", fg="#27ae60")
        
        self.timer_id = self.after(1000, self.actualizar_timers)

    def iniciar_almuerzo(self):
        print("Botón 'Iniciar Almuerzo' presionado.")
        registro_actual = registrar_evento(self.datos_empleado['id empleado'], "inicio_almuerzo")
        if registro_actual:
            print("Inicio de almuerzo registrado exitosamente.")
            self.almuerzo_activo = True
            self.inicio_almuerzo_time = datetime.now()
            self.btn_almuerzo_inicio.config(state="disabled")
            self.btn_almuerzo_fin.config(state="normal")

    def finalizar_almuerzo(self):
        print("Botón 'Finalizar Almuerzo' presionado.")
        registro_actual = registrar_evento(self.datos_empleado['id empleado'], "fin_almuerzo")
        if registro_actual:
            print("Fin de almuerzo registrado exitosamente.")
            self.almuerzo_activo = False
            self.alarma_almuerzo_on = False
            self.almuerzo_timer_label.config(fg="#2980b9")
            self.btn_almuerzo_fin.config(state="disabled")
            
            # Actualizar los datos del empleado con la nueva información
            self.datos_empleado.update(registro_actual)
            
            tiempo_almuerzo_tomado = registro_actual.get('tiempo almuerzo minutos', 0)
            if pd.notna(tiempo_almuerzo_tomado):
                horas_alm = int(tiempo_almuerzo_tomado // 60)
                mins_alm = int(tiempo_almuerzo_tomado % 60)
                tiempo_str = f"{horas_alm:02d}:{mins_alm:02d}"
                messagebox.showinfo("Almuerzo Finalizado", 
                                f"Has finalizado tu hora de almuerzo.\n"
                                f"Tiempo de almuerzo tomado: {tiempo_str}\n"
                                f"¡A seguir trabajando!")
                self.mensaje_label.config(text=f"Almuerzo finalizado. Tiempo tomado: {tiempo_str}", 
                                        fg="#27ae60")
            else:
                messagebox.showinfo("Almuerzo Finalizado", 
                                "Has finalizado tu hora de almuerzo. ¡A seguir trabajando!")
                self.mensaje_label.config(text="Almuerzo finalizado.", 
                                        fg="#27ae60")

            self.tiempo_almuerzo_restante = timedelta(minutes=DURACION_ALMUERZO_MINUTOS)
            self.mensaje_almuerzo_mostrado = False

    def activar_alarma_almuerzo(self):
        self.alarma_almuerzo_on = True
        current_color = self.almuerzo_timer_label.cget("fg")
        new_color = "red" if current_color == "black" else "black"
        self.almuerzo_timer_label.config(fg=new_color, text="TIEMPO AGOTADO")
        self.mensaje_label.config(text="¡ATENCIÓN! Su tiempo de almuerzo ha terminado. Por favor, finalice el almuerzo.", 
                                fg="red")
        if self.almuerzo_activo:
            self.after(500, self.activar_alarma_almuerzo)

    def marcar_salida(self):
        print("Botón 'Marcar Salida' presionado.")
        if messagebox.askyesno("Confirmar Salida", "¿Estás seguro de que deseas marcar tu salida?"):
            registro_actual = registrar_evento(self.datos_empleado['id empleado'], "salida")
            if registro_actual:
                print("Salida registrada exitosamente.")
                horas_trabajadas = registro_actual.get('horas trabajadas', 0)
                tiempo_extra = registro_actual.get('tiempo extra minutos', 0)
                
                mensaje_salida = f"¡Salida registrada exitosamente!\n"
                mensaje_salida += f"Horas trabajadas: {horas_trabajadas:.2f}\n"
                if pd.notna(tiempo_extra) and tiempo_extra > 0:
                    mensaje_salida += f"Tiempo extra: {tiempo_extra} minutos"
                
                messagebox.showinfo("Salida Registrada", mensaje_salida)
                if self.timer_id:
                    self.after_cancel(self.timer_id)
                    self.timer_id = None
                self.controller.show_frame("LoginPage")

# --- INICIO DE LA APLICACIÓN ---
if __name__ == "__main__":
    if inicializar_archivos():
        app = App()
        app.mainloop()