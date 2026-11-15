# Relación con los trabajos del semestre

La implementación mantiene Django con plantillas y formularios del servidor. No incorpora una API REST, un frontend separado ni herramientas de despliegue adicionales.

| Repositorio revisado | Evidencia en el código | Aplicación en esta evaluación |
|---|---|---|
| [FernandoEV1](https://github.com/ElTortuguita/FernandoEV1) | `miPrimeraApp/views.py` envía un contexto a `render` | Bienvenida y panel de `core` |
| [Evaluacion2Repuestos](https://github.com/ElTortuguita/Evaluacion2Repuestos) | Modelos, `ModelForm`, validación con `is_valid`, Bootstrap | Campos del catálogo y formularios |
| [PracticaTaller](https://github.com/ElTortuguita/PracticaTaller) | CRUD, `get_object_or_404` y DataTables en el listado | Confirmación de acciones y búsqueda, ordenamiento y paginación |
| [EV3PRACTICA](https://github.com/ElTortuguita/EV3PRACTICA) | `login_required`, vistas de autenticación y SB Admin 2 | Catálogo con reservas protegidas, login, logout y panel |
| [TallerMedico](https://github.com/ElTortuguita/TallerMedico) | `AbstractUser`, rol, `RolRequeridoMixin`, CRUD con clases y filtros por usuario | `Usuario`, permisos y consultas según autoría e historial |

En `TallerMedico` la conexión usa `mysql.connector.django`. Se conserva ese controlador con Django 5.2.18.

La inspección se realizó sobre estos commits:

- FernandoEV1: `e2fd016800c70c73590137ffa7901459b958b9e4`.
- Evaluacion2Repuestos: `fd35e119b99e62b4564f18bb47ad049c77f9f5eb`.
- PracticaTaller: `a0aa5f152c02ce5f6de636501556c140b98b567b`.
- EV3PRACTICA: `5f9208ee1dbd4340f501b3b21f600a8d8811e405`.
- TallerMedico: `c828089e054be4dbc0b2cf282cfd57a94b36f4d2`.

## Adaptaciones que requieren comprensión

Los repositorios permiten identificar técnicas utilizadas, pero no demuestran por sí solos qué explicó el profesor en cada clase. Las relaciones del modelo Reserva y sus reglas se construyeron para el nuevo enunciado. Se mantiene un flujo simple de consulta, validación y guardado. El control de concurrencia entre reservas simultáneas queda fuera de esta implementación de aula, porque ese patrón no aparece en los ejemplos revisados.

`unique_together` exige en la base que la pareja usuario y experiencia no se repita. Los validadores de precio, cupo y fecha aplican las reglas del nuevo problema. Las pruebas automatizadas son material de comprobación y no una funcionalidad que deba exponerse como contenido del curso.

## Correspondencia con la pauta

| Requisito | Ubicación |
|---|---|
| Proyecto y tres apps | `inventarioAventura/`, `core/`, `cuentas/`, `experiencias/` |
| Usuario extendido y roles | `cuentas/models.py`, `cuentas/mixins.py` |
| Categoría, experiencia y reserva | `experiencias/models.py` |
| CRUD y autoría | `experiencias/views.py`, `cuentas/views.py` |
| Sesión y acceso | Middleware de `settings.py`, `cuentas/urls.py`, mixin y decorador |
| MySQL | `settings.py`, migraciones y `base_datos/` |
| SB Admin 2 y DataTables | `templates/base.html`, `static/js/tablas.js` |
| Cuentas y registros mínimos | `cargar_demo.py`, `CREDENCIALES.md` |
| Respaldo y documentación | SQL entregado, README y esta carpeta |
