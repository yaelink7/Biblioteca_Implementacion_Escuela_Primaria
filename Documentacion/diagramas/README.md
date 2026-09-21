# Los ocho diagramas del Avance 2

Los ocho entregables gráficos que pidió el profesor —**nueve diagramas**, porque el
sexto son dos—, hechos a partir del esquema y del código que corren hoy, no de la
documentación. **Si algo aquí no coincide con el sistema, gana el sistema y estos
archivos están mal.**

| # | Entregable | Archivo | Issue | Responsable |
|---|---|---|---|---|
| 1 | Casos de uso | [DIA-01](DIA-01_casos_de_uso.md) · [`.svg`](DIA-01_casos_de_uso.svg) | [#59](https://github.com/yaelink7/Biblioteca_Implementacion_Escuela_Primaria/issues/59) | Pedro Cabrera |
| 2 | Casos de uso extendido | [DIA-02](DIA-02_casos_de_uso_extendido.md) | [#60](https://github.com/yaelink7/Biblioteca_Implementacion_Escuela_Primaria/issues/60) | Rey David Montes |
| 3 | Diagrama de proceso | [DIA-03](DIA-03_diagrama_de_proceso.md) | [#61](https://github.com/yaelink7/Biblioteca_Implementacion_Escuela_Primaria/issues/61) | Rey David Montes |
| 4 | Flujo de datos | [DIA-04](DIA-04_flujo_de_datos.md) | [#62](https://github.com/yaelink7/Biblioteca_Implementacion_Escuela_Primaria/issues/62) | Rey David Montes |
| 5 | Modelado de base de datos | [DIA-05](DIA-05_modelado_de_base_de_datos.md) | [#63](https://github.com/yaelink7/Biblioteca_Implementacion_Escuela_Primaria/issues/63) | Pedro Cabrera |
| 6a | Modelo entidad-relación | [DIA-06a](DIA-06a_modelo_entidad_relacion.md) | [#64](https://github.com/yaelink7/Biblioteca_Implementacion_Escuela_Primaria/issues/64) | Pedro Cabrera |
| 6b | Modelo relacional | [DIA-06b](DIA-06b_modelo_relacional.md) + [.svg](DIA-06b_modelo_relacional.svg) | [#64](https://github.com/yaelink7/Biblioteca_Implementacion_Escuela_Primaria/issues/64) | Pedro Cabrera |
| 7 | Documentación de la base | [DIA-07](DIA-07_documentacion_de_la_base.md) | [#65](https://github.com/yaelink7/Biblioteca_Implementacion_Escuela_Primaria/issues/65) | Pedro Cabrera |
| 8 | Interfaces | [DIA-08](DIA-08_interfaces.md) | [#66](https://github.com/yaelink7/Biblioteca_Implementacion_Escuela_Primaria/issues/66) | Rey David Montes |

## Cómo verlos dibujados

**En GitHub, sin instalar nada.** Los diagramas están escritos en Mermaid dentro de
los `.md`, y GitHub los renderiza solo. Abre cualquier archivo en el repositorio y
aparecen ya dibujados.

**En VS Code**, con la extensión *Markdown Preview Mermaid Support*, y `Ctrl+Shift+V`
para la vista previa.

**Para exportar a imagen** y pegarla en el documento de Word: abre
[mermaid.live](https://mermaid.live), pega el bloque de código que va entre las
líneas ` ```mermaid ` y ` ``` `, y descarga el PNG o el SVG. Ahí mismo se puede
retocar el diagrama antes de exportarlo.

**El entregable 6 son dos diagramas separados**: el entidad-relación es el modelo
conceptual, y el relacional es su traducción al esquema físico. Van en archivos
distintos y se exportan como dos imágenes.

El diagrama de casos de uso es un SVG hecho a mano: se abre en el navegador, en
Inkscape o directamente en Word con *Insertar → Imagen*. Al ser vectorial no se pixela
al ampliarlo.

## Por qué en Markdown y no en Word

Tres razones prácticas:

1. **Se versionan.** Un cambio en el esquema se ve en el historial de Git como una
   línea modificada, no como un archivo binario nuevo.
2. **Se editan sin herramientas.** Cualquiera del equipo cambia un nodo escribiendo
   texto, sin abrir un editor de diagramas ni pelearse con las cajas.
3. **GitHub los dibuja solo**, así que el equipo los revisa desde el navegador.

Cuando llegue el momento de armar el Avance 2, se exportan las imágenes y se pegan;
el texto explicativo de cada archivo sirve como redacción de partida.

## Qué hay en cada archivo

Cada entregable trae el diagrama **y su explicación**, porque un diagrama suelto no
se sostiene en una exposición. Además, varios traen una nota sobre por qué el sistema
está hecho así — el límite de un préstamo por alumno como índice único, el reporte de
deudores que abre ya generado, el diálogo de préstamo que no es un formulario.

## Dos avisos antes de entregarlos

**Siete de las ocho historias de la reunión con la escuela modifican el esquema**
(issues #72 a #79): colección restringida a las cinco de Libros del Rincón,
asignatura, CURP, maestro de grupo, datos del tutor, retiro del correo del alumno,
costo de reposición y cuatro vistas de estadísticas.

`DIA-05`, `DIA-06a`, `DIA-06b` y `DIA-07` documentan ese mismo esquema, y `DIA-08`
describe tres pantallas que van a cambiar. **Conviene aplicar la migración 10 antes
de dar por buenos esos cinco**, o habrá que rehacerlos. Los cinco llevan una nota de
vigencia al final.

**Los UML del repositorio Java ya no corresponden.** Cambió el esquema, apareció la
capa de servicios y las reglas se movieron a la base de datos. Partir de ellos
produce un diagrama equivocado.

## De dónde salió cada dato

Todo se verificó contra la fuente, no contra la documentación:

| Insumo | Fuente |
|---|---|
| Tablas, columnas, restricciones, llaves | Las 9 migraciones de `database/migraciones/` |
| Disparadores y su momento exacto | El `create trigger` de cada migración |
| Políticas de acceso | `04_reportes_y_seguridad.sql` y `09_...sql` |
| Pantallas y controles | Los 11 archivos `.ui` de `src/biblioteca/ui/disenos/` |
| Origen de los datos de cada pantalla | Los repositorios de `src/biblioteca/repositorios/` |
| Requisitos citados | Capítulo 3 del Avance 1.3 |
