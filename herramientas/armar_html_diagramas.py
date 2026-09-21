# -*- coding: utf-8 -*-
"""Arma un solo archivo HTML con los nueve diagramas, para mandarlo a revisar.

Lleva dentro las dos bibliotecas que necesita, asi que funciona sin internet:
quien lo reciba solo le da doble clic. Los dos SVG hechos a mano van embebidos
como data URI para que sus estilos no se mezclen con los del documento.
"""
import base64
import json
import pathlib
import re
import subprocess
import urllib.request

PROY = pathlib.Path(__file__).resolve().parent.parent
DIAG = PROY / "Documentacion" / "diagramas"
BASE = PROY / ".cache_diagramas"          # las bibliotecas descargadas

#: Las dos bibliotecas van dentro del HTML para que funcione sin internet.
#: Se descargan una sola vez y quedan en .cache_diagramas/, que esta ignorado.
BIBLIOTECAS = {
    "marked.js": "https://cdn.jsdelivr.net/npm/marked@12/marked.min.js",
    "mermaid.min.js": "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js",
}


def asegurar_bibliotecas():
    BASE.mkdir(exist_ok=True)
    for nombre, url in BIBLIOTECAS.items():
        destino = BASE / nombre
        if destino.exists() and destino.stat().st_size > 1000:
            continue
        print(f"descargando {nombre}...")
        urllib.request.urlretrieve(url, destino)

ORDEN = [
    ("DIA-01_casos_de_uso.md", "Casos de uso"),
    ("DIA-02_casos_de_uso_extendido.md", "Casos de uso extendido"),
    ("DIA-03_diagrama_de_proceso.md", "Diagrama de proceso"),
    ("DIA-04_flujo_de_datos.md", "Flujo de datos"),
    ("DIA-05_modelado_de_base_de_datos.md", "Modelado de base de datos"),
    ("DIA-06a_modelo_entidad_relacion.md", "Modelo entidad-relación"),
    ("DIA-06b_modelo_relacional.md", "Modelo relacional"),
    ("DIA-07_documentacion_de_la_base.md", "Documentación de la base"),
    ("DIA-08_interfaces.md", "Interfaces"),
]


def svg_a_data_uri(nombre):
    datos = DIAG.joinpath(nombre).read_bytes()
    b64 = base64.b64encode(datos).decode("ascii")
    return f"data:image/svg+xml;base64,{b64}"


def preparar(texto):
    """Sustituye las imagenes SVG por su data URI y quita los enlaces locales."""
    def reemplazo(m):
        alt, archivo = m.group(1), m.group(2)
        return f'<p class="figura"><img alt="{alt}" src="{svg_a_data_uri(archivo)}"></p>'
    texto = re.sub(r"!\[([^\]]*)\]\(([^)]+\.svg)\)", reemplazo, texto)
    # Los enlaces a otros archivos del repo no sirven en un HTML suelto.
    texto = re.sub(r"\[([^\]]+)\]\((DIA-[^)]+\.(?:md|svg))\)", r"\1", texto)
    return texto


asegurar_bibliotecas()

secciones = []
for archivo, titulo in ORDEN:
    secciones.append({
        "id": archivo.split("_")[0].lower().replace(".", ""),
        "clave": archivo.split("_")[0],
        "titulo": titulo,
        "md": preparar(DIAG.joinpath(archivo).read_text(encoding="utf-8")),
    })

commit = subprocess.run(["git", "-C", str(PROY), "rev-parse", "--short", "HEAD"],
                        capture_output=True, text=True).stdout.strip()

marked = BASE.joinpath("marked.js").read_text(encoding="utf-8")
mermaid = BASE.joinpath("mermaid.min.js").read_text(encoding="utf-8")

HTML = """<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Diagramas del Avance 2 · Biblioteca Adalberto Tejeda</title>
<style>
  :root { --azul:#2D4B73; --gris:#5D6675; --linea:#D8DEE9; --fondo:#F7F9FC; --ambar:#A8621B; }
  * { box-sizing: border-box; }
  body { font-family: Calibri, Carlito, "Segoe UI", Arial, sans-serif; color:#1B2430;
         background:#fff; margin:0; line-height:1.55; }
  .hoja { max-width: 980px; margin: 0 auto; padding: 32px 24px 80px; }
  header { border-bottom: 3px solid var(--azul); padding-bottom: 18px; margin-bottom: 8px; }
  header h1 { color: var(--azul); margin: 0 0 6px; font-size: 30px; }
  header .sub { color: var(--gris); font-size: 15px; }
  header .meta { color: var(--gris); font-size: 12.5px; margin-top: 10px; }
  nav { background: var(--fondo); border:1px solid var(--linea); border-radius:6px;
        padding: 16px 20px; margin: 24px 0 8px; }
  nav h2 { font-size: 13px; text-transform: uppercase; letter-spacing:1px;
           color: var(--azul); margin: 0 0 10px; }
  nav ol { margin: 0; padding-left: 20px; columns: 2; column-gap: 32px; }
  nav li { margin: 4px 0; break-inside: avoid; }
  nav a { color:#1B2430; text-decoration: none; }
  nav a:hover { color: var(--azul); text-decoration: underline; }
  section { border-top: 1px solid var(--linea); margin-top: 44px; padding-top: 28px; }
  section:first-of-type { border-top: none; }
  .clave { display:inline-block; background:var(--azul); color:#fff; font-size:11px;
           font-weight:bold; letter-spacing:1px; padding:3px 9px; border-radius:3px; }
  h1,h2,h3 { color: var(--azul); line-height:1.3; }
  h1 { font-size: 25px; margin: 10px 0 14px; }
  h2 { font-size: 19px; margin: 30px 0 10px; }
  h3 { font-size: 16px; margin: 22px 0 8px; }
  table { border-collapse: collapse; width: 100%; margin: 16px 0; font-size: 14px; }
  th { background: var(--fondo); color: var(--azul); text-align:left; }
  th, td { border: 1px solid var(--linea); padding: 7px 10px; vertical-align: top; }
  code { background: var(--fondo); border:1px solid var(--linea); border-radius:3px;
         padding: 1px 5px; font-family: Consolas, monospace; font-size: 12.5px; }
  pre { background: var(--fondo); border:1px solid var(--linea); border-radius:5px;
        padding: 14px; overflow-x: auto; }
  pre code { background: none; border: none; padding: 0; font-size: 12.5px; }
  blockquote { border-left: 4px solid var(--ambar); background:#FDF8F2; margin: 18px 0;
               padding: 12px 18px; color:#5A4630; border-radius: 0 5px 5px 0; }
  blockquote p { margin: 6px 0; }
  .figura { text-align: center; margin: 24px 0; }
  .figura img { max-width: 100%; height: auto; border:1px solid var(--linea); border-radius:5px; }
  .mermaid-out { text-align: center; margin: 24px 0; overflow-x: auto; }
  .mermaid-out svg { max-width: 100%; height: auto; }
  .fallo { background:#FDECEC; border:1px solid #C0392B; color:#8B2520; padding:10px;
           border-radius:4px; font-family: Consolas, monospace; font-size:12px; }
  footer { margin-top: 60px; padding-top: 18px; border-top:1px solid var(--linea);
           color: var(--gris); font-size: 12.5px; }
  @media print {
    nav { break-after: page; }
    section { break-before: page; border-top: none; }
    .hoja { max-width: none; padding: 0; }
  }
</style></head><body>
<div class="hoja">
<header>
  <h1>Diagramas del Avance 2</h1>
  <div class="sub">Sistema de Biblioteca · Escuela Primaria Adalberto Tejeda</div>
  <div class="meta">Nueve diagramas para los ocho entregables · Universidad Veracruzana ·
    Programación e Implementación de Sistemas<br>
    Generado del repositorio en el commit <code>__COMMIT__</code>. Este archivo funciona sin
    conexión a internet: no hace falta instalar nada.</div>
</header>
<nav><h2>Contenido</h2><ol id="toc"></ol></nav>
<div id="cuerpo"></div>
<footer>
  Los datos de estos diagramas salieron del esquema y del código que corren hoy
  —las nueve migraciones de <code>database/migraciones/</code> y los once archivos
  <code>.ui</code>—, no de la documentación. Si algo aquí no coincide con el sistema,
  gana el sistema.
</footer>
</div>

<script>__MARKED__</script>
<script>__MERMAID__</script>
<script>
const SECCIONES = __DATOS__;
const toc = document.getElementById('toc');
const cuerpo = document.getElementById('cuerpo');

for (const s of SECCIONES) {
  const li = document.createElement('li');
  li.innerHTML = '<a href="#' + s.id + '">' + s.clave + ' · ' + s.titulo + '</a>';
  toc.appendChild(li);

  const sec = document.createElement('section');
  sec.id = s.id;
  sec.innerHTML = '<span class="clave">' + s.clave + '</span>' + marked.parse(s.md);
  cuerpo.appendChild(sec);
}

// El bundle deja el objeto en globalThis.mermaid al terminar de cargarse.
(async () => {
  window.mermaid.initialize({ startOnLoad: false, theme: 'default', securityLevel: 'loose' });

  const bloques = document.querySelectorAll('pre code.language-mermaid');
  let n = 0;
  for (const bloque of bloques) {
    const destino = document.createElement('div');
    destino.className = 'mermaid-out';
    try {
      const { svg } = await window.mermaid.render('mm' + (n++), bloque.textContent);
      destino.innerHTML = svg;
    } catch (e) {
      destino.innerHTML = '<div class="fallo">No se pudo dibujar: ' + (e.message || e) + '</div>';
    }
    bloque.parentElement.replaceWith(destino);
  }
  document.body.dataset.listo = String(n);
})();
</script>
</body></html>"""

html = (HTML
        .replace("__COMMIT__", commit)
        .replace("__MARKED__", marked)
        .replace("__MERMAID__", mermaid)
        .replace("__DATOS__", json.dumps(secciones, ensure_ascii=False)))

destino = DIAG / "Diagramas_Avance_2.html"
destino.write_text(html, encoding="utf-8")
print(f"{destino.name} · {destino.stat().st_size/1024/1024:.1f} MB · {len(secciones)} diagramas")
