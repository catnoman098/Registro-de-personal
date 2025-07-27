Descripción del proyecto
-	Este proyecto es una aplicación de escritorio desarrollada en Python utilizando Tkinter para la interfaz gráfica y Pandas para la gestión de datos. El sistema permite registrar la entrada, almuerzo y salida de empleados, guardando la información en archivos Excel. Ideal para pequeñas empresas o proyectos de grado que necesiten controlar tiempos laborales de forma sencilla, cabe aclarar que puede ser escalable para tener un mayor control y por supuesto.

Librerías usadas

•	tkinter: para la creación de la interfaz gráfica.
•	tkinter.font, messagebox, Toplevel, Radiobutton, StringVar: componentes de interfaz específicos.
•	pandas: para manejar la lectura y escritura de archivos Excel.
•	datetime, timedelta: para el manejo de fechas y horas.
•	os: para verificar y gestionar archivos en el sistema.

Entorno de desarrollo

•	Entorno: local, ejecutado en un sistema operativo con soporte para Tkinter (Windows, Linux o MacOS).
•	IDE recomendado: PyCharm o Visual Studio Code.
•	Versión de Python recomendada: 3.10 o superior.

Archivos principales y flujo de funcionamiento:

•	Registros_base.py: archivo principal de la aplicación.

•	empleados_nuevo.xlsx: archivo de empleados (se genera automáticamente).
• registro_personal_nuevo.xlsx: archivo de registros de entradas, salidas y almuerzos (se genera automáticamente).
•	Inicio: al ejecutar el script, se verifica que existan los archivos Excel. Si no existen, se crean.
•	Pantalla de Login: el empleado ingresa su ID.

Verificación:

o	Si ya marcó entrada y salida, muestra aviso.
o	Si ya marcó entrada pero no salida, pasa al dashboard directamente.
o	Si no hay registro, pide seleccionar la jornada laboral.
•	Selección de jornada: el empleado elige entre 4, 5, 6 o 7 horas.

Dashboard:
o	Muestra datos del empleado.
o	Control de tiempo de almuerzo (iniciar/finalizar).
o	Control de salida (marca horas trabajadas y tiempo extra).
•	Salida: se registra la salida, calcula tiempos y vuelve a la pantalla de login.

