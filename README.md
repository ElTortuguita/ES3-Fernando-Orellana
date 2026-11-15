# Aventuras del Sur

Aplicación de Django para la Evaluación Sumativa 3 de Programación Back End. Gestiona categorías, experiencias y reservas del ecoparque mediante usuarios con roles. Usa MySQL Server 8.0 y MySQL Workbench para administrar y respaldar la base.

## Instalación en Windows

Desde PowerShell, dentro de esta carpeta:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item inventarioAventura/config_local.example.py inventarioAventura/config_local.py
```

Editar `inventarioAventura/config_local.py` y escribir la contraseña de la conexión local MySQL80. El archivo está excluido de Git. Si el usuario, puerto o nombre de la base son diferentes, configurar las variables `MYSQL_USER`, `MYSQL_PORT`, `MYSQL_HOST` y `MYSQL_DATABASE` antes de ejecutar Django. La configuración predeterminada usa `root`, `127.0.0.1:3306` y `aventuras_del_sur_db`.

En MySQL Workbench, abrir **Local instance MySQL80**, abrir `base_datos/crear_base.sql` y ejecutar su contenido. Luego elegir una de estas dos alternativas:

**Crear las tablas y los datos demo desde Django:**

```powershell
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py cargar_demo
```

**Restaurar el respaldo entregado:** en Workbench, abrir **Server > Data Import**, elegir **Import from Self-Contained File**, seleccionar `base_datos/aventuras_del_sur_mysql.sql`, elegir `aventuras_del_sur_db` como esquema de destino e iniciar la importación. Usar un esquema nuevo o vacío para no sobrescribir trabajo existente. Después ejecutar `manage.py migrate` para comprobar el estado de las migraciones. El respaldo contiene 5 usuarios, 4 categorías, 8 experiencias y 7 reservas. El comando demo crea 6 reservas iniciales como mínimo y no borra registros existentes.

Para iniciar:

```powershell
.\.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8013
```

Abrir http://127.0.0.1:8013/ y consultar `CREDENCIALES.md`. Las dependencias de SB Admin 2 y DataTables están guardadas localmente. La aplicación no necesita una CDN para mostrarse.

## Ejecución desde Visual Studio Code

Abrir esta carpeta con **File > Open Folder**. Tener instaladas las extensiones Python y Python Debugger de Microsoft. Después de crear `.venv` e instalar `requirements.txt` como se indica arriba, presionar **F5** y usar la configuración **Aventuras del Sur - Django**. La configuración de `.vscode/launch.json` inicia el servidor en la terminal integrada con el Python de `.venv`.

Abrir http://127.0.0.1:8013/. Mantener VS Code abierto durante la demostración. Para detener el servidor, usar **Shift+F5**. MySQL80 debe estar iniciado. Si el puerto 8013 ya está ocupado, comprobar si hay otro servidor del proyecto en ejecución antes de iniciarlo otra vez.

## Organización

- `inventarioAventura`: configuración, rutas generales y conexión MySQL.
- `core`: bienvenida pública y panel según el rol.
- `cuentas`: usuario extendido, login, logout y gestión administrativa de usuarios.
- `experiencias`: modelos, formularios, CRUD, catálogo e inscripciones.
- `templates`: plantillas con herencia de `base.html`.
- `static`: SB Admin 2, Bootstrap, jQuery, DataTables y estilos del proyecto.
- `base_datos`: creación de esquema y respaldo SQL.
- `documentacion`: explicación del código, guion y criterios de la pauta.

## Permisos

| Acción | Administrador | Guía | Turista |
|---|---|---|---|
| Gestionar usuarios | Sí | No | No |
| CRUD de categorías | Sí | No | No |
| Crear experiencias | Sí | Sí, a su nombre | No |
| Listar y editar experiencias del panel | Todas | Solo propias | No |
| Eliminar experiencias | Sí | No | No |
| Consultar catálogo público | Sí | Sí | Sí |
| Inscribirse | No | No | Sí, a su nombre |
| Consultar reservas | Todas | No | Solo propias |
| Actualizar estado de pago | Sí | No | No |

El catálogo también es público para visitantes sin sesión. Los enlaces del menú dependen del rol y cada vista vuelve a comprobar los permisos en el servidor. El campo `creador` se asigna desde la sesión y no desde un formulario enviado por el navegador.

## Decisiones funcionales

- Se sigue el enunciado detallado del ecoparque. La mención inicial a una clínica veterinaria parece un resto de otra guía y debe confirmarse con el profesor si existen dudas.
- `Experiencia.activo` permite implementar el catálogo de experiencias activas que pide la pauta. Se muestran actividades futuras, activas y cuya categoría también está activa.
- Una reserva ocupa una plaza. Tanto pagos pendientes como confirmados consumen cupo. No se integra un pago bancario: el administrador registra su estado.
- Un turista no puede inscribirse dos veces en una misma experiencia. La base también exige la combinación única usuario y experiencia.
- Los registros relacionados se protegen con `PROTECT`. Si una categoría tiene experiencias o una experiencia tiene reservas, se ofrece desactivarla para conservar el historial. Un registro sin dependencias sí puede eliminarse.
- El administrador no puede eliminar su propia cuenta, desactivarse o quitarse su rol desde el panel.
- El control de cupos comprueba las reservas existentes antes de inscribir al turista, con el flujo simple de consultas y guardado usado en los ejercicios. No garantiza el cupo frente a solicitudes simultáneas. Un despliegue con múltiples visitantes requeriría control de concurrencia.

## Verificación

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run
.\.venv\Scripts\python.exe manage.py test experiencias --noinput
```

Las pruebas usan una base temporal con prefijo `test_`. El usuario MySQL necesita permisos para crearla y eliminarla. No cambian los datos demo. Se verifican permisos, asignación del creador, cupos, duplicados, privacidad del historial, CRUD administrativo, formularios, CSRF y cierre de sesión. El respaldo SQL se comprobó restaurándolo en una base temporal independiente.

## Exportación desde Workbench

En **Server > Data Export**, seleccionar únicamente `aventuras_del_sur_db`, elegir **Export to Self-Contained File**, indicar una ruta `.sql` e iniciar la exportación. Guardar el nuevo archivo en `base_datos/` si se modificaron datos para la entrega. No exportar las bases de otros proyectos.

## Git

La carpeta de trabajo tiene un repositorio Git local. El ZIP de entrega contiene el código y los documentos, sin `.git`, entorno virtual ni contraseña MySQL. Para conectar la carpeta a un repositorio nuevo:

```powershell
git remote add origin URL_DEL_REPOSITORIO_NUEVO
git push -u origin main
```

Repositorio de esta evaluación: https://github.com/ElTortuguita/ES3-Fernando-Orellana. La rama principal es `main`. La presentación con notas está en `presentacion/`. Los cinco repositorios de referencia se conservaron sin modificaciones.

## Alcance

Proyecto para demostración local. `DEBUG` está habilitado y la clave de Django y credenciales demo son de desarrollo. Antes de publicar en Internet se debe configurar el despliegue y cambiar las credenciales. La fecha de entrega informada es el lunes 16 de noviembre de 2026 y la exposición dura entre 5 y 7 minutos.
