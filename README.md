# Sistema de Biblioteca — Escuela Primaria Adalberto Tejeda

Migración a Python del sistema de gestión bibliotecaria desarrollado originalmente
en Java (NetBeans + Swing + MySQL), ahora sobre **Supabase**.

Proyecto integrador de **Programación e Implementación de Sistemas**, 7.º semestre.

| | |
|---|---|
| Metodología | SCRUM — 5 sprints de 2 semanas |
| Periodo | 14 sep – 28 nov 2026 |
| Proyecto Java original | [Proyecto-Biblioteca-IngenieriaSoftware](https://github.com/yaelink7/Proyecto-Biblioteca-IngenieriaSoftware) |

## Equipo

| Integrante | Rol |
|---|---|
| Yael Arenas Guevara | Scrum Master · Desarrollo |
| Rey David Montes Ciriaco | Product Owner · Desarrollo |
| Yahir Reyes Velasco | Desarrollo |
| Pedro Cabrera Barrios Ángel | Desarrollo · Calidad |
| Roberto Ellyan Vázquez Arriaga | Calidad |

## Instalación

Requiere **Python 3.12 o superior** y **Git**.

```bash
git clone https://github.com/yaelink7/Biblioteca_Implementacion_Escuela_Primaria.git
cd Biblioteca_Implementacion_Escuela_Primaria
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Después copia `.env.example` como `.env` y pide las llaves al Scrum Master.
**El archivo `.env` nunca se sube al repositorio.**

```bash
copy .env.example .env
python main.py
```

Si aparece el listado de libros, la conexión funciona.

## Extensiones de VS Code

Al abrir la carpeta, VS Code ofrece instalar las extensiones recomendadas
(están en `.vscode/extensions.json`). Acepta la sugerencia, o instálalas a mano:

| Extensión | Para qué |
|---|---|
| **Python** (`ms-python.python`) | Ejecutar y depurar |
| **Pylance** (`ms-python.vscode-pylance`) | Autocompletado y errores de tipo |
| **Ruff** (`charliermarsh.ruff`) | Formato automático al guardar |
| **PostgresTools** (`supabase.postgrestools`) | Consultas SQL contra Supabase |
| **GitLens** (`eamodio.gitlens`) | Ver quién cambió cada línea |

## Estructura

```
src/biblioteca/
  core/          Configuración y cliente de Supabase   (era DAOBiblia/ConexionBD)
  modelos/       Clases del dominio                    (era ClasesBiblia/)
  repositorios/  Acceso a datos                        (era DAOBiblia/)
  servicios/     Reglas de negocio                     (nuevo)
  ui/            Ventanas PyQt6                        (era GUIBiblia/)
database/
  migraciones/   Esquema de la base, versionado
tests/           Pruebas con pytest                    (era test/)
Documentacion/   Entregables de la materia
```

## Base de datos

El esquema vive en `database/migraciones/` y ya está aplicado en Supabase.
Las reglas de negocio están **dentro de Postgres**, no en el código Python,
para que la futura app móvil las herede sin reimplementarlas:

| Regla | Dónde vive | Requisito |
|---|---|---|
| Un libro por usuario | Índice único parcial en `prestamos` | REQ-PRE-01 |
| Plazo de 7 días | Trigger `calcular_fecha_limite` | REQ-PRE-02 |
| Descuento de inventario | Trigger `mover_inventario` | REQ-PRE-01 |
| No dar de baja con préstamos activos | Trigger `validar_baja_de_libro` | REQ-LIB-03 |
| Historial permanente | `on delete restrict` en `prestamos` | REQ-PRE-03 |
| El alumno solo ve lo suyo | Políticas RLS | Factibilidad Legal |

### Diferencias con el esquema Java

| Java (MySQL) | Python (Supabase) | Motivo |
|---|---|---|
| `ON DELETE CASCADE` en `prestamos` | `ON DELETE RESTRICT` | Borraba el historial, violando REQ-PRE-03 |
| Sin tabla de credenciales | Supabase Auth + `perfiles.rol` | REQ-USU-01, REQ-USU-02 |
| `Telefono`, `CodigoPostal` como `bigint` | `text` | Un CP con cero inicial perdía el cero |
| Año de publicación sin validar | Trigger `validar_ano_publicacion` | Corrige el defecto D-08 de las pruebas |
| Columna `Disponible` | Se deduce en la vista `v_catalogo` | Podía contradecir a `existencias` |
| Borrado físico de libros | Baja lógica (`activo`, `motivo_baja`) | REQ-LIB-03 |

## Ejecutar las pruebas

```bash
pytest
```

## Convención de commits

Cada commit menciona la historia del backlog que atiende:

```
USU-04: pantalla de inicio de sesión
LIB-05: baja lógica validando préstamos activos
```
